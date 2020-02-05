import random

from fabric.api import cd, env, execute, local, parallel, roles, run, runs_once, task
from fabric.contrib.files import exists

# Changable settings
env.roledefs = {
    'web': [
        '{{ cookiecutter.project_slug }}@scorch.devsoc.org',
        '{{ cookiecutter.project_slug }}@smaug.devsoc.org',
    ],
    'demo': [
        '{{ cookiecutter.project_slug }}@trogdor.devsoc.org',
    ],
    'cron': [
        '{{ cookiecutter.project_slug }}@{{ ["scorch", "smaug"]|random() }}.devsoc.org',
    ],
}

env.home = env.get('home', '/var/www/{{ cookiecutter.project_slug }}')
env.virtualenv = env.get('virtualenv', '/var/envs/{{ cookiecutter.project_slug }}')
env.appname = env.get('appname', '{{ cookiecutter.project_slug }}')
env.repo = env.get('repo', '{{ cookiecutter.project_slug }}')
env.media = env.get('media', '{{ cookiecutter.project_slug }}')
env.media_bucket = env.get('media_bucket', 'contentfiles-media-eu-west-1')
env.database = env.get('database', '{{ cookiecutter.project_slug }}_django')

CRONTAB = """
MAILTO=""

{daily}         /usr/local/bin/django-cron python manage.py clearsessions
"""

# Avoid tweaking these
env.use_ssh_config = True
GIT_REMOTE = 'git@github.com:developersociety/{env.repo}.git'


@task
def demo():
    env.roledefs['web'] = env.roledefs['demo']
    env.roledefs['cron'] = env.roledefs['demo']
    env.media_bucket = 'contentfiles-demo-media-eu-west-1'


@task
@roles('cron')
def cron(remove=None):
    """
    Crontab setup.

    Can also be removed if needed.

    fab cron
    fab cron:remove=True
    """
    # Allow quick removal if needed
    if remove:
        run('crontab -r')
        return

    # Deterministic based on hostname
    random.seed(env.host_string)

    # Several templates - can add more if needed
    def every_x(minutes=60, hour='*', day='*', month='*', day_of_week='*'):
        # Add some randomness to minutes
        start = random.randint(0, minutes - 1)
        minute = ','.join(str(x) for x in range(start, 60, minutes))

        return '{minute} {hour} {day} {month} {day_of_week}'.format(
            minute=minute, hour=hour, day=day, month=month, day_of_week=day_of_week)

    cron = CRONTAB.format(
        daily=every_x(hour=random.randint(0, 23)),
    )

    run("echo '{}' | crontab -".format(cron))


@task
@roles('web')
@parallel
def clone_repo(branch='master'):
    """
    Initial site setup.

    Only intended to be run once, but can be used to switch branch.

    fab clone_repo
    fab clone_repo:branchname
    """
    with cd(env.home):
        if not exists('.git'):
            git_repo = GIT_REMOTE.format(env=env)
            run('git clone --quiet --recursive {} .'.format(git_repo))
        else:
            run('git fetch')

        run('git checkout {}'.format(branch))


@task
@roles('web')
@parallel
def update():
    """ Pull latest git repository changes and install requirements. """
    with cd(env.home):
        run('git pull')

        # Save the current git commit for Sentry release tracking
        run('git rev-parse HEAD > .sentry-release')

        # Install python/node packages
        run('pip install --quiet --requirement requirements/production.txt')

        # Install nvm using .nvmrc version
        run('nvm install --no-progress')

        # Check for changes in nvm version and copy to node_modules for future checks
        run(
            'cmp --silent .nvmrc node_modules/.nvmrc || '
            'rm node_modules/.package-lock.json'
            'cp -a .nvmrc node_modules/.nvmrc'
        )

        # Install node packages
        run(
            'cmp --silent package-lock.json node_modules/.package-lock.json || '
            'npm ci --no-progress && '
            'cp -a package-lock.json node_modules/.package-lock.json'
        )

        # Clean up any potential cruft
        run('find -name "__pycache__" -prune -exec rm -rf {} \;')


@task
@runs_once
@roles('web')
def migrate():
    """ Migrate database changes. """
    with cd(env.home):
        run('python manage.py migrate')


@task
@roles('web')
@parallel
def static():
    """ Update static files. """
    with cd(env.home):
        # Clean dist folder
        run('rm -rf static/dist')

        # Generate CSS
        run('npm run production --silent')

        # Collect static files
        run('python manage.py collectstatic --verbosity=0 --noinput')

{%- if cookiecutter.multilingual == 'y' %}
@task
@roles('web')
@parallel
def translations():
    """ Update translation files. """
    with cd(env.home):
        run('make translations')
{%- endif %}


@task(name='reload')
@roles('web')
@parallel
def reload_uwsgi(force_reload=None):
    """
    Reload uWSGI.

    fab reload
    fab reload:True
    fab reload:force_reload=True
    """
    if force_reload:
        run('uwsgi --stop /run/uwsgi/{}/uwsgi.pid'.format(env.appname))
    else:
        run('uwsgi --reload /run/uwsgi/{}/uwsgi.pid'.format(env.appname))


@task
@roles('web')
@runs_once
def sentry_release():
    """ Register new release with Sentry. """
    with cd(env.home):
        version = run('sentry-cli releases propose-version')
        run('sentry-cli releases new --project {project} {version}'.format(
            project=env.repo, version=version
        ))
        run('sentry-cli releases set-commits --auto {version}'.format(version=version))
        run('sentry-cli releases deploys {version} new --env $SENTRY_ENVIRONMENT'.format(
            version=version
        ))


@task
def deploy(force_reload=None):
    """
    Deploy to remote server.

    Steps includes pull repo, migrate, collect static, install requirements.

    fab deploy
    fab deploy:True
    fab deploy:force_reload=True
    """
    execute(update)
    execute(migrate)
    execute(static)
    {%- if cookiecutter.multilingual == 'y' %}
    execute(translations)
    {%- endif %}
    execute(reload_uwsgi, force_reload=force_reload)
    execute(cron)
    execute(sentry_release)


@task
def get_backup(hostname=None, replace_hostname='127.0.0.1', replace_port=8000):
    """
    Get remote backup and restore database locally.

    fab get_backup
    fab get_backup:www.example.com
    fab get_backup:www.example.com,192.1.1.1
    fab get_backup:hostname=www.example.com,replace_hostname=192.1.1.1,replace_port=8000
    """
    # Recreate database
    local('dropdb --if-exists {}'.format(env.database))
    local('createdb {}'.format(env.database))

    # Connect to the server and dump database.
    backup_ssh = random.choice(env.roledefs['web'])
    commands = [
        """
        ssh -C {} '(
            source $HOME/.bash_env \
            && source {}/bin/activate \
            && {}/manage.py dump_masked_data
        )'
        """.format(
            backup_ssh, env.virtualenv, env.home,
        ).strip()
    ]

    if hostname:
        if replace_port:
            replace_host = '{}:{}'.format(replace_hostname, replace_port)
        else:
            replace_host = replace_hostname

        # If hostname is passed replace with replace_host.
        commands.append('sed -e "s|{}|{}|g"'.format(hostname, replace_host))

    # Restore database.
    commands.append('psql --single-transaction {}'.format(env.database))

    local(' | '.join(commands))


@task
def get_media(directory=''):
    """
    Download remote media files. It uses credentials from ~/.aws/config.

    fab get_media
    fab get_media:assets
    """
    # Sync files from our S3 bucket/directory
    local(
        'aws s3 sync '
        's3://{media_bucket}/{media}/{directory} '
        'htdocs/media/{directory}'.format(
            media_bucket=env.media_bucket, media=env.media, directory=directory
        )
    )


@task
@runs_once
@roles('web')
def get_env():
    """ Get the current environment variables, ready for local export."""
    env.output_prefix = False
    run('export | sed -e "s/declare -x/export/g"')


@task
def ssh(index='1'):
    """ SSH to the remote server, pass ssh:2 to go to the second defined. """
    index = int(index) - 1
    server = env.roledefs['web'][index]
    local('ssh {}'.format(server))

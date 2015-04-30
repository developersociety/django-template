# -*- coding: utf-8 -*-

from fabric.api import env, run, cd, roles, local, parallel, task
from fabric.contrib.files import exists
import random

# Changable settings
env.roledefs = {
    'web': [
        '{{ project_name }}@scorch.blanctools.com',
        '{{ project_name }}@smaug.blanctools.com',
    ],
    'cron': [
        '{{ project_name }}@scorch.blanctools.com',
    ],
}

env.home = env.get('home', '/var/www/{{ project_name }}')
env.repo = env.get('repo', '{{ project_name }}')
env.database = env.get('database', '{{ project_name }}_django')

CRONTAB = """
MAILTO=admin@blanc.ltd.uk

{daily}         /usr/local/bin/django-cron python manage.py clearsessions
"""

# Avoid tweaking these
env.use_ssh_config = True
GIT_REMOTE = 'git@github.com:blancltd/{env.repo}.git'
DATABASE_SERVER = 'golestandt.blanctools.com'


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
    daily = "{} {} * * *".format(random.randint(0, 59), random.randint(0, 23))
    hourly = "{} * * * *".format(random.randint(0, 59))
    random_15 = random.randint(0, 14)
    every_15 = "{}-{}/15 * * * *".format(random_15, 60 - 15 + random_15)
    random_10 = random.randint(0, 9)
    every_10 = "{}-{}/10 * * * *".format(random_10, 60 - 10 + random_10)
    random_5 = random.randint(0, 4)
    every_5 = "{}-{}/5 * * * *".format(random_5, 60 - 5 + random_5)

    cron = CRONTAB.format(
        daily=daily, hourly=hourly, every_15=every_15, every_10=every_10, every_5=every_5)

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
def deploy(force_reload=None):
    """
    Deploy to remote server.

    Steps includes pull repo, migrate, install requirements, collect static.

    fab deploy
    fab deploy:True
    fab deploy:force_reload=True
    """
    with cd(env.home):
        run('git pull')

        run('pip install --quiet --requirement requirements/production.txt')

        # Clean up any potential cruft
        run('find . -name "*.pyc" -delete')

        # Migrate database changes
        run('python manage.py migrate')

        # Static files
        run('python manage.py collectstatic --verbosity=0 --noinput')

        if force_reload:
            run('killall -TERM uwsgi')
        else:
            run('killall -HUP uwsgi')


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
    commands = ['ssh -C {} sudo -u postgres pg_dump --no-owner {}'.format(
        DATABASE_SERVER, env.database
    )]

    if hostname:
        # If hostname is passed replace with replace_hostname.
        commands.append('sed -e "s|{}|{}:{}|g" |'.format(
            hostname, replace_hostname, replace_port
        ))

    # Restore database.
    commands.append('psql --single-transaction {}'.format(env.database))

    local(' | '.join(commands))

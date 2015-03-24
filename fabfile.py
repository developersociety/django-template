# -*- coding: utf-8 -*-

from fabric.api import env, run, cd, roles, local

env.use_ssh_config = True

env.roledefs = {
    'web': [
        '{{ project_name }}@runicaath.blanctools.com'
    ]
}

env.home = '/var/www/{{ project_name }}'

env.requirements = '{}/{}'.format(env.home, 'requirements')

DATABASE_NAME = '{{ project_name }}_django'
DATABASE_SERVER = 'golestandt.blanctools.com'


@roles('web')
def deploy(force_reload=None):
    """
    Deploy to remote server steps includes pull repo, migrate, install requirements,
    collect static.

    How to use it:

    fab deploy or fab deploy:force_reload=True
    """

    with cd(env.home):
        run('git fetch')
        run('git pull origin master')

        with cd(env.requirements):
            run('pip intall -r production.txt')

        # Migarte database changes.
        run('python manage.py migrate ' '--settings={{ project_name }}.settings.production')
        # Collectstatic.
        run(
            'python manage.py collectstatic --noinput '
            '--settings={{ project_name }}.settings.production'
        )

        if force_reload:
            run('killall -TERM uwsgi')
        else:
            run('killall -HUP uwsgi')


def get_backup(hostname=None, replace_hostname='127.0.0.1'):
    """
    Get remote backup and restore database locally.

    How to run with arguments:

    fab get_backup:hostname=example.com,replace_hostname=192.1.1.1

    """

    # Drop database if exists.
    local('dropdb --if-exists {}'.format(DATABASE_NAME))
    # Create new database.
    local('createdb {}'.format(DATABASE_NAME))

    # Connect to the server and dump database.
    command = 'ssh -C {} sudo -u postgres pg_dump --no-owner {} |'.format(
        DATABASE_SERVER, DATABASE_NAME
    )

    if hostname:
        # If hostname is passed replace with replace_hostname.
        command = '{} sed -e "s|{}|{}:8000|g" |'.format(
            command, hostname, replace_hostname
        )

    # Restore database.
    command = "{} psql --single-transaction {}".format(command, DATABASE_NAME)

    local(command)



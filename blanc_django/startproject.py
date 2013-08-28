#!/usr/bin/env python
from fabric.api import *
import blanc_django
import os
import stat


DJANGO_REQUIREMENTS = [
    'Django==1.5.2',
    'pytz==2013b',
    'pylibmc==1.2.3',
    'psycopg2==2.5.1',
    'Pillow==2.1.0',
]

UWSGI_TEMPLATE = """
[uwsgi]
socket=127.0.0.1:0
home=/var/www/{hostname}/pyenv
pythonpath=/var/www/{hostname}/app
module={project}.wsgi
processes=1
master=true
idle=300
die-on-idle=true
offload-threads=1
check-static=/var/www/{hostname}/htdocs
#static-expires-uri=^/static/ 31536000
log-syslog=uwsgi-{project}
"""

CRON_TEMPLATE = """
#!/bin/sh
. /var/www/{hostname}/pyenv/bin/activate
exec python /var/www/{hostname}/app/manage.py $@
"""

ROBOTS_TEMPLATE = """
User-agent: *
Disallow: /
"""

GITIGNORE_TEMPLATE = """
*.pyc
/app/{project}/local_settings.py
/htdocs/media
/htdocs/static
/pyenv
"""

SUCCESS_MESSAGE = """
Visit: https://drake-admin.hawkz.com/phppgadmin/

Database SQL (one command at a time):
CREATE ROLE {project}_django WITH LOGIN ENCRYPTED PASSWORD '{database_password}';
CREATE DATABASE {project}_django WITH OWNER={project}_django ENCODING='utf8';

or GeoDjango (avoid unless needed):
CREATE ROLE {project}_django WITH LOGIN ENCRYPTED PASSWORD '{database_password}';
CREATE DATABASE {project}_django WITH OWNER={project}_django ENCODING='utf8' TEMPLATE=template_postgis;
"""

VALIDATE_HOSTNAME = '^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$'


def ask_hostname():
    return prompt('Website hostname? (eg. www.example.com)', validate=VALIDATE_HOSTNAME)


def ask_project():
    return prompt('Project name?')


def setup_requirements():
    os.makedirs('conf')

    with open('conf/requirements.txt', 'w') as f:
        for i in DJANGO_REQUIREMENTS:
            f.write(i + '\n')

    local('pip install -r conf/requirements.txt')


def setup_uwsgi_ini(hostname, project):
    with open('conf/uwsgi.ini', 'w') as f:
        f.write(UWSGI_TEMPLATE.format(**{
            'hostname': hostname,
            'project': project,
        }).lstrip())


def setup_cron(hostname):
    os.makedirs('cron')

    with open('cron/manage.sh', 'w') as f:
        f.write(CRON_TEMPLATE.format(**{
            'hostname': hostname,
        }).lstrip())

    st = os.stat('cron/manage.sh')
    os.chmod('cron/manage.sh', st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def setup_robots():
    os.makedirs('htdocs')

    with open('htdocs/robots.txt', 'w') as f:
        f.write(ROBOTS_TEMPLATE.lstrip())


def setup_gitignore(project):
    with open('.gitignore', 'w') as f:
        f.write(GITIGNORE_TEMPLATE.format(**{
            'project': project,
        }).lstrip())


def setup_project(hostname, project):
    os.makedirs('app')

    project_template = os.path.join(blanc_django.__path__[0], 'conf')

    # Bit of an evil hack - but it works!
    from django.utils.crypto import get_random_string
    from blanc_django.django_commands.startproject import Command
    startproject = Command()

    # Add the various additional template options we want
    database_password = get_random_string(length=16)
    startproject.extra_options = {
        'hostname': hostname,
        'database_password': database_password,
    }

    startproject.run_from_argv(['django-admin.py', 'startproject', project, 'app', '--template=%s' % (project_template,)])

    return database_password


def show_instructions(*args, **kwargs):
    print SUCCESS_MESSAGE.format(**kwargs)


def main():
    hostname = ask_hostname()
    project = ask_project()
    setup_requirements()
    setup_uwsgi_ini(hostname, project)
    setup_cron(hostname)
    setup_robots()
    setup_gitignore(project)
    database_password = setup_project(hostname, project)
    show_instructions(hostname=hostname, project=project, database_password=database_password)

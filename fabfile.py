# -*- coding: utf-8 -*-

from fabric.api import env, run, cd, roles

env.use_ssh_config = True

env.roledefs = {
    'web': [
        '{{ project_name }}@runicaath.blanctools.com'
    ]
}

env.home = '/var/www/{{ project_name }}'


@roles('web')
def deploy():
    """Deploy to remote server."""

    with cd(env.home):
        run('git fetch')
        run('git pull origin master')
        run('killall -QUIT uwsgi')


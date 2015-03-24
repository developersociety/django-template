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
def deploy(force_reload=None):
    """Deploy to remote server."""

    with cd(env.home):
        run('git fetch')
        run('git pull origin master')
        if force_reload:
            run('killall -TERM uwsgi')
        else:
            run('killall -HUP uwsgi')


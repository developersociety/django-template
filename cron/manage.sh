#!/bin/bash
. $HOME/.bash_env
. /var/www/{{ project_name }}/pyenv/bin/activate
exec python /var/www/{{ project_name }}/manage.py $@

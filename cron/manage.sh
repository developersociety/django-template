#!/bin/sh
. /var/www/{{ project_name }}/pyenv/bin/activate
exec python /var/www/{{ project_name }}/manage.py $@

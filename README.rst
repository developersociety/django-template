Blanc LTD django-template
=========================

To run locally:

#. Create a Django project directory structure::

    django-admin startproject --template=https://github.com/blancltd/django-template/archive/master.zip project_name

#. Install dependencies::

    pip install -r requirements/local.txt
    npm install

#. Create tables::

    ./manage.py syncdb

{{ '=' * cookiecutter.project_name|length }}
{{ cookiecutter.project_name }}
{{ '=' * cookiecutter.project_name|length }}

Development setup
=================

Install npm required packages:

    $ npm install

Install the requirements:

    $ pip install -r requirements/local.txt

Create database:

    $ createdb {{ cookiecutter.project_slug }}_django

Run migrations:

    $ python manage.py migrate

You can now run the development server:

    $ python manage.py runserver

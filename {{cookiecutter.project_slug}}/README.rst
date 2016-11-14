{{ '=' * cookiecutter.project_name|length }}
{{ cookiecutter.project_name }}
{{ '=' * cookiecutter.project_name|length }}

Development setup
=================

Install npm required packages:

.. code:: console

    $ npm install

Install the requirements:

.. code:: console

    $ pip install -r requirements/local.txt

Create database:

.. code:: console

    $ createdb {{ cookiecutter.project_slug }}_django

Run migrations:

.. code:: console

    $ python manage.py migrate

You can now run the development server:

.. code:: console

    $ python manage.py runserver

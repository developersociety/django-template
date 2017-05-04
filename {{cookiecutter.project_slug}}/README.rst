{{ '=' * cookiecutter.project_name|length }}
{{ cookiecutter.project_name }}
{{ '=' * cookiecutter.project_name|length }}

Development setup
=================

Presuming you're using the Virtualenv Wrapper and Dev Tools:

.. code:: console

    $ blanc-clone {{ cookiecutter.project_slug }}
    $ make reset

You can now run the development server:

.. code:: console

    $ python manage.py runserver

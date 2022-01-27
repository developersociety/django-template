# {{ cookiecutter.project_name }}

_Project top level description goes here_

- Demo site: _TODO_
- Live site: _TODO_
- Slack channels: _TODO_
- Notion documentation: _TODO_

## Development setup

It's recommended you use [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
and [The Developer Society Dev Tools](https://github.com/developersociety/tools).

Presuming you are using those tools, getting started on this project is pretty straightforward:

```console
$ dev-clone {{ cookiecutter.project_slug }}
$ workon {{ cookiecutter.project_slug }}
$ make reset
```

You can now run the development server:

```console
$ python manage.py runserver
```

SHELL=/bin/bash
.DEFAULT_GOAL := help
PROJECT_SLUG={{ cookiecutter.project_slug }}

# ---------------------------------
# Project specific targets
# ---------------------------------
#
# Add any targets specific to the current project in here.
{%- if cookiecutter.multilingual == 'y'  %}
translations: ## Create/compile dummy translations
	rm -rf locale/{en,uni}
	mkdir -p locale/{en,uni}/LC_MESSAGES
	./manage.py makemessages --verbosity=0

	podebug --rewrite=unicode locale/{en,uni}/LC_MESSAGES/django.po
	sed -i -e 's/.Plural-Forms:.*//' locale/{en,uni}/LC_MESSAGES/django.po
	find locale -name '*-e' -delete
	./manage.py compilemessages --verbosity=0
{%- endif %}


# -------------------------------
# Common targets for Dev projects
# -------------------------------
#
# Edit these targets so they work as expected on the current project.
#
# Remember there may be other tools which use these targets, so if a target is not suitable for
# the current project, then keep the target and simply make it do nothing.

help: ## This help dialog.
help: help-display

nuke: ## Full wipe of the local environment, uncommitted files, and database.
nuke: venv-check venv-wipe git-full-clean database-drop

reset: ## Reset your local environment. Useful after switching branches, etc.
reset: venv-check venv-wipe install-local fab-get-data django-migrate django-user-passwords django-dev-createsuperuser{%- if cookiecutter.wagtail == 'y' %} django-rebuild-index{%- endif %}

clear: ## Like reset but without the wiping of the installs.
clear: fab-get-data django-migrate django-user-passwords django-dev-createsuperuser{%- if cookiecutter.wagtail == 'y' %} django-rebuild-index{%- endif %}

check: ## Check for any obvious errors in the project's setup.
check: pipdeptree-check npm-check django-check

format: ## Run this project's code formatters.
format: black-format isort-format prettier-format

lint: ## Lint the project.
lint: npm-install black-lint isort-lint flake8-lint eslint-lint prettier-lint

test: ## Run unit and integration tests.
test: django-test

test-report: ## Run and report on unit and integration tests.
test-report: coverage-clean test coverage-report

deploy: ## Deploy this project to demo or live.
deploy: fab-deploy



# ---------------
# Utility targets
# ---------------
#
# Targets which are used by the common targets. You likely want to customise these per project,
# to ensure they're pointing at the correct directories, etc.

# Virtual Environments
venv-check:
ifndef VIRTUAL_ENV
	$(error Must be in a virtualenv)
endif

venv-wipe: venv-check
	if ! pip list --format=freeze | grep -v "^pip=\|^setuptools=\|^wheel=" | xargs pip uninstall -y; then \
	    echo "Nothing to remove"; \
	fi


# Destructive cleaning
git-full-clean:
	git clean -ffdx

database-drop:
	dropdb --if-exists ${PROJECT_SLUG}_django


# Installs
install-local: npm-install pip-install-local


# Pip
pip-install-local: venv-check
	pip install -r requirements/local.txt


# Fabfile
fab-get-data: fab-get-backup fab-get-media

fab-get-backup:
	fab get_backup

fab-get-media:
	fab get_media

fab-deploy:
	fab deploy


# ISort
isort-lint:
	isort --check-only --diff apps project

isort-format:
	isort apps project


# Flake8
flake8-lint:
	flake8 apps project


# Coverage
coverage-report: coverage-html coverage-xml
	coverage report --show-missing

coverage-html:
	coverage html

coverage-xml:
	coverage xml

coverage-clean:
	rm -rf htmlcov
	rm -rf reports
	rm -f .coverage


# Django
django-check: django-check-missing-migrations django-check-validate-templates

django-test: django-collectstatic
	PYTHONWARNINGS=all coverage run --include="apps/*" ./manage.py test --noinput . apps

django-check-missing-migrations:
	./manage.py makemigrations --settings=project.settings.migrations --check --dry-run

django-collectstatic:
	./manage.py collectstatic --verbosity 0 --noinput

django-check-validate-templates:
	./manage.py validate_templates --verbosity 0

django-dev-createsuperuser: DJANGO_DEV_USERNAME ?= _dev@dev.ngo
django-dev-createsuperuser: DJANGO_DEV_PASSWORD ?= password
django-dev-createsuperuser: DJANGO_DEV_EMAIL ?= _dev@dev.ngo
django-dev-createsuperuser:
	@echo "import sys; from django.contrib.auth import get_user_model; obj = get_user_model().objects.create_superuser('$(DJANGO_DEV_USERNAME)', '$(DJANGO_DEV_EMAIL)', '$(DJANGO_DEV_PASSWORD)');" | python manage.py shell >> /dev/null
	@echo
	@echo "Superuser details: "
	@echo
	@echo "    $(DJANGO_DEV_USERNAME):$(DJANGO_DEV_PASSWORD)"
	@echo

django-user-passwords: DJANGO_USER_PASSWORD ?= password
django-user-passwords:
	@echo "from django.contrib.auth.hashers import make_password; from django.contrib.auth import get_user_model; get_user_model().objects.update(password=make_password('$(DJANGO_USER_PASSWORD)'));" | python manage.py shell >> /dev/null

django-migrate:
	./manage.py migrate

{%- if cookiecutter.wagtail == 'y' %}

django-rebuild-index:
	./manage.py update_index
{%- endif %}


# NPM
npm-check: npm-install npm-run-production

npm-install:
	cmp --silent package-lock.json node_modules/.package-lock.json || (npm ci && cp -a package-lock.json node_modules/.package-lock.json)

npm-run-production:
	npm run production --silent


# ESLint
eslint-lint:
	npm run eslint -- static/src/js

# Prettier
prettier-lint:
	npm run prettier --silent -- --list-different "static/src/{js,scss}/**" "*.js"

prettier-format:
	npm run prettier --silent -- --write "static/src/{js,scss}/**" "*.js"


# Black
black-lint:
	black --check apps project

black-format:
	black apps project


#pipdeptree
pipdeptree-check:
	pipdeptree --warn fail > /dev/null


# Help
help-display:
	@awk '/^[\-[:alnum:]]*: ##/ { split($$0, x, "##"); printf "%20s%s\n", x[1], x[2]; }' $(MAKEFILE_LIST)

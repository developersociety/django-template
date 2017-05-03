SHELL=/bin/bash
.DEFAULT_GOAL := help


# ---------------------------------
# Project specific targets
# ---------------------------------
#
# Add any targets specific to the current project in here.



# ---------------------------------
# Common targets for Blanc projects
# ---------------------------------
#
# Edit these targets so they work as expected on the current project.
#
# Remember there may be other tools which use these targets, so if a target is not suitable for
# the current project, then keep the target and simply make it do nothing.

help: ## This help dialog.
help: help-display

clean: ## Remove unneeded files generated from the various build tasks.
clean: coverage-clean

reset: ## Reset your local environment. Useful after switching branches, etc.
reset: venv-check venv-wipe install-local fab-get-data django-migrate django-dev-createsuperuser

check: ## Check for any obvious errors in the project's setup.
check: django-check npm-check

format: ## Run this project's code formatters.
format: yapf-format isort-format

lint: ## Lint the project.
lint: yapf-lint isort-lint flake8-lint jshint-lint

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
	if ! pip list --format=freeze | grep -v "^appdirs=\|^distribute=\|^packaging=\|^pip=\|^pyparsing=\|^setuptools=\|^six=\|^wheel=" | xargs pip uninstall -y; then \
	    echo "Nothing to remove"; \
	fi


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
isort-version:
	isort --version

isort-lint: isort-version
	isort --recursive --check-only --diff {{ cookiecutter.project_slug }} apps

isort-format: isort-version
	isort --recursive {{ cookiecutter.project_slug }} apps


# Flake8
flake8-lint:
	flake8 {{ cookiecutter.project_slug }} apps


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

django-drop-test-database:
	./manage.py drop_test_database --noinput

django-test: django-collectstatic django-drop-test-database
	coverage run --include="{{ cookiecutter.project_slug }}/*,apps/*" ./manage.py test --noinput . apps

django-check-missing-migrations:
	! ./manage.py makemigrations --dry-run --exit

django-collectstatic:
	./manage.py collectstatic --verbosity 0 --noinput

django-check-validate-templates:
	./manage.py validate_templates --verbosity 0

django-dev-createsuperuser: DJANGO_DEV_USERNAME ?= _dev
django-dev-createsuperuser: DJANGO_DEV_PASSWORD ?= password
django-dev-createsuperuser: DJANGO_DEV_EMAIL ?= _dev@dev.ngo
django-dev-createsuperuser:
	@echo "import sys; from django.contrib.auth import get_user_model; obj = get_user_model().objects.create_superuser('$(DJANGO_DEV_USERNAME)', '$(DJANGO_DEV_EMAIL)', '$(DJANGO_DEV_PASSWORD)');" | python manage.py shell >> /dev/null
	@echo
	@echo "Superuser details: "
	@echo
	@echo "    $(DJANGO_DEV_USERNAME):$(DJANGO_DEV_PASSWORD)"
	@echo

django-migrate:
	./manage.py migrate


# NPM
npm-check: npm-install npm-run-production

npm-install:
	npm install

npm-run-production:
	npm run production


# JSHint
jshint-lint:
	npm run jshint -- static/


# YAPF
yapf-lint:
	yapf_lint_output="`yapf -r -p -d --exclude="*/migrations/*.py" --style .style.yapf {{ cookiecutter.project_slug }} apps`" && \
	if [[ $$yapf_lint_output ]]; then echo -e "$$yapf_lint_output"; exit 1; fi

yapf-format:
	yapf -r -i -p --exclude="*/migrations/*.py" --style .style.yapf {{ cookiecutter.project_slug }} apps


# Help
help-display:
	@awk '/^[[:alnum:]-]*: ##/ { split($$0, x, "##"); printf "%20s%s\n", x[1], x[2]; }' $(MAKEFILE_LIST)

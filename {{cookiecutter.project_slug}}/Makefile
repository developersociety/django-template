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
reset: venv-check venv-wipe install-local fab-get-backup django-migrate django-user-passwords django-dev-createsuperuser

full-reset: ## Reset your local environment and download all media files.
full-reset: venv-check venv-wipe install-local fab-get-data django-migrate django-user-passwords django-dev-createsuperuser

clear: ## Like reset but without the wiping of the installs.
clear: fab-get-backup django-migrate django-user-passwords django-dev-createsuperuser

full-clear: ## Fresh download of remotely stored data including media files.
full-clear: fab-get-data django-migrate django-user-passwords django-dev-createsuperuser

check: ## Check for any obvious errors in the project's setup.
check: pipdeptree-check npm-check django-check

format: ## Run this project's code formatters.
format: ruff-format prettier-format stylelint-format djlint-format

lint: ## Lint the project.
lint: ruff-lint eslint-lint prettier-lint stylelint-lint djlint-lint djlint-check

test: ## Run unit and integration tests.
test: django-test

test-fast: ## Run tests in parallel, without reports
test-fast: django-test-fast

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
	fab $${site:-live} get_backup

fab-get-media:
	fab $${site:-live} get_media

fab-deploy:
	fab $${site:-live} deploy


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

django-test-fast: django-collectstatic
	PYTHONWARNINGS=all ./manage.py test --noinput --parallel

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


# NPM
npm-check: npm-install npm-run-production

npm-install:
	cmp --silent package-lock.json node_modules/.package-lock.json || (npm ci && cp -a package-lock.json node_modules/.package-lock.json)

npm-run-production:
	npm run production --silent


# ESLint
eslint-lint:
	npm run eslint --silent -- static/src/js


# Prettier
prettier-lint:
	npm run prettier --silent -- --list-different "static/src/{js,scss}/**" "*.js"

prettier-format:
	npm run prettier --silent -- --write "static/src/{js,scss}/**" "*.js"


# stylelint
stylelint-lint:
	npm run stylelint --silent -- static/src/scss

stylelint-format:
	npm run stylelint --silent -- static/src/scss --fix


# Ruff
ruff-lint:
	ruff check
	ruff format --check

ruff-format:
	ruff check --fix-only
	ruff format


# DJ lint
djlint-lint:
	djlint templates --lint

djlint-check:
	djlint templates --check

djlint-format:
	djlint templates --reformat


#pipdeptree
pipdeptree-check:
	pipdeptree --warn fail > /dev/null


# Help
help-display:
	@awk '/^[\-[:alnum:]]*: ##/ { split($$0, x, "##"); printf "%20s%s\n", x[1], x[2]; }' $(MAKEFILE_LIST)

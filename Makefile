VENV=venv/bin/activate

server:
	@. $(VENV) && venv/bin/python3.6 manage.py runserver
.PHONY: server

createsuperuser:
	@. $(VENV) && venv/bin/python3.6 manage.py createsuperuser
.PHONY: createsuperuser

shell:
	@. $(VENV) && venv/bin/python3.6 manage.py shell_plus
.PHONY: shell

showmigrations:
	@. $(VENV) && venv/bin/python3.6 manage.py showmigrations
.PHONY: showmigrations

make-migration:
	@. $(VENV) && venv/bin/python3.6 manage.py makemigrations
.PHONY: make-migration

migrate:
	@. $(VENV) && venv/bin/python3.6 manage.py migrate --no-input
.PHONY: migrate

collectstatic:
	@. $(VENV) && venv/bin/python3.6 manage.py collectstatic --no-input
.PHONY: migrate

virtualenv:
	@virtualenv venv --python=python3.6
.PHONY: virtualenv

install:
	@. $(VENV) && pip3 install -r requirements.txt
.PHONY: install

pylama:
	@. $(VENV) && ls -d */ | xargs pylama
.PHONY: pylama

apply-isort:
	@. $(VENV) && isort --recursive --apply --settings-path=setup.cfg
.PHONY: apply-isort

checks:
	@. $(VENV) && venv/bin/python3.6 manage.py check --fail-level=WARNING
.PHONY: checks

isort:
	@. $(VENV) && isort --recursive --check-only --diff --settings-path=setup.cfg
.PHONY: isort

local-ci: isort pylama
.PHONY: local-ci
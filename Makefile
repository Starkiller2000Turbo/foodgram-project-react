WORKDIR = backend
TEMPLATES-DIR = $(WORKDIR)/templates
MANAGE = python $(WORKDIR)/manage.py

default:
	$(MANAGE) makemigrations
	$(MANAGE) migrate
	$(MANAGE) runserver

style:
	isort $(WORKDIR)
	black -S -l 79 $(WORKDIR)
	flake8 $(WORKDIR)
	mypy $(WORKDIR)

migrations:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate

superuser:
	$(MANAGE) createsuperuser

run:
	$(MANAGE) runserver

test:
	$(MANAGE) test $(WORKDIR)

shell:
	$(MANAGE) shell

ingredients:
	$(MANAGE) import_ingredients

tags:
	$(MANAGE) import_tags

import:
	$(MANAGE) import_ingredients
	$(MANAGE) import_tags

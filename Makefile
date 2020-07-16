.DEFAULT_GOAL := help
.PHONY: help

include .env
export

# taken from https://container-solutions.com/tagging-docker-images-the-right-way/

help: ## Print this help
	@grep -E '^[a-zA-Z_-\.]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

ps: ## docker-compose ps
	docker-compose ps

up: ## docker-compose up -d
	docker-compose up -d

from-scratch: ## docker-compose up -d --build
	docker-compose up -d --build

down: ## docker-compose down
	docker-compose down

maps.logs: ## Show container logs for <maps> service
	docker-compose logs --follow --tail 10 maps

maps.flake8: ## Run flake8 on <maps>
	docker-compose exec maps flake8 project

api.logs: ## Show container logs for <graphapi> service
	docker-compose logs --follow --tail 10 graphapi

api.repl: ## Get access to a python REPL within the application context in the <graphapi> container
	@docker-compose exec graphapi python manage.py shell

neo4j.db.recreate: ## Drops database in <core1> and recreates it from scratch
	@docker-compose exec graphapi python manage.py recreate_db

maps.sh: ## Get shell access to <maps> service
	@docker-compose exec maps bash

bump.major: ## Updates CHANGELOG and bumps to next major VERSION (i.e. VERSION.y.z)
	@PART=major sh ./bump_version.sh 

bump.minor: ## Updates CHANGELOG and bumps to next minor VERSION (i.e. x.VERSION.z)
	@PART=minor sh ./bump_version.sh 

bump.patch: ## Updates CHANGELOG and bumps to next patch VERSION (i.e. x.y.VERSION)
	@PART=patch sh ./bump_version.sh 

bump.changelog: ## Updates CHANGELOG
	@sh ./bump_changelog.sh

bump.undo: ## Goes back one commit, i.e. reverts changes on files from last version bump (experimental)
	@sh ./undo_bump_version.sh

pipenv.freeze.graphapi: ## dumps Pipfile.lock into a requirements.txt used in the docker build
	pipenv lock --requirements > services/graph-api/requirements.txt
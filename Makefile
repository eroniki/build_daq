SHELL=/bin/bash
env_file = .env
include ${env_file}

.PHONY: clean up down restart stop reload ps logs logsf push env

all: build-core

default: all

build-core: reload
	docker exec -it $@ bash
	
clean: pyclean prune

up:
	@echo "Starting up containers for $(PROJECT_NAME)..."
	docker-compose up --build --detach --remove-orphans

down:
	@echo "Removing containers."
	docker-compose down	--remove-orphans

restart:
	@echo "Restarting containers."
	docker-compose restart

stop:
	@echo "Stopping containers for $(PROJECT_NAME)..."
	docker-compose stop

reload: reload_env reload_conts

reload_conts: stop down up

reload_env:
	@echo "Reloading the environment variables."
	@source ${env_file}

ps:
	@docker ps --filter name="$(PROJECT_NAME)*"

logs:
	@echo "Displaying past containers logs"
	docker-compose logs

logsf:
	@echo "Follow containers logs output"
	docker-compose logs -f

push:
	@docker login
	@docker-compose push

pyclean:
	@sudo find . -regex '^.*\(__pycache__\|\.py[co]\)$$' -delete

prune: prune_conts prune_vols

prune_conts:
	docker system prune --all --force

prune_vols:
	docker volume prune --force


DOCKER_COMPOSE_ARGS?=-f docker-compose.yml -f docker-compose.override.yml
DOCKER_COMPOSE?=docker compose ${DOCKER_COMPOSE_ARGS}

.PHONY: default
default: requirements-develop.txt
	pip install -r requirements-develop.txt
	python setup.py develop

requirements.txt:
	pip-compile -v requirements.in

requirements-develop.txt: requirements.txt
	pip-compile -v requirements-develop.in

.PHONY: runserver
runserver:
	python src/manage.py runserver 0.0.0.0:8000

.PHONY: check
check:
	black src/
	isort src/
	flake8 src/

.PHONY: build
build:
	test ! -d /app
	cd provision/docker/backend && docker build --target=base -t ghcr.io/somosaseb/somosaseb-api/base:latest .
	cd provision/docker/backend && docker build --target=develop -t ghcr.io/somosaseb/somosaseb-api/develop:latest .
	docker build -t ghcr.io/somosaseb/somosaseb-api:latest .

.PHONY: push
push: build
	docker push ghcr.io/somosaseb/somosaseb-api:latest

docker-compose.override.yml:
	echo 'version: "3.7"' >> docker-compose.override.yml

.PHONY: backend
backend: docker-compose.override.yml
	test ! -d /app
	${DOCKER_COMPOSE} up -d database
	${DOCKER_COMPOSE} run --rm --service-ports --use-aliases backend --shell

.PHONY: shell
shell: docker-compose.override.yml
	test ! -d /app
	# docker exec -it $$(docker compose ps | grep -E "backend.+running.+:8000" | cut -d" " -f1) bash
	${DOCKER_COMPOSE} exec -e COLUMNS="`tput cols`" -e LINES="`tput lines`" backend gosu app bash

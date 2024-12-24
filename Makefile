DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
ENV_EMAIL = --env-file .env_email
ENV_AWS = --env-file .env_aws
APP_FILE = docker_compose/app.yaml
STORAGES_FILE = docker_compose/storages.yaml
APP_CONTAINER = main-app
CELERY_FILE = docker_compose/celery.yaml

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV}  up --build -d

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} ${ENV_EMAIL} ${ENV_AWS}  up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} down

.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: all
all:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} -f ${CELERY_FILE} ${ENV} ${ENV_EMAIL} ${ENV_AWS}  up --build -d

.PHOBY: migrations
migrations:
	${EXEC} ${APP_CONTAINER} alembic upgrade head
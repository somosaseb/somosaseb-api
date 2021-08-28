#!/usr/bin/env bash
set -eux

IMAGE_NAME=ghcr.io/somosaseb/somosaseb-api:latest
CONTAINER_NAME=api.aseb.bo
ENV_FILE=${HOME}/.env

docker run \
  --pull always \
  --network host \
  --interactive \
  --rm \
  --tty \
  --env-file ${ENV_FILE} \
  \
  ${IMAGE_NAME} \
  gosu app python src/manage.py migrate
docker stop -t0 ${CONTAINER_NAME} ||:
docker rm -f ${CONTAINER_NAME} ||:
docker run \
  --detach \
  --pull always \
  --hostname backend \
  --env-file ${ENV_FILE} \
  --network host \
  --restart unless-stopped \
  --name ${CONTAINER_NAME} \
  \
  ${IMAGE_NAME} \
  /app/bin/runserver

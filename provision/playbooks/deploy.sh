#!/usr/bin/env bash
set -eux

docker pull ghcr.io/somosaseb/somosaseb-api:latest
docker run --rm -it --env-file $(pwd)/.env \
  ghcr.io/somosaseb/somosaseb-api:latest \
  gosu app python src/manage.py migrate

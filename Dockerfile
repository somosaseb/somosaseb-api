FROM node:14 as frontend

COPY src/frontend/package.json .
COPY src/frontend/package-lock.json .

RUN set -eux \
    && npm ci

COPY src/frontend/ .

RUN set -eux \
    && NODE_ENV=production npm run build

FROM aseb/core/base:latest

RUN set -eux \
    && mkdir -p /python \
    && chown -R ${APP_USER}:${APP_USER} /python \
    && gosu ${APP_USER} python -m venv /python \
    && gosu ${APP_USER} pip install --no-cache-dir -U pip wheel \
    && gosu ${APP_USER} pip install newrelic

COPY --chown=${APP_USER}:${APP_USER} requirements.txt /requirements.txt

RUN set -eux \
    && gosu ${APP_USER} pip install -r /requirements.txt

COPY --chown=${APP_USER}:${APP_USER} . /app
COPY --chown=${APP_USER}:${APP_USER} --from=frontend dist /app/public

ENV PYTHONPATH=/app/src

RUN set -eux \
    && export DJANGO_SETTINGS_MODULE=aseb.settings.test \
    && gosu ${APP_USER} pip install -e . \
    && gosu ${APP_USER} python src/manage.py collectstatic \
        --noinput -v2 \
        --ignore "package.json" \
        --ignore "*.md" \
        --ignore "*.scss" \
        --ignore "*.less"

ENV DJANGO_SETTINGS_MODULE=core.settings.production

EXPOSE 8000

CMD ["/app/bin/runserver"]

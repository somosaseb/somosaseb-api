FROM python:3.9.6-buster as base

ENV LANG="C.UTF-8" \
    LANGUAGE="en_US:en" \
    LC_COLLATE=C \
    DEBIAN_FRONTEND=noninteractive \
    TERM="xterm-256color"

RUN set -eux; \
    \
    export GOSU_VERSION=1.13; \
    fetchDeps="ca-certificates wget dirmngr gnupg cabextract xfonts-utils"; \
    savedAptMark="$(apt-mark showmanual)"; \
    dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')"; \
# Sometimes keyservers are not available, we will try several until one works.
    keyservers=" \
    ha.pool.sks-keyservers.net \
    hkp://p80.pool.sks-keyservers.net:80 \
    keyserver.ubuntu.com \
    hkp://keyserver.ubuntu.com:80 \
    pgp.mit.edu \
    "; \
    \
    echo deb http://deb.debian.org/debian buster main contrib non-free > /etc/apt/source.list ; \
    echo deb http://deb.debian.org/debian buster-updates main contrib non-free >> /etc/apt/source.list ; \
    echo deb http://security.debian.org buster/updates main >> /etc/apt/source.list ; \
    apt-get update; \
    apt-get install -y --no-install-recommends $fetchDeps; \
    rm -rf /var/lib/apt/lists/*; \
    \
# grab gosu for easy step-down from root
# https://github.com/tianon/gosu/releases
    wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/${GOSU_VERSION}/gosu-$dpkgArch"; \
    wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/${GOSU_VERSION}/gosu-$dpkgArch.asc"; \
    export GNUPGHOME="$(mktemp -d)"; \
    for server in ${keyservers}; do \
    gpg --no-tty --batch --keyserver "${server}" --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4 && break || : ; \
    done; \
    gpg  --no-tty --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu; \
    gpgconf --kill all; \
    rm -r "$GNUPGHOME" /usr/local/bin/gosu.asc; \
    chmod +x /usr/local/bin/gosu; \
    gosu nobody true; \
    \
# reset apt-mark's "manual" list so that "purge --auto-remove" will remove all build dependencies
    apt-mark auto '.*' > /dev/null; \
    [ -z "$savedAptMark" ] || apt-mark manual $savedAptMark; \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
    \
    rm -rf /var/cache/apt/*; \
    rm -rf /usr/share/man/*; \
    rm -rf /usr/share/doc/*; \
    rm -rf /var/lib/apt/lists/*;

RUN set -eux; \
    \
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -; \
    echo "deb http://apt.postgresql.org/pub/repos/apt/ buster-pgdg main" > /etc/apt/sources.list.d/pgdg.list; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
# Database management
        postgresql-client-common \
        postgresql-client-12 \
# Common tools for development and building
        build-essential \
        git \
        curl \
## Swig is required by m2crypto, required by django-ses[bounce]
        swig \
        gettext \
        tzdata \
        ca-certificates \
        locales \
# Library headers to build python packages
        musl-dev \
        zlib1g-dev \
        libc6-dev \
        libpq-dev \
        libxml2-dev \
        libxslt1-dev \
        libjansson-dev \
        libpcre3-dev \
        libpng-dev \
        libfreetype6-dev \
        libjpeg-dev \
        libssl-dev \
        zlib1g-dev \
        libbz2-dev \
        liblzma-dev \
        libffi-dev; \
    \
    rm -rf /var/cache/apt/*; \
    rm -rf /usr/share/man/*; \
    rm -rf /usr/share/doc/*; \
    rm -rf /var/lib/apt/lists/*;

ARG UID=1000
ARG GID=1000
ARG UNAME=app

RUN set -eux; \
# Setup non-root user
    \
    groupadd --gid ${GID} ${UNAME}; \
    \
    adduser \
    --uid ${UID} \
    --gid ${GID} \
    --disabled-password \
    --quiet \
    ${UNAME}; \
    \
    mkdir -p /app; \
    mkdir -p /python; \
    chown -R app:app /home/app; \
    chown -R app:app /app; \
    chown -R app:app /python;


ENV APP_UID=${UID} \
    APP_GID=${GID} \
    APP_USER=${UNAME} \
    PIP_TIMEOUT=60 \
    PIP_DISABLE_PIP_VERSION_CHECK=true \
    PIP_DOWNLOAD_CACHE=/python/pip-cache \
    DEFAULT_LOCAL_TMP=/python/tmp \
    XDG_CACHE_HOME=/python/cache \
    PYTHONENV=/python \
    PYTHONPATH=/app/src \
    PYTHONBUFFERED=1 \
    PYTHONHASHSEED=random \
    PATH="/app/bin:/python/bin:${PATH}"

COPY entrypoint-production.sh /sbin/docker-entrypoint.sh

ENTRYPOINT ["/sbin/docker-entrypoint.sh"]

WORKDIR /app

CMD ["python"]

# -- Develop image --

FROM base as develop

ENV ENVIRONMENT=develop

RUN set -eux; \
# Common utils dependencies
    \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        bash-completion \
        vim \
        unzip \
        htop \
        lsof \
        tmux; \
    \
# Install node
    curl -sL https://deb.nodesource.com/setup_12.x | bash - ;\
    apt-get install -y --no-install-recommends\
        nodejs; \
    \
# Cleanup
    rm -rf /var/cache/apt/*; \
    rm -rf /usr/share/man/*; \
    rm -rf /usr/share/doc/*; \
    rm -rf /var/lib/apt/lists/*;

VOLUME /home/app
VOLUME /python

COPY entrypoint-develop.sh /sbin/docker-entrypoint.sh

#!/usr/bin/env bash
set -eo pipefail
shopt -s nullglob

cd /app

YELLOW="\e[0;93m"
GREEN="\e[0;92m"
BOLD="\e[1m"
RESET="\e[0m"

step()    { echo -e "${YELLOW}${BOLD}===> ${RESET}${*}${RESET}"; }
success() { echo -e "${RESET}${GREEN}${BOLD}${*}${RESET}"; }

step "Environment: ${ENVIRONMENT}"
step "Current dir: $(pwd)"
step "Python version: $(python --version)"

function check_permissions() {
    (
        find /app /python \
            -not \( -name "frontend"  -prune \) \
            -not \( -name "node_modules"  -prune \) \
            -not \( -name ".git" -prune  \) \
            -not \( -name ".cache" -prune \) \
            -not -uid ${APP_UID} \
            -exec chown ${APP_USER}:${APP_USER} \{\} \; >/dev/null &

        chown ${APP_USER}:${APP_USER} /home/${APP_USER} >/dev/null &

        wait
    ) &

    step "Run permissions check"
}

function setup_python_env() {
    if [[ -f /python/bin/python ]]; then return 0; fi

    (
        set -x

        mkdir -p /python
        chown ${APP_USER}:${APP_USER} -R /python
        gosu ${APP_USER} python -m venv /python

        function pip-install() { gosu ${APP_USER} /python/bin/pip install ${*}; }
        function pip-compile() { gosu ${APP_USER} /python/bin/pip-compile --verbose ${*}; }

        pip-install --upgrade setuptools wheel pip-tools

        test ! -f requirements.txt \
            && pip-compile requirements.in ||:

        test ! -f requirements-develop.txt \
            && pip-compile requirements-develop.in ||:
    )

    gosu ${APP_USER} make default

    step "Python environment $(success [Done])"
}

(
    setup_python_env
    check_permissions
)

case "$1" in
    -)
        # Switch to app user
        if [[ ${1} = '-' ]]; then shift; fi
        set -- gosu ${APP_USER} "$@"
    ;;
    --shell)
        if [[ ${1} = '-' ]]; then shift; fi
        set -- gosu ${APP_USER} bash
    ;;
esac

step "Running: $*"

exec "$@"
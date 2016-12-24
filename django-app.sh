#!/bin/bash

# Application entry point framework for Django
# Copyright (C) 2016  Sergej Alikov <sergej.alikov@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

set -euo pipefail

APP_NAME="${APP_NAME:-djangoapp}"
PYTHON="${PYTHON:-python3}"
SYSTEMD_SERVICE="${SYSTEMD_SERVICE:-/etc/systemd/system/${APP_NAME}.service}"

PROG=$(basename "${0}")
BASE_DIR=$(dirname "${0}")

ENV_FILE="${BASE_DIR}/.env"
DEFAULT_VIRTUALENV_PATH="/usr/lib/${APP_NAME}/venv"
SECRET_LENGTH=64

FORCE=FALSE


usage () {
    cat <<EOF | to_stderr
Usage: ${PROG} [OPTIONS] COMMAND [ARGS]

COMMANDS:

  setup                       Interactive setup
  create-service USER         Create service to start application during system
                              boot process. Only SystemD is supported at the moment.
                              USER is a system user the application will be
                              running as
  create-virtualenv           Build virtualenv. Does nothing if virtual environment
                              exists already
  install-requirements        Installs required packages into existing configured
                              virtual environment
  manage [ARGS]               Invoke Django manage.py with ARGS
  test                        Run test suites
  migrate                     Run DB migrations
  collectstatic               Collect static files to the static root
  run COMMAND [ARGS]          Load environment and execute acommand in it (eg. gunicorn)


OPTIONS:

  -f, --force                 Forced mode
  -e, --envfile PATH          Specify custom .env location (current: ${ENV_FILE}))
  -h, --help                  Display this help text
EOF
}

to_stderr () {
    >&2 cat
}

msg () {
    local fmt str

    {
        if [[ "${#}" -gt 1 ]]; then
            printf "${@}"
        else
            printf "%s\n" "${@}"
        fi

    } | to_stderr
}

error () {
    msg "ERROR: %s\n" "${@}"
}

cmd_is_available () {
    which "${1}" >/dev/null 2>&1
}

is_true () {
    [[ "${1,,}" =~ ^(1|yes|on|true)$ ]]
}

is_function () {
    local function_name="${1}"

    declare -F "${function_name}" >/dev/null
}

is_in () {
    value="${1}"
    shift

    for i in "${@}"; do
        if [[ "${i}" = "${value}" ]]; then
            return 0
        fi
    done

    return 1
}

# Prompt for value on tty and return answer on stdout
get_value () {
    local prompt="${1}"
    local default_value="${2}"
    local val

    msg "%s [%s]: " "${prompt}" "${default_value}"
    read -r val
    msg

    printf "%q\n" "${val:-${default_value}}"
}

get_choice () {
    local prompt="${1}"
    local default_value="${2}"
    shift 2

    # Need at least one choice
    [[ "${#}" -gt 0 ]] || return 1

    local choice
    until is_in "${choice:-}" "${@}"; do
        choice=$(get_value "${prompt} (${*})" "${default_value}")
    done

    echo "${choice}"
}


load_env_file () {
    local rc=0

    set -a
    source "${ENV_FILE}" || rc=$?
    set +a

    if ! [[ "${rc}" -eq 0 ]]; then
        error "Unable to load ${ENV_FILE}. Running setup might help"
        return "${rc}"
    fi
}

secret () {
    local len="${1}"
    tr -dc "[:graph:]" < /dev/urandom | head -c "${len}" | base64 -w 0 || true
}

is_virtualenv () {
    local path="${1}"

    [[ -e "${path}/bin/activate" ]]
}

create_virtualenv () {
    local path="${1}"

    if [[ -e "${path}" ]]; then
        if is_virtualenv "${path}"; then
            rm -rf --one-file-system --preserve-root -- "${path}"
        else
            error "${path} exists, but is not a virtualenv, aborting"
            return 1
        fi
    fi

    virtualenv -p "${PYTHON}" "${path}"
}

activate_virtualenv () {
    local path="${1}"

    local rc=0

    set +u
    source "${path}/bin/activate" || rc=$?
    set -u

    if ! [[ "${rc}" -eq 0 ]]; then
        msg "Unable to activate ${path} virtualenv. Did you create it?"
        return "${rc}"
    fi
}

buildconfig () {
    local secret_key virtualenv_path

    msg "Please provide the Django secret key or use the auto-generated one"
    secret_key=$(get_value "Django SECRET" "$(secret "${SECRET_LENGTH}")")

    msg "Please provide the path to the virtual environment"
    virtualenv_path=$(get_value "Virtual environment path" "${DEFAULT_VIRTUALENV_PATH}")

    cat <<EOF
VIRTUALENV=${virtualenv_path}
SECRET_KEY=${secret_key}
EOF

    # Call the customized setup function if defined
    if is_function app_buildconfig; then
        app_buildconfig "${@}"
    fi
}

create_service () {
    local service_user="${1:-}"
    local systemd=FALSE

    if ! [[ "${service_user}" ]]; then
        error "Please provide user argument"
        return 1
    fi

    if cmd_is_available systemctl; then
        if $(systemctl --quiet is-active -- '-.mount'); then
            systemd=TRUE
        fi
    fi

    if is_true "${systemd}"; then
        cat <<EOF >"${SYSTEMD_SERVICE}"
[Unit]
Description=$(basename "${SYSTEMD_SERVICE}")
After=network.target

[Service]
User=${service_user}
ExecStart=$(readlink -f "${0}") start
EOF
    else
        error "Only SystemD-based systems are supported at the moment"
        return 1
    fi
}

install_requirements () {
    pip install -r "${BASE_DIR}/requirements.txt"
}

managepy () {
    exec python "${BASE_DIR}/manage.py" "${@}"
}

display_usage_and_exit () {

    usage | to_stderr

    # Call the customized usage function if defined
    if is_function app_usage; then
        cat <<EOF | to_stderr

${APP_NAME}-specific commands and options

EOF
        app_usage | to_stderr
    fi

    exit "${1:-0}"
}

do_cmd () {
    local command="${1}"
    shift

    if [[ "${command}" = "setup" ]]; then

        if [[ -f "${ENV_FILE}" ]] && ! is_true "${FORCE}"; then
            error "${ENV_FILE} exists already. Please specify forced mode to overwrite"
            return 1
        fi

        buildconfig "${@}" >"${ENV_FILE}"

        return 0

    else
        load_env_file
    fi

    # Call the customized command handler if defined
    if is_function app_do_cmd; then
        app_do_cmd "${command}" "${@}"
    fi

    case "${command}" in

        create-virtualenv)
            if ! is_virtualenv "${VIRTUALENV}" || is_true "${FORCE}"; then
                create_virtualenv "${VIRTUALENV}"
            fi
            ;;

        create-service)
            create_service "${@}"
            ;;

        install-requirements)
            activate_virtualenv "${VIRTUALENV}"
            install_requirements
            ;;

        # Convenience shortcuts
        test|migrate|collectstatic)
            set "${command}" "${@}"
            ;&  # fall-through

        manage)
            activate_virtualenv "${VIRTUALENV}"
            managepy "${@}"
            ;;

        run)
            activate_virtualenv "${VIRTUALENV}"
            exec "${@}"
            ;;

        *)
            error "Unknown command ${command}"
            return 1
            ;;
    esac
}

main () {
    local command

    [[ "${#}" -gt 0 ]] || display_usage_and_exit 1

    while [[ "${#}" -gt 0 ]]; do

        case "${1}" in

            -h|--help|help|'')
                display_usage_and_exit
                ;;

            -f|--force)
                FORCE=TRUE
                ;;

            -e|--env)
                shift
                ENV_FILE="${1}"
                ;;

            *)
                do_cmd "${@}"
                break
                ;;

        esac

        shift

    done
}

if [[ -n "${BASH_SOURCE:-}" && "${0}" = "${BASH_SOURCE}" ]]; then
    main "${@}"
fi

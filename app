#!/bin/bash

# Application-specific entry point framework handlers
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

APP_NAME="droll"
DEFAULT_STATICFILES_PATH="/var/lib/${APP_NAME}/media"
DEFAULT_DATABASE_URL="sqlite:///db.sqlite3"
WSGI="${APP_NAME}.wsgi"
DEFAULT_GUNICORN_BIND="127.0.0.1:8080"
DEFAULT_GUNICORN_WORKERS=$(($(nproc) * 2 + 1))


# Load the entry point framework
source "$(dirname "${0}")/django-app.sh"


# Application-specific usage message section
app_usage () {
    cat <<EOF
COMMANDS:

  start                       Start app in gunicorn
EOF
}

# Application-specific command dispatcher
app_do_cmd () {
    local command="${1}"
    shift

    case "${command}" in

        start)
            activate_virtualenv "${VIRTUALENV}"
            exec gunicorn "${WSGI}" --chdir "${BASE_DIR}" --name "${APP_NAME}" --workers="${GUNICORN_WORKERS}" --bind="${GUNICORN_BIND}" --log-file=-
            ;;

    esac
}

# Application-specific setup procedure
app_buildconfig () {
    local database_url bind_to num_workers
    local static_backend static_root sftp_host sftp_user sftp_password

    msg "Please provide the 12factor-app-compatible database URL. Example: postgres://user:pass@pg.example.com:5432/dbname"
    database_url=$(get_value "Database URL" "${DEFAULT_DATABASE_URL}")

    msg  "Please provide the address:port gunicorn should bind to"
    gunicorn_bind=$(get_value "Bind to" "${DEFAULT_GUNICORN_BIND}")

    msg "Please specify the number of workers gunicorn should create"
    gunicorn_workers=$(get_value "Workers" "${DEFAULT_GUNICORN_WORKERS}")

    static_backend=$(get_choice "Staticfiles backend" "local" "local" "sftp")

    case "${static_backend}" in

        local)
            msg  "Please provide the local path to store the static files"
            static_root=$(get_value "Staticfiles local path" "${DEFAULT_STATICFILES_PATH}")
            ;;

        sftp)

            msg "Please provide the address of the SFTP server which will host the static files"
            static_sftp_host=$(get_value "SFTP host" "")

            msg "Please provide the username to use when connecting to the ${static_sftp_host}"
            static_sftp_user=$(get_value "SFTP username" "")

            msg "Please provide the password for the ${static_sftp_user}. Leave empty if you plan to use pubkey authentication"
            static_sftp_password=$(get_value "SFTP password" "")

            msg  "Please provide the path on the ${static_sftp_host} to store the static files"
            static_sftp_root=$(get_value "Staticfiles remote path" "${DEFAULT_STATICFILES_PATH}")
            ;;
    esac


    cat <<EOF
DATABASE_URL=${database_url}
GUNICORN_BIND=${gunicorn_bind}
GUNICORN_WORKERS=${gunicorn_workers}
STATIC_BACKEND=${static_backend}
STATIC_ROOT=${static_root:-}
STATIC_SFTP_HOST=${static_sftp_host:-}
STATIC_SFTP_ROOT=${static_sftp_root:-}
STATIC_SFTP_USERNAME=${static_sftp_user:-}
STATIC_SFTP_PASSWORD=${static_sftp_password:-}
EOF
}


if [[ -n "${BASH_SOURCE:-}" && "${0}" = "${BASH_SOURCE}" ]]; then
    main "${@}"
fi

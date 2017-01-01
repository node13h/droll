# Copyright (C) 2017 Sergej Alikov <sergej.alikov@gmail.com>

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


from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from storages.backends.sftpstorage import SFTPStorage


class SFTPStaticFilesStorage(SFTPStorage):
    """Proxy class to the django-storages SFTPStorage.
    Acts as a layer of abstraction and a way to work around
    the current bugs in SFTPStorage
    """

    def __init__(self):
        try:
            conf = settings.STATIC_STORAGE_SFTP
        except AttributeError:
            raise ImproperlyConfigured(
                'Please set the STATIC_STORAGE_SFTP setting')

        try:
            host = conf['HOST']
        except KeyError:
            raise ImproperlyConfigured(
                'HOST key is required in STATIC_STORAGE_SFTP setting')

        super().__init__(
            host,
            params=conf.get('CONNECT_PARAMS', {}),
            interactive=conf.get('INTERACTIVE', False),
            file_mode=conf.get('FILE_MODE', None),
            dir_mode=conf.get('DIR_MODE', None),
            uid=conf.get('UID', None),
            gid=conf.get('GID', None),
            known_host_file=conf.get('KNOWN_HOST_FILE', None),
            root_path=conf.get('ROOT', None),
            base_url=conf.get('BASE_URL', None))

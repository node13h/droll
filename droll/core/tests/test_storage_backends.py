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


from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

from ..storage_backends import SFTPStaticFilesStorage


class StaticFileStorageTestCase(TestCase):
    def test_settings(self):
        settings = {
            'STATIC_STORAGE_SFTP': {
                'HOST': 'sftp.example.com',
                'CONNECT_PARAMS': {
                    'username': 'user',
                    'password': 'pass',
                },
                'INTERACTIVE': True,
                'FILE_MODE': 666,
                'DIR_MODE': 777,
                'UID': 'root',
                'GID': 'nobody',
                'KNOWN_HOST_FILE': '/usr/lib/app/known_hosts',
                'ROOT': '/srv/app/static',
                'BASE_URL': '/app/static/',
            }
        }

        with self.settings(**settings):
            s = SFTPStaticFilesStorage()

        self.assertEqual(s._host, 'sftp.example.com')
        self.assertEqual(s._params, {'username': 'user', 'password': 'pass'})
        self.assertTrue(s._interactive)
        self.assertEqual(s._file_mode, 666)
        self.assertEqual(s._dir_mode, 777)
        self.assertEqual(s._uid, 'root')
        self.assertEqual(s._gid, 'nobody')
        self.assertEqual(s._known_host_file, '/usr/lib/app/known_hosts')
        self.assertEqual(s._root_path, '/srv/app/static')
        self.assertEqual(s._base_url, '/app/static/')

    def test_minimal_settings(self):
        settings = {
            'STATIC_STORAGE_SFTP': {
                'HOST': 'sftp.example.com',
            },
            'MEDIA_URL': '/media/',
        }

        with self.settings(**settings):
            s = SFTPStaticFilesStorage()

        self.assertEqual(s._host, 'sftp.example.com')
        self.assertEqual(s._params, {})
        self.assertFalse(s._interactive)
        self.assertIsNone(s._file_mode)
        self.assertIsNone(s._dir_mode)
        self.assertIsNone(s._uid)
        self.assertIsNone(s._gid)
        self.assertIsNone(s._known_host_file)
        self.assertEqual(s._root_path, '')
        self.assertEqual(s._base_url, '/media/')

    def test_no_host_raises(self):
        settings = {
            'STATIC_STORAGE_SFTP': {
                'CONNECT_PARAMS': {
                    'username': 'user',
                    'password': 'pass',
                },
                'INTERACTIVE': True,
                'FILE_MODE': 666,
                'DIR_MODE': 777,
                'UID': 'root',
                'GID': 'nobody',
                'KNOWN_HOST_FILE': '/usr/lib/app/known_hosts',
                'ROOT': '/srv/app/static',
                'URL': '/app/static/',
            }
        }

        with self.settings(**settings):
            with self.assertRaises(ImproperlyConfigured):
                SFTPStaticFilesStorage()

    def test_no_settings_raises(self):
        with self.settings():
            if hasattr(settings, 'STATIC_STORAGE_SFTP'):
                del settings.STATIC_STORAGE_SFTP

            with self.assertRaises(ImproperlyConfigured):
                SFTPStaticFilesStorage()

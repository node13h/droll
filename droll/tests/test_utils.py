import os
from unittest import TestCase
from unittest.mock import patch

from droll.application import utils


def fake_env(func):
    def func_wrapper(self):
        with patch.object(os, 'environ', self.envmock):
            func(self)

    return func_wrapper


class EnvTestCase(TestCase):

    def setUp(self):
        self.envmock = {
            'TEST_ENV_TRUE': 'true',
            'TEST_ENV_1': '1',
            'TEST_ENV_YES': 'yes',
            'TEST_ENV_ON': 'on',
            'TEST_ENV_TRUE_CASE': 'true',
            'TEST_ENV_OTHER': 'any-other-value',
            'TEST_ENV_EMPTY': '',
            'TEST_ENV_STR': 'A Test String',
            'TEST_ENV_INT': '9000',
            'TEST_ENV_LIST': 'one,t wo,three',
        }

    @fake_env
    def test_get_bool(self):
        env = utils.Env()

        self.assertTrue(env.get_bool('TEST_ENV_TRUE'))
        self.assertTrue(env.get_bool('TEST_ENV_TRUE_CASE'))
        self.assertTrue(env.get_bool('TEST_ENV_1'))
        self.assertTrue(env.get_bool('TEST_ENV_YES'))
        self.assertTrue(env.get_bool('TEST_ENV_ON'))
        self.assertFalse(env.get_bool('TEST_ENV_OTHER'))
        self.assertFalse(env.get_bool('TEST_ENV_EMPTY'))
        self.assertFalse(env.get_bool('TEST_ENV_NON_EXISTING'))

        self.assertTrue(env.get_bool('TEST_ENV_NON_EXISTING', default=True))
        self.assertFalse(env.get_bool('TEST_ENV_OTHER', default=True))

    @fake_env
    def test_get_int(self):
        env = utils.Env()

        self.assertEqual(env.get_int('TEST_ENV_INT'), 9000)
        self.assertEqual(env.get_int('TEST_ENV_INT', 100500), 9000)
        self.assertIsNone(env.get_int('TEST_ENV_STR'))
        self.assertIsNone(env.get_int('TEST_ENV_NON_EXISTING'))
        self.assertEqual(env.get_int('TEST_ENV_STR', 100500), 100500)
        self.assertEqual(env.get_int('TEST_ENV_NON_EXISTING', 100500), 100500)

    @fake_env
    def test_get(self):
        env = utils.Env()

        self.assertEqual(env.get('TEST_ENV_STR'), 'A Test String')
        self.assertIsNone(env.get('TEST_ENV_NON_EXISTING'))
        self.assertEqual(env.get('TEST_ENV_NON_EXISTING', default='Test'), 'Test')

    @fake_env
    def test_get_list(self):
        env = utils.Env()

        self.assertEqual(env.get_list('TEST_ENV_STR'), ['A Test String'])
        self.assertEqual(env.get_list('TEST_ENV_EMPTY'), [])
        self.assertIsNone(env.get_int('TEST_ENV_NON_EXISTING'))
        self.assertEqual(env.get_list('TEST_ENV_LIST'), ['one', 't wo', 'three'])
        self.assertEqual(env.get_list(
            'TEST_ENV_NON_EXISTING', default=['Test']), ['Test'])

    @fake_env
    def test_setitem(self):
        env = utils.Env()

        env['TEST_ENV_SET_BOOL_TRUE'] = True
        env['TEST_ENV_SET_BOOL_FALSE'] = False
        env['TEST_ENV_SET_INT'] = 9000
        env['TEST_ENV_SET_STR'] = 'Test'
        self.assertEqual(os.environ['TEST_ENV_SET_BOOL_TRUE'], 'true')
        self.assertEqual(os.environ['TEST_ENV_SET_BOOL_FALSE'], '')
        self.assertEqual(os.environ['TEST_ENV_SET_INT'], '9000')
        self.assertEqual(os.environ['TEST_ENV_SET_STR'], 'Test')

    @fake_env
    def test_delitem(self):
        env = utils.Env()

        del env['TEST_ENV_STR']

        self.assertNotIn('TEST_ENV_STR', os.environ)

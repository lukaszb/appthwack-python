"""
    thwacky.tests.test_api
    ~~~~~~~~~~~~~~~~~~~~~~

    Contains tests for `AppThwackApi` functionality.
"""
__author__ = 'Andrew Hawker <andrew@appthwack.com>'

import os
import unittest
from thwacky.tests import fixtures
from thwacky.thwacky import AppThwackApi, AppThwackApiError

class TestAppThwackApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.expected_status_code = 200
        cls.expected_content_type = 'application/json'
        cls.expected = cls.expected_status_code, cls.expected_content_type
        cls.env_key = 'APPTHWACK_API_KEY'
        cls.api_key = '<Test Key>'
        cls.api = AppThwackApi(cls.api_key)

    def assert_api_key(self, api):
        assert api.api_key == self.api_key

    def test_api_key_nonexistent(self):
        self.assertRaises(ValueError, AppThwackApi)

    def test_api_key_argument(self):
        self.assert_api_key(self.api)

    def test_api_key_environment(self):
        os.environ[self.env_key] = self.api_key
        api = AppThwackApi()
        self.assert_api_key(api)
        del os.environ[self.env_key]


if __name__ == '__main__':
    unittest.main()
"""
    thwacky.tests.test_rest
    ~~~~~~~~~~~~~~~~~~~~~~~

    Contains tests for REST client functionality.
"""
__author__ = 'Andrew Hawker <andrew@appthwack.com>'

import unittest
from thwacky.tests import fixtures
from thwacky.thwacky import expects, AppThwackApiError, RequestsMixin


class TestRequestsMixin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.requests = RequestsMixin()
        cls.requests.api_key = '<Test Key>'
        cls.expected_status_code = 200
        cls.expected_content_type = 'application/json'
        cls.expected_url_resources = ('api', 'project')
        cls.expected = cls.expected_status_code, cls.expected_content_type

    def assert_valid_response(self, response):
        def assert_url(response, expected_resources):
            assert response.url == '/'.join(filter(None, (self.requests.domain,) + expected_resources))
        def assert_auth(response, expected_api_key):
            assert response.auth == (expected_api_key, None)

        fixtures.assert_status_code(response, self.expected_status_code)
        fixtures.assert_content_type(response, self.expected_content_type)
        assert_url(response, self.expected_url_resources)
        assert_auth(response, self.requests.api_key)


    def test_expected_get_response(self):
        self.requests.session = fixtures.SessionMock(*self.expected)
        response = self.requests.get('project')
        self.assert_valid_response(response)

    def test_expected_post_response(self):
        self.requests.session = fixtures.SessionMock(*self.expected)
        response = self.requests.post('project')
        self.assert_valid_response(response)

    def test_exception_on_unexpected_post_status_code(self):
        self.requests.session = fixtures.SessionMock(404, self.expected_content_type)
        self.assertRaises(AppThwackApiError, self.requests.get, 'project')

    def test_exception_on_unexpected_post_content_type(self):
        self.requests.session = fixtures.SessionMock(self.expected_status_code, 'text/html')
        self.assertRaises(AppThwackApiError, self.requests.get, 'project')

    def test_exception_on_unexpected_post_status_code(self):
        self.requests.session = fixtures.SessionMock(404, self.expected_content_type)
        self.assertRaises(AppThwackApiError, self.requests.post, 'project')

    def test_exception_on_unexpected_post_content_type(self):
        self.requests.session = fixtures.SessionMock(self.expected_status_code, 'text/html')
        self.assertRaises(AppThwackApiError, self.requests.post, 'project')


class TestExpectsDecorator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.expected_status_code = 200
        cls.expected_content_type = 'application/json'
        cls.expected = cls.expected_status_code, cls.expected_content_type
        cls.request_mock = lambda self, status_code, content_type: fixtures.ResponseMock(status_code, content_type)

    def test_valid_response(self):
        response = expects(*self.expected)(self.request_mock)(*self.expected)
        fixtures.assert_status_code(response, self.expected_status_code)
        fixtures.assert_content_type(response, self.expected_content_type)

    def test_invalid_response_status_code(self):
        request = expects(*self.expected)(self.request_mock)
        self.assertRaises(AppThwackApiError, request, 400, self.expected_content_type)

    def test_invalid_response_content_type(self):
        request = expects(*self.expected)(self.request_mock)
        self.assertRaises(AppThwackApiError, request, self.expected_status_code, 'text/html')


if __name__ == '__main__':
    unittest.main()
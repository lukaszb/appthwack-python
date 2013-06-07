"""
    thwacky.tests.fixtures
    ~~~~~~~~~~~~~~~~~~~~~~

    Contains test fixtures and test helper functions.
"""
__author__ = 'Andrew Hawker <andrew@appthwack.com>'

import json

def assert_status_code(response, expected_status_code):
    assert response.status_code == expected_status_code

def assert_content_type(response, expected_content_type):
    assert response.headers.get('content-type') == expected_content_type


class ResponseMock(object):

    def __init__(self, status_code, content_type, **kwargs):
        self.status_code = status_code
        self.content_type = content_type
        self.text = str(self)
        self.__dict__.update(kwargs)

    def __str__(self):
        return '<MockResponse: {0} - {1}>'.format(self.status_code, self.content_type)

    @property
    def headers(self):
        return {'content-type': self.content_type}

    def json(self):
        return json.loads(self.text)


class SessionMock(object):

    def __init__(self, status_code, content_type):
        self.status_code = status_code
        self.content_type = content_type

    def get(self, url, **kwargs):
        return ResponseMock(self.status_code, self.content_type, url=url, **kwargs)

    def post(self, url, **kwargs):
        return ResponseMock(self.status_code, self.content_type, url=url, **kwargs)
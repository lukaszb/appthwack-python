"""
    thwacky.tests.test_utils
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Contains tests for top level utility functions.
"""
__author__ = 'Andrew Hawker <andrew@appthwack.com>'

import unittest
from thwacky.thwacky import urlify, keyword_filter


class TestUrlify(unittest.TestCase):
    def test_no_inputs(self):
        assert urlify() == ''

    def test_resources(self):
        assert urlify('api') == 'api'
        assert urlify('api', 'run') == 'api/run'
        assert urlify('api', 'run', 'status') == 'api/run/status'

    def test_query_string(self):
        assert urlify(**dict(project='thwacky')) == 'project=thwacky'
        assert urlify(**dict(project='thwacky', state='testing')) == 'project=thwacky&state=testing'

    def test_resources_with_query_string(self):
        resources = 'api project'.split()
        params = dict(project='thwacky', state='testing')
        assert urlify(*resources, **params) == 'api/project?project=thwacky&state=testing'


class TestKeywordFilter(unittest.TestCase):
    def test_no_keys(self):
        assert keyword_filter(()) == (None, None)

    def test_no_matches(self):
        keys = 'name'.split()
        assert keyword_filter(keys) == (None, None)

    def test_one_match(self):
        keys = 'name'.split()
        assert keyword_filter(keys, **dict(name='thwacky')) == ('name', 'thwacky')

    def test_multi_match(self):
        keys = 'name id'.split()
        assert keyword_filter(keys, **dict(name='thwacky', id=10)) == ('name', 'thwacky')


if __name__ == '__main__':
    unittest.main()


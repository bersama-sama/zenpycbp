# Zenpy accepts an API token
# Or a password
import os
from zenpy import Zenpy
import unittest

creds = {
    'email' : os.environ.get("ZENPY_TEST_EMAIL"),
    'password' : os.environ.get("ZENPY_TEST_PASSWORD"),
    'subdomain': os.environ.get("ZENPY_TEST_SUBDOMAIN"),
    'domain': os.environ.get("ZENPY_TEST_DOMAIN")
}

class TagsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.zenpy_client = Zenpy(**creds)
    @classmethod
    def tearDownClass(self):
        self.zenpy_client = None

    def test_get_CBP(self):
        no_params_tags = []
        for tag in self.zenpy_client.tags():
            no_params_tags.append(tag)
        params_tags = []
        for tag in self.zenpy_client.tags(cursor_pagination=1):
            params_tags.append(tag)
        self.assertEqual(len(no_params_tags), len(params_tags), "Cardinality same")
        self.assertNotEqual(len(no_params_tags), 0, "Cardinality positive")

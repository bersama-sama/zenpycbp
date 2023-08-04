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

class UsersTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.zenpy_client = Zenpy(**creds)
    @classmethod
    def tearDownClass(self):
        self.zenpy_client = None

    def test_get_CBP(self):
        no_params_users = []
        for user in self.zenpy_client.users():
            no_params_users.append(user)
        params_users = []
        for user in self.zenpy_client.users(cursor_pagination=1):
            params_users.append(user)
        self.assertEqual(len(no_params_users), len(params_users), "Cardinality same")
        self.assertNotEqual(len(no_params_users), 0, "Cardinality positive")

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

class MacrosTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.zenpy_client = Zenpy(**creds)
    @classmethod
    def tearDownClass(self):
        self.zenpy_client = None

    def test_get_CBP(self):
        no_params_macros = []
        for macro in self.zenpy_client.macros():
            no_params_macros.append(macro)
        params_macros = []
        for macro in self.zenpy_client.macros(cursor_pagination=1):
            params_macros.append(macro)

        self.assertEqual(len(no_params_macros), len(params_macros), "Cardinality same")
        self.assertNotEqual(len(no_params_macros), 0, "Cardinality positive")
        self.assertGreater(len(params_macros), 1, "Should have more than one")

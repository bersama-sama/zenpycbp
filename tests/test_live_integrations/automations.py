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

class AutomationsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.zenpy_client = Zenpy(**creds)
    @classmethod
    def tearDownClass(self):
        self.zenpy_client = None

    def test_get_CBP(self):
        no_params_automations = []
        for automation in self.zenpy_client.automations():
            no_params_automations.append(automation)
        params_automations = []
        for automation in self.zenpy_client.automations(cursor_pagination=1):
            params_automations.append(automation)

        self.assertEqual(len(no_params_automations), len(params_automations), "Cardinality same")
        self.assertNotEqual(len(no_params_automations), 0, "Cardinality positive")
        self.assertGreater(len(params_automations), 2, "Should have more than two")

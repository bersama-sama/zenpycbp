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

class TriggersTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.zenpy_client = Zenpy(**creds)
    @classmethod
    def tearDownClass(self):
        self.zenpy_client = None

    def test_get_CBP(self):
        no_params_tiggers = []
        for trigger in self.zenpy_client.triggers():
            no_params_tiggers.append(trigger)
        params_triggers = []
        for trigger in self.zenpy_client.triggers(cursor_pagination=1):
            params_triggers.append(trigger)
        self.assertEqual(len(no_params_tiggers), len(params_triggers), "Cardinality same")
        self.assertNotEqual(len(no_params_tiggers), 0, "Cardinality positive")

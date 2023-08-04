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

class TicketAuditsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.zenpy_client = Zenpy(**creds)
    @classmethod
    def tearDownClass(self):
        self.zenpy_client = None

    def test_get_CBP(self):
        no_params_audits = []
        for audit in self.zenpy_client.tickets.audits():
            no_params_audits.append(audit)
        params_audits = []
        for audit in self.zenpy_client.tickets.audits(cursor_pagination=1):
            params_audits.append(audit)
        self.assertEqual(len(no_params_audits), len(params_audits), "Cardinality same")
        self.assertNotEqual(len(no_params_audits), 0, "Cardinality positive")

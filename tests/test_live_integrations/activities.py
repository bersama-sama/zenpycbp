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

class ActivitiesTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.zenpy_client = Zenpy(**creds)
    @classmethod
    def tearDownClass(self):
        self.zenpy_client = None

    def test_get_CBP(self):
        no_params_activities = []
        for activity in self.zenpy_client.activities():
            no_params_activities.append(activity)
        params_activities = []
        for activity in self.zenpy_client.activities(cursor_pagination=1):
            params_activities.append(activity)
        self.assertEqual(len(no_params_activities), len(params_activities), "Cardinality same")
        self.assertNotEqual(len(no_params_activities), 0, "Cardinality positive")

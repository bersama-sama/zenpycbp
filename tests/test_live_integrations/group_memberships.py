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

class GroupMembershipsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.zenpy_client = Zenpy(**creds)
    @classmethod
    def tearDownClass(self):
        self.zenpy_client = None

    def test_get_CBP(self):
        no_params_membershipos = []
        for membership in self.zenpy_client.group_memberships():
            no_params_membershipos.append(membership)
        params_memberships = []
        for membership in self.zenpy_client.group_memberships(cursor_pagination=1):
            params_memberships.append(membership)
        self.assertEqual(len(no_params_membershipos), len(params_memberships), "Cardinality same")
        self.assertNotEqual(len(no_params_membershipos), 0, "Cardinality positive")

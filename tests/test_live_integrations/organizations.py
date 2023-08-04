# Zenpy accepts an API token
# Or a password
import os
import sys
from zenpy import Zenpy
from zenpy.lib.api_objects import Organization
import unittest
from random import randint

creds = {
    'email' : os.environ.get("ZENPY_TEST_EMAIL"),
    'password' : os.environ.get("ZENPY_TEST_PASSWORD"),
    'subdomain': os.environ.get("ZENPY_TEST_SUBDOMAIN"),
    'domain': os.environ.get("ZENPY_TEST_DOMAIN")
}

class OrganizationsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.zenpy_client = Zenpy(**creds)
        self.my_organizations = self.create_organizations(self)

    @classmethod
    def tearDownClass(self):
        self.destroy_my_organizations(self)
        self.zenpy_client = None

    def create_organizations(self):
        rand_hex_str_1 = hex(randint(0, sys.maxsize))
        rand_hex_str_2 = hex(randint(0, sys.maxsize))
        self.zenpy_client.organizations.create(Organization(name="From ZenPyTest " + rand_hex_str_1, description="Thing " + rand_hex_str_1))
        self.zenpy_client.organizations.create(Organization(name="From ZenPyTest " + rand_hex_str_2, description="Thing " + rand_hex_str_2))
        my_organizations = []
        for org in self.zenpy_client.organizations():
            if org.name == "From ZenPyTest " + rand_hex_str_1 or org.name == "From ZenPyTest " + rand_hex_str_2:
                my_organizations.append(org)

        return my_organizations

    def destroy_my_organizations(self):
        for org in self.my_organizations:
            self.zenpy_client.organizations.delete(org)

    def test_get_CBP(self):
        no_params_organizations = []
        for org in self.zenpy_client.organizations():
            no_params_organizations.append(org)
        params_organizations = []
        for org in self.zenpy_client.organizations(cursor_pagination=1):
            params_organizations.append(org)
        self.assertEqual(len(no_params_organizations), len(params_organizations), "Cardinality same")
        self.assertNotEqual(len(no_params_organizations), 0, "Cardinality positive")
        self.assertGreater(len(no_params_organizations), 2, "Cardinality greater than 2 (that were created)")
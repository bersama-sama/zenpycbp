# Zenpy accepts an API token
# Or a password
import os
import sys
from zenpy import Zenpy
from zenpy.lib.api_objects import Group
import unittest
from random import randint

creds = {
    'email' : os.environ.get("ZENPY_TEST_EMAIL"),
    'password' : os.environ.get("ZENPY_TEST_PASSWORD"),
    'subdomain': os.environ.get("ZENPY_TEST_SUBDOMAIN"),
    'domain': os.environ.get("ZENPY_TEST_DOMAIN")
}

class GroupsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.zenpy_client = Zenpy(**creds)
        self.my_groups = self.create_groups(self)

    @classmethod
    def tearDownClass(self):
        self.destroy_my_groups(self)
        self.zenpy_client = None

    def create_groups(self):
        rand_hex_str_1 = hex(randint(0, sys.maxsize))
        rand_hex_str_2 = hex(randint(0, sys.maxsize))
        self.zenpy_client.groups.create(Group(name="From ZenPyTest " + rand_hex_str_1, description="Thing " + rand_hex_str_1))
        self.zenpy_client.groups.create(Group(name="From ZenPyTest " + rand_hex_str_2, description="Thing " + rand_hex_str_2))
        my_groups = []
        for group in self.zenpy_client.groups():
            if group.name == "From ZenPyTest " + rand_hex_str_1 or group.name == "From ZenPyTest " + rand_hex_str_2:
                my_groups.append(group)

        return my_groups

    def destroy_my_groups(self):
        for group in self.my_groups:
            self.zenpy_client.groups.delete(group)

    def test_get_CBP(self):
        no_params_groups = []
        for group in self.zenpy_client.groups():
            no_params_groups.append(group)
        params_groups = []
        for group in self.zenpy_client.groups(cursor_pagination=1):
            params_groups.append(group)
        self.assertEqual(len(no_params_groups), len(params_groups), "Cardinality same")
        self.assertNotEqual(len(no_params_groups), 0, "Cardinality positive")
        self.assertGreater(len(no_params_groups), 2, "Cardinality greater than 2 (that were created)")
# Zenpy accepts an API token
# Or a password
import os
import sys
from zenpy import Zenpy
from zenpy.lib.api_objects import RecipientAddress
import unittest
from random import randint

creds = {
    'email' : os.environ.get("ZENPY_TEST_EMAIL"),
    'password' : os.environ.get("ZENPY_TEST_PASSWORD"),
    'subdomain': os.environ.get("ZENPY_TEST_SUBDOMAIN"),
    'domain': os.environ.get("ZENPY_TEST_DOMAIN")
}

class RecipientAddressesestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.zenpy_client = Zenpy(**creds)
        self.my_addresses = self.create_addresses(self)

    @classmethod
    def tearDownClass(self):
        self.destroy_my_addresses(self)
        self.zenpy_client = None

    def create_addresses(self):
        rand_hex_str_1 = hex(randint(0, sys.maxsize))
        rand_hex_str_2 = hex(randint(0, sys.maxsize))
        self.zenpy_client.recipient_addresses.create(RecipientAddress(name="From ZenPyTest " + rand_hex_str_1, email="Thing" + rand_hex_str_1 + "@" + creds['subdomain'] + ".com"))
        self.zenpy_client.recipient_addresses.create(RecipientAddress(name="From ZenPyTest " + rand_hex_str_2, email="Thing" + rand_hex_str_2 + "@" + creds['subdomain'] + ".com"))
        my_addresses = []
        for address in self.zenpy_client.recipient_addresses():
            if address.name == "From ZenPyTest " + rand_hex_str_1 or address.name == "From ZenPyTest " + rand_hex_str_2:
                my_addresses.append(address)

        return my_addresses

    def destroy_my_addresses(self):
        for address in self.my_addresses:
            self.zenpy_client.recipient_addresses.delete(address)

    def test_get_CBP(self):
        no_params_addresses = []
        for address in self.zenpy_client.recipient_addresses():
            no_params_addresses.append(address)
        params_addresses = []
        for address in self.zenpy_client.recipient_addresses(cursor_pagination=1):
            params_addresses.append(address)
        self.assertEqual(len(no_params_addresses), len(params_addresses), "Cardinality same")
        self.assertNotEqual(len(no_params_addresses), 0, "Cardinality positive")
        self.assertGreater(len(no_params_addresses), 2, "Cardinality greater than 2 (that were created)")
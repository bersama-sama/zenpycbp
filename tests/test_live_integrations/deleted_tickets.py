# Zenpy accepts an API token
# Or a password
import os
import sys
from zenpy import Zenpy
from zenpy.lib.api_objects import Ticket
import unittest
from random import randint

creds = {
    'email' : os.environ.get("ZENPY_TEST_EMAIL"),
    'password' : os.environ.get("ZENPY_TEST_PASSWORD"),
    'subdomain': os.environ.get("ZENPY_TEST_SUBDOMAIN"),
    'domain': os.environ.get("ZENPY_TEST_DOMAIN")
}

class DeletedTicketsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.zenpy_client = Zenpy(**creds)
        self.my_tickets = self.create_tickets(self)
        self.delete_my_tickets(self)


    @classmethod
    def tearDownClass(self):
        self.destroy_my_tickets(self)
        self.zenpy_client = None

    def create_tickets(self):
        rand_hex_str_1 = hex(randint(0, sys.maxsize))
        rand_hex_str_2 = hex(randint(0, sys.maxsize))
        self.zenpy_client.tickets.create(Ticket(subject="From ZenPyTest " + rand_hex_str_1, description="Thing " + rand_hex_str_1))
        self.zenpy_client.tickets.create(Ticket(subject="From ZenPyTest " + rand_hex_str_2, description="Thing " + rand_hex_str_2))
        my_tickets = []
        for ticket in self.zenpy_client.tickets():
            if ticket.subject == "From ZenPyTest " + rand_hex_str_1 or ticket.subject == "From ZenPyTest " + rand_hex_str_2:
                my_tickets.append(ticket)
        return my_tickets

    def delete_my_tickets(self):
        for ticket in self.my_tickets:
            self.zenpy_client.tickets.delete(ticket)

    def destroy_my_tickets(self):
        for ticket in self.my_tickets:
            self.zenpy_client.tickets.permanently_delete(ticket)

    def test_get_CBP(self):
        no_params_tickets = []
        for ticket in self.zenpy_client.tickets.deleted():
            no_params_tickets.append(ticket)
        params_tickets = []
        for ticket in self.zenpy_client.tickets.deleted(cursor_pagination=1):
            params_tickets.append(ticket)

        self.assertEqual(len(no_params_tickets), len(params_tickets), "Cardinality same")
        self.assertNotEqual(len(no_params_tickets), 0, "Cardinality positive")
        self.assertGreater(len(no_params_tickets), 1, "Should have more than one")

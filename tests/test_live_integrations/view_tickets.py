# Zenpy accepts an API token
# Or a password
import os
from zenpy import Zenpy
from zenpy.lib.api_objects import Ticket, View
import unittest

creds = {
    'email' : os.environ.get("ZENPY_TEST_EMAIL"),
    'password' : os.environ.get("ZENPY_TEST_PASSWORD"),
    'subdomain': os.environ.get("ZENPY_TEST_SUBDOMAIN"),
    'domain': os.environ.get("ZENPY_TEST_DOMAIN")
}

class ViewTicketsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.zenpy_client = Zenpy(**creds)
        for view in self.zenpy_client.views():
            if view.title == "Your unsolved tickets":
                self.target_view = view
                break
    @classmethod
    def tearDownClass(self):
        self.zenpy_client = None

    def test_get_CBP(self):
        no_params_tickets = []
        for ticket in self.zenpy_client.views.tickets(self.target_view):
            no_params_tickets.append(ticket)
        params_tickets = []
        for ticket in self.zenpy_client.views.tickets(self.target_view, cursor_pagination=1):
            params_tickets.append(ticket)

        self.assertEqual(len(no_params_tickets), len(params_tickets), "Cardinality same")
        self.assertNotEqual(len(no_params_tickets), 0, "Cardinality positive")
        self.assertGreater(len(params_tickets), 2, "Tickets has appreciable count")

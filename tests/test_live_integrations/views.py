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

class ViewsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.zenpy_client = Zenpy(**creds)
        self.no_params_views = []
        for view in self.zenpy_client.views():
            self.no_params_views.append(view)
    @classmethod
    def tearDownClass(self):
        self.zenpy_client = None

    def test_list_by_id(self):
        view = self.zenpy_client.views(id=self.no_params_views[0].id)
        self.assertEqual(view.id, self.no_params_views[0].id, "View obtrained")

    def test_get_CBP(self):
        params_views = []
        for view in self.zenpy_client.views(cursor_pagination=1):
            params_views.append(view)
        self.assertEqual(len(self.no_params_views), len(params_views), "Cardinality same")
        self.assertNotEqual(len(self.no_params_views), 0, "Cardinality positive")

    def test_count(self):
        cnt = self.zenpy_client.views.count()
        self.assertGreater(cnt.value, 0, "Has non zero count")
    def test_get_active_views(self):
        params_views = []
        for view in self.zenpy_client.views.active():
            params_views.append(view)
        self.assertNotEqual(len(self.no_params_views), 0, "Cardinality positive")
    def test_get_compact_views(self):
        params_views = []
        for view in self.zenpy_client.views.compact():
            params_views.append(view)
        self.assertNotEqual(len(self.no_params_views), 0, "Cardinality positive")

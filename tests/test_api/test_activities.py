from test_api.fixtures import ZenpyApiTestCase


class TestActivities(ZenpyApiTestCase):
    __test__ = True

    def test_get_activities_cbp_obp(self):
        with self.recorder.use_cassette(
                self.generate_cassette_name(), serialize_with="prettyjson"
        ):
            activities_default = [a for a in self.zenpy_client.activities()]
            self.assertNotEqual(len(activities_default), 0, "Getting default activities failed")

            activities_cbp = [a for a in self.zenpy_client.activities(cursor_pagination=True)]
            self.assertNotEqual(len(activities_cbp), 0, "Getting activities with CBP failed")

            activities_obp = [a for a in self.zenpy_client.activities(cursor_pagination=False)]
            self.assertNotEqual(len(activities_obp), 0, "Getting activities with OBP failed")

            self.assertEqual(len(activities_obp), len(activities_cbp), "Getting activities with OBP<>CBP")

            activities_cbp_1 = [a for a in self.zenpy_client.activities(cursor_pagination=1)]
            self.assertEqual(len(activities_cbp_1), len(activities_cbp), "Getting activities with CBP=1 failed")

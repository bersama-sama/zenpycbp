from test_api.fixtures import ZenpyApiTestCase

from test_api.fixtures.__init__ import (
    SingleCreateApiTestCase,
    SingleUpdateApiTestCase,
    SingleDeleteApiTestCase,
    PaginationTestCase,
)

from zenpy.lib.api_objects import (
    Automation,
    Activity
)


class TestActivities(PaginationTestCase):
    __test__ = True
    ZenpyType = Activity
    api_name = "activities"
    object_kwargs = {}


class TestAutomations(SingleCreateApiTestCase, SingleUpdateApiTestCase, SingleDeleteApiTestCase, PaginationTestCase):
    __test__ = True
    ZenpyType = Automation
    api_name = "automations"

    object_kwargs = dict(
        title="testAutomation{}",
        all=[
                {"field": "status", "operator": "is", "value": "pending"},
                {"field": "PENDING", "operator": "greater_than", "value": "24"}
        ],
        actions=[{"field": "status", "value": "open"}]
    )

    def create_objects(self):
        """ We can't use create_multiple_zenpy_objects for automations - they must have different conditions """
        for i in range(100, 105):
            zenpy_object = Automation(
                title="testAutomation{}".format(i),
                all=[
                        {"field": "PENDING", "operator": "is", "value": "{}".format(i)}
                ],
                actions=[{"field": "status", "value": "open"}]
            )
            self.created_objects.append(self.create_method(zenpy_object))

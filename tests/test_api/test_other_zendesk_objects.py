from test_api.fixtures import ZenpyApiTestCase

from test_api.fixtures.__init__ import (
    SingleCreateApiTestCase,
    SingleUpdateApiTestCase,
    SingleDeleteApiTestCase,
    CRUDApiTestCase,
    PaginationTestCase,
)

from zenpy.lib.api_objects import (
    Automation,
    Activity,
    Macro,
    Ticket,
    TicketAudit,
    GroupMembership,
    Group,
    Organization
)

from zenpy.lib.exception import (
    RecordNotFoundException,
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


class TestMacrosCreateUpdateDelete(SingleUpdateApiTestCase, SingleCreateApiTestCase, PaginationTestCase):
    __test__ = True
    ZenpyType = Macro
    object_kwargs = dict(
        title="TestMacro", actions=[{"field": "status", "value": "solved"}]
    )
    api_name = "macros"

    def create_objects(self):
        for i in range(100, 105):
            zenpy_object = Macro(**self.object_kwargs)
            self.created_objects.append(self.create_method(zenpy_object))


class TestDeletedTickets(PaginationTestCase):
    __test__ = True
    ZenpyType = Ticket
    api_name = "tickets"
    expected_single_result_type = TicketAudit
    object_kwargs = dict(subject="test", description="test")
    pagination_limit = 10

    def create_objects(self):
        # Firstly, let's create some tickets
        job_status = self.create_multiple_zenpy_objects(5)
        for r in job_status.results:
            self.created_objects.append(Ticket(id=r.id))

        # And then delete
        self.delete_method(self.created_objects)
        self.created_objects = []

    def test_delete_and_restore(self):
        """ Test restoring tickets """
        cassette_name = "{}".format(self.generate_cassette_name())
        with self.recorder.use_cassette(
            cassette_name=cassette_name, serialize_with="prettyjson"
        ):
            # Let's create a ticket
            ticket_audit = self.create_single_zenpy_object()
            ticket = self.unpack_object(ticket_audit)

            # Then delete it
            self.delete_method(ticket)

            # Then restore
            self.get_api_method("restore")(ticket)

            # And check if it is ok
            ticket_restored = self.api(id=ticket.id)
            self.assertIsInstance(ticket_restored, self.ZenpyType)
            self.assertInCache(ticket_restored)
            self.recursively_call_properties(ticket_restored)

    def test_permanently_delete(self):
        """ Test deteling tickets permanently """
        cassette_name = "{}".format(self.generate_cassette_name())
        with self.recorder.use_cassette(
            cassette_name=cassette_name, serialize_with="prettyjson"
        ):
            # Let's create a ticket
            ticket_audit = self.create_single_zenpy_object()
            ticket = self.unpack_object(ticket_audit)

            # Then delete it
            self.delete_method(ticket)
            self.created_objects = []
            job_status = self.get_api_method("permanently_delete")(ticket)
            self.wait_for_job_status(job_status)

            # Then try to restore
            with self.assertRaises(RecordNotFoundException):
                self.get_api_method("restore")(ticket)


class TestGroupMemberships(PaginationTestCase):
    __test__ = True
    ZenpyType = GroupMembership
    api_name = "group_memberships"
    object_kwargs = {}
    pagination_limit = 10


class TestGroupCreateUpdateDelete(
    SingleCreateApiTestCase, SingleUpdateApiTestCase, SingleDeleteApiTestCase, PaginationTestCase
):
    __test__ = True
    ZenpyType = Group
    object_kwargs = dict(name="testGroup{}")
    api_name = "groups"
    pagination_limit = 10

    def create_objects(self):
        for i in range(5):
            zenpy_object = self.instantiate_zenpy_object(format_val=i)
            self.created_objects.append(self.create_method(zenpy_object))

    def destroy_objects(self):
        for zenpy_object in self.created_objects:
            self.delete_method(zenpy_object)
        self.created_objects = []


class TestOrganizationCreateUpdateDelete(CRUDApiTestCase, PaginationTestCase):
    __test__ = True
    ZenpyType = Organization
    object_kwargs = dict(name="testOrganization{}")
    api_name = "organizations"
    pagination_limit = 10

    def create_objects(self):
        job_status = self.create_multiple_zenpy_objects(5)
        for r in job_status.results:
            self.created_objects.append(Organization(id=r.id))

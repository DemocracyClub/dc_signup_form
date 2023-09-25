from dataclasses import dataclass
import json


class TestBackend:
    def submit(self, data, mailing_lists):
        print(
            {
                "data": data,
                "mailing_lists": mailing_lists,
            }
        )


@dataclass
class EmailSubscriber:
    name: str
    email: str
    list_uuids: list
    source: str = None
    extra_context: dict = None
    status: str = "enabled"

    def __post_init__(self):
        # Validate email
        if "@" not in self.email:
            raise ValueError("Invalid email address.")
        if "@" in self.name:
            raise ValueError("Name cannot contain an email address")
        if not isinstance(self.list_uuids, list):
            raise ValueError("'list_uuids' must be a list")
        self.list_uuids = list([int(x) for x in self.list_uuids])

    def as_listmonk_json(self):
        if self.source:
            if not self.extra_context:
                self.extra_context = {}
            self.extra_context["source_url"] = self.source
        return {
            "email": self.email,
            "name": self.name,
            "status": self.status,
            "lists": self.list_uuids,
            "attribs": self.extra_context,
        }


class EventBridgeBackend:
    def __init__(self, source=None, bus_arn=None):
        if not source:
            raise ValueError("'source' required. This should be the project name")

        self.source = source

        if not bus_arn:
            raise ValueError("'bus_arn' for this environment required")
        self.bus_arn = bus_arn

        self.dev_mode = False
        if bus_arn.endswith("development"):
            self.dev_mode = True

        # Import locally because it's an optional extra only used in this class
        import boto3

        self.client = boto3.client("events", region_name="eu-west-2")

    def list_name_to_list_id(self, dev_mode):
        """
        ListMonk uses numeric list IDs to add subscribers.

        These IDs are just the PK of the list in the database, so depend on the install.

        There is no way to give them a slug or other unique ID that can be relied on.

        Because of this, we hard code these IDs here. It's not ideal, but at least
        keeps the logic ina single place.

        Because these IDs (might) change between ListMonk installs, we need two dicts,
        one for dev and one for prod.
        """

        if dev_mode:
            return {"main_list": "3"}

        # Prod values
        return {"main_list": "4"}

    def submit(self, data, mailing_lists):
        list_id_map = self.list_name_to_list_id(self.dev_mode)
        list_ids = list([list_id_map[list_name] for list_name in mailing_lists])
        subscriber = EmailSubscriber(
            email=data["email"], name=data["full_name"], list_uuids=list_ids, source=data.get("source_url")
        )

        self.client.put_events(
            Entries=[
                {
                    "Source": self.source,
                    "DetailType": "new_subscription",
                    "Detail": json.dumps(subscriber.as_listmonk_json()),
                    "EventBusName": self.bus_arn,
                },
            ],
        )

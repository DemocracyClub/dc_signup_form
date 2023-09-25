import contextlib
import json

import boto3
from moto import mock_events, mock_sqs


@contextlib.contextmanager
def mocked_eventbridge():
    with mock_events(), mock_sqs():
        bus_arn_name = "arn:testing"
        client_kwargs = {
            "region_name": "eu-west-2",
            "aws_access_key_id": "testing",
            "aws_secret_access_key": "testing",
            "aws_session_token": "testing",
        }
        client = boto3.client("events", **client_kwargs)
        client.create_event_bus(Name=bus_arn_name)

        sqs_client = boto3.client("sqs", **client_kwargs)
        statement = [
            {
                "Effect": "Allow",
                "Principal": {"Service": "events.amazonaws.com"},
                "Action": "sqs:SendMessage",
                "Resource": "*",
            }
        ]
        policy = json.dumps({"Version": "2012-10-17", "Statement": [statement]})
        QueueName = "TestQueue"
        RuleName = "TestRule"
        RuleTargetId = "TestTarget"
        queue = sqs_client.create_queue(
            QueueName=QueueName, Attributes={"Policy": policy}
        )
        queueurl = queue["QueueUrl"]
        queueattrs = sqs_client.get_queue_attributes(
            QueueUrl=queueurl, AttributeNames=["QueueArn"]
        )
        queuearn = queueattrs["Attributes"]["QueueArn"]
        # eventpattern = {"source": [EventSource], "detail": {"hello": ["world"]}}
        client.put_rule(
            Name=RuleName,
            State="ENABLED",
            EventPattern='{"source": ["UnitTest"]}',
            EventBusName=bus_arn_name,
        )
        client.put_targets(
            Rule=RuleName,
            Targets=[{"Id": RuleTargetId, "Arn": queuearn}],
            EventBusName=bus_arn_name,
        )

        def get_messages():
            resp = sqs_client.receive_message(QueueUrl=queueurl)
            if "Messages" in resp:
                return resp["Messages"]
            return []

        yield get_messages

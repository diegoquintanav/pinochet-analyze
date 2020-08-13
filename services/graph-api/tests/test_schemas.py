import pytest
from graphene.test import Client

from project.api.schemas import schema

# These are cheap tests to probe some functionalities.
# this is testing against the live graph, be careful. 
# Normally you'd want to create a test graph, and seed it using fixtures.


@pytest.fixture()
def client():
    yield Client(schema)


def test_datetimes_are_parsed(client):

    q1 = """{
  violent_event(event_id: "07a0ab60-0cc5-478e-908c-18dd0a0fa221") {
    event_id
    start_date_daily
  }
}
"""
    executed = client.execute(q1)

    assert executed == {
        "data": {
            "violent_event": {
                "event_id": "07a0ab60-0cc5-478e-908c-18dd0a0fa221",
                "start_date_daily": "1973-09-12",
            }
        }
    }


def test_location_by_description(client):

    q2 = """{
  locations_from_description (desc: ".*[Ll]igua.*") {
    location_id
  }
}
"""
    executed = client.execute(q2)

    assert executed == {
        "data": {
            "locations_from_description": [
                {"location_id": "33ee2cf0c2206455ec1587603640c8be"},
                {"location_id": "86db8a4b16145fff63c313eb36c3ae66"},
                {"location_id": "1fedbe9fe3cd9884ae6457ec660d4311"},
            ]
        }
    }

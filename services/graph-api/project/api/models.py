import os
import typing as T
from datetime import datetime

import maya
from flask import current_app
from graphql import GraphQLError
from py2neo import Graph
from py2neo.ogm import (
    GraphObject,
    Label,
    Property,
    RelatedFrom,
    RelatedObjects,
    RelatedTo,
)

from .utils import to_md5

graph = Graph(
    host=os.environ.get("NEO4J_HOST"),
    port=os.environ.get("NEO4J_PORT"),
    user=os.environ.get("NEO4J_USER"),
    password=os.environ.get("NEO4J_PASSWORD"),
)

DATE_FORMAT = "%Y-%m-%d"


class BaseModel(GraphObject):
    """
    Implements some basic functions to guarantee some standard functionality
    across all models. The main purpose here is also to compensate for some
    missing basic features that we expected from GraphObjects, and improve the
    way we interact with them.
    """

    __dtypes_schema__ = None

    _id_hash_mapping = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @classmethod
    def all(cls):
        return cls.match(graph)

    def as_dict(self):
        return dict(self.__node__)

    def save(self):
        graph.push(self)

    def fetch(self):
        pk = getattr(self, "__primarykey__")
        return self.match(graph, getattr(self, pk)).first()

    def extract_id(self, attrs: T.List):
        return to_md5([getattr(self, attr) for attr in attrs])

    def fetch_by_attr(self, attr, value, exact=True):
        # https://py2neo.org/v4/ogm.html#object-matching
        operator = "=" if exact else "=~"
        q = f"_.{attr} {operator} '{value}'"  #  e.g. _.name =~ ".*K.*" noqa
        return list(self.match(graph).where(q))


class Victim(BaseModel):
    """Base class for a victim"""

    __primarykey__ = "individual_id"

    # from data
    individual_id = Property()
    group_id = Property()
    first_name = Property()
    last_name = Property()
    age = Property()
    minor = Property()
    male = Property()
    number_previous_arrests = Property()
    occupation = Property()
    occupation_detail = Property()
    victim_affiliation = Property()
    victim_affiliation_detail = Property()
    targeted = Property()

    victim_of = RelatedTo("ViolentEvent", "VICTIM_OF")


class Perpetrator(BaseModel):

    __primarykey__ = "perpetrator_id"

    perpetrator_id = Property()
    perpetrator_affiliation = Property()
    perpetrator_affiliation_detail = Property()
    war_tribunal = Property()

    perpetrator_of = RelatedTo("ViolentEvent", "PERPETRATOR_OF")

    _id_hash_mapping = [
        "perpetrator_affiliation",
        "perpetrator_affiliation_detail",
        "war_tribunal",
    ]

    def get_instance_id(self):
        return self.extract_id(self._id_hash_mapping)


class Location(BaseModel):

    __primarykey__ = "location_id"

    location_id = Property()
    exact_coordinates = Property()
    location = Property()
    place = Property()
    location_order = Property()
    latitude = Property()
    longitude = Property()

    next_location = RelatedTo("Location", "NEXT_LOCATION")

    previous_locations = RelatedFrom("Location", "NEXT_LOCATION")
    first_violent_events = RelatedFrom("ViolentEvent", "FIRST_LOCATION")
    in_violent_events = RelatedFrom("ViolentEvent", "IN_LOCATION")
    last_violent_events = RelatedFrom("ViolentEvent", "LAST_LOCATION")

    _id_hash_mapping = [
        "exact_location",
        "location",
        "place",
        "latitude",
        "longitude",
        "location_order",
    ]

    def get_instance_id(self):
        return self.extract_id(self._id_hash_mapping)


class ViolentEvent(BaseModel):

    __primarykey__ = "event_id"

    event_id = Property()
    violence = Property()
    method = Property()
    interrogation = Property()
    torture = Property()
    mistreatment = Property()
    press = Property()
    start_date_daily = Property()
    end_date_daily = Property()
    start_date_monthly = Property()
    end_date_monthly = Property()
    page = Property()
    additional_comments = Property()

    # outgoing relationships
    first_location = RelatedTo("Location", "FIRST_LOCATION")
    in_location = RelatedTo("Location", "IN_LOCATION")
    last_location = RelatedTo("Location", "LAST_LOCATION")

    # incoming relationships
    victims = RelatedFrom("Victim", "VICTIM_OF")
    perpetrators = RelatedFrom("perpetrator", "PERPETRATOR_OF")

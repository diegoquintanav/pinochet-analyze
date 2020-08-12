import os
import typing as T

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


class CustomProperty(Property):
    """Implements a datatype"""

    def __init__(self, **kwargs):
        dtype = kwargs.pop("dtype")
        if dtype is not None:
            self.dtype = dtype
        super().__init__(**kwargs)

    def __set__(self, instance, value):
        if hasattr(self, "dtype"):
            try:
                instance.__node__[self.key] = self.dtype(value)
            except ValueError:
                current_app.logger.error(
                    f"Could not convert {value}", exc_info=True
                )


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
        # value = value if exact else f".*{value}.*"
        q = f"_.{attr} {operator} '{value}'"  #  e.g. _.name =~ ".*K.*" noqa
        return list(self.match(graph).where(q))


class Victim(BaseModel):
    """Base class for a victim"""

    __primarykey__ = "individual_id"

    # from data
    individual_id = CustomProperty(dtype=int)
    group_id = CustomProperty(dtype=int)
    first_name = CustomProperty(dtype=str)
    last_name = CustomProperty(dtype=str)
    age = CustomProperty(dtype=str)
    minor = CustomProperty(dtype=bool)
    male = CustomProperty(dtype=bool)
    number_previous_arrests = CustomProperty(dtype=str)
    occupation = CustomProperty(dtype=str)
    occupation_detail = CustomProperty(dtype=str)
    victim_affiliation = CustomProperty(dtype=str)
    victim_affiliation_detail = CustomProperty(dtype=str)
    targeted = CustomProperty(dtype=str)

    victim_of = RelatedTo("ViolentEvent", "VICTIM_OF")

class Perpetrator(BaseModel):

    __primarykey__ = "perpetrator_id"

    perpetrator_id = CustomProperty(dtype=str)
    perpetrator_affiliation = CustomProperty(dtype=str)
    perpetrator_affiliation_detail = CustomProperty(dtype=str)
    war_tribunal = CustomProperty(dtype=bool)

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

    location_id = CustomProperty(dtype=str)
    exact_coordinates = CustomProperty(dtype=bool)
    location = CustomProperty(dtype=str)
    place = CustomProperty(dtype=str)
    location_order = CustomProperty(dtype=str)
    latitude = CustomProperty(dtype=str)
    longitude = CustomProperty(dtype=str)

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

    event_id = CustomProperty(dtype=str)
    violence = CustomProperty(dtype=str)
    method = CustomProperty(dtype=str)
    interrogation = CustomProperty(dtype=bool)
    torture = CustomProperty(dtype=bool)
    mistreatment = CustomProperty(dtype=bool)
    press = CustomProperty(dtype=bool)
    start_date_daily = CustomProperty(dtype=str)
    end_date_daily = CustomProperty(dtype=str)
    start_date_monthly = CustomProperty(dtype=str)
    end_date_monthly = CustomProperty(dtype=str)
    page = CustomProperty(dtype=str)
    additional_comments = CustomProperty(dtype=str)

    # outgoing relationships
    first_location = RelatedTo("Location", "FIRST_LOCATION")
    in_location = RelatedTo("Location", "IN_LOCATION")
    last_location = RelatedTo("Location", "LAST_LOCATION")

    # incoming relationships
    victims = RelatedFrom("Victim", "VICTIM_OF")
    perpetrators = RelatedFrom("perpetrator", "PERPETRATOR_OF")

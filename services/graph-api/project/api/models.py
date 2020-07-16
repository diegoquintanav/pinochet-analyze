import os
import maya
from graphql import GraphQLError
from py2neo import Graph
from py2neo.ogm import GraphObject, Property, Label, RelatedTo
from flask import current_app
from .utils import Neo4jDatePair


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
                    f"Could not convert {value} to {dtype}", exc_info=True)


class BaseModel(GraphObject):
    """
    Implements some basic functions to guarantee some standard functionality
    across all models. The main purpose here is also to compensate for some
    missing basic features that we expected from GraphObjects, and improve the
    way we interact with them.
    """

    __dtypes_schema__ = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @property
    def all(self):
        return self.match(graph)

    def as_dict(self):
        return self._GraphObject__ogm.__dict__.get('node')

    def save(self):
        graph.push(self)


class Victim(BaseModel):
    """Base class for a victim"""
    __primarykey__ = 'individual_id'

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

    def fetch(self):
        return self.match(graph, self.individual_id).first()


class Perpetrator(BaseModel):
    perpetrator_affiliation = CustomProperty(dtype=str)
    perpetrator_affiliation_detail = CustomProperty(dtype=str)
    war_tribunal = CustomProperty(dtype=bool)


class Location(BaseModel):
    exact_coordinates = CustomProperty(dtype=bool)
    location = CustomProperty(dtype=str)
    place = CustomProperty(dtype=str)


class ViolentEvent(BaseModel):
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

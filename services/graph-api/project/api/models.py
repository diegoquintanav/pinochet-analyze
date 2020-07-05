import os
import maya
from graphql import GraphQLError
from py2neo import Graph
from py2neo.ogm import GraphObject, Property, Label, RelatedTo

from flask import current_app

graph = Graph(
    host=os.environ.get("NEO4J_HOST"),
    port=os.environ.get("NEO4J_PORT"),
    user=os.environ.get("NEO4J_USER"),
    password=os.environ.get("NEO4J_PASSWORD"),
)


class BaseModel(GraphObject):
    """
    Implements some basic functions to guarantee some standard functionality
    across all models. The main purpose here is also to compensate for some
    missing basic features that we expected from GraphObjects, and improve the
    way we interact with them.
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @property
    def all(self):
        return self.match(graph)

    def save(self):
        graph.push(self)


class Victim(BaseModel):
    """Base class for a person"""
    __primarykey__ = 'individual_id'

    # from data
    individual_id = Property()
    group_id = Property()
    first_name = Property()  # todo: use Label for matching, see https://py2neo.org/v4/ogm.html#labels
    last_name = Property()  # todo: use Label for matching, see https://py2neo.org/v4/ogm.html#labels
    age = Property()
    minor = Property()
    male = Property()
    number_previous_arrests = Property()
    occupation = Property()
    occupation_detail = Property()
    victim_affiliation = Property()
    victim_affiliation_detail = Property()
    targeted = Property()

    def as_dict(self):
        return {
            'individual_id': self.individual_id,
            'group_id': self.group_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'minor': self.minor,
            'male': self.male,
            'number_previous_arrests': self.number_previous_arrests,
            'occupation': self.occupation,
            'occupation_detail': self.occupation_detail,
            'victim_affiliation': self.victim_affiliation,
            'victim_affiliation_detail': self.victim_affiliation_detail,
            'targeted': self.targeted,
        }

    def fetch(self):
        return self.match(graph, self.individual_id).first()

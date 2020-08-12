from graphene import (
    Boolean,
    Date,
    Field,
    Int,
    List,
    ObjectType,
    String,
    Schema,
)

from project.api.models import Victim, Perpetrator, Location, ViolentEvent


class VictimSchema(ObjectType):
    individual_id = Int()
    group_id = Int()
    first_name = String()
    last_name = String()
    age = String()  # support for "NA" # TODO: Model NA as nulls?
    minor = Boolean()
    male = Boolean()
    number_previous_arrests = String()
    occupation = String()
    occupation_detail = String()
    victim_affiliation = String()
    victim_affiliation_detail = String()
    targeted = String()
    full_name = String()

    def resolve_full_name(self, info):
        return f"{self.first_name} {self.last_name}"


class PerpetratorSchema(ObjectType):
    perpetrator_id = String()
    perpetrator_affiliation = String()
    perpetrator_affiliation_detail = String()
    war_tribunal = Boolean()


class LocationSchema(ObjectType):

    location_id = String()
    exact_coordinates = Boolean()
    location = String()
    place = String()
    location_order = String()
    latitude = String()
    longitude = String()


class ViolentEventSchema(ObjectType):

    event_id = String()
    violence = String()
    method = String()
    interrogation = Boolean()
    torture = Boolean()
    mistreatment = Boolean()
    press = Boolean()
    start_date_daily = Date()
    end_date_daily = Date()
    start_date_monthly = Date()
    end_date_monthly = Date()
    page = String()
    additional_comments = String()

    victims = List(VictimSchema)
    perpetrators = List(PerpetratorSchema)
    locations = List(LocationSchema)

    # TODO: firstlocation, lastlocation,

    def resolve_victims(self, info):
        return None

    def resolve_perpetrators(self, info):
        return None

    def resolve_locations(self, info):
        return None


class Query(ObjectType):

    victim = Field(lambda: VictimSchema, individual_id=Int())
    all_victims = List(lambda: VictimSchema)

    perpetrator = Field(lambda: PerpetratorSchema, perpetrator_id=String())
    all_perpetrators = List(lambda: PerpetratorSchema)

    violent_event = Field(lambda: ViolentEventSchema, event_id=String())
    all_violent_events = List(lambda: ViolentEventSchema)

    location = Field(lambda: LocationSchema, location_id=String(),)
    all_locations = List(lambda: LocationSchema)
    locations_from_description = List(lambda: LocationSchema, desc=String())

    def resolve_victim(self, info, individual_id):
        victim = Victim(individual_id=individual_id).fetch()
        return VictimSchema(**victim.as_dict())

    def resolve_all_victims(self, info):
        return (VictimSchema(**victim.as_dict()) for victim in Victim.all())

    def resolve_location(self, info, location_id):
        location = Location(location_id=location_id).fetch()
        return LocationSchema(**location.as_dict())

    def resolve_all_locations(self, info):
        return (LocationSchema(**loc.as_dict()) for loc in Location.all())

    def resolve_locations_from_description(self, info, desc):
        locations = Location(location=desc).fetch_by_attr(
            "location", desc, exact=False
        )

        return (LocationSchema(**loc.as_dict()) for loc in locations)

    def resolve_perpetrator(self, info, perpetrator_id):
        perp = Perpetrator(perpetrator_id=perpetrator_id).fetch()
        return PerpetratorSchema(**perp.as_dict())

    def resolve_all_perpetrators(self, info):
        return (
            PerpetratorSchema(**perp.as_dict()) for perp in Perpetrator.all()
        )

    def resolve_violent_event(self, info, event_id):
        event = ViolentEvent(event_id=event_id).fetch()
        return ViolentEventSchema(**event.as_dict())

    def resolve_all_violent_events(self, info):
        return (
            ViolentEventSchema(**event.as_dict())
            for event in ViolentEvent.all()
        )


schema = Schema(query=Query, auto_camelcase=False)


if __name__ == "__main__":
    from graphene.test import Client

    client = Client(schema)
    executed = client.execute(
        """{
  locations(location_description: ".*[l]igua.*") {
    location_id
  }
}
"""
    )

    "33ee2cf0c2206455ec1587603640c8be"
    "86db8a4b16145fff63c313eb36c3ae66"
    "1fedbe9fe3cd9884ae6457ec660d4311"  # ligua
    assert executed == {
        "data": {
            "locations": [{"location_id": "1fedbe9fe3cd9884ae6457ec660d4311"}]
        }
    }


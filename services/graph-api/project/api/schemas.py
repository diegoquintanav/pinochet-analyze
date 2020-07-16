import graphene

from .models import Victim


class VictimSchema(graphene.ObjectType):
    individual_id = graphene.Int()
    group_id = graphene.Int()
    first_name = graphene.String()
    last_name = graphene.String()
    age = graphene.String()  # support for "NA" # TODO: Model NA as nulls?
    minor = graphene.Boolean()
    male = graphene.Boolean()
    number_previous_arrests = graphene.String()
    occupation = graphene.String()
    occupation_detail = graphene.String()
    victim_affiliation = graphene.String()
    victim_affiliation_detail = graphene.String()
    targeted = graphene.String()


class PerpetratorSchema(graphene.ObjectType):
    perpetrator_affiliation = graphene.String()
    perpetrator_affiliation_detail = graphene.String()
    war_tribunal = graphene.Boolean()

class LocationSchema(graphene.ObjectType):
    exact_coordinates = graphene.Boolean()
    location = graphene.String()
    place = graphene.String()


class ViolenceEventSchema(graphene.ObjectType):
    violence = graphene.String()
    method = graphene.String()
    interrogation = graphene.Boolean()
    torture = graphene.Boolean()
    mistreatment = graphene.Boolean()
    press = graphene.Boolean()
    start_date_daily = graphene.Date()
    end_date_daily = graphene.Date()
    start_date_monthly = graphene.Date()
    end_date_monthly = graphene.Date()
    page = graphene.String()
    additional_comments = graphene.String()


class Query(graphene.ObjectType):

    # this defines a Field `hello` in our Schema with a single Argument `name`

    victims = graphene.List(lambda: VictimSchema)
    victim = graphene.Field(lambda: VictimSchema,
                            individual_id=graphene.Int())

    # perpetrator = graphene.Field(lambda: PerpetratorSchema)
    # violence_event = graphene.Field(lambda: ViolenceEventSchema)

    def resolve_victims(root, info):
        return [VictimSchema(**victim.as_dict()) for victim in Victim().all]

    def resolve_victim(root, info, individual_id):
        victim = Victim(individual_id=individual_id).fetch()
        return VictimSchema(**victim.as_dict())

    # def resolve_perpetrator(root, info):
    #     victim = Victim(individual_id=individual_id).fetch()
    #     return VictimSchema(**victim.as_dict())

    # def resolve_victim(root, info):
    #     victim = Victim(individual_id=individual_id).fetch()
    #     return VictimSchema(**victim.as_dict())


schema = graphene.Schema(query=Query, auto_camelcase=False)

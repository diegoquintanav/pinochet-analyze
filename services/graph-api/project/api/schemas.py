import graphene

from .models import Victim


class VictimSchema(graphene.ObjectType):
    individual_id = graphene.Int()
    group_id = graphene.Int()
    first_name = graphene.String()
    last_name = graphene.String()
    age = graphene.String()  # support for "NA"
    minor = graphene.Boolean()
    male = graphene.Boolean()
    number_previous_arrests = graphene.String()
    occupation = graphene.String()
    occupation_detail = graphene.String()
    victim_affiliation = graphene.String()
    victim_affiliation_detail = graphene.String()
    targeted = graphene.String()


class Query(graphene.ObjectType):

    # this defines a Field `hello` in our Schema with a single Argument `name`

    victims = graphene.List(lambda: VictimSchema)
    victim = graphene.Field(lambda: VictimSchema,
                            individual_id=graphene.Int())

    def resolve_victims(root, info):
        return [VictimSchema(**victim.as_dict()) for victim in Victim().all]

    def resolve_victim(root, info, individual_id):
        victim = Victim(individual_id=individual_id).fetch()
        return VictimSchema(**victim.as_dict())


schema = graphene.Schema(query=Query, auto_camelcase=False)

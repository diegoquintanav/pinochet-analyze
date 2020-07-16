import csv
from flask import current_app
from pathlib import Path
from ..api.models import graph, Location, Victim, Perpetrator, ViolentEvent


def clear_graph():
    return graph.run("MATCH (n) DETACH DELETE n").stats()


def __create_node(graph_object):
    current_app.logger.debug(f"Creating {graph_object}")
    graph.create(graph_object)


def seed_graph(filepath):

    with open(filepath) as fp:
        csv_reader = csv.DictReader(f=fp)
        for row in csv_reader:
            # create victims
            victim = Victim(
                individual_id=row["individual_id"],
                group_id=row["group_id"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                age=row["age"],
                minor=row["minor"],
                male=row["male"],
                nationality=row["nationality"],
                number_previous_arrests=row["number_previous_arrests"],
                occupation=row["occupation"],
                occupation_detail=row["occupation_detail"],
                victim_affiliation=row["victim_affiliation"],
                victim_affiliation_detail=row["victim_affiliation_detail"],
                targeted=row["targeted"]
            )

            perp = Perpetrator(
                perpetrator_affiliation=row["perpetrator_affiliation"],
                perpetrator_affiliation_detail=row["perpetrator_affiliation_detail"],
                war_tribunal=row["war_tribunal"],
            )

            locations = []

            # there are 6 locations max in the dataset. We will fetch those that are not empty
            for n in range(1, 7):
                loc = Location(
                    exact_location=row[f"exact_coordinates_{n}"],
                    location=row.get(f"location_{n}", None) or row.get(
                        f"start_location_{n}", None) or row.get(f"end_location_{n}", None),
                    place=row[f"place_{n}"],
                )
                locations.append((n, loc))

            event = ViolentEvent(
                violence=row["violence"],
                method=row["method"],
                interrogation=row["interrogation"],
                torture=row["torture"],
                mistreatment=row["mistreatment"],
                press=row["press"],
                start_date_daily=row["start_date_daily"],
                end_date_daily=row["end_date_daily"],
                start_date_monthly=row["start_date_monthly"],
                end_date_monthly=row["end_date_monthly"],
                page=row["page"],
                additional_comments=row["additional_comments"],
            )

            # create nodes
            __create_node(victim)
            __create_node(perp)
            for n, location in locations:
                __create_node(location)
            __create_node(event)

            status = "success"
    return status

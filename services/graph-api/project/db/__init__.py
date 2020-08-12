import csv
import hashlib
import time
import typing as T
import uuid
from pathlib import Path

from flask import current_app
from progress.bar import IncrementalBar

from project.api.models import (
    Location,
    Perpetrator,
    Victim,
    ViolentEvent,
    graph,
)


def to_md5(elements: T.List, *args, **kwargs):
    pre = "".join(str(arg).lower() for arg in elements)
    return hashlib.md5(pre.encode("utf-8")).hexdigest()


def clear_graph(dry_run=False):
    if dry_run:
        return {}
    return graph.run("MATCH (n) DETACH DELETE n").stats()


def __create_node(graph_object, dry_run=False):
    current_app.logger.debug(f"Creating {graph_object}")
    if dry_run:
        current_app.logger.debug("Using --dry-run. Nothing was created.")
    else:
        current_app.logger.debug("Done")
        graph.create(graph_object)


def get_locations(row: dict) -> T.List[Location]:
    locations = []

    # there are 6 locations max in the dataset. We will fetch those that are not empty
    for n in range(1, 7):
        location_name = (
            row.get(f"location_{n}", None)
            or row.get(f"start_location_{n}", None)
            or row.get(f"end_location_{n}", None)
        )

        if location_name is not None and location_name != "NA":

            loc_mapping = {
                "exact_location": row[f"exact_coordinates_{n}"],
                "location": location_name,
                "place": row[f"place_{n}"],
                "latitude": row[f"latitude_{n}"],
                "longitude": row[f"longitude_{n}"],
                "location_order": n,
            }

            loc = Location(
                location_id=to_md5(loc_mapping.values()), **loc_mapping
            )

            locations.append(loc)
    return locations


def seed_graph(filepath, **kwargs):

    dry_run = kwargs.pop("dry_run", False)

    # we know this number counting the rows before
    # with wc -l pinochet.csv
    bar = IncrementalBar("Insertions", max=2398)

    with open(filepath) as fp:
        csv_reader = csv.DictReader(f=fp)
        for row in csv_reader:
            # create victims
            victim = Victim(
                individual_id=row["individual_id"],  # pk
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
                targeted=row["targeted"],
            )

            perp_mapping = {
                "perpetrator_affiliation": row["perpetrator_affiliation"],
                "perpetrator_affiliation_detail": row[
                    "perpetrator_affiliation_detail"
                ],
                "war_tribunal": row["war_tribunal"],
            }

            perp = Perpetrator(
                perpetrator_id=to_md5(perp_mapping.values()), **perp_mapping
            )

            locations = get_locations(row)

            # to track what is the last location in the row ended up being
            max_n = len(locations)

            event = ViolentEvent(
                event_id=uuid.uuid4(),  # pk
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

            # create relationships
            if locations:
                event.first_location.add(locations[0])
                event.last_location.add(locations[-1])
                for index, location in enumerate(locations):
                    if index != 0:
                        locations[index - 1].next_location.add(location)
                    location.in_violent_events.add(event)

            victim.victim_of.add(event)
            perp.perpetrator_of.add(event)

            # create nodes
            __create_node(victim, dry_run)
            __create_node(perp, dry_run)
            __create_node(event, dry_run)

            for location in locations:
                __create_node(location, dry_run)

            # increment progress bar
            bar.next()

    status = "Success"
    bar.finish()
    return status

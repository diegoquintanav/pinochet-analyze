import os
from pathlib import Path
import click
from flask import current_app
from flask.cli import FlaskGroup

from project import create_app
from project.db import clear_graph, seed_graph

# create_app is not handled correctly
# see https://github.com/pallets/flask/issues/3701
cli = FlaskGroup(create_app=create_app, set_debug_flag=False)

@cli.command("delete_db")
@click.option("--dry-run", is_flag=True)
def delete_db(dry_run):
    current_app.logger.info("Deleting graph (--dry-run)" if dry_run else "Deleting graph")
    status = clear_graph(dry_run=dry_run)
    for k, v in status.items():
        current_app.logger.info(k + ": " + str(v))
    current_app.logger.info("Done")


@cli.command("seed_db")
@click.option("--dry-run", is_flag=True)
def seed_db(dry_run):
    PINOCHET_CSV = os.environ.get(
        "PINOCHET_CSV", Path(__file__).parent.joinpath("project", "db", "pinochet.csv"))
    current_app.logger.info("Seeding tables (--dry-run)" if dry_run else "Seeding tables")
    status = seed_graph(filepath=PINOCHET_CSV, dry_run=dry_run)
    current_app.logger.info(status)
    current_app.logger.info("Done")


@cli.command("recreate_db")
@click.option("--dry-run", is_flag=True)
@click.pass_context
def recreate_db(ctx, dry_run):
    current_app.logger.info("Deleting graph")
    ctx.invoke(delete_db, dry_run=dry_run)
    current_app.logger.info("Recreating graph")
    ctx.invoke(seed_db, dry_run=dry_run)
    current_app.logger.info("Done")


@cli.command("app_config")
def app_config():
    print("current_app.debug from cli.command")
    print(current_app.debug)
    print("current_app.config from cli.command")
    print(current_app.config)


if __name__ == "__main__":
    cli()

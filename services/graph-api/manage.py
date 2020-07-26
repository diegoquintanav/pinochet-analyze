import os
from pathlib import Path
import click
from flask import app
from flask.cli import FlaskGroup

from project import create_app
from project.db import clear_graph, seed_graph

# create_app is not handled correctly
# see https://github.com/pallets/flask/issues/3701
app = create_app()

cli = FlaskGroup(create_app=create_app)


@cli.command("delete_db")
@click.option("--dry-run", is_flag=True)
def delete_db(dry_run):
    app.logger.info("Deleting graph")
    status = clear_graph(dry_run=dry_run)
    for k, v in status.items():
        app.logger.info(k + ": " + str(v))
    app.logger.info("Done")


@cli.command("seed_db")
@click.option("--dry-run", is_flag=True)
def seed_db(dry_run):
    PINOCHET_CSV = os.environ.get(
        "PINOCHET_CSV", Path(__file__).parent.joinpath("project", "db", "pinochet.csv"))
    app.logger.info("Seeding tables")
    status = seed_graph(filepath=PINOCHET_CSV, dry_run=dry_run)
    app.logger.info(status)
    app.logger.info("Done")


@cli.command("recreate_db")
@click.option("--dry-run", is_flag=True)
@click.pass_context
def recreate_db(ctx, dry_run):
    app.logger.info("Deleting graph")
    ctx.invoke(delete_db, dry_run=dry_run)
    app.logger.info("Recreating graph")
    ctx.invoke(seed_db, dry_run=dry_run)
    app.logger.info("Done")


@cli.command("app_config")
def app_config():
    print("app.debug from cli.command")
    print(app.debug)
    print("app.config from cli.command")
    print(app.config)


if __name__ == "__main__":
    cli()

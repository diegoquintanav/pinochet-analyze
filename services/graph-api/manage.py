import click
from flask.cli import FlaskGroup

from project import create_app
from project.db import clear_graph, seed_graph

app = create_app()

cli = FlaskGroup(create_app=create_app)


@cli.command("delete_db")
def delete_db():
    app.logger.info("Deleting graph")
    status = clear_graph()
    for k, v in status.items():
        app.logger.info(k + ": " + str(v))
    app.logger.info("Done")


@cli.command("seed_db")
def seed_db():
    PINOCHET_CSV = "/usr/src/app/project/db/pinochet.csv"  # TODO: improve this
    app.logger.info("Seeding tables")
    status = seed_graph(filepath=PINOCHET_CSV)
    app.logger.info(status)
    app.logger.info("Done")


@cli.command("recreate_db")
@click.pass_context
def recreate_db(ctx):
    app.logger.info("Deleting graph")
    ctx.invoke(delete_db)
    app.logger.info("Recreating graph")
    ctx.invoke(seed_db)
    app.logger.info("Done")


if __name__ == "__main__":
    cli()

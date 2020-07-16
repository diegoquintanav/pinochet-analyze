from flask.cli import FlaskGroup

from project import create_app

app = create_app()

cli = FlaskGroup(create_app=create_app)


@cli.command("recreate_db")
def recreate_db():
    app.logger.info("Dropping tables")
    # db.drop_all()
    app.logger.info("Recreating tables")
    # db.create_all()
    # db.session.commit()
    app.logger.info("Done")


if __name__ == "__main__":
    cli()

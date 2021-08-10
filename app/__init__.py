import click
from os import getenv
from dotenv import load_dotenv
from flask import Flask, render_template, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask.cli import with_appcontext

from .utils import format_url

db = SQLAlchemy()

load_dotenv()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=getenv('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI=format_url(getenv('DATABASE_URL')),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    # initialise flask with the app
    db.init_app(app)
    # register init-db command with flask
    register_sync_db_command(app)

    with app.app_context():
        #  routes
        from .views import views
        from .auth import auth

        app.register_blueprint(views, url_prefix='/')
        app.register_blueprint(auth, url_prefix='/')

        # login manager

        login_manager = LoginManager()
        login_manager.login_view = "auth.login"
        login_manager.init_app(app)

        from .models import User

        @login_manager.user_loader
        def load_user(id):
            return User.query.get(int(id))

        @app.context_processor
        def inject_user():
            return dict(user=current_user)

        return app


def sync_db():
    with current_app.app_context():
        db.drop_all()
        db.create_all()


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    sync_db()
    click.echo("Initialized the database.")


def register_sync_db_command(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.cli.add_command(init_db_command)

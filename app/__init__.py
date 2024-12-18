"""app/__init__.py"""

import os
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager
from app.config.settings import config
from app.models import db, User
from app.routes import main_bp
from app.auth.routes import auth_bp
from flask_wtf.csrf import CSRFProtect, CSRFError
from datetime import datetime

# Initialize extensions
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
load_dotenv()


def configure_app(app, config_name):
    """Load configuration based on environment."""
    config_name = config_name or os.getenv('FLASK_ENV', 'development')
    if config_name not in config:
        raise KeyError(f"Invalid configuration name '{config_name}'. Valid options are: {list(config.keys())}")
    app.config.from_object(config[config_name])
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key')
    assert app.config['SECRET_KEY'], "SECRET_KEY is missing!"


def register_error_handlers(app):
    """Register global error handlers."""

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("error.html", message="Page not found."), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("error.html", message="An internal server error occurred."), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template("error.html", message="CSRF token is missing or invalid."), 400



def create_app(config_name=None):
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    configure_app(app, config_name)

    if app.config["DEBUG"]:
        print(f"Config in use: {config_name}")
        for rule in app.url_map.iter_rules():
            print(f"Rule: {rule}, Endpoint: {rule.endpoint}")

    # Adjust database configuration for testing environment
    if app.config["ENV"] == "testing":
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL', 'sqlite:///:memory:')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config["WTF_CSRF_ENABLED"] = False

    # Initialize extensions
    csrf.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Flask context processor
    @app.context_processor
    def inject_current_year():
        """Inject the current year into all templates."""
        return {'current_year': datetime.now().year}

    # Register error handlers
    register_error_handlers(app)

    # Login manager settings
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "warning"

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id))

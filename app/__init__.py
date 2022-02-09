from flask import Flask


def create_app(config_filename='config.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_filename, silent=True)

    from app.db import db

    db.init_app(app)

    from app.countries.views import bp as countries
    from app.universities.views import bp as universities

    app.register_blueprint(countries)
    app.register_blueprint(universities)

    from app.core.token import token
    from app.core.password import hash_password

    token.init_app(app)
    hash_password.init_app(app)

    return app

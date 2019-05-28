from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db=SQLAlchemy()

def create_app():
    app=Flask(__name__,instance_relative_config=True)
    app.config.from_pyfile('config.py',silent=True)

    db.init_app(app)

    csrf = CSRFProtect()
    csrf.init_app(app)

    from app.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    return app



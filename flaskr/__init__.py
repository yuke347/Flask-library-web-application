import os
from flask import Flask,g,current_app
import psycopg2
import sqlite3
import click


def create_app(test_config=None):
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path,"flaskr.sqlite")
    )
    print(app.instance_path)
    print(os.path.join(app.instance_path,"flaskr.sqlite"))
    if test_config is None:
        app.config.from_pyfile("config.py",silent=True)    
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db,auth,func,user
    db.init_app(app)
    # from . import auth
    app.register_blueprint(auth.bp)
    app.register_blueprint(func.bp)
    app.register_blueprint(user.bp)
    return app



create_app()


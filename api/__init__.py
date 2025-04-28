from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    app.config.from_mapping(
        SECRET_KEY='tuo_segreto_super_sicuro',
        SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:1234@localhost/m321',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        PERMANENT_SESSION_LIFETIME=timedelta(days=7)
    )
    
    db.init_app(app)
    
    with app.app_context():
        from . import models
        db.create_all()

    
    return app
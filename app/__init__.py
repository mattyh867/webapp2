from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin

app = Flask(__name__)
app.config.from_object('config')
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
admin = Admin(app, template_mode='bootstrap4')

app.app_context().push()

from app import views, models

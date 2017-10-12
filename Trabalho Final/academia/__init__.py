from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbacademia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 
db = SQLAlchemy(app)

from academia import views
from academia import models



admin = Admin(app, name = 'academia', template_mode = 'bootstrap3')

admin.add_view(ModelView(models.Usuario, db.session))
  
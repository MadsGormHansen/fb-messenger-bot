from flask import Flask
from models import Result
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key= "MA1114ha"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://mgh:Analytics4ever1@responsive-sandbox.cloudapp.net/SMP?driver=SQL+Server+Native+Client+11.0'

#engine = app.create_engine("mssql+pyodbc://mgh:Analytics4ever1@responsive-sandbox.cloudapp.net/SMP?driver=SQL+Server+Native+Client+11.0")

db = SQLAlchemy(app)

db.session.add(Result("Good","I","I23"))
db.session.add(Result("Good2","i2","I45"))

db.session.commit()

from flask import Flask
#from models import Result
from app import received_postback
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key= "MA1114ha"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://mgh:Analytics4ever1@responsive-sandbox.cloudapp.net/SMP?driver=SQL+Server+Native+Client+11.0'

#engine = app.create_engine("mssql+pyodbc://mgh:Analytics4ever1@responsive-sandbox.cloudapp.net/SMP?driver=SQL+Server+Native+Client+11.0")

db = SQLAlchemy(app)

print(received_postback.sender_id)


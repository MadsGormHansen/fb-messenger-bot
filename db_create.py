from flask import Flask
from models import db, Result
from app import received_message
import inspect


app = Flask(__name__)

app.secret_key= "MA1114ha"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://mgh:Analytics4ever1@responsive-sandbox.cloudapp.net/SMP?driver=SQL+Server+Native+Client+11.0'

var= vars(received_message)

text_file = open("testsheet.txt", "w")
text_file.write(var)
text_file.close()

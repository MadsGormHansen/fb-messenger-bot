from flask import Flask
from models import db, Result
from app import received_message
import inspect


app = Flask(__name__)

app.secret_key= "MA1114ha"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://mgh:Analytics4ever1@responsive-sandbox.cloudapp.net/SMP?driver=SQL+Server+Native+Client+11.0'



#db.session.add(Result("12321", "fjfjfeie","dfadfefadfe"))
#db.session.commit()

#code = inspect.getmembers(received_message)
#print code
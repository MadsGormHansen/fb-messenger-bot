import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import Result, db, app
#from app import app 
#from fbmq import Page

app.secret_key= "MA1114ha"
app.config.from_object(os.environ["PAGE_ACCESS_TOKEN"])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://mgh:Analytics4ever1@responsive-sandbox.cloudapp.net/SMP?driver=SQL+Server+Native+Client+11.0'

db.session.add(Result("1234","hjehj","dfhafei"))
db.seesion.commit()
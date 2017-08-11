import os
from flask import Flask, request
from app import received_message
from models import Result
from flask_sqlalchemy import SQLAlchemy
from fbmq import Page,Attachment, Template, QuickReply 

app = Flask(__name__)

app.secret_key= "MA1114ha"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://mgh:Analytics4ever1@responsive-sandbox.cloudapp.net/SMP?driver=SQL+Server+Native+Client+11.0'


#engine = app.create_engine("mssql+pyodbc://mgh:Analytics4ever1@responsive-sandbox.cloudapp.net/SMP?driver=SQL+Server+Native+Client+11.0")

dir(received_message)

#def 

#db.session.add(Result(sender_id, "fjfjfeie","dfadfefadfe"))
#db.session.commit()

#db.session.add(Result("123","dfafd","dfafd"))
#db.session.commit()




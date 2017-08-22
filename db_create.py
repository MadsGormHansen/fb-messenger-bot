# -*- coding: utf-8 -*-
'''
import os
import sys
import json
import os
import inspect
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import Result, app, db
from fbmq import Page 
from app import received_message, page


app.secret_key= "MA1114ha"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://mgh:Analytics4ever1@responsive-sandbox.cloudapp.net/SMP?driver=SQL+Server+Native+Client+11.0'

@page.handle_message
def when_received(event):
    code = inspect.getmodule(received_message)
    print code 

    db.session.add(Result("12345","hjehj","dfhafei"))
    db.session.commit()
'''
 # coding: utf-8
import os
from fbmq import Page
from flask_sqlalchemy import SQLAlchemy
from models import Result, db
from app import send

@page.handle_message
def receved_tosend(event):
    Sender_id = event.Sender_id
    message = event.message
    time_of_message = event.timestamp
    send_import= send

    db.session.add(Result('121', "test1", "test1"))
    db.session.commit()
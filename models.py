from flask import Flask
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import create_engine, Column, Integer, String

app = Flask(__name__)

Base = declarative_base()
engine= create_engine('mssql+pyodbc://mgh:Analytics4ever1@responsive-sandbox.cloudapp.net/SMP?driver=SQL+Server+Native+Client+11.0')

class Result(Base):
    __tablename__ = 'Results'

    id = Column(Integer, primary_key=True)
    Session_id = Column(Integer, nullable=True)
    Receive_text = Column(String, nullable=True)
    Send_text = Column(String, nullable=True)

    def __init__(self, Session_id, Receive_text, Send_text):
        self.Session_id = Session_id
        self.Receive_text = Receive_text
        self.Send_text = Send_text

    def __repr__(self):
        return '<Session {}>'.format(self.Session)

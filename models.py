from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key= "MA1114ha"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://mgh:Analytics4ever1@responsive-sandbox.cloudapp.net/SMP?driver=SQL+Server+Native+Client+11.0'

db = SQLAlchemy(app)

class Result(db.Model):
    __tablename__ = 'Results'

    id = db.Column(db.Integer, primary_key=True)
    Session_id = db.Column(db.Integer, nullable=True)
    Receive_text = db.Column(db.String, nullable=True)
    Send_text = db.Column(db.String, nullable=True)

    def __init__(self, Session_id, Receive_text, Send_text):
        self.Session_id = Session_id
        self.Receive_text = Receive_text
        self.Send_text = Send_text

    def __repr__(self):
        return '<Session {}>'.format(self.Session)

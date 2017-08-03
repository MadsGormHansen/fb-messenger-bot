from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Result(db.Model):
    __tablename__ = 'Results'

    id = db.Column(db.Integer, primary_key=True)
    Session_id = db.Column(db.String, nullable=False)
    Receive_text = db.Column(db.String, nullable=False)
    Send_text = db.Column(db.String, nullable=False)

    def __init__(self, Session_id, Receive_text, Send_text):
        self.Session_id = Session_id
        self.Receive_text = Receive_text
        self.Send_text = Send_text

    def __repr__(self):
        return '<Session {}>'.format(self.Session)

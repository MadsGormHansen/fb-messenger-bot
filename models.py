from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Result(db.Model):
    __tablename__ = 'Results'

    id = db.Column(db.Integer, primary_key=True)
    Session = db.Column(db.String, nullable=False)
    Receive_text = db.Column(db.String, nullable=False)
    Send_text = db.Column(db.String, nullable=False)

    def __init__(self, Session, Receive_text, Send_text):
        self.Session = Session
        self.Receive_text = Receive_text
        self.Send_text = Send_text

    def __repr__(self):
        return '<Session {}>'.format(self.Session)

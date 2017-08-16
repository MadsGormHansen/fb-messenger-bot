from flask import Flask
from models import db, Result
#engine = app.create_engine("mssql+pyodbc://mgh:Analytics4ever1@responsive-sandbox.cloudapp.net/SMP?driver=SQL+Server+Native+Client+11.0")

#receved_senderid= received_message.get('sender_id')
#print(receved_senderid)
#db.session.add(Result(receved_senderid,"hej", "hej"))

app = Flask(__name__)

app.secret_key= "MA1114ha"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://mgh:Analytics4ever1@responsive-sandbox.cloudapp.net/SMP?driver=SQL+Server+Native+Client+11.0'

#db.session.add(Result("123534", "hej hej", "hfuhfeaijdfo"))

#db.session.commit()
#def 

db.session.add(Result("12323232321", "fjfjfeie","dfadfefadfe"))
db.session.commit()

#db.session.add(Result("123","dfafd","dfafd"))
#db.session.commit()




import os
import sys
import json
from flask import Flask, request
from fbmq import Page


page = Page(os.environ["PAGE_ACCESS_TOKEN"])

app = Flask(__name__)

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200
  
@app.route('/', methods=['POST'])
def webhook():
  page.handle_webhook(request.get_data(as_text=True))
  return "ok"

@page.handle_message
def received_message(event):
  sender_id = event.sender_id
  recipient_id = event.recipient_id
  message = event.message_text
  time_of_message = event.timestamp
  message = event.message
  page.send(sender_id, "thank you! your message is")


Kom_i_gang = ("kom igang")
test = ("test")
Hej_receive = ("hej", "hello", "hi", "hejsa")
Velkomst_send = ["Velkommen til Flora, Hvad kan jeg hjaelpe med?", "Velkommen til flora, jeg er en chatbot om meget gerne vil hjaelpe dig med at finde et par flotte blomster, laekker chokolade eller en god gin, hvad kan jeg goere for dig?"]
eftervelkomst_receive1 = ("koebe", "se", "undersoege", "sende", "taenke", "taenkte", "hjaelpe", "hjaelp", "har i", "skal bruge") 
eftervelkomst_receive2 = ("blomster", "buketter", "flot") 
eftervelkomst_receive3 = ("alkohol", "gin", "rom", "vodka", "cognac", "vin", "oel", "smag")
eftervelkomst_receive4 = ("chokolade", "kakao", "laekkerier", "soedt")
eftervelkomst_receive5 = ("gave", "pakke")
eftervelkomst_send1 = ("hvem oensker du at sende en buket?", "hvem kan jeg hjaelpe dig med at koebe blomster til?")
eftervelkomst_send2 = ("hvem har du taenkt dig at give en gave? Jeg kan andbefale vores nye ASK gin!", "hvem kan jeg hjaelpe dig med at give en gave?")
eftervelkomst_send3 = ("Jeg elsker chokolade ", u"hvem kan jeg hjaelpe dig med at give en gave? Jeg kan andbefale cho cho chokolade!")
person_detect = ("mor", "far", "kaereste", "kone", "sambo", "foraeldre", "medarbejder", "kollega", "teammate")
person_kaerlighed = ("kone", "kaereste")
person_arbejde = ("medarbejder", "kollega", "teammate")
person_foraeldre = ("mor", "far", "foraeldre")


  
@page.handle_postback
def received_postback(event):
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    time_of_postback = event.timestamp

    payload = event.postback_payload

    print("Received postback for user %s and page %s with payload '%s' at %s"
          % (sender_id, recipient_id, payload, time_of_postback))

    page.send(sender_id, "Postback called")

@page.after_send
def after_send(payload, response):
  """:type payload: fbmq.Payload"""
  print("complete")
  





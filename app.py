import os
import sys
import json
import random
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
  
Velkomst_send = ["Velkommen til Flora, Hvad kan jeg hjaelpe med?", "Velkommen til flora, jeg er en chatbot om meget gerne vil hjaelpe dig med at finde et par flotte blomster, laekker chokolade eller en god gin, hvad kan jeg goere for dig?"]
Kom_i_gang =["Kom i gang"]
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


quick_replies = [
  QuickReply(title="Blomster", payload="PICK_Blomster"),
  QuickReply(title="Alkohol", payload="PICK_Alkohol"),
  QuickReply(title="Chokolade", payload="PICK_chokolade"),
  QuickReply(title="Gave", payload="PICK_Gave")
]


text= ["hej"]

listing = []

def postback(postback_text):
    for word in postback_text.split():
        return random.choice(Velkomst_send)
    return "none"

def efter_velkomst(message):
    for word in message.split():
        if word.lower() in eftervelkomst_receive2:
            return random.choice(eftervelkomst_send1)
        if word.lower() in eftervelkomst_receive3:
            return random.choice(eftervelkomst_send2)
        if word.lower() in eftervelkomst_receive4:
            return random.choice(eftervelkomst_send3)
    return "none"

def send(message):
    for word in message.split():
        if word.lower() in Kom_i_gang:
            return velkomst_check(message) 
        if word.lower() in eftervelkomst_receive1:
            return efter_velkomst(message)
    return "none"


@page.handle_message
def received_message(event):
    global listing
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    message = event.message_text
    time_of_message = event.timestamp
    reply_text = send(message)
    if reply_text != "none":
        page.send(sender_id, reply_text)
    else: page.send(sender_id, "Jeg forstaer ikke, hvad oensker du at undersoege?", quick_replies=quick_replies, metadata="DEVELOPER_DEFINED_METADATA")
    listing.append((message, reply_text))

  
@page.handle_postback
def received_postback(event):
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    time_of_postback = event.timestamp
    payload = event.postback_payload
    
    page.send(sender_id, postback(postback_text))

@page.after_send
def after_send(payload, response):
  """:type payload: fbmq.Payload"""
  print("complete")
  





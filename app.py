# -*- coding: cp1252 -*-
import os
import sys
import json
import random
from flask import Flask, request
from fbmq import Attachment, Template, QuickReply, Page


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

Velkomst_send = ["Velkommen","Velkommen"]
Kom_i_gang =["Kom igang"]

eftervelkomst_receive1 = (u"købe", "se", "undersøge", "sende", "tænke", "tænkte", "hjælpe", "hjælp", "har i", "skal bruge") 
eftervelkomst_receive2 = ("blomster", "buketter", "flot") 
eftervelkomst_receive3 = ("alkohol", "gin", "rom", "vodka", "cognac", "vin", "oel", "smag")
eftervelkomst_receive4 = ("chokolade", "kakao", "laekkerier", "soedt")
eftervelkomst_receive5 = ("gave", "pakke")
eftervelkomst_send1 = (u"hvem ønsker du at sende en buket?", u"hvem kan jeg hjælpe dig med at købe blomster til?")
eftervelkomst_send2 = ("hvem har du taenkt dig at give en gave? Jeg kan andbefale vores nye ASK gin!", "hvem kan jeg hjaelpe dig med at give en gave?")
eftervelkomst_send3 = ("Jeg elsker chokolade ", u"hvem kan jeg hjaelpe dig med at give en gave? Jeg kan andbefale cho cho chokolade!")
eftervelkomst_send3 = ("hvem tænker du at give en gave", "hvem ønsker du at give en gave")
person_detect = ("mor", "far", "kaereste", "kone", "sambo", "foraeldre", "medarbejder", "kollega", "teammate")
person_kaerlighed = ("kone", "kaereste")
person_arbejde = ("medarbejder", "kollega", "teammate")
person_foraeldre = ("mor", "far", "foraeldre")
Anledning = ("jubileaum", "foedselsdag", "bryllup", "kobberbryllup", "guldbryllup", "soelvbryllup", "bryllupsdag", "mors dag", "morsdag", "fars dag", "farsdag")
Andledning_send = ("hvilken anledning gives der blomster til?")

quick_replies = [
  QuickReply(title="Blomster", payload="PICK_Blomster"),
  QuickReply(title="Alkohol", payload="PICK_Alkohol"),
  QuickReply(title="Chokolade", payload="PICK_chokolade"),
  QuickReply(title="Gave", payload="PICK_Gave")
]


def efter_velkomst(message):
    for word in message.split():
        if word.lower() in eftervelkomst_receive2:
            return 1
        elif word.lower() in eftervelkomst_receive3:
            return 2
        elif word.lower() in eftervelkomst_receive4:
            return 3
        elif word.lower() in eftervelkomst_receive5:
            return 4
    return 0


def person_detectblomster(message):
    for word in message.split():
        if word.lower() in person_detect:
            return "Har din" +" " + str(word)+ " " + "nogle ynglings blomster?"
    return "none"

def person_detectalkohol(message):
    for word in message.split():
        if word.lower() in person_detect:
            return "Vil din" +" " + str(word)+ " " + "vaere mest interesseret i oel, vin eller alkohol?"
    return "none"

def first_trigger(message):
    for word in message.split():
        if word.lower() in eftervelkomst_receive1:
            return 1
        
def send(message):
    first_trigger_var= first_trigger(message)
    eftervelkomstvar= efter_velkomst(message)
    person_detectblomstervar= person_detectblomster(message)
    person_detectalkoholvar = person_detectalkohol(message)
    
    if first_trigger_var == 1 :
        if eftervelkomstvar == 1 and person_detectblomstervar != "none":
            return person_detectblomstervar
        elif eftervelkomstvar == 1:
            return random.choice(eftervelkomst_send1)
        elif eftervelkomstvar == 2 and person_detectalkoholvar != "none":
            return person_detectalkoholvar
        elif eftervelkomstvar == 2:
            return random.choice(eftervelkomst_send2)
        elif eftervelkomstvar == 3:
            return random.choice(eftervelkomst_send3)
        elif eftervelkomstvar == 4:
            return random.choice(eftervelkomst_send4)
        else: return "none"
    else: return "none3"

    
@page.handle_message
def received_message(event):
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    message = event.message_text.decode('iso-8859-1')
    time_of_message = event.timestamp
    reply_text = send(message)

    if reply_text == "none":
        page.send(sender_id, "Jeg forstaer ikke, hvad oensker du at undersoege?", quick_replies=quick_replies, metadata="DEVELOPER_DEFINED_METADATA")
    else: page.send(sender_id, reply_text)

    print

@page.handle_postback
def received_postback(event): 
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    time_of_postback = event.timestamp
    payload = event.postback_payload
    reply_payload = random.choice(Velkomst_send)
    
    page.send(sender_id, reply_payload)
    
@page.after_send
def after_send(payload, response):
    """:type payload: fbmq.Payload"""
    print("complete")
    


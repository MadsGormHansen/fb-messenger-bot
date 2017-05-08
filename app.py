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
  
Velkomst_send = ["Velkommen til flora, jeg er en chatbot som meget gerne vil hjaelpe dig med at finde et par flotte blomster, laekker chokolade eller en god gin, hvad kan jeg goere for dig?","Velkommen"]
Kom_i_gang =["Kom igang"]
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
Anledning = ("jubileaum", "foedselsdag", "bryllup", "kobberbryllup", "guldbryllup", "soelvbryllup", "bryllupsdag", "mors dag", "morsdag", "fars dag", )
Andledning_send = ("hvilken anledning gives der blomster til?")

quick_replies = [
  QuickReply(title="Blomster", payload="PICK_Blomster"),
  QuickReply(title="Alkohol", payload="PICK_Alkohol"),
  QuickReply(title="Chokolade", payload="PICK_chokolade"),
  QuickReply(title="Gave", payload="PICK_Gave")
]

global listing
listing = []

def efter_velkomst(message):
    for word in message.split():
        if word.lower() in eftervelkomst_receive2:
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
    global listing
    first_trigger_var= first_trigger(message)
    eftervelkomstvar= efter_velkomst(message)
    person_detectblomstervar= person_detectblomster(message)
    person_detectalkoholvar = person_detectalkohol(message)
    if listing[-1] in [Kom_i_gang, Velkomst_send] and first_trigger_var is 1:
        if eftervelkomstvar is 1 and person_detectblomstervar != "none":
            return person_detectblomstervar
        elif eftervelkomstvar is 1:
            return random.choice(eftervelkomst_send1)
        elif eftervelkomstvar is 2 and person_detectalkoholvar != "none":
            return person_detectalkoholvar
        elif eftervelkomstvar is 2:
            return random.choice(eftervelkomst_send2)
        elif eftervelkomstvar is 3:
            return random.choice(eftervelkomst_send3)
        elif eftervelkomstvar is 4:
            return random.choice(eftervelkomst_send4)
        else: return "none2"
    else: return "none1"
    

@page.handle_message
def received_message(event):
    global listing
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    message = event.message_text
    time_of_message = event.timestamp
    reply_text = send(message)

    listing.append([message, reply_text])

    if reply_text == "none":
        page.send(sender_id, "Jeg forstaer ikke, hvad oensker du at undersoege?", quick_replies=quick_replies, metadata="DEVELOPER_DEFINED_METADATA")
    else: page.send(sender_id, reply_text)

    
  
@page.handle_postback
def received_postback(event):
    global listing 
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    time_of_postback = event.timestamp
    payload = event.postback_payload
    reply_payload = random.choice(Velkomst_send)
    listing.append([payload, reply_payload])
    page.send(sender_id, reply_payload)
    print listing[-1]
  





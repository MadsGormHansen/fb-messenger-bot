# -*- coding: utf-8 -*-
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

Velkomst_send = ["Hej og velkommen til Interflora! Jeg er din automatiske chatbod og vil hjælpe dig med at finde det rigtige. Fortæl først, hvad du kigger efter, fx  blomster, chokolade, vin eller gavepakker.","Hej, hvad kan jeg hjælpe dig med? Jeg er din chatbod, og du skal blot fortælle, hvad du er interesseret i, så vil jeg prøve at hjælpe dig. "]
Kom_i_gang =["Kom igang"]

eftervelkomst_receive1 = ("købe", "se", "undersøge", "sende", "tænke", "tænkte", "hjælpe", "hjælp", "har i", "skal bruge", "interesseret", "jeg skal have", "have", "finde" )
eftervelkomst_receive2 = ("blomster", "buketter", "flot", "blomst", "buket") 
eftervelkomst_receive3 = ("alkohol", "gin", "rom", "vodka", "cognac", "vin", "oel", "smag")
eftervelkomst_receive4 = ("chokolade", "kakao", "lækkerier", "soedt")
eftervelkomst_receive5 = ("gave", "pakke")

eftervelkomst_send1 = ("Ok, så vil jeg hjælpe dig med at finde den rigtige buket. Fortæl hvem der skal have blomster, eller om de er til en særlig anledning, fx bryllup eller fødselsdag", "Hvem skal have blomsterne? Er de måske til en særlig anledning, fx bryllup eller fødselsdag?")

eftervelkomst_send2 = ("hvem har du tænkt dig at give en gave? Jeg kan andbefale vores nye ASK gin!", "hvem kan jeg hjælpe dig med at give en gave?")
eftervelkomst_send3 = ("Jeg elsker chokolade ", u"hvem kan jeg hjaelpe dig med at give en gave? Jeg kan andbefale cho cho chokolade!")
eftervelkomst_send3 = ("hvem tænker du at give en gave", "hvem ønsker du at give en gave")

person_detect = ("mor", "mors", "far","fars" , "kæreste", "kærestes", "kone", "kones", "sambo", "forældre", "forældres", "medarbejder", "kollega", "teammate")

person_kaerlighed = ("kone", "kaereste")
person_arbejde = ("medarbejder", "kollega", "teammate")
person_foraeldre = ("mor", "far", "foraeldre")

Anledning = ("jubilæum", "fødselsdag", "bryllup", "kobberbryllup", "guldbryllup", "sølvbryllup", "bryllupsdag", "mors dag", "morsdag", "fars dag", "farsdag", "begravelse", "sygdom")

Andledning_send = ("hvilken anledning gives der blomster til?")

Pris_send = ("Fint, har du tænkt på, hvor meget buketten cirka skal koste?")  

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

def person_detectanledning(message):
    for word in message.split():
        if word.lower() in Anledning:
            return "Kender din anledning"
    return "none"

def first_trigger(message):
    for word in message.split():
        if word.lower() in eftervelkomst_receive1:
            return 1


def send(message):
    first_trigger_var= first_trigger(message)
    eftervelkomstvar= efter_velkomst(message)
    person_detectblomstervar= person_detectblomster(message)
    person_detectanledningvar = person_detectanledning(message)
    
    if first_trigger_var == 1:
        if eftervelkomstvar == 1 and person_detectblomstervar != "none" and person_detectanledningvar != "none":
            return "Jeg kender anledning, person og blomster 1"
        if eftervelkomstvar == 1 and person_detectanledningvar != "none":
            return "Jeg kender person og anledning"
        if eftervelkomstvar == 1 and person_detectblomstervar != "none":
            return "Jeg kender person og blomster 1"
        elif eftervelkomstvar == 1:
            return "Jeg kender blomster"
        elif eftervelkomstvar == 2:
            return "jeg kender alkohol"
        elif eftervelkomstvar == 3:
            return "Jeg kender chokolade"
        elif eftervelkomstvar == 4:
            return "Jeg kender gave" 
        else: return "send quickreply1"
    elif message == "Blomster"
        return "Quickreply blomster"    
    else: "none"
    
@page.handle_message
def received_message(event):
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    message = event.message_text.encode('utf8')
    time_of_message = event.timestamp
    reply_text = send(message)
    reply_text = reply_text if isinstance(reply_text, str) else reply_text.encode('utf-8') if isinstance(reply_text,unicode) else None
    if reply_text == "send quickreply1":
        page.send(sender_id, "Jeg forstaer ikke, hvad oensker du at undersoege?", quick_replies=quick_replies, metadata="DEVELOPER_DEFINED_METADATA")
    else: page.send(sender_id, reply_text)

    print "text in handle message", reply_text

@page.handle_postback
def received_postback(event): 
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    time_of_postback = event.timestamp
    payload = event.postback_payload
    reply_payload = random.choice(Velkomst_send)
    
    page.send(sender_id, reply_payload)

    print "payload in postback", payload


@page.callback(['PICK_Blomster'])
def callback_clicked_button(payload, event):
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    reply_blomsterpayload = "Jeg kender blomster fra quickreply"
    
    page.send(sender_id, reply_blomsterpayload)

    return "payload in postback", payload
    

@page.after_send
def after_send(payload, response):
    """:type payload: fbmq.Payload"""
    print("complete")
    


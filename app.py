# -*- coding: utf-8 -*-
import os
import sys
import json
import random
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from fbmq import Attachment, Template, QuickReply, Page

app = Flask(__name__)

app.secret_key= "MA1114ha"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://mgh:Analytics4ever1@responsive-sandbox.cloudapp.net/SMP?driver=SQL Server Native Client 11.0'

#engine = app.create_engine("mssql+pyodbc://mgh:Analytics4ever1@responsive-sandbox.cloudapp.net/SMP?driver=SQL+Server+Native+Client+11.0")

db = SQLAlchemy(app)

page = Page(os.environ["PAGE_ACCESS_TOKEN"])

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

Kom_i_gang = ["Kom igang"]
Velkomst_send = "Hej og velkommen til Interflora! Mit navn er Flora og jeg er din automatiske chatbot som vil hjælpe dig med at finde det helt rigtige. Fortæl først, hvad du kigger efter, fx blomster, chokolade, vin eller gavepakker."
eftervelkomst_receive1 = ("købe", "se", "undersøge", "sende", "tænke", "tænkte", "hjælpe", "hjælp", "har", "bruge", "have", "finde", "sende")
eftervelkomst_receive2 = ("blomster", "buketter", "flot", "blomst", "buket") 
eftervelkomst_receive3 = ("alkohol", "gin", "rom", "vodka", "cognac", "vin", "øl", "smag")
eftervelkomst_receive4 = ("chokolade", "kakao", "lækkerier", "soedt")
eftervelkomst_receive5 = ("gave", "pakke")

eftervelkomst_receive12 = ("til","holder", "gør", "skal", "afholder")
interesseret = ("interesseret")
blomster = ("blomster","blomst")

eftervelkomst_send1 = ("Ok, så vil jeg hjælpe dig med at finde den rigtige buket. Fortæl hvem der skal have blomster, eller om de er til en særlig anledning, fx bryllup eller fødselsdag", "Hvem skal have blomsterne? Er de måske til en særlig anledning, fx bryllup eller fødselsdag?")

eftervelkomst_send2 = ("hvem har du tænkt dig at give en gave? Jeg kan andbefale vores nye ASK gin!", "hvem kan jeg hjælpe dig med at give en gave?")
eftervelkomst_send3 = ("Jeg elsker chokolade ", "hvem kan jeg hjaelpe dig med at give en gave? Jeg kan andbefale cho cho chokolade!")
eftervelkomst_send3 = ("hvem tænker du at give en gave", "hvem ønsker du at give en gave")

person_detect = ("mor", "mors", "far", "fars" , "kæreste", "kærestes", "kone", "kones", "sambo", "forældre", "forældres", "medarbejder", "kollega", "teammate", "mor,", "far,", "kæreste,", "kone,", "forældre,")

Anledning = ("jubilæum", "fødselsdag", "bryllup", "kobberbryllup", "guldbryllup", "sølvbryllup", "bryllupsdag", "farsdag", "morsdag" ,"begravelse", "sygdom", "fordi", "fylder")

Andledning_send = ("hvilken anledning gives der blomster til?")

Pris_detect = ("kr", "koste")

Pris_send = ("Fint, har du tænkt på, hvor meget buketten cirka skal koste?")  

quick_replies = [
  QuickReply(title="Buketter", payload="PICK_Blomster"),
  QuickReply(title="Alkohol", payload="PICK_Alkohol"),
  QuickReply(title="Chokolade", payload="PICK_chokolade"),
  QuickReply(title="Gave", payload="PICK_Gave")
]


blomster_url = Template.Generic([
  Template.GenericElement("Lav tæt buket (Florist Choice)",
                          subtitle="Overlad trygt ansvaret til vores dygtige florister og lad dem sammensætte en tæt, smuk og unik buket der vil skabe glæde hos den heldige modtager.",
                          item_url="https://www.interflora.dk/produkt/lav-taet-buket-florist-choice",
                          image_url="https://www.interflora.dk/sites/default/files/styles/product_large/public/Lav_taet_buket_florist_choice_mellem_1825.jpg?itok=_7FnADUk",
                          buttons=[
                              Template.ButtonWeb("Til produkt", "https://www.interflora.dk/produkt/lav-taet-buket-florist-choice"),
                              Template.ButtonPostBack("Find bedre match", "AfterURL"),
                              Template.ButtonWeb("Til hjemmeside", "https://www.interflora.dk/")
                          ])
])


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


def person_detect1(message):
    for word in message.split():
        if word.lower() in person_detect:
            return "I hvilken anledning vil du gerne gi’ din" +" " + str(word)+ " " + "blomster? Fx fødselsdag, bryllup eller andet?"
    return "none"


def person_detect2(message):
    for word in message.split():
        if word.lower() in person_detect:
            return "Skal din" +" " + str(word)+ " " + " have en gave til en bestemt anledning? Er det til en fødselsdag eller bare fordi?"
    return "none"

def person_detect3(message):
    for word in message.split():
        if word.lower() in person_detect:
            return "Hvad er din" + " " + str(word)+ " " + "interesseret i? Er det en buket blomster, vin eller chokolade?"
    return "none"

def anledning_detect1(message):
    for word in message.split():
        if word.lower() in Anledning:
            return "Ok, du skal til" + " " + str(word)+ ". Hvem afholder" +" "+ str(word)+"?"
    return "none"


def first_trigger(message):
    for word in message.split():
        if word.lower() in eftervelkomst_receive1:
            return 1

def second_trigger(message):
    for word in message.split():
        if word.lower() in eftervelkomst_receive12:
            return 1

def third_trigger(message):
    for word in message.split():
        if word.lower() in blomster:
            return 1
        
def fourth_trigger(message):
     for word in message.split():
        if word.lower() in Pris_detect:
            return 1
        
def send(message):
    first_trigger_var= first_trigger(message)
    second_trigger_var = second_trigger(message)
    third_trigger_var = third_trigger(message)
    fourth_trigger_var = fourth_trigger(message)
    eftervelkomstvar= efter_velkomst(message)
    person_detect1var = person_detect1(message)
    person_detect2var = person_detect2(message)
    person_detect3var = person_detect3(message)
    anledning_detect1var = anledning_detect1(message)
    
    if first_trigger_var == 1:
        if eftervelkomstvar == 1 and person_detect1var != "none" and anledning_detect1var != "none":
            return Pris_send
        elif eftervelkomstvar == 1 and anledning_detect1var != "none":
            return "Ok, så vil jeg hjælpe dig med at finde den rigtige buket. Fortæl, hvem er den heldige som skal have en flot buket blomster?"
        elif eftervelkomstvar == 1 and person_detect1var != "none":
            return person_detect1var
        elif person_detect3var != "none" and anledning_detect1var != "none":
            return person_detect3var
        elif anledning_detect1var != "none":
            return anledning_detect1var
        elif person_detect2var != "none":
            return person_detect2var
        elif eftervelkomstvar == 1:
            return random.choice(eftervelkomst_send1)
        else: return "send quickreply1"  
    elif second_trigger_var == 1:
        if person_detect3var != "none" and anledning_detect1var != "none":
            return person_detect3var
        if anledning_detect1var != "none":
            return Pris_send
        elif person_detect1var != "none":
            return person_detect1var
        else: return "none1"
    elif third_trigger_var == 1:
        return Pris_send
    elif anledning_detect1var != "none":
        return Pris_send
    elif fourth_trigger_var == 1:
        return "send url"

@page.handle_message
def received_message(event):
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    message = event.message_text.encode('utf8')
    time_of_message = event.timestamp
    reply_text = send(message)
    reply_text = reply_text if isinstance(reply_text, str) else reply_text.encode('utf-8') if isinstance(reply_text,unicode) else None
    if reply_text == "send quickreply1":
        page.send(sender_id, "Jeg er en chatbot og bliver kun klogere af data. Forstår ikke helt hvad du siger, kan du hælpe mig lidt? Hvad oensker du at undersoege?", quick_replies=quick_replies, metadata="DEVELOPER_DEFINED_METADATA")
    elif reply_text == "send url":
        page.send(sender_id, blomster_url)
    else: page.send(sender_id, reply_text)
    
    db.session.add(Result(sender_id,message,reply_text))
    print(reply_text)
    print(message)


@page.handle_postback
def received_postback(event): 
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    time_of_postback = event.timestamp
    payload = event.postback_payload
    reply_payload = Velkomst_send
    
    if payload == "Kom igang":
        page.send(sender_id, reply_payload)
    elif payload == "AfterURL":
        page.send(sender_id, "Ok, så prøver jeg igen! Er du måske mere interesseret i en god flaske vin eller vores helt egen Gin?")
    else: "Error, Postback"

    print(payload)
    print(reply_payload)

@page.callback(['PICK_Blomster'])
def callback_clicked_button(payload, event):
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    reply_blomsterpayload =  "Hvem skal have blomsterne? Er de måske til en særlig anledning, fx bryllup eller fødselsdag?"
    
    page.send(sender_id, reply_blomsterpayload) 

@page.after_send
def after_send(payload, response):
    """:type payload: fbmq.Payload"""
    


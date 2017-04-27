# -*- coding: cp1252 -*-
import os
import sys
import json
import random
import itertools

import requests
from flask import Flask, request

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

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing
                              
    if data["object"] == "page":

        for entry in data["entry"]:
            if 'messaging' in entry:
                for messaging_event in entry["messaging"]:

                    if messaging_event.get("message"):  # someone sent us a message

                        sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                        recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                        message_text = messaging_event["message"][u"text"]  # the message's text
                        reply_text = Send(message_text)

                        previous_messages.extend(message_text, reply_text)
                        
                        send_message(sender_id, reply_text)
                     
                    if messaging_event.get("delivery"):  # delivery confirmation
                        pass

                    if messaging_event.get("optin"):  # optin confirmation
                        pass

                    if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                        pass

    return "ok", 200

Kom_i_gang = ("kom i gang")
Hej_receive = ("hej", "hello", "hi", "hejsa")
Velkomst_send = ["Velkommen til Flora, Hvad kan jeg hjaelpe med?", "Velkommen til flora, jeg er en chatbot om meget gerne vil hjaelpe dig med at finde et par flotte blomster, laekker chokolade eller en god gin, hvad kan jeg gøre for dig?"]
eftervelkomst_receive1 = ("koebe", "se", "undersoege","sende", "taenke", "taenkte", "hjaelpe", "hjaelp") 
eftervelkomst_receive2 = ("blomster", "buketter", "flot") 
eftervelkomst_receive3 = ("alkohol", "gin", "rom", "vodka", "cognac", "vin", "oel", "smag")
eftervelkomst_receive4 = ("chokolade", "kakao", "laekkerier", "soedt")
eftervelkomst_send1 = ("hvem oensker du at sende en buket?", "hvem kan jeg hjaelpe dig med at koebe blomster til?")
eftervelkomst_send2 = ("hvem har du taenkt dig at give en gave? Jeg kan andbefale vores nye ASK gin!", "hvem kan jeg hjaelpe dig med at give en gave?")
eftervelkomst_send3 = ("Jeg elsker chokolade ", u"hvem kan jeg hjaelpe dig med at give en gave? Jeg kan andbefale cho cho chokolade!")
person_detect = ("mor", "far", "kaereste", "kone", "sambo", "foraeldre", "medarbejder", "kollega", "teammate")
person_kaerlighed = ("kone", "kaereste")
person_arbejde = ("medarbejder", "kollega", "teammate")
person_foraeldre = ("mor", "far", "foraeldre")


class previous_messages(unicode):
    def _init_(self,message_text, reply_text):
        self.message_text = message_text
        self.reply_text = reply_text

def velkomst_check(message_text):
    for word in message_text.split():
        if word.lower() in Kom_i_gang:
            return random.choice(Velkomst_send)
    return "hejsa"

    
def efter_velkomst(message_text):
    for word in message_text.split():
        if word.lower() in eftervelkomst_receive2:
            return random.choice(eftervelkomst_send1)
        if word.lower() in eftervelkomst_receive3:
            return random.choice(eftervelkomst_send2)
        if word.lower() in eftervelkomst_receive4:
            return random.choice(eftervelkomst_send3)
    return "hejso"


def Send(message_text):
    for word in message_text.split():
        if word.lower() in Kom_i_gang:
            return velkomst_check(message_text) 
        if word.lower() in eftervelkomst_receive1:
            return efter_velkomst(message_text)
    return "fuck dig"



def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)

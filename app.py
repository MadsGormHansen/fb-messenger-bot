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


global listing

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
    reply_text = send(message)
    page.send(sender_id, reply_text)
    listing.append((message,reply_text))


text=("hej")

def send(message):
    for word in message:
        if word.lower() in text:
            return "hej"
    return "none"

  
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
  





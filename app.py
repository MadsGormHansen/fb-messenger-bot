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

@app.route('/webhook', methods=['POST'])
def webhook():

  page.handle_webhook(request.get_data(as_text=True))
  return "ok"

  log(event)

@page.handle_message
def received_message(event):
  sender_id = event.sender_id
  recipient_id = event.recipient_id
  message = event.message_text
  time_of_message = event.timestamp
  message = event.message
  page.send(recipient_id, "thank you! your message is")
  log(event)
  
@page.handle_postback
def received_postback(event):
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    time_of_postback = event.timestamp

    payload = event.postback_payload

    print("Received postback for user %s and page %s with payload '%s' at %s"
          % (sender_id, recipient_id, payload, time_of_postback))

    page.send(recipient_id, "Postback called")

@page.after_send
def after_send(payload, response):
  """:type payload: fbmq.Payload"""
  print("complete")
  





import os
import sys
import json
import random
import itertools
import requests
from flask import Flask, request
from fbmq import Attachment, Template, QuickReply, Page

page = fbmq.Page(EAAD5ZA0yoEewBAIh13Kg8HthCP5mBV90m9e2b98vLKTACbWGLD0ZAPlFzf7J4bgESHLp1XXyM45MP42z01AWZCB35Qhv6n0keaSGQZCxZCe3vAbd22tjwzHtgx3hgFRqs6kHCb757onZCtEWmqULI2aT5GMJtalSZBy90HvN7uYxgZDZD)

@app.route('/webhook', methods=['POST'])
def webhook():
  page.handle_webhook(request.get_data(as_text=True))
  return "ok"


@page.handle_message
def message_handler(event):
  """:type event: fbmq.Event"""
  sender_id = event.sender_id
  message = event.message_text
  
  page.send(sender_id, "thank you! your message is '%s'" % message)

@page.after_send
def after_send(payload, response):
  """:type payload: fbmq.Payload"""
  print("complete")




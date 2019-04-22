# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

# This code is based on https://github.com/line/line-bot-sdk-python

import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import requests
import json

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN") 
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET") 
AZURE_QNAMAKER_URL = os.environ.get("AZURE_QNAMAKER_URL") 
AZURE_QNAMAKER_SUBSCRIPTION_KEY = os.environ.get("AZURE_QNAMAKER_SUBSCRIPTION_KEY") 

app = Flask(__name__)

#print(LINE_CHANNEL_ACCESS_TOKEN)
#print("----------------------")
#print(LINE_CHANNEL_SECRET)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

def ask(question):
    # ask for question to QnA Maker
    response = requests.post(
        AZURE_QNAMAKER_URL,
        headers = {'Content-Type': 'application/json',
            'Authorization': AZURE_QNAMAKER_SUBSCRIPTION_KEY},
        data = json.dumps({'question': question})
    )

    # someting happen on the server.
    if (response.status_code != 200):
        return response.status_code

    data = response.json()
#    print(data)
    return data['answers'][0]['answer']

@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
#        TextSendMessage(text=event.message.text))
        TextSendMessage(text=ask(event.message.text)))

if __name__ == "__main__":
    app.run()

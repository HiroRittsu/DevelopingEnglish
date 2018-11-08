import json
import os
import sys
from argparse import ArgumentParser

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

app = Flask(__name__)

class LineApp:

    line_bot_api = None
    handler = None
    to = ''
    receive = []

    def __init__(self, channel_secret, channel_access_token):
        self.line_bot_api = LineBotApi(channel_access_token)
        self.handler = WebhookHandler(channel_secret)

    @app.route("/callback", methods=['POST'])
    def callback(self):
        signature = request.headers['X-Line-Signature']

        body = request.get_data(as_text=True)
        app.logger.info("Request body: " + body)

        self.to = json.loads(body)["events"][0]["source"]["userId"]

        try:
            self.handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return 'OK'


    '''
    @handler.add(MessageEvent, message=TextMessage)
    def replay_msgs(self, event):
        self.line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )
    '''

    @handler.add(MessageEvent, message=TextMessage)
    def pull_msgs(self, event):
        self.receive.append(event.message.text)


    def push_msgs(self,str):
        if not self.to == '':
            self.line_bot_api.push_message(
                self.to,
                TextSendMessage(str)
            )

        else:
            print("not addr")
import json
import concurrent.futures
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
handler = None

class LineApp:

    line_bot_api = None
    to = ''
    receive = []

    def __init__(self, channel_secret, channel_access_token):
        global handler
        self.line_bot_api = LineBotApi(channel_access_token)
        handler = WebhookHandler(channel_secret)

        #スレッド起動
        print("debug")
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        executor.submit(self.line_init)

    def line_init(self):
        print("debug")
        arg_parser = ArgumentParser(
            usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
        )
        arg_parser.add_argument('-p', '--port', default=8000, help='port')
        arg_parser.add_argument('-d', '--debug', default=False, help='debug')
        options = arg_parser.parse_args()

        app.run(debug=options.debug, port=options.port)


    @app.route("/callback", methods=['POST'])
    def callback(self):
        signature = request.headers['X-Line-Signature']

        body = request.get_data(as_text=True)
        app.logger.info("Request body: " + body)

        self.to = json.loads(body)["events"][0]["source"]["userId"]

        try:
            handler.handle(body, signature)
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

    result = ''
    @handler.add(MessageEvent, message=TextMessage)
    def pull_msgs(self, event):
        self.result = event.message.text
        self.receive.append(self.result)
    '''


    def push_msgs(self,str):
        if not self.to == '':
            self.line_bot_api.push_message(
                self.to,
                TextSendMessage(str)
            )

        else:
            print("not addr")
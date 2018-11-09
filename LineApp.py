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

msgs = []
userId = ''
groupId = ''

#################handler##########
# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)
###################################

@app.route("/callback", methods=['POST'])
def callback():
    global userId
    global groupId
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    print(json.loads(body))

    userId = json.loads(body)["events"][0]["source"]["userId"]
    #groupId = json.loads(body)["events"][0]["source"]["groupId"]

    # handle webhook body
    try:
        handler.handle(body, signature)
        # handler.add(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def pull_msgs(event):
    msgs.append(event.message.text)


class LineApp:

    def __init__(self):
        # スレッド起動
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        executor.submit(self.line_init)

    def line_init(self):
        arg_parser = ArgumentParser(
            usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
        )
        arg_parser.add_argument('-p', '--port', default=8000, help='port')
        arg_parser.add_argument('-d', '--debug', default=False, help='debug')
        options = arg_parser.parse_args()

        app.run(debug=options.debug, port=options.port)

    def push_msgs(self,str):
        if not groupId == '':
            line_bot_api.push_message(
                groupId,
                TextSendMessage(str)
            )
            return

        elif not userId == '':
            line_bot_api.push_message(
                userId,
                TextSendMessage(str)
            )
            return

        else:
            print("not addr")

    def get_msgs(self):
        if not len(msgs) == 0:
            pass
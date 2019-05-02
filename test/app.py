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

# get channel_secret and channel_access_token from your environment variable
channel_secret = ''
channel_access_token = ''
with open('../token', 'r') as f:
	for l in f.readlines():
		if 'LINE_CHANNEL_SECRET' in l:
			channel_secret = l.split(':')[1].replace('\n', '')
		if 'LINE_CHANNEL_ACCESS_TOKEN' in l:
			channel_access_token = l.split(':')[1].replace('\n', '')

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
	print("debugdebugdebu")
	# get X-Line-Signature header value
	signature = request.headers['X-Line-Signature']

	# get request body as text
	body = request.get_data(as_text=True)
	app.logger.info("Request body: " + body)

	print(json.loads(body))

	# handle webhook body
	try:
		handler.handle(body, signature)
		# handler.add(body, signature)
	except InvalidSignatureError:
		abort(400)

	return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
	line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(text=event.message.text)
	)

	line_bot_api.push_message(
		'U444d8a9ca45523b6fcda0226769d9983',
		TextSendMessage("Hello")
	)


if __name__ == "__main__":
	arg_parser = ArgumentParser(
		usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
	)
	arg_parser.add_argument('-p', '--port', default=8000, help='port')
	arg_parser.add_argument('-d', '--debug', default=False, help='debug')
	options = arg_parser.parse_args()

	app.run(debug=options.debug, port=options.port)

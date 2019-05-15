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
import numpy as np
import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
	LineBotApi, WebhookHandler, WebhookParser
)
from linebot.exceptions import (
	InvalidSignatureError
)
from linebot.models import (
	MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
token_file = np.loadtxt('../token', delimiter=':', dtype='str')
channel_secret = str(token_file[0][1]).replace('b\'', '').replace('\'', '')
channel_access_token = str(token_file[1][1]).replace('b\'', '').replace('\'', '')

print(channel_secret)
print(channel_access_token)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
	id = ''
	events = None
	signature = request.headers['X-Line-Signature']

	# get request body as text
	body = request.get_data(as_text=True)
	# app.logger.info("Request body: " + body)

	print(body)

	# parse webhook body
	try:
		events = parser.parse(body, signature)
	except InvalidSignatureError:
		abort(400)

	if 'userId' in body:
		id = json.loads(body)["events"][0]["source"]["userId"]

	if 'groupId' in body:
		id = json.loads(body)["events"][0]["source"]["groupId"]

	# if event is MessageEvent and message is TextMessage, then echo text
	for event in events:
		if not isinstance(event, MessageEvent):
			continue
		if not isinstance(event.message, TextMessage):
			continue

	return 'OK'


if __name__ == "__main__":
	arg_parser = ArgumentParser(
		usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
	)
	arg_parser.add_argument('-p', '--port', default=8000, help='port')
	arg_parser.add_argument('-d', '--debug', default=False, help='debug')
	options = arg_parser.parse_args()

	app.run(debug=options.debug, port=options.port)

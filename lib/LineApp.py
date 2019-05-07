import json
import concurrent.futures
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
	MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,
)

msgs = []

#################handler##########
# get channel_secret and channel_access_token from your environment variable
token_file = np.loadtxt('../token', delimiter=':', dtype='str')
channel_secret = token_file[0][1]
channel_access_token = token_file[1][1]

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
print(channel_access_token, channel_secret)
# parser = WebhookParser(channel_secret)

app = Flask(__name__)


###################################
# 受け取り
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
		abort(400)

	return 'OK'


'''
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

		msgs.append([id, event.message.text])

	return 'OK'
	'''


#####################################################

class LineApp:

	def __init__(self, id: str):
		self.id = id
		# スレッド起動
		executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
		executor.submit(self.__line_init__)

	def __line_init__(self):
		arg_parser = ArgumentParser(
			usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
		)
		arg_parser.add_argument('-p', '--port', default=8000, help='port')
		arg_parser.add_argument('-d', '--debug', default=False, help='debug')
		options = arg_parser.parse_args()

		app.run(debug=options.debug, port=options.port)

	def push_msgs(self, msg: str):
		line_bot_api.push_message(
			self.id,
			TextSendMessage(msg)
		)

	def push_img(self, url: str):
		line_bot_api.push_message(
			self.id,
			ImageSendMessage(
				original_content_url=url,
				preview_image_url=url
			)
		)

	def get_msgs(self):
		result = []
		for msg in msgs:
			print(msg)
			if msg[0] == self.id:
				result.append([self.id, msg[1]])
		return result

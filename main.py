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
import os

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["bWmb+oqy/Pthyrg2V9K8hO7kzKAczw5uYa9bs+Z7XrwhTR2uzEpmcRyXjomrwiCi0S+v2qeE17uiTbhC5yNtHxsWB/EVeuGCWqCzuR1KxzhwdWBs+fgk7HiV5RJ0O6QKvu+ZUhEVwRzlP/JTIN2opwdB04t89/1O/w1cDnyilFU="]
YOUR_CHANNEL_SECRET = os.environ["622f8b68f12dcc8140a0332622ffae57"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 80))
    app.run(host="localhost", port=port)

import os
import time
import random

import coordinator

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

# config
config = {
    "development": "config.DevelopmentConfig",
    "testing": "config.TestingConfig",
    "production": "config.ProductionConfig"
}

# make flask instance
app = Flask(__name__, instance_relative_config=True)

# set flask config
app.config.from_object(config[os.getenv('FLASK_ENV', 'production')])
app.config.from_pyfile('private_config.cfg', silent=True)

# made line api
line_bot_api = LineBotApi(app.config['LINE_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(app.config['LINE_CHANNEL_SECRET'])

# bot scenario
scenario = coordinator.Coordinator()


# webhook
@app.route("/webhook", methods=['POST'])
def webhook():
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


# TextMessage handler
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    send_message = scenario.text_message_handler(event)

    # 即答せずに少し待つ
    time.sleep(random.randrange(5, 20, 1))

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=send_message)
        )

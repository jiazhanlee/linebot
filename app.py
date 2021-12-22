from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


#======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
#======這裡是呼叫的檔案內容=====

#======python的函數庫==========
import tempfile, os
import datetime
import time
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('LuPIwCBAyHeODvMDw1iMRNnIWCv9hI8mPMhFXIfmy9R/GYb93mBtKhoZ6tpSdTjN54I5x5xYoljZx+aw3qs8C3JDwkHKAQRtnlN/04rdF8wqfvrQQpEL9mNDwaUXIEy7rVGS517LIn9K6TBgeVEO3QdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('0ed276cf24dc7a616b58febc28d9602d')


# 監聽所有來自 /callback 的 Post Request
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


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if '最新合作廠商' in msg:
        message = imagemap_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '最新活動訊息' in msg:
        message = buttons_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '註冊會員' in msg:
        message = Confirm_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '旋轉木馬' in msg:
        message = Carousel_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '圖片畫廊' in msg:
        message = test()
        line_bot_api.reply_message(event.reply_token, message)
    elif '功能列表' in msg:
        message = TextSendMessage("功能列表:\n最新合作廠商\n最新活動訊息\n註冊會員\n圖片\n輸入等於符號加上關鍵字為搜尋產品\n其餘輸入則無效")
        line_bot_api.reply_message(event.reply_token, message)
    elif '查詢其他功能' in msg:
        message = TextSendMessage("功能列表:\n最新合作廠商\n最新活動訊息\n註冊會員\n圖片\n輸入等於符號加上關鍵字為搜尋產品\n其餘輸入則無效")
        line_bot_api.reply_message(event.reply_token, message)
    elif '有哪些抽獎品項呢' in msg:
        message = TextSendMessage("https://shopee.tw/")
        line_bot_api.reply_message(event.reply_token, message)
    elif '現在、立刻、馬上' in msg:
        message = TextSendMessage("https://shopee.tw/buyer/signup")
        line_bot_api.reply_message(event.reply_token, message)
    elif '=' in msg:
        message = TextSendMessage("https://shopee.tw/search?keyword"+msg)
        line_bot_api.reply_message(event.reply_token, message)
    else:
        message = TextSendMessage('無效!請輸入功能列表查詢指令!')
        line_bot_api.reply_message(event.reply_token, message)


@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

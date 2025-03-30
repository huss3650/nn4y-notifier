from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "7774334363:AAFHqwMFpFtK23xTxLwTCzVSjnHKCDiu0ss"
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/"

# نخزن المشتركين مؤقتاً
subscribers = set()

def send_message(chat_id, text):
    requests.post(f"{TELEGRAM_API}sendMessage", json={
        "chat_id": chat_id,
        "text": text
    })

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def receive_update():
    data = request.get_json()
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")

    if text == "/start":
        subscribers.add(chat_id)
        send_message(chat_id, "هلا بك! راح توصلك إشعارات بكل حساب جديد في nn4y.life")

    return "ok", 200

@app.route("/notify", methods=["GET"])
def notify_subscribers():
    username = request.args.get("username")
    if not username:
        return "Missing username", 400

    message = f"تمت إضافة حساب جديد: @{username}\nسارع بمشاهدته قبل لا يطير!\nnn4y.life"
    for user in subscribers:
        send_message(user, message)

    return "Notification sent", 200

app.run(host="0.0.0.0", port=5000)

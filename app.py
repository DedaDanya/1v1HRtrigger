import os
import requests
from flask import Flask, request

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

TRIGGER = "здравствуйте, меня заинтересовала вакансия, готов работать у вас"

ANSWER = """Здравствуйте!

Поздравляем Вас с прохождением первого отборочного этапа. Следующий шаг - собеседование

Из предложенных ниже вариантов, выберите удобный  день и время для прохождения собеседования. 

https://calink.ru/HR-1x1

Перед собеседованием важно посмотреть видео-ролик с предложением о работе:

https://kinescope.io/mnSiNgHcrnE3ZoFQKTyj85

❗️Пожалуйста, напишите в чат вашу рабочую почту (ту, которую указали при записи на собеседование), это необходимо для дальнейшего взаимодействия. Спасибо!

До встречи на собеседовании!"""

app = Flask(__name__)


def send_message(chat_id, text, business_connection_id=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": text
    }

    if business_connection_id:
        data["business_connection_id"] = business_connection_id

    requests.post(url, json=data, timeout=10)


@app.route("/", methods=["GET"])
def home():
    return "Bot is running"


@app.route("/setwebhook", methods=["GET"])
def set_webhook():
    if not WEBHOOK_URL:
        return "WEBHOOK_URL is not set", 400

    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    response = requests.post(url, json={
        "url": f"{WEBHOOK_URL}/webhook",
        "allowed_updates": ["message", "business_message"]
    })

    return response.text


@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.json

    message = update.get("business_message") or update.get("message")
    if not message:
        return "ok"

    text = message.get("text", "")
    chat_id = message["chat"]["id"]
    business_connection_id = message.get("business_connection_id")

    if TRIGGER in text.lower():
        send_message(chat_id, ANSWER, business_connection_id)

    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
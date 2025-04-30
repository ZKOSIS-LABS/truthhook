from flask import Flask, request, abort
import os, requests

app = Flask(__name__)

# Read env vars
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID   = os.getenv("CHAT_ID")
SECRET    = os.getenv("SECRET")

TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

@app.route("/api/webhook", methods=["POST"])
def webhook():
    # Verify secret query param
    if request.args.get("secret") != SECRET:
        abort(403)

    payload = request.json.get("resource", {})
    items = payload.get("defaultDatasetItems", [])
    for item in items:
        author = item.get("author", {}).get("username")
        text   = item.get("text")
        url    = item.get("url")
        if author in ("EricTrump", "DonaldJTrumpJr"):
            msg = f"@{author}\n\n{text}\n\n{url}"
            requests.post(TELEGRAM_URL, json={
                "chat_id": CHAT_ID,
                "text": msg,
                "parse_mode": "HTML"
            })
    return ("", 200)

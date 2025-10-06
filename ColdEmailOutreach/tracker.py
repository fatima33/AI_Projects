from flask import Flask, request, send_file
from db import mark_email_opened

app = Flask(__name__)

@app.route("/track_open")
def track_open():
    email_id = request.args.get("id")
    mark_email_opened(email_id)
    return send_file("static/pixel.png", mimetype="image/png")

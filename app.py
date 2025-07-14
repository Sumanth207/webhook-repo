from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from models import format_event
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event_type = request.headers.get("X-GitHub-Event")

    if event_type == "pull_request":
        action = data.get("action")
        if action == "closed" and data["pull_request"]["merged"]:
            event_type = "merge"

    payload = {
        "event_type": event_type,
        "author": data["pusher"]["name"] if event_type == "push" else data["sender"]["login"],
        "from_branch": data.get("pull_request", {}).get("head", {}).get("ref", data.get("from_branch")),
        "to_branch": data.get("pull_request", {}).get("base", {}).get("ref", data.get("ref", "").split("/")[-1]),
        "timestamp": datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")
    }

    mongo.db.events.insert_one(payload)
    return jsonify({"message": "Event stored"}), 201

@app.route('/events', methods=['GET'])
def get_events():
    events = mongo.db.events.find().sort("_id", -1).limit(10)
    formatted = [format_event(e) for e in events]
    return jsonify(formatted)

if __name__ == '__main__':
    app.run(debug=True)
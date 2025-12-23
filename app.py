from flask import Flask, jsonify, request
import random
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify(
        message="Hello, Flask!",
    )


@app.route("/api/greeting", methods=["GET"])
def greeting():
    name = request.args.get("name", default="Guest")
    return jsonify(
        message=f"Hello, {name}!"
    )


@app.route("/api/time")
def current_time():
    now = datetime.utcnow()
    return jsonify(
        utc_time = now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        timestamp = now.timestamp()
    )
    

@app.route("/api/number")
def random_number():
    number = random.randint(1, 100)  # returns a random integer between 1 and 100
    return jsonify(
        random_number=number
    )


fun_facts = [
    "Honey never spoils.",
    "Octopuses have three hearts.",
    "A group of flamingos is called a flamboyance.",
    "Bananas are berries, but strawberries aren't."
]

@app.route("/funfact")
def random_fun_fact():
    fact = random.choice(fun_facts)
    return jsonify(
        fun_fact=fact
    )


@app.route("/api/health")
def health():
    return jsonify(
        status="ok",
        service="flask-api"
    )
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

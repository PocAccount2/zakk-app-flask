from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify(
        message="Hello, Flask!",
    )


def greeting():
    name = request.args.get("name", default="Guest")
    return jsonify(
        message=f"Hello, {name}!"
    )


@app.route("/api/health")
def health():
    return jsonify(
        status="ok",
        service="flask-api"
    )
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

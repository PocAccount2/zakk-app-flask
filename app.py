from flask import Flask, jsonify, request, make_response,send_from_directory
import random
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)



@app.route("/openapi.yaml")
def serve_openapi():
    return send_from_directory(os.getcwd(), "openapi.yaml")


# -------------------------
# 1. Missing Security Headers
# -------------------------
@app.after_request
def add_headers(response):
    # INTENTIONALLY NOT setting security headers
    return response


@app.route("/")
def home():
    return jsonify(message="Hello, Flask!")


# -------------------------
# 2. Reflected XSS
# -------------------------
@app.route("/api/greeting", methods=["GET"])
def greeting():
    name = request.args.get("name", "Guest")
    # Vulnerable: unsanitized user input reflected
    return f"<h1>Hello {name}</h1>"


# -------------------------
# 3. SQL Injection
# -------------------------
@app.route("/api/user")
def get_user():
    user_id = request.args.get("id")

    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    # Vulnerable SQL query
    query = f"SELECT username FROM users WHERE id = {user_id}"
    cursor.execute(query)

    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify(username=row[0])
    return jsonify(error="User not found")


# -------------------------
# 4. Command Injection (Basic)
# -------------------------
@app.route("/api/ping")
def ping():
    host = request.args.get("host")
    # Vulnerable: user input used in system command
    output = f"Pinged {host}"
    return jsonify(result=output)


# -------------------------
# 5. Information Disclosure
# -------------------------
@app.route("/api/debug")
def debug_info():
    return jsonify(
        env=str(app.config),
        headers=dict(request.headers)
    )


# -------------------------
# 6. Insecure Cookies
# -------------------------
@app.route("/api/login")
def login():
    resp = make_response(jsonify(message="Logged in"))
    resp.set_cookie("sessionid", "123456")  # No HttpOnly, Secure flags
    return resp


# -------------------------
# 7. No Authentication / Authorization
# -------------------------
@app.route("/api/admin")
def admin():
    return jsonify(
        admin_panel=True,
        secret="super-secret-admin-data"
    )


# -------------------------
# Normal endpoints
# -------------------------
@app.route("/api/time")
def current_time():
    now = datetime.utcnow()
    return jsonify(
        utc_time=now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        timestamp=now.timestamp()
    )


@app.route("/api/number")
def random_number():
    return jsonify(random_number=random.randint(1, 100))


@app.route("/api/health")
def health():
    return jsonify(status="ok", service="flask-api")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

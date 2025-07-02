from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Cloud!"

@app.route("/api/save", methods=["POST"])
def save():
    data = request.json
    print("📝 Datos recibidos:", data)
    return jsonify({"ok": True}), 200

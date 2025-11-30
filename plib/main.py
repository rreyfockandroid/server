from flask import Flask, jsonify, request
from config.config import Config

app = Flask(__name__)

@app.get("/")
def home():
    print("home - 1request:", request.url)

    return "<h1>Flask działa!</h1>"

@app.get("/info")
def info():
    print("info - 1request:", request.url)

    return jsonify(message="Hello from Flask!", status="OK")

@app.get("/hello/<name>")
def hello(name):
    print("hello - 1request:", request.url)

    return f"Cześć {name}!"


if __name__ == "__main__":
    cfg = Config()
    print(cfg)
    
    app.run(host="0.0.0.0", port=cfg.port)
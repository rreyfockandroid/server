from flask import Flask, jsonify, request
from config.config import Config
from model.qwen import ask_model
from metrics.myappi import init_myappi, profile_request


app = Flask(__name__)
init_myappi(app)

@app.get("/qwen")
# @profile_request
def qwen():
    q = request.args.get('query')
    qres = ask_model(q)
    return qres


@app.get("/")
# @profile_request
def home():
    print("home - 1request:", request.url)
    return "<h1>Flask działa!</h1>"


@app.get("/info")
# @profile_request
def info():
    print("info - 1request:", request.url)
    return jsonify(message="Hello from Flask!", status="OK")


@app.get("/hello/<name>")
# @profile_request
def hello(name):
    print("hello - 1request:", request.url)
    return f"Cześć {name}!"


if __name__ == "__main__":
    cfg = Config()
    print(cfg)
    app.run(host="0.0.0.0", port=cfg.port)
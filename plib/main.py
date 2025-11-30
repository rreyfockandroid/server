from flask import Flask, jsonify, request
from config.config import Config
from model.qwen import ask_model
import yappi
import time
from functools import wraps

app = Flask(__name__)

# === PROFILOWANIE ===
def profile_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        yappi.clear_stats()
        yappi.set_clock_type("wall")
        yappi.start()
        result = func(*args, **kwargs)
        yappi.stop()
        return result
    return wrapper


@app.get("/yappi-stats")
def yappi_stats():
    yappi.get_func_stats().sort("ttot", "desc")

    stats = []
    for s in yappi.get_func_stats():
        stats.append({
            "name": s.name,
            "module": s.module,
            "lineno": s.lineno,
            "ncall": s.ncall,
            "t_total_cpu": round(s.ttot, 6),  # total time
            "t_sub_cpu": round(s.tsub, 6),    # time excluding subcalls
            "t_avg_cpu": round(s.tavg, 6)     # avg call time
        })
    t = int(time.time())
    ystat = yappi.get_func_stats()
    ystat.save(f"profile_{t}.callgrind", type="callgrind")
    ystat.save(f"profile_{t}.pstat", type="pstat")
    return jsonify(stats)


# === ROUTY APLIKACJI ===

@app.get("/qwen")
@profile_request
def qwen():
    q = request.args.get('query')
    qres = ask_model(q)
    return qres


@app.get("/")
@profile_request
def home():
    print("home - 1request:", request.url)
    return "<h1>Flask działa!</h1>"


@app.get("/info")
@profile_request
def info():
    print("info - 1request:", request.url)
    return jsonify(message="Hello from Flask!", status="OK")


@app.get("/hello/<name>")
@profile_request
def hello(name):
    print("hello - 1request:", request.url)
    return f"Cześć {name}!"


if __name__ == "__main__":
    cfg = Config()
    print(cfg)
    app.run(host="0.0.0.0", port=cfg.port)
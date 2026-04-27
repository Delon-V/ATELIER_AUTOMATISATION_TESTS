from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

API_URL = "https://api.quotable.io/random"

def test_api():
    start = time.time()
    try:
        r = requests.get(API_URL, timeout=5)
        latency = time.time() - start

        return {
            "status_code": r.status_code,
            "latency": round(latency, 3),
            "success": r.status_code == 200
        }

    except Exception as e:
        return {
            "status_code": 500,
            "latency": None,
            "success": False,
            "error": str(e)
        }

@app.route("/")
def home():
    return jsonify(test_api())

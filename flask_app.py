from flask import Flask, render_template
import requests
import time

app = Flask(__name__)

APIS = {
    "Agify": "https://api.agify.io/?name=michael",
    "Quotable": "https://api.quotable.io/random"
}

history = []

def test_api(name, url):
    start = time.time()
    try:
        r = requests.get(url, timeout=5)
        latency = time.time() - start

        result = {
            "name": name,
            "status": r.status_code,
            "latency": round(latency, 3),
            "success": r.status_code == 200
        }
    except:
        result = {
            "name": name,
            "status": 500,
            "latency": None,
            "success": False
        }

    history.append(result)
    return result

def get_uptime():
    if not history:
        return 0
    success = sum(1 for h in history if h["success"])
    return round((success / len(history)) * 100, 2)

@app.route("/")
def dashboard():
    results = [test_api(name, url) for name, url in APIS.items()]
    uptime = get_uptime()

    return render_template("index.html", results=results, uptime=uptime, history=history[-10:])

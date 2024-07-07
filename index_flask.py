from flask import Flask, send_file
import subprocess

app = Flask(__name__)


@app.route("/")
def index():
    return send_file("index.html")


@app.route("/bitfinex")
def bitfinex():
    return send_file("output/sum/Bitfinex-sum-cloud-tkx-merged.csv.html")


@app.route("/sector")
def sector():
    return send_file("output\sum\SPDR_ETFS-sum-cloud-tkx-merged.csv.html")


@app.route("/update")
def update():
    subprocess.call([".\env\Scripts\python", "runBitfinex.py"])
    return "Updated"


if __name__ == "__main__":
    app.run()

from flask import Flask, send_file
import runBitfinex
import subprocess

app = Flask(__name__)


@app.route("/")
def index():
    return send_file("index.html")


@app.route("/spx500")
def spx500():
    return send_file("output/sum/SPX500-sum-cloud-tkx-merged.csv.html")


@app.route("/nasdaq100")
def nasdaq100():
    return send_file("output/sum/Nasdaq100-sum-cloud-tkx-merged.csv.html")


@app.route("/dowjones30")
def dowjones30():
    return send_file("output/sum/DowJones30-sum-cloud-tkx-merged.csv.html")


@app.route("/oanda")
def oanda():
    return send_file("output/sum/Oanda-sum-cloud-tkx-merged.csv.html")


@app.route("/ftse100")
def ftse100():
    return send_file("output/sum/FTSE100-sum-cloud-tkx-merged.csv.html")


@app.route("/bitfinex")
def bitfinex():
    return send_file("output/sum/Bitfinex-sum-cloud-tkx-merged.csv.html")


@app.route("/ftse250")
def ftse250():
    return send_file("output/sum/FTSE250-sum-cloud-tkx-merged.csv.html")


@app.route("/futurescurrency")
def ftsefuturescurrency250():
    return send_file(
        "output/sum/FuturesCurrency-sum-cloud-tkx-merged.csv.html"
    )


@app.route("/sector")
def sector():
    return send_file("output/sum/SPDR_ETFS-sum-cloud-tkx-merged.csv.html")


@app.route("/update")
def update():
    # subprocess.call([".\env\Scripts\python", "runBitfinex.py"])

    fetch_Bitfinex_1H = True
    fetch_Bitfinex_4H = True
    fetch_Bitfinex_D = True
    fetch_Bitfinex_W = True
    fetch_Bitfinex_M = True
    fetch_Kicker_use_datetime_format = False
    run_Multi_TimeFrame_Merger_Bitfinex = True
    fetch_kicker = False

    _runBitfinex = runBitfinex
    return _runBitfinex.main(
        fetch_Bitfinex_1H,
        fetch_Bitfinex_4H,
        fetch_Bitfinex_D,
        fetch_Bitfinex_W,
        fetch_Bitfinex_M,
        fetch_Kicker_use_datetime_format,
        run_Multi_TimeFrame_Merger_Bitfinex,
        fetch_kicker,
    )


if __name__ == "__main__":
    app.run()

# Cloud Signal Python #

[View demo here](https://harryguiacorn.github.io/Ichimoku-Cloud-Signal-Python/ "S&P500 Cloud Scan")

<a target="_blank" href="https://colab.research.google.com/github/harryguiacorn/Cloud-Signal-Python">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open Live In Colab"/>
</a>


## Status Update [2026.08.29] ## 
Overall facelift and added scans, which includes Cloud, Tenkan-sen and Kijun-sen, and Chikou span counts.
<img width="1217" height="693" alt="image" src="https://github.com/user-attachments/assets/7c8311d3-f36e-41d6-82c2-1d803260b543" />
<img width="1206" height="601" alt="image" src="https://github.com/user-attachments/assets/2291b6e1-4cd6-4966-8809-14d8864886b4" />
<img width="1844" height="582" alt="image" src="https://github.com/user-attachments/assets/50b65452-5fb3-4120-8af8-b3c8ab428094" />
<img width="1632" height="728" alt="image" src="https://github.com/user-attachments/assets/92f25b3c-d967-41c7-b6f4-7cb3dab4ff49" />



## Status Update [2024.02.06] ## 

Uncover market movers with ease! This application analyses data silently and generates web pages displaying strength scores for every stock in major indices. Dive deeper into each stock's cloud and TKx strength, calculated using powerful multi-timeframe Ichimoku analysis. Finally, see the ultimate verdict: a clear total score for each stock. Dominate the market by sorting through this scorecard, instantly identifying the champions and laggards primed for your trading moves.

![image](https://github.com/harryguiacorn/Ichimoku-Cloud-Signal-Python/assets/1398153/f6b655be-a4a3-489a-94e3-71f8ce627f5b)

![image](https://github.com/harryguiacorn/Ichimoku-Cloud-Signal-Python/assets/1398153/861cfde8-851b-4beb-80ec-c6e6625bbfc2)

![image](https://github.com/harryguiacorn/Ichimoku-Cloud-Signal-Python/assets/1398153/cb903cdf-f2f0-414e-85f0-f6576f826deb)

![image](https://github.com/harryguiacorn/Ichimoku-Cloud-Signal-Python/assets/1398153/ba8a2fde-33c2-40c2-ad7f-0a1e612e65fa)

![image](https://github.com/harryguiacorn/Ichimoku-Cloud-Signal-Python/assets/1398153/312d3ea9-c5ea-451b-8b97-31c49ffa8c87)

![image](https://github.com/harryguiacorn/Ichimoku-Cloud-Signal-Python/assets/1398153/ac38ff46-8025-4031-a94b-9daf60c69ad9)

![image](https://github.com/harryguiacorn/Ichimoku-Cloud-Signal-Python/assets/1398153/46f66f48-7f16-4434-adda-24493831d434)

![image](https://github.com/harryguiacorn/Ichimoku-Cloud-Signal-Python/assets/1398153/70c626d8-3d2f-44e6-9d84-4375035c7495)

![image](https://github.com/harryguiacorn/Ichimoku-Cloud-Signal-Python/assets/1398153/254b69e2-3caa-4030-bb09-d3de1abbef8c)

![image](https://github.com/harryguiacorn/Ichimoku-Cloud-Signal-Python/assets/1398153/c471fa6d-cd46-407c-9b0b-0f561e12dca9)


## Status Update [2023.11.14] ## 
- This project is work in progress, the intention is to produce Ichimoku Cloud signals like in the author's [Cloud Service](https://github.com/harryguiacorn/cloudservice) which is written in PHP. The back end of the coding is taking shape, see below screenshots from one of output files:
### Ichimoku Kijun-sen Signal ###
<img width="498" alt="Screenshot 2022-11-15 at 18 07 50" src="https://user-images.githubusercontent.com/1398153/201997990-165cd688-8f86-47c1-bb34-2b334a26a77a.png">

### Candlestick Kicker Signal ###
<img width="498" alt="Screenshot 2022-11-15 at 18 08 09" src="https://user-images.githubusercontent.com/1398153/201998002-d8365f05-8a34-42cb-8501-5fcd05a59ce9.png">





## Getting started

The project requires Python 3.14.8 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with
`.venv\Scripts\Activate.ps1`.

To run one market, use the registry-driven runner. For example:

```bash
python -m cloud_signal.runners.run_market --market SPX500
python -m cloud_signal.runners.run_market --market MajorETFs --timeframes 1h d
```

Market names, asset lists, output locations, and timeframes are configured in
[`config/markets.toml`](config/markets.toml). See
[`RUNNERS.md`](RUNNERS.md) for all runner options and output details. Running
`python main.py` starts every enabled market scan and the email digest; use it
only when that full workflow is intended.

The Yahoo Finance runners need no API credentials. For OANDA, copy
`.env.example` to `.env` and set `OANDA_ACCESS_TOKEN`; set `OANDA_ACCOUNT_ID`
when using the account instruments endpoint. The practice API is used by
default. The legacy FXCM integration requires `FXCM_ACCESS_TOKEN` and the
optional `fxcmpy` package. Never commit `.env` or put credentials in source
code.

Run the test suite with:

```bash
python -m pip install pytest
python -m pytest -q
```

Scans that fetch large markets such as the S&P 500 can take a while because
they download and process historical data for many symbols.

## Shared cache and scheduled scans

Yahoo OHLC data is cached in `.cache/cloud_signal`, independently of market
directories. Cache entries are keyed by provider, normalized ticker, interval,
adjustment basis, and lookback, so a market can run on its own and still reuse
data from a prior scan. The default cache freshness is 15 minutes for hourly
bars and 6 hours for other intervals. Override it with
`CLOUD_SIGNAL_RAW_CACHE_TTL_SECONDS`; set `CLOUD_SIGNAL_CACHE_DIR` to use a
different local cache directory.

Ichimoku results are keyed by their source-data fingerprint and calculation
version. When source bars change, the runner recalculates from a 104-bar
warm-up before the earliest changed row; the retained prefix is unaffected by
the update. Regression tests compare this incremental result with full-history
recalculation for corrected and appended bars. Market-specific CSV outputs are
still written for existing downstream workflows.

The **Daily Ichimoku Scan** workflow is the only scheduled workflow. It runs
the Hong Kong, UK, and remaining market groups at their existing scan times,
one group at a time, restoring and saving a shared GitHub Actions cache. Use
its manual **Run workflow** market selector to run one market independently
(including `Nas100`) or select `all`.

GitHub Actions caches are immutable, size-limited, and subject to eviction and
retention limits. They provide best-effort reuse between workflow runs, not a
durable shared database; if an entry is unavailable, the scan downloads and
calculates it again.

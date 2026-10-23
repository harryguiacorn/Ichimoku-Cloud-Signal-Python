## Entrypoints & Logs

Runner implementations live under the installable `cloud_signal.runners` package. Lightweight root-level shims and the legacy `scripts` package remain only for backwards compatibility.

- Canonical modules: `cloud_signal/runners/runDJ30.py`, `cloud_signal/runners/runSPX500.py`, etc.
- Major ETF module: `cloud_signal/runners/runMajorETFs.py`.
- Root-level shims: `runDJ30.py`, `runSPX500.py`, `runNas100.py`, `runFTSE100.py`, `runFTSE250.py`, `runFutures.py`, `runHSI.py`, `runKraken.py`, `runBitfinex.py`, `runOanda.py`, `runCurrencyFutures.py`, `runRussell1000.py`, `runSPDR_ETFs.py`, `runDJ30_source_russell.py`, `main.py`

How the shims work
- Each shim imports the corresponding `scripts.<module>` and calls its `main()` when executed as a script. Example shim:
  ```py
  from scripts import runDJ30

  if __name__ == '__main__':
      runDJ30.main()
  ```

Logs
- Logs are written to `output/logs/`.
- Historical `error_log_*.txt` files are retained in `output/logs/archive/` for reference; new runs do not use that archive.
- Each runner uses the bootstrap helper `scripts._bootstrap.setup_runner_logging(...)` to configure a per-run log file named like:
  - `output/logs/<module>_<RUNNER_CLASS>.txt` (for example `runSPX500_GetDataSPX500.txt`)

Run examples (with venv activated)
```powershell
python runDJ30.py
python -m cloud_signal.runners.runSPX500
python -m cloud_signal.runners.runMajorETFs
python -m cloud_signal.runners.run_market --market MajorETFs
cloud-signal-dj30
```

Notes
- Yahoo-enabled runs reuse each symbol's existing raw-data CSV, normalize timestamps to UTC, refresh an overlapping recent window in batches of up to 20 symbols, and merge updated rows. If a batch request fails, the runner retries its symbols individually. The first run for a symbol still downloads the configured lookback; remove its raw-data CSV to force a full refetch.
- The Major ETFs runner processes one symbol at a time and passes its Ichimoku DataFrame through the Cloud, TKx, and Chikou controllers. Each controller also retains standalone file-backed execution; both paths persist the established per-symbol CSV outputs.
- Major ETFs fetches all symbols for a timeframe through the market-data model's batched loader, then processes each symbol from the returned in-memory data. Stage timings for market-data fetch, indicator/signal processing, aggregation, and merging are written to the runner log.
- Signal writers preserve the full per-symbol history CSV and also write a `_latest.csv` sidecar containing its final row. Aggregators use the sidecar when present and fall back to the historical CSV for older data.
- Each runner log includes elapsed time for every controller workflow stage, including symbol fetching, market-data loading, Ichimoku/signal calculation, aggregation, and merging, plus the total market-run duration. Major ETFs also logs its per-timeframe data, calculation, and aggregation phases. Runs remain sequential; use these timings to identify bottlenecks before considering concurrency.
- The dispatcher accepts `--timeframes` to run a subset, for example `python -m cloud_signal.runners.run_market --market SPX500 --timeframes 1h d`. A partial run disables the multi-timeframe merger so it does not consume stale files from skipped timeframes; only per-timeframe outputs are refreshed. Major ETFs uses the same option and logs its stage timings.
- The Flask-based `scripts/index_flask.py` is deprecated and intentionally ignored by smoke tests.
- If you prefer to preserve original git history for a given entrypoint, use `git mv` to relocate that single file out of `scripts/` instead of adding a shim.

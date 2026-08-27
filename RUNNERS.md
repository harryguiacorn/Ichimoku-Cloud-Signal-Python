## Entrypoints & Logs

Runner implementations live under the installable `cloud_signal.runners` package. Lightweight root-level shims and the legacy `scripts` package remain only for backwards compatibility.

- Canonical modules: `cloud_signal/runners/runDJ30.py`, `cloud_signal/runners/runSPX500.py`, etc.
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
cloud-signal-dj30
```

Notes
- The Flask-based `scripts/index_flask.py` is deprecated and intentionally ignored by smoke tests.
- If you prefer to preserve original git history for a given entrypoint, use `git mv` to relocate that single file out of `scripts/` instead of adding a shim.

## Entrypoints & Logs

This project now centralizes runner scripts under the `scripts/` package. Lightweight root-level shims were added to preserve the old CLI entrypoint names.

- Canonical modules: `scripts/runDJ30.py`, `scripts/runSPX500.py`, etc.
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
- Each runner uses the bootstrap helper `scripts._bootstrap.setup_runner_logging(...)` to configure a per-run log file named like:
  - `output/logs/<module>_<RUNNER_CLASS>.txt` (for example `runSPX500_GetDataSPX500.txt`)

Run examples (with venv activated)
```powershell
python runDJ30.py
python scripts\runSPX500.py
```

Notes
- The Flask-based `scripts/index_flask.py` is deprecated and intentionally ignored by smoke tests.
- If you prefer to preserve original git history for a given entrypoint, use `git mv` to relocate that single file out of `scripts/` instead of adding a shim.

"""
DEPRECATED: This module contained hard-coded orchestration settings for market runs.

As of August 2026, all market configuration—including asset lists, timeframes, output paths,
and runtime flags—has been centralized in the registry-driven model:

    - See: config/markets.toml (TOML-based source of truth)
    - See: cloud_signal/runners/market_registry.py (Python registry loader)
    - See: cloud_signal/runners/run_market.py (Generic parametrized runner)

Each market's runtime flags are now stored in the [market.runtime] section of markets.toml.
The registry automatically loads these at startup and passes them to legacy runner modules.

For backward compatibility, all original settings are preserved as module-level constants below.
These are now derived from the registry and serve as fallback defaults only.
"""

from cloud_signal.runners.market_registry import RUNTIME_DEFAULTS

# Legacy module-level constants (deprecated; use registry instead)
# These are automatically populated from RUNTIME_DEFAULTS for backward compatibility


def _populate_legacy_constants():
    """Populate module-level flags from the registry for backward compatibility."""
    for market_name, runtime_flags in RUNTIME_DEFAULTS.items():
        for flag_name, flag_value in runtime_flags.items():
            globals()[flag_name] = flag_value


_populate_legacy_constants()
del _populate_legacy_constants

"""Compatibility alias for the packaged Dow Jones controller."""

import pandas as pd

from cloud_signal.mvc.controllers.GetSymbolDowJones30 import Model, requests

__all__ = ["Model", "pd", "requests"]

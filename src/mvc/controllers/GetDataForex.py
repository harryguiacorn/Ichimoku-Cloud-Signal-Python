# NOTE: fxcmpy connection happens at import time here; preserve behavior but log instead of printing
import fxcmpy
import logging

logger = logging.getLogger(__name__)

TOKEN = "921d339a2c07207b682273693bd0668dfb1c1287"
con = fxcmpy.fxcmpy(access_token=TOKEN, log_level="error")
instruments = con.get_instruments()
logger.info("Sample instruments: %s", instruments[:5])
# ['EUR/USD', 'USD/JPY', 'GBP/USD', 'USD/CHF', 'EUR/CHF']

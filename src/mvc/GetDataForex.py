import fxcmpy 
TOKEN = "921d339a2c07207b682273693bd0668dfb1c1287"
con = fxcmpy.fxcmpy(access_token = TOKEN, log_level = 'error')
instruments = con.get_instruments()
print(instruments[:5]) 
# ['EUR/USD', 'USD/JPY', 'GBP/USD', 'USD/CHF', 'EUR/CHF']

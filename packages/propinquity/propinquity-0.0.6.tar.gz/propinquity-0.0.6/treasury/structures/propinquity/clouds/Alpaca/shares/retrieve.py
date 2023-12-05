
'''
	import propinquity.clouds.Alpaca.shares.retrieve as retrieve_Alpaca_shares
	retrieve_Alpaca_shares.wonderfully ()
'''



import datetime
import json

from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame

def wonderfully ():
	client = CryptoHistoricalDataClient ()

	span = [
		datetime.datetime (2023, 11, 28),
		datetime.datetime (2023, 12, 2)
	]

	interval = TimeFrame.Day

	request_params = CryptoBarsRequest (
		symbol_or_symbols = ["BTC/USD"],
		timeframe = interval,
		start = span [0],
		end = span [1]
	)

	Alpaca_bars = client.get_crypto_bars (request_params)

	return Alpaca_bars
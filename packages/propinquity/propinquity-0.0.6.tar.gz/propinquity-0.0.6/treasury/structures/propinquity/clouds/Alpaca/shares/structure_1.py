

'''
	import propinquity.clouds.Alpaca.shares.structure_1 as structure_1
	shares = structure_1.calculate ()
'''

import datetime
import json

from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame

import propinquity.clouds.Alpaca.shares.retrieve as retrieve_Alpaca_shares
	
import botany	
	
def calculate ():
	Alpaca_bars = retrieve_Alpaca_shares.wonderfully ()
	Alpaca_df_JSON = json.loads (Alpaca_bars.df.to_json (orient = "split"))

	print (Alpaca_bars.df)
	botany.show (Alpaca_df_JSON)

	columns = Alpaca_df_JSON ["columns"]
	index = Alpaca_df_JSON ["index"]
	data = Alpaca_df_JSON ["data"]
	
	proceeds = []
	
	s = 0;
	last_interval_index = len (index) - 1;
	last_column_index = len (columns) - 1;
	
	while s <= last_interval_index:
		u_timestamp_with_ms = index [s][1]
		u_timestamp = str (index [s][1]) [:-3]
		date_string = datetime.datetime.utcfromtimestamp (int (u_timestamp)).strftime('%Y-%m-%d %H:%M:%S')
	
		'''
			1701151200000
			print (datetime.datetime.utcfromtimestamp (int ('1701151200')).strftime('%Y-%m-%d %H:%M:%S'))
		'''
		interval = {
			"date string": date_string,
			"u timestamp": u_timestamp,
		}
		
		s2 = 0
		while s2 <= last_column_index:
			interval [columns [ s2 ]] = data [s][s2]
	
			s2 += 1
	
		proceeds.append (interval)
		s += 1

	return proceeds
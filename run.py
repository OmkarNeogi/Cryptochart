from models.cryptocurrency_model import CryptocurrencyModel

def init_collection_and_populate(crypto_model):
	from requests import get as requests_get
	import datetime
	import numpy
	import pprint

	start_date = "2017-11-01"
	end_date = datetime.datetime.now().strftime("%Y-%m-%d")
	coindesk_url = "https://api.coindesk.com/v1/bpi/historical/close.json?start="+start_date+"&end="+end_date
	# coindesk_url = "https://api.coindesk.com/v1/bpi/historical/close.json"

	coindesk_response = requests_get(coindesk_url)
	mixed = [(date, coindesk_response.json()['bpi'][date]) for date in coindesk_response.json()['bpi']]
	
	todays_date = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d")

	n = 15
	prev = None
	sma_15 = []
	smma = None
	current_sum = 0

	gain_sum, loss_sum = 0, 0
	avg_gain, avg_loss = 0, 0
	rsi = []
	c = 0
	for index in range(len(mixed)):
		result_smma, result_rsi = None, None

		if index < (n-1):
			current_sum += mixed[index][1]
		if index == (n-1):
			prev = current_sum
			smma = prev / index
		elif index > (n-1):
			prev = prev - smma + mixed[index][1]
			smma = prev / n
		if smma:
			result_smma = smma
			# sma_15.append((mixed[index][0], smma))
		# SMMA link: www.20minutetraders.com/learning/moving_averages/smooth-moving-average.php

		
		if index < 14:
			if index == 0:
				continue
			difference = mixed[index][1] - mixed[index-1][1]
			if difference > 0:
				gain_sum += difference
			elif difference < 0:
				loss_sum += abs(difference)
		elif index == 14:
			difference = mixed[index][1] - mixed[index-1][1]
			if difference > 0:
				gain_sum += difference
			elif difference < 0:
				loss_sum += abs(difference)

			avg_gain = gain_sum / 14
			avg_loss = loss_sum / 14

			rs = avg_gain / avg_loss

			result_rsi = 100 - 100 / (1 + rs)
			# rsi.append((mixed[index][0], result_rsi))
		else:
			difference = mixed[index][1] - mixed[index-1][1]
			current_gain = max(difference, 0)
			current_loss = abs(min(difference, 0))
			avg_gain = ((avg_gain * 13) + current_gain) / 14
			avg_loss = ((avg_loss * 13) + current_loss) / 14

			rs = avg_gain / avg_loss
			result_rsi = 100 - 100 / (1 + rs)
			rsi.append((mixed[index][0], result_rsi))
		document = {
			'date_of_price': datetime.datetime.strptime(mixed[index][0], "%Y-%m-%d"),
			'date_string': mixed[index][0],
			'price': mixed[index][1],
			'smma': {
				'granularity': 15,
				'unit': 'day',
				'value': result_smma
			},
			'rsi': result_rsi,
			'updated_at': todays_date
		}
		# pprint.pprint(document)

		query = {'fixed_data.date_of_price':datetime.datetime.strptime(mixed[index][0], "%Y-%m-%d")}
		crypto_model.upsert(query, {"fixed_data": document})


def main():
	crypto_model = CryptocurrencyModel('btc')
	init_collection_and_populate(crypto_model)

if __name__ == "__main__":
	main()
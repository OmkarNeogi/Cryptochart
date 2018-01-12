from models.cryptocurrency_model import CryptocurrencyModel

def init_collection_and_populate(crypto_model):
	from requests import get as requests_get
	import datetime
	import numpy
	import pprint
	import matplotlib
	matplotlib.use('TkAgg')
	import matplotlib.pyplot as plt

	start_date = "2017-12-11"
	end_date = datetime.datetime.now().strftime("%Y-%m-%d")
	coindesk_url = "https://api.coindesk.com/v1/bpi/historical/close.json?start="+start_date+"&end="+end_date
	# coindesk_url = "https://api.coindesk.com/v1/bpi/historical/close.json"

	coindesk_response = requests_get(coindesk_url)
	# print(coindesk_response.json())

	todays_date = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d")

	prices = [coindesk_response.json()['bpi'][date] for date in coindesk_response.json()['bpi']]
	dates = [date for date in coindesk_response.json()['bpi']]

	mixed = [(date, coindesk_response.json()['bpi'][date]) for date in coindesk_response.json()['bpi']]
	# pprint.pprint(mixed)
	
	n = 15
	prev = None
	sma_15 = []
	smma = None
	current_sum = 0

	prev_value = None
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
			sma_15.append((mixed[index][0], smma))
		# SMMA link: www.20minutetraders.com/learning/moving_averages/smooth-moving-average.php

		if index < 13:
			if index == 0:
				continue
			difference = mixed[index-1][1] - mixed[index][1]
			if difference < 0:
				gain_sum += difference
			elif difference > 0:
				loss_sum += difference
		elif index == 13:
			avg_loss = loss_sum / 14
			avg_gain = gain_sum / 14

			rs = avg_gain / avg_loss
			result_rsi = 100 - 100 / (1 + rs)
			rsi.append((mixed[index][0], result_rsi))
			print('equal ', mixed[index])
		else:
			difference = mixed[index][1] - mixed[index-1][1]
			current_gain = max(difference, 0)
			current_loss = abs(min(difference, 0))
			avg_gain = avg_gain * 13 + mixed[index][1] + current_gain
			avg_loss = avg_loss * 13 + mixed[index][1] + current_loss

			rs = avg_gain / avg_loss
			result_rsi = 100 - 100 / (1 + rs)
			rsi.append((mixed[index][0], result_rsi))
			print(mixed[index])
		if c > 30:
			break
		c += 1
		prev_value = mixed[index][1]

	# print(sma_15)
	# plt.plot(dates, prices)
	# new_dates = [item[0] for item in sma_15]
	# new_rates = [item[1] for item in sma_15]
	# plt.plot(new_dates, new_rates)

	rsi_dates = [item[0] for item in rsi]
	rsi_values = [item[1] for item in rsi]
	print('\n\n')
	pprint.pprint(rsi)
	# plt.plot(rsi_dates, rsi_values)
	# plt.show()



	# for date in coindesk_response.json()['bpi']:
	# 	price = coindesk_response.json()['bpi'][date]

	# 	main_data_struct.append(document)

	# document = {
	# 	'date_of_price': datetime.datetime.strptime(date, "%Y-%m-%d"),
	# 	'price': price,
	# 	'updated_at': todays_date
	# }


def perform_analyses(crypto_model):
	import numpy
	import pprint

	last_31_dats_data = crypto_model.get_last_n_days_data(31)
	input_date = [(item['price'], item['date_of_price']) for item in last_31_dats_data]




def main():
	crypto_model = CryptocurrencyModel('btc')
	init_collection_and_populate(crypto_model)
	# perform_analyses(crypto_model)

if __name__ == "__main__":
	main()
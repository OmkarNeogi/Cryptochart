class CryptocurrencyModel:
	def __init__(self, currency_name):
		from pymongo import MongoClient
		import json

		MONGODB_URI = json.load(open('api_keys.json'))['mongodb']['MONGODB_URI']
		client = MongoClient(MONGODB_URI)
		# Obscure this before uploading or make private repo.

		self.db = client.get_database('cryptochart')
		self.collection_name = currency_name
		self.collection = self.db[currency_name]

	def insert(self, document):
		# UNIT TESTED. PUTS RECORDS INTO MONGO INDIVIDUALLY (not insert_many())
		response = self.collection.insert_one(document)
		return response

	def upsert(self, query, document):
		response = self.collection.update(query, document, upsert=True)
		return response

	def query_one(self, where, select=None):
		# UNIT TESTED. 
		if select:
			return self.collection.find_one(where)
		else:
			return self.collection.find_one(where, select)

	def query_many(self, where, select=None):
		# UNIT TESTED.
		result = []
		if select:
			response = self.collection.find(where, select)
			for row in response:
				result.append(row)
		else:
			response = self.collection.find(where)
			for row in response:
				result.append(row)
		return result


	def get_last_n_days_data(self, n):
		''' 
		UNIT TESTED
		'''
		import datetime

		def get_current_date_in_correct_format():
			return datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
		start_date = get_current_date_in_correct_format()

		result = []

		date_N_days_ago = start_date - datetime.timedelta(days=n)
		for cursor in self.collection.find({'fixed_data.date_of_price':{"$gte": date_N_days_ago}}, {'fixed_data':1, '_id':0}):
			result.append(cursor['fixed_data'])
		return result
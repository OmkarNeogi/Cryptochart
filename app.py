from flask import Flask, jsonify
import datetime
from models.cryptocurrency_model import CryptocurrencyModel

app = Flask(__name__)

@app.route('/chart/<string:currency>', methods=["GET"])
def get_last_n_days_charts(currency):
	cryptocurrency_model = CryptocurrencyModel(currency)
	response = cryptocurrency_model.get_last_n_days_data(5)
	return jsonify({'data':response})

app.run(debug=True)
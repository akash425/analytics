from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from queries import top_5_products, monthly_revenue, avg_sales_by_category_subcategory, yearly_sales_with_growth

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')

app = Flask(__name__)

# MongoDB connection at module level
client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True)
db = client['ecom_db']
collection = db['orders']

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "API ready. Try /api/top-products"})

@app.route('/api/top-products', methods=['GET'])
def get_top_products():
    """Top 5 products by total sales"""
    try:
        results = top_5_products(collection)
        return jsonify({"data": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/monthly-revenue', methods=['GET'])
def get_monthly_revenue():
    try:
        results = monthly_revenue(collection)
        return jsonify({"data": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/avg-sales', methods=['GET'])
def get_avg_sales():
    try:
        results = avg_sales_by_category_subcategory(collection)
        return jsonify({"data": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/yearly-growth', methods=['GET'])
def get_yearly_growth():
    try:
        results = yearly_sales_with_growth(collection)
        return jsonify({"data": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5008)


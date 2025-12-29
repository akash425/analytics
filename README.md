# E-commerce Analytics with MongoDB

A Python project for loading and analyzing e-commerce order data using MongoDB and PyMongo.

## Features

- Load CSV order data into MongoDB
- Run analytics queries on order data
- Calculate top products, monthly revenue, category averages, and yearly growth

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root:
```
MONGO_URI=mongodb://localhost:27017/
```
Or use your MongoDB Atlas connection string.

3. Ensure `data/orders.csv` exists with your order data.

## Usage

### Load Data
Load orders from CSV into MongoDB:
```bash
python3 load_orders.py
```

### Run Analytics
Execute all analytics queries:
```bash
python3 queries.py
```

### Individual Queries
- `top_products.py` - Top 5 products by total sales
- `monthly_revenue.py` - Monthly revenue across all years
- `avg_sales_by_category.py` - Average sales by category and subcategory
- `yearly_sales_growth.py` - Yearly sales with growth percentage

## Project Structure

```
analytics/
├── data/
│   └── orders.csv          # Order data file
├── load_orders.py           # Load CSV into MongoDB
├── mongo_connect.py         # MongoDB connection setup
├── queries.py              # Main script to run all queries
├── top_products.py         # Top 5 products query
├── monthly_revenue.py      # Monthly revenue query
├── avg_sales_by_category.py # Category averages query
├── yearly_sales_growth.py  # Yearly growth query
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Database

- Database: `ecom_db`
- Collection: `orders`

## Requirements

- Python 3.7+
- MongoDB (local or Atlas)
- pandas
- pymongo
- python-dotenv


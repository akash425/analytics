# E-commerce Analytics with MongoDB

A Python project for loading and analyzing e-commerce order data using MongoDB and PyMongo. Includes both command-line analytics and a REST API.

## Features

- Load CSV order data into MongoDB
- Run analytics queries on order data
- Calculate top products, monthly revenue, category averages, and yearly growth
- REST API endpoints for accessing analytics data

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

### Run Analytics (Command Line)
Execute all analytics queries:
```bash
python3 queries.py
```

This will run all four analytics queries and display the results:
- **Top 5 Products** - Products with highest total sales
- **Monthly Revenue** - Total revenue per month across all years
- **Average Sales by Category** - Average sales grouped by category and subcategory
- **Yearly Sales Growth** - Yearly sales totals with year-over-year growth percentage

### REST API
Start the Flask API server:
```bash
python3 app.py
```

The API will run on `http://0.0.0.0:5008` (or `http://localhost:5008`).

#### API Endpoints

- `GET /` - API status message
- `GET /api/top-products` - Top 5 products by total sales
- `GET /api/monthly-revenue` - Monthly revenue across all years
- `GET /api/avg-sales` - Average sales by category and subcategory
- `GET /api/yearly-growth` - Yearly sales with growth percentage

All endpoints return JSON responses with a `data` field containing the query results.

Example:
```bash
curl http://localhost:5008/api/top-products
```

## Project Structure

```
analytics/
├── data/
│   └── orders.csv          # Order data file
├── load_orders.py           # Load CSV into MongoDB
├── mongo_connect.py         # MongoDB connection setup
├── queries.py              # All analytics query functions
├── app.py                  # Flask REST API server
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Analytics Queries

All queries are defined in `queries.py`:

- `top_5_products(collection)` - Returns top 5 products by total sales
- `monthly_revenue(collection)` - Returns total revenue per month
- `avg_sales_by_category_subcategory(collection)` - Returns average sales by category/subcategory
- `yearly_sales_with_growth(collection)` - Returns yearly sales with YoY growth percentage

## Database

- Database: `ecom_db`
- Collection: `orders`

## Requirements

- Python 3.7+
- MongoDB (local or Atlas)
- pandas>=2.0.0
- pymongo>=4.0.0
- python-dotenv>=1.0.0
- flask (for API server)

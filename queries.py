import pymongo
import os
from dotenv import load_dotenv


def top_5_products(collection):
    """Get top 5 products by total sales."""
    # $group: Group by Product ID, sum Sales as total_sales
    pipeline = [
        {"$group": {"_id": "$Product ID", "total_sales": {"$sum": "$Sales"}}},
        # $sort: Sort descending by total_sales
        {"$sort": {"total_sales": -1}},
        # $limit: Get top 5 only
        {"$limit": 5},
        # $project: Select product_id and rounded total_sales, exclude _id
        {"$project": {"_id": 0, "product_id": "$_id", "total_sales": {"$round": ["$total_sales", 2]}}}
    ]
    
    # Execute aggregation and return results
    results = list(collection.aggregate(pipeline))
    for item in results:
        print(f"Product ID: {item['product_id']}, Total: ${item['total_sales']:.2f}")
    return results


def monthly_revenue(collection):
    """Calculate total sales revenue per month across all years."""
    pipeline = [
        # Extract year and month from Order Date using $year and $month
        {"$addFields": {"year": {"$year": "$Order Date"}, "month": {"$month": "$Order Date"}}},
        # Group by year and month, sum Sales as total_revenue
        {"$group": {"_id": {"year": "$year", "month": "$month"}, "total_revenue": {"$sum": "$Sales"}}},
        # Sort ascending by year then month
        {"$sort": {"_id.year": 1, "_id.month": 1}},
        # Project: Create YYYY-MM string using $dateToString with $dateFromParts, round total_revenue
        {
            "$project": {
                "_id": 0,
                "month_year": {
                    "$dateToString": {
                        "format": "%Y-%m",
                        "date": {"$dateFromParts": {"year": "$_id.year", "month": "$_id.month", "day": 1}}
                    }
                },
                "total_revenue": {"$round": ["$total_revenue", 2]}
            }
        }
    ]
    
    # Execute aggregation and return results
    results = list(collection.aggregate(pipeline))
    for item in results:
        print(f"{item['month_year']}: ${item['total_revenue']:.2f}")
    return results


def avg_sales_by_category_subcategory(collection):
    """Calculate average sales by category and sub-category."""
    pipeline = [
        # $group: Group by Category and Sub-Category, calculate average Sales
        {"$group": {"_id": {"category": "$Category", "subcategory": "$Sub-Category"}, "avg_sales": {"$avg": "$Sales"}}},
        # $sort: Sort ascending by category then subcategory
        {"$sort": {"_id.category": 1, "_id.subcategory": 1}},
        # $project: Select category, subcategory, rounded avg_sales, exclude _id
        {"$project": {"_id": 0, "category": "$_id.category", "subcategory": "$_id.subcategory", "avg_sales": {"$round": ["$avg_sales", 2]}}}
    ]
    
    # Execute aggregation and return results
    results = list(collection.aggregate(pipeline))
    for item in results:
        print(f"{item['category']} > {item['subcategory']}: ${item['avg_sales']:.2f}")
    return results


def yearly_sales_with_growth(collection):
    """Calculate total sales per year and year-over-year growth percentage."""
    # Aggregation pipeline: Group by year, sum Sales, sort ascending
    pipeline = [
        {"$group": {"_id": {"$year": "$Order Date"}, "total_sales": {"$sum": "$Sales"}}},
        {"$sort": {"_id": 1}}
    ]
    
    # Execute aggregation to get yearly sales data
    yearly_data = list(collection.aggregate(pipeline))
    
    # Calculate growth in Python (easier than complex MongoDB expressions)
    results = []
    prev_sales = None
    
    for item in yearly_data:
        year = item["_id"]
        sales = round(item["total_sales"], 2)
        
        # Calculate growth: ((current - prev) / prev) * 100
        if prev_sales is not None:
            growth = ((sales - prev_sales) / prev_sales) * 100
        else:
            growth = 0  # First year has no previous year to compare
        
        results.append({
            "year": year,
            "total_sales": sales,
            "growth_percent": round(growth, 2)
        })
        
        # Print formatted output
        if prev_sales is not None:
            print(f"Year {year}: ${sales:.2f}, Growth: {growth:.1f}%")
        else:
            print(f"Year {year}: ${sales:.2f}, Growth: N/A")
        
        prev_sales = sales
    
    return results


if __name__ == "__main__":
    # Connect to MongoDB
    load_dotenv()
    uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    client = pymongo.MongoClient(uri, tlsAllowInvalidCertificates=True)
    db = client['ecom_db']
    collection = db['orders']
    
    # Run all query functions
    top_5_products(collection)
    print("\n" + "="*40 + "\n")
    
    monthly_revenue(collection)
    print("\n" + "="*40 + "\n")
    
    avg_sales_by_category_subcategory(collection)
    print("\n" + "="*40 + "\n")
    
    yearly_sales_with_growth(collection)
    
    client.close()

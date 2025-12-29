import pymongo

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


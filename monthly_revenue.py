import pymongo

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


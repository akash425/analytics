import pymongo

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


import pymongo

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


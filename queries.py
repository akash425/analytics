import pymongo
import os
from dotenv import load_dotenv
from top_products import top_5_products
from monthly_revenue import monthly_revenue
from avg_sales_by_category import avg_sales_by_category_subcategory
from yearly_sales_growth import yearly_sales_with_growth

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


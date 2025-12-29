import pandas as pd
import pymongo
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')

def load_orders_to_mongodb():
    """Load orders.csv into MongoDB collection."""
    try:
        # Connect to MongoDB (with SSL support for Atlas)
        client = pymongo.MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True)
        db = client['ecom_db']
        collection = db['orders']
        
        # Read CSV and convert 'Order Date' to datetime (DD/MM/YYYY format)
        df = pd.read_csv('data/orders.csv')
        df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
        
        # Print row count before insertion
        row_count = len(df)
        print(f"Rows in CSV: {row_count}")
        
        # Drop collection if it exists
        if collection.name in db.list_collection_names():
            collection.drop()
            print("Dropped existing 'orders' collection")
        
        # Convert DataFrame to dicts and insert into MongoDB
        orders_dict = df.to_dict('records')
        result = collection.insert_many(orders_dict)
        print(f"Inserted {len(result.inserted_ids)} documents into MongoDB")
        
        client.close()
    except pymongo.errors.ConnectionFailure as e:
        print(f"Error connecting to MongoDB: {e}")
    except FileNotFoundError:
        print("Error: 'data/orders.csv' file not found")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    load_orders_to_mongodb()


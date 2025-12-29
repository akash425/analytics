import pymongo
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()
uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')

# Connect to MongoDB
client = pymongo.MongoClient(uri, tlsAllowInvalidCertificates=True)
db = client['ecom_db']
coll = db['orders']

if __name__ == "__main__":
    print(f"Connected to {db.name}.{coll.name}")
    client.close()


# analyzeDB.py
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import json
from bson import ObjectId
from datetime import datetime


# Class for converting ObjectId to JSON
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return super(JSONEncoder, self).default(obj)


# Load environment variables from .env file
load_dotenv()

# URI from .env file
uri = os.environ.get('DB_URI', 'mongodb://localhost:27017/')

# Create connection to MongoDB server
client = MongoClient(uri, server_api=ServerApi('1'))

# Connect to database
db = client['yoga_spot_db']


def print_collection_data(collection_name):
    """
    Print all data from a specified collection
    """
    print(f"\n--- Collection: {collection_name} ---\n")

    collection = db[collection_name]
    data = list(collection.find())

    if not data:
        print(f"No data found in {collection_name} collection")
        return

    # Print number of documents
    print(f"Total documents: {len(data)}\n")

    # Print each document in formatted JSON
    for doc in data:
        json_str = json.dumps(doc, indent=2, cls=JSONEncoder)
        print(json_str)
        print("-" * 50)


def main():
    """
    Main function - prints all collections and their data
    """
    print("\n=== MongoDB Database Analysis ===\n")

    # Get list of collections
    collections = db.list_collection_names()

    print(f"Database: yoga_spot_db")
    print(f"Total collections: {len(collections)}")
    print(f"Collections: {', '.join(collections)}\n")

    # Print data from each collection
    for collection_name in collections:
        print_collection_data(collection_name)


if __name__ == "__main__":
    # Test database connection
    try:
        client.admin.command('ping')
        print("MongoDB connection successful!")

        # Run main function
        main()

    except Exception as e:
        print(f"MongoDB connection error: {e}")

    finally:
        # Close connection
        client.close()
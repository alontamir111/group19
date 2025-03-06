# analyzeDB.py
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import json
from bson import ObjectId
from datetime import datetime


# מחלקה להמרת ObjectId ל-JSON
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return super(JSONEncoder, self).default(obj)


# טעינת משתני סביבה מקובץ .env
load_dotenv()

# URI מקובץ .env
uri = os.environ.get('DB_URI', 'mongodb://localhost:27017/')

# יצירת התחברות לשרת MongoDB
client = MongoClient(uri, server_api=ServerApi('1'))

# התחברות למסד הנתונים
db = client['yoga_spot_db']


def print_collection_data(collection_name):
    """
    הדפסת כל הנתונים מאוסף מסוים
    """
    print(f"\n--- Collection: {collection_name} ---\n")

    collection = db[collection_name]
    data = list(collection.find())

    if not data:
        print(f"No data found in {collection_name} collection")
        return

    # הדפסת מספר המסמכים
    print(f"Total documents: {len(data)}\n")

    # הדפסת כל מסמך בפורמט JSON מסודר
    for doc in data:
        json_str = json.dumps(doc, indent=2, cls=JSONEncoder)
        print(json_str)
        print("-" * 50)


def main():
    """
    פונקציה ראשית - מדפיסה את כל האוספים והנתונים שלהם
    """
    print("\n=== MongoDB Database Analysis ===\n")

    # קבלת רשימת האוספים
    collections = db.list_collection_names()

    print(f"Database: yoga_spot_db")
    print(f"Total collections: {len(collections)}")
    print(f"Collections: {', '.join(collections)}\n")

    # הדפסת נתונים מכל אוסף
    for collection_name in collections:
        print_collection_data(collection_name)


if __name__ == "__main__":
    # בדיקת חיבור למסד הנתונים
    try:
        client.admin.command('ping')
        print("MongoDB connection successful!")

        # הרצת הפונקציה הראשית
        main()

    except Exception as e:
        print(f"MongoDB connection error: {e}")

    finally:
        # סגירת החיבור
        client.close()
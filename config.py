from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError

MONGO_URI = "mongodb+srv://tanishasinghamrita2003_db_user:Tanisha1233@cluster0.3nl8vth.mongodb.net/?appName=cluster0"

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")  # Test the connection immediately
    print("✅ Connected to MongoDB successfully!")
except ConfigurationError as e:
    print(f"❌ Configuration error (check your URI): {e}")
    raise
except ConnectionFailure as e:
    print(f"❌ Could not connect to MongoDB (check network/IP whitelist): {e}")
    raise

db = client["rakshai_db"]
sos_collection = db["sos_logs"]
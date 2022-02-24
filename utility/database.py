from pymongo import MongoClient
from dotenv import load_dotenv
import os

# load .env file
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# connection with the databse
client = MongoClient(MONGO_URI)
db = client.miniurl
collection = db.urls


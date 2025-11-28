from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["ai_girlfriend_bot"]

users = db["users"]
chats = db["chat_history"]
settings = db["settings"]

# Init settings if not exists
if settings.count_documents({}) == 0:
    settings.insert_one({
        "_id": "config",
        "gf_name": "Aarohi",
        "ai_enabled": True
    })

def get_settings():
    return settings.find_one({"_id": "config"})

def update_gf_name(name):
    settings.update_one({"_id": "config"}, {"$set": {"gf_name": name}})

def update_ai_status(status: bool):
    settings.update_one({"_id": "config"}, {"$set": {"ai_enabled": status}})

def save_user(user):
    users.update_one(
        {"user_id": user.id},
        {
            "$set": {
                "username": user.username,
                "first_name": user.first_name
            }
        },
        upsert=True
    )

def save_chat(user_id, user_msg, bot_msg):
    chats.insert_one({
        "user_id": user_id,
        "user": user_msg,
        "bot": bot_msg
    })

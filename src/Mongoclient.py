from pymongo import MongoClient
import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["echomind_db"]

def add_user(user):
    collection = db["users"]
    inserted_id = collection.insert_one(user).inserted_id
    print(f"Inserted Successfully with ID: {inserted_id}")

def find_user(chat_id):
    collection = db["users"]
    result = collection.find_one({"chat_id":chat_id});
    print(f"Found user: {result}")
    return result

def add_chat_history(chat_id, user_input, bot_reply):
    chat_history_item = {
        "chat_id": chat_id,
        "user_input": user_input,
        "bot_reply": bot_reply,
        "timestamp": datetime.datetime.now()
    }
    collection = db["chat_history"]
    inserted_id = collection.insert_one(chat_history_item).inserted_id
    print(f"Chat item Inserted Successfully with ID: {inserted_id}")

def add_file_details(filename, description):
    file_detail_item = {
        "filename": filename,
        "description": description,
        "timestamp": datetime.datetime.now()
    }
    collection = db["file_details"]
    inserted_id = collection.insert_one(file_detail_item).inserted_id
    print(f"File detail item Inserted Successfully with ID: {inserted_id}")
    

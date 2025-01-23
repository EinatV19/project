from pymongo import MongoClient

# Connect to MongoDB server on localhost
client = MongoClient('mongodb://localhost:27017/')

# Connect to the database (if it doesn't exist, it will be created automatically)
db = client['classroom']

# Connect to the "users" collection (if it doesn't exist, it will be created automatically)
users_collection = db['users']

# Data to insert into the "users" collection
users_data = [
    {"name": "John Doe", "mail": "john.doe@example.com", "password": "hashedpassword1", "role": "student"},
    {"name": "Jane Smith", "mail": "jane.smith@example.com", "password": "hashedpassword2", "role": "teacher"},
    {"name": "Alice Johnson", "mail": "alice.johnson@example.com", "password": "hashedpassword3", "role": "student"},
    {"name": "Bob Brown", "mail": "bob.brown@example.com", "password": "hashedpassword4", "role": "teacher"},
    {"name": "Charlie Green", "mail": "charlie.green@example.com", "password": "hashedpassword5", "role": "student"}
]

# Insert the data into the "users" collection
users_collection.insert_many(users_data)

# Confirm data insertion
print("5 users have been inserted into the 'users' collection.")

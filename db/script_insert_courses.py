from pymongo import MongoClient

# Connect to MongoDB server on localhost
client = MongoClient('mongodb://localhost:27017/')

# Connect to the database (same database as before)
db = client['classroom']

# Connect to the "courses" collection (it will be created if it doesn't exist)
courses_collection = db['courses']

# Data to insert into the "courses" collection
# For this example, we're referencing existing teacher emails from the "users" collection
courses_data = [
    {"name": "Mathematics 101", "subject": "Mathematics", "teacher_mail": "jane.smith@example.com"},
    {"name": "Physics 101", "subject": "Physics", "teacher_mail": "bob.brown@example.com"},
    {"name": "History 101", "subject": "History", "teacher_mail": "jane.smith@example.com"},
    {"name": "Biology 101", "subject": "Biology", "teacher_mail": "bob.brown@example.com"},
    {"name": "Chemistry 101", "subject": "Chemistry", "teacher_mail": "jane.smith@example.com"}
]

# Insert the data into the "courses" collection
courses_collection.insert_many(courses_data)

# Confirm data insertion
print("5 courses have been inserted into the 'courses' collection.")

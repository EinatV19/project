from pymongo import MongoClient

def get_courses_by_teacher(teacher_mail):
    # Connect to MongoDB server (localhost)
    client = MongoClient('mongodb://localhost:27017/')

    # Connect to the school database
    db = client['classroom']

    # Connect to the "courses" collection
    courses_collection = db['courses']

    # Query to find all courses where teacher_mail matches the provided email
    teacher_courses = courses_collection.find({"teacher_mail": teacher_mail})

    # Return the list of courses (convert the cursor to a list for easier use)
    return list(teacher_courses)

# Example usage
teacher_mail = "bob.brown@example.com"
courses = get_courses_by_teacher(teacher_mail)

# Print the courses
for course in courses:
    print(course)

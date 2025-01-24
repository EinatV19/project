from pymongo import MongoClient


def check_user(mail,password):
    # Connect to MongoDB server (localhost)
    client = MongoClient('mongodb://localhost:27017/')

    # Connect to the school database
    db = client['classroom']

    # Connect to the "users" collection
    users_collection = db['users']

    # Query to check if mail and password combination exists
    user = users_collection.find_one({"mail": mail, "password": password})

    if user:
        return True, "Login Successful"
    else:
        return False, "Invalid email or password"  # Error message    return x
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
# teacher_mail = "bob.brown@example.com"
# courses = get_courses_by_teacher(teacher_mail)
#
# # Print the courses
# for course in courses:
#     print(course)

bool, msg = check_user("john.doe@example.com","hashedpassword1")

if (bool):
    print(msg)
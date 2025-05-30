import base64
from bson import  ObjectId, Binary
from pymongo import MongoClient

# Connect to MongoDB once when the module is loaded
def connect_to_db():
    """Connects to MongoDB and returns the database instance."""
    client = MongoClient("mongodb://localhost:27017/")
    db = client["classroom"]
    return db

# Get the database instance
db = connect_to_db()

print("db connected")
users_collection = db["users"]  # Users collection
courses_collection = db["courses"]  # Courses collection

# LOGIN
def check_user(mail, password):
    """Check if a user exists in the database."""
    user = users_collection.find_one({"mail": mail, "password": password})
    if user:
        return '{"status":"success", "message": "Login successful!"}'
    return '{"status":"fail", "message": "Invalid"}'

# REGISTER
def register_user(mail, password):
    existing_user = users_collection.find_one({"mail": mail})
    if existing_user:
        return '{"status":"fail", "message": "User already exists"}'

    # אם המשתמש לא קיים, נרשום אותו במסד הנתונים
    users_collection.insert_one({"mail": mail, "password": password})
    return  '{"status":"success", "message":"Registration successful"}'

def add_course(course_details):

    # Insert the course into MongoDB
    result = courses_collection.insert_one(course_details)

    if result.inserted_id:
        return {"status": "success", "message": "Course added successfully", "course_id": str(result.inserted_id)}
    else:
        return {"status": "fail", "message": "Failed to add course"}


def serialize_course(course):
    """Convert MongoDB course document into a JSON-friendly format."""
    course["_id"] = str(course["_id"])  # Convert ObjectId to string

    # Convert tasks list (if exists)
    if "tasks" in course:
        for task in course["tasks"]:
            if "file_data" in task and isinstance(task["file_data"], bytes):
                task["file_data"] = base64.b64encode(task["file_data"]).decode("utf-8")  # Convert to Base64

    return course


def get_courses_by_user(user_email):
    """Fetch all courses where the user is a teacher or a student."""
    try:
        teacher_courses = list(courses_collection.find({"teacher_mail": user_email}))
        student_courses = list(courses_collection.find({"students": user_email}))

        # Convert documents to JSON-friendly format
        teacher_courses = [serialize_course(course) for course in teacher_courses]
        student_courses = [serialize_course(course) for course in student_courses]

        return {
            "status": "success",
            "teacher_courses": teacher_courses,
            "student_courses": student_courses
        }
    except Exception as e:
        return {"status": "fail", "message": str(e)}


def add_student_to_course(course_details):
    """
    Adds a student to the 'students' list of a course.

    :param course_details: Dictionary with 'id' (course_id) and 'student_mail' (email).
    :return: JSON response indicating success or failure.
    """
    try:
        course_id = course_details.get("course_id")  # Course ID as string
        student_mail = course_details.get("student_mail")  # Student email

        if not course_id or not student_mail:
            return {"status": "fail", "message": "Missing course ID or student email."}

        # Convert course_id to ObjectId (MongoDB format)
        course_object_id = ObjectId(course_id)

        # Check if course exists
        course = courses_collection.find_one({"_id": course_object_id})
        if not course:
            return {"status": "fail", "message": "Course not found."}

        # Add student to 'students' list (if not already added)
        update_result = courses_collection.update_one(
            {"_id": course_object_id},
            {"$addToSet": {"students": student_mail}}  # $addToSet prevents duplicates
        )

        if update_result.modified_count > 0:
            return {"status": "success", "message": "Student added to course."}
        else:
            return {"status": "fail", "message": "Student is already in the course."}

    except Exception as e:
        return {"status": "fail", "message": f"Error: {str(e)}"}

def add_task_to_course(task):
    """
    Adds a new task to a course document in MongoDB.
    :param task: Dictionary containing task details.
    """

    # Convert course_id from string to ObjectId
    course_id = ObjectId(task["course_id"])

    # Prepare task dictionary
    new_task = {
        "task_name": task["task_name"],
        "due_date": task["due_date"],
        "description": task["description"],
        "file_name": task["file_name"],
        "file_data": Binary(base64.b64decode(task["file_data"]))  # Convert Base64 to Binary
    }

    # Add task to the `tasks` array inside the correct course
    result = courses_collection.update_one(
        {"_id": course_id},  # Find the course by ID
        {"$push": {"tasks": new_task}}  # Append new task to tasks array
    )

    # Check if the update was successful
    if result.matched_count > 0:
        return("Task added successfully!")
    else:
        return("Course not found.")


def delete_course(course_id):
    """Deletes a course and removes it from all students."""
    course_object_id = ObjectId(course_id)

    # 1️⃣ Delete course from courses collection
    result = courses_collection.delete_one({"_id": course_object_id})

    if result.deleted_count == 0:
        return {"status": "fail", "message": "Course not found"}

    # 2️⃣ Remove the course from all students' course lists
    users_collection.update_many(
        {"courses": course_object_id},
        {"$pull": {"courses": course_object_id}}
    )

    return {"status": "success", "message": "Course deleted successfully"}
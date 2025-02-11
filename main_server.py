import json
import socket
import threading
from pymongo import MongoClient

from db.script_insert_courses import courses_collection


# MongoDB setup
def connect_to_db():
    client = MongoClient('mongodb://localhost:27017/')  # Replace with your connection string
    db = client['classroom']
    return db

# Check user function
def check_user(mail, password):
    user = users_collection.find_one({"mail": mail, "password": password})
    if user:
        return '{"status":"success", "message": "Login successful!"}'
    return '{"status":"fail", "message": "Invalid"}'

def register_user(mail, password):
    existing_user = users_collection.find_one({"mail": mail})
    if existing_user:
        return '{"status":"fail", "message": "User already exists"}'

    # אם המשתמש לא קיים, נרשום אותו במסד הנתונים
    users_collection.insert_one({"mail": mail, "password": password})
    return  '{"status":"success", "message":"Registration successful"}'


# Function to get courses by teacher email
def get_courses_by_teacher(teacher_mail):

    # Query to find all courses for the given teacher's email
    courses_cursor = courses_collection.find({"teacher_mail": teacher_mail})

    # Use count_documents() to count the number of matching documents
    if courses_collection.count_documents({"teacher_mail": teacher_mail}) == 0:
        return {"status": "fail", "message": "No courses found for this teacher."}

    # Format the result into a list of dictionaries
    course_list = []
    for course in courses_cursor:
        # MongoDB documents have an "_id" field by default, we exclude it if you don't need it
        course_data = {
            "id":str(course["_id"]),
            "name": course["name"],
            "subject": course["subject"],
            "teacher_mail": course["teacher_mail"],
             "tasks": course.get("tasks", [])  # If "tasks" is missing, return an empty list
        }
        course_list.append(course_data)

    return {"status": "success", "courses": course_list}

# Handle client messages
def add_course(details):
    new_course = json.loads(details)
    existing_course = courses_collection.find_one({"name": new_course["name"]})
    if existing_course:
        return '{"status":"fail", "message": "Course already exists"}'

    # אם הקורס לא קיים, נרשום אותו במסד הנתונים
    courses_collection.insert_one({"teacher_mail": new_course["teacher_mail"],
                                   "name": new_course["name"],
                                   "subject": new_course["subject"]})
    return '{"status":"success", "message":"Course created"}'


def handle_client(client_socket):
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            # split message by : char => (command:details)
            command, details = message.split(':', 1)
            if command == "login":
                #split details into two variables: mail and password
                mail, password = details.split(',')
                #check in mongo db if user exists
                response = check_user(mail, password)
            elif command == "register":
                # split details into two variables: mail and password
                mail, password = details.split(',')
                # register user in mongo db (if user not exists)
                response = register_user(mail, password)
            elif command == "courses":
                # retrieve all courses of current user (teacher).
                # get_courses_by_teacher returns json of all the courses so we add to serialize it for sending by socket
                response = json.dumps(get_courses_by_teacher(details))
            elif command == "new_course":
                #add course to db
                response = add_course(details)
            else:
                response = "Invalid command."

            # sending to client the response
            client_socket.send(response.encode('utf-8'))

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

# Main server function
def start_server():
    global users_collection
    global courses_collection
    db = connect_to_db()
    users_collection = db['users']
    courses_collection = db['courses']
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5000))
    server.listen(5)
    print("Server is running and waiting for connections...")

    while True:
        client_socket, addr = server.accept()
        print(f"New connection from {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_server()


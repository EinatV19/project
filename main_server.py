import json
import socket
import threading
from pymongo import MongoClient

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
    # Print the teacher_mail to make sure it's being passed correctly
    print(f"Looking for teacher mail: {teacher_mail}")

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
            "name": course["name"],
            "subject": course["subject"],
            "teacher_mail": course["teacher_mail"]
        }
        course_list.append(course_data)

    return {"status": "success", "courses": course_list}

# Handle client messages
def handle_client(client_socket):
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            # Example message: "login:mail@example.com,password123"
            command, details = message.split(':', 1)
            if command == "login":
                mail, password = details.split(',')
                response = check_user(mail, password)
            elif command == "register":
                mail, password = details.split(',')
                response = register_user(mail, password)
            elif command == "courses":
                response = json.dumps(get_courses_by_teacher(details))
            else:
                response = "Invalid command."

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


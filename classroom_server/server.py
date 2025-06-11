import base64
import json
import os.path
import socket
import threading
# from pymongo import MongoClient

from classroom_server.database import check_user, register_user, get_courses_by_user, add_task_to_course, add_course, \
    delete_course, add_student_to_course


# # Handle client messages
# def add_course(details):
#     new_course = json.loads(details)
#     existing_course = courses_collection.find_one({"name": new_course["name"]})
#     if existing_course:
#         return '{"status":"fail", "message": "Course already exists"}'
#
#     # אם הקורס לא קיים, נרשום אותו במסד הנתונים
#     courses_collection.insert_one({"teacher_mail": new_course["teacher_mail"],
#                                    "name": new_course["name"],
#                                    "subject": new_course["subject"]})
#     return '{"status":"success", "message":"Course created"}'

# from bson import ObjectId, Binary
#
# def add_task_to_course(task):
#     """
#     Adds a new task to a course document in MongoDB.
#     :param task: Dictionary containing task details.
#     """
#
#     # Convert course_id from string to ObjectId
#     course_id = ObjectId(task["course_id"])
#
#     # Prepare task dictionary
#     new_task = {
#         "task_name": task["task_name"],
#         "due_date": task["due_date"],
#         "description": task["description"],
#         "file_name": task["file_name"],
#         "file_data": Binary(base64.b64decode(task["file_data"]))  # Convert Base64 to Binary
#     }
#
#     # Add task to the `tasks` array inside the correct course
#     result = courses_collection.update_one(
#         {"_id": course_id},  # Find the course by ID
#         {"$push": {"tasks": new_task}}  # Append new task to tasks array
#     )
#
#     # Check if the update was successful
#     if result.matched_count > 0:
#         return("Task added successfully!")
#     else:
#         return("Course not found.")
#

def handle_client(client_socket):
    try:
        while True:
            message = client_socket.recv(4096).decode()
            # while True:
            #     part = client_socket.recv(4096)
            #     if not part:  # No more data, break
            #         break
            #     message+=part
        #     message = client_socket.recv(4096).decode()

            if not message or message == "disconnect":
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
                # retrieve all courses of current user
                response_dict = get_courses_by_user(details)
                response = json.dumps( response_dict )
            elif command == "new_course":
                course_details = json.loads(details)
                #add course to db
                response_dict = add_course(course_details)
                response = json.dumps( response_dict )
            elif command == "delete_course":
                response_dict = delete_course(details)
                response = json.dumps(response_dict)
            elif command == "join_course":
                course_details = json.loads(details)
                response_dict = add_student_to_course(course_details)
                response = json.dumps(response_dict)
            elif command == "new_task":
                task = json.loads(details)  # Deserialize JSON
                response = add_task_to_course(task)

                # # Save the file
                # with open(file_name, "wb") as file:
                #     file.write(file_data)
                #
                # print(f"Received task: {task_name}")
                # print(f"Saved file: {file_name}")
            elif command == "download_task":
                task_details = json.loads(details)
                task_name = task_details.get("task_name",'')
                course_id = task_details.get("course_id",'')
                send_task(client_socket,task_name,course_id)
                response = "file sent Successfuly"
            else:
                response = "Invalid command."

            # sending to client the response
            client_socket.send(response.encode('utf-8'))

    except Exception as e:
        print(f"Error: {e}")
    finally:
        print(f"Socket Closing")
        client_socket.close()

def send_task(client,task_name,course_id):
    task_name = task_name.replace('.','-')
    task_path = os.path.join("Courses",course_id,task_name,task_name+".docx")
    file_size = os.path.getsize(task_path)
    print(f"sending task {task_path} size: {file_size}")
    client.send(str(file_size).encode())
    client.recv(1024)
    with open(task_path,"rb") as file:
        file_content = file.read()
        client.send(file_content)
    print("task sent successfuly")

# Main server function
def start_server():
    # global users_collection
    # global courses_collection
    # # db = connect_to_db()
    # users_collection = db['users']
    # courses_collection = db['courses']
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


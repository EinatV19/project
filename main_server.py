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
        return "{'status':'success', 'message': 'Login successful!'}"
    return "{'status':'fail', 'message': 'Invalid'}"

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
    db = connect_to_db()
    users_collection = db['users']

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

 #   ---------------------------------------------------------------------------


    # פונקציה להרשמת משתמש חדש
    def register_user(mail, password):
        existing_user = users_collection.find_one({"mail": mail})
        if existing_user:
            return "{'status':'fail', 'message': 'User already exists'}"

        # אם המשתמש לא קיים, נרשום אותו במסד הנתונים
        users_collection.insert_one({"mail": mail, "password": password})
        return "{'status':'success', 'message': 'Registration successful'}"


    # עדכון הקוד ב-handle_client כך שיתמוך בבקשה להרשמה
    def handle_client(client_socket):
        try:
            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break

                command, details = message.split(':', 1)
                if command == "login":
                    mail, password = details.split(',')
                    response = check_user(mail, password)
                elif command == "register":
                    mail, password = details.split(',')
                    response = register_user(mail, password)
                else:
                    response = "Invalid command."

                client_socket.send(response.encode('utf-8'))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()


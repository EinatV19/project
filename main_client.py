import socket

class Client:
    def __init__(self, host='127.0.0.1', port=5000):
        """
        Initialize the client with the server's host and port.
        """
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        """
        Connect to the server.
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            print("Connected to the server.")
        except Exception as e:
            print(f"Failed to connect to the server: {e}")

    def send_message(self, message):
        """
        Send a message to the server and receive a response.
        :param message: The message string to send to the server.
        :return: The server's response.
        """
        try:
            self.socket.send(message.encode('utf-8'))
            response = self.socket.recv(1024).decode('utf-8')
            return response
        except Exception as e:
            return f"Error communicating with server: {e}"

    def close(self):
        """
        Close the connection to the server.
        """
        if self.socket:
            self.socket.close()
            print("Disconnected from the server.")

# if __name__ == "__main__":
#     client = Client()
#
#     # Connect to the server
#     client.connect()
#
#     try:
#         while True:
#             print("\n1. Login\n2. Exit")
#             choice = input("Enter your choice: ")
#
#             if choice == '1':
#                 mail = input("Enter email: ")
#                 password = input("Enter password: ")
#                 message = f"login:{mail},{password}"
#                 response = client.send_message(message)
#                 print(f"Server response: {response}")
#             elif choice == '2':
#                 print("Exiting...")
#                 break
#             else:
#                 print("Invalid choice.")
#     finally:
#         # Close the connection when done
#         client.close()

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

    def receive_file(self,file_size,save_location):
        self.socket.send(b"R")
        chunk = b''
        while file_size>0:
            chunk += self.socket.recv(1024)
            file_size -= 1024
        with open(save_location, "wb") as file:
            file.write(chunk)
        return self.socket.recv(1024).decode()

    def send_message(self, message):
        """
        Send a message to the server and receive a response.
        :param message: The message string to send to the server.
        :return: The server's response.
        """
        try:
            self.socket.sendall(message.encode('utf-8'))
            response = self.socket.recv(1024).decode('utf-8')
            return response
        except Exception as e:
            return f"Error communicating with server: {e}"



    def disconnect(self):
        """
        Send a disconnect signal to the server and close the socket.
        """
        try:
            if self.socket:
                self.socket.send(b"disconnect")  # Send disconnect signal
                self.socket.close()
                print("Disconnected from the server.")
        except Exception as e:
            print(f"Error disconnecting: {e}")

    def close(self):
        """
        Close the connection to the server.
        """
        self.disconnect()  # Ensure proper disconnection before closing
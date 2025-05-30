import socket
import threading
import cv2
import pyaudio

class TeacherServer:
    def __init__(self, server_ip='0.0.0.0', video_port=9999, audio_port=8888):
        """
        Initialize the video and audio server.
        """
        self.server_ip = server_ip
        self.video_port = video_port
        self.audio_port = audio_port
        self.running = False  # Track server status

        # Sockets for video & audio
        self.video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Client lists
        self.video_clients = []
        self.audio_clients = []

    def start_server(self):
        """
        Starts the teacher's video and audio server.
        """
        if self.running:
            print("Server is already running!")
            return

        self.running = True
        print("Starting Teacher Server...")

        # Bind and listen on video and audio sockets
        self.video_socket.bind((self.server_ip, self.video_port))
        self.video_socket.listen(5)

        self.audio_socket.bind((self.server_ip, self.audio_port))
        self.audio_socket.listen(5)

        # Start client handling and streaming threads
        threading.Thread(target=self.handle_video_clients, daemon=True).start()
        threading.Thread(target=self.handle_audio_clients, daemon=True).start()
        threading.Thread(target=self.send_video, daemon=True).start()
        threading.Thread(target=self.send_audio, daemon=True).start()

    def stop_server(self):
        """
        Stops the teacher's server and closes all sockets.
        """
        self.running = False
        print("Shutting down the Teacher Server...")

        # Close all sockets
        self.video_socket.close()
        self.audio_socket.close()

    def handle_video_clients(self):
        """Accept and manage video clients."""
        while self.running:
            conn, addr = self.video_socket.accept()
            print(f"Video client connected: {addr}")
            self.video_clients.append(conn)

    def handle_audio_clients(self):
        """Accept and manage audio clients."""
        while self.running:
            conn, addr = self.audio_socket.accept()
            print(f"Audio client connected: {addr}")
            self.audio_clients.append(conn)

    def send_video(self):
        """Capture and stream video to clients."""
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            print("Error: Cannot access the camera.")
            return

        try:
            while self.running:
                ret, frame = camera.read()
                if not ret:
                    print("Error: Failed to read from camera.")
                    break

                frame = cv2.resize(frame, (640, 480))
                _, buffer = cv2.imencode('.jpg', frame)
                frame_data = buffer.tobytes()

                for client in self.video_clients[:]:
                    try:
                        client.send(len(frame_data).to_bytes(4, 'big'))
                        client.sendall(frame_data)
                    except Exception as e:
                        print(f"Error sending video: {e}")
                        self.video_clients.remove(client)

        except Exception as e:
            print(f"Video Error: {e}")
        finally:
            camera.release()

    def send_audio(self):
        """Capture and stream audio to clients."""
        audio = pyaudio.PyAudio()
        audio_stream = audio.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=44100,
                                  input=True,
                                  frames_per_buffer=1024)

        try:
            while self.running:
                audio_data = audio_stream.read(1024)
                for client in self.audio_clients[:]:
                    try:
                        client.send(len(audio_data).to_bytes(4, 'big'))
                        client.sendall(audio_data)
                    except Exception as e:
                        print(f"Error sending audio: {e}")
                        self.audio_clients.remove(client)
        except Exception as e:
            print(f"Audio Error: {e}")
        finally:
            audio_stream.stop_stream()
            audio_stream.close()

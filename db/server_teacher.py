import socket
import threading
import cv2
import pyaudio

def teacher_server(server_ip, video_port, audio_port):
    # Initialize video and audio sockets
    video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    video_socket.bind((server_ip, video_port))
    video_socket.listen(5)  # Allow multiple connections

    audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    audio_socket.bind((server_ip, audio_port))
    audio_socket.listen(5)

    video_clients = []
    audio_clients = []

    def handle_video_clients():
        while True:
            conn, addr = video_socket.accept()
            print(f"Video client connected: {addr}")
            video_clients.append(conn)

    def handle_audio_clients():
        while True:
            conn, addr = audio_socket.accept()
            print(f"Audio client connected: {addr}")
            audio_clients.append(conn)

    def send_video():
        # Initialize camera
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            print("Error: Cannot access the camera.")
            return

        try:
            while True:
                ret, frame = camera.read()
                if not ret:
                    print("Error: Failed to read from camera.")
                    break

                # Resize and encode frame as JPEG
                frame = cv2.resize(frame, (640, 480))
                _, buffer = cv2.imencode('.jpg', frame)
                frame_data = buffer.tobytes()

                # Send the frame size and data to all video clients
                for client in video_clients[:]:
                    try:
                        client.send(len(frame_data).to_bytes(4, 'big'))
                        client.sendall(frame_data)
                    except Exception as e:
                        print(f"Error sending video to client: {e}")
                        video_clients.remove(client)  # Remove disconnected client

        except Exception as e:
            print(f"Video Error: {e}")
        finally:
            camera.release()

    def send_audio():
        # Initialize audio stream
        audio = pyaudio.PyAudio()
        audio_stream = audio.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=44100,
                                  input=True,
                                  frames_per_buffer=1024)

        try:
            while True:
                audio_data = audio_stream.read(1024)
                # Send audio data to all audio clients
                for client in audio_clients[:]:
                    try:
                        client.send(len(audio_data).to_bytes(4, 'big'))
                        client.sendall(audio_data)
                    except Exception as e:
                        print(f"Error sending audio to client: {e}")
                        audio_clients.remove(client)  # Remove disconnected client
        except Exception as e:
            print(f"Audio Error: {e}")
        finally:
            audio_stream.stop_stream()
            audio_stream.close()

    # Start threads for handling clients and sending data
    threading.Thread(target=handle_video_clients, daemon=True).start()
    threading.Thread(target=handle_audio_clients, daemon=True).start()
    threading.Thread(target=send_video, daemon=True).start()
    threading.Thread(target=send_audio, daemon=True).start()

    print("Teacher server is running. Waiting for clients...")
    try:
        while True:
            pass  # Keep the server running
    except KeyboardInterrupt:
        print("Shutting down server...")
        video_socket.close()
        audio_socket.close()

# Example usage
teacher_server('0.0.0.0', 9999, 8888)

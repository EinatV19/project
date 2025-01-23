import socket
import threading
import cv2
import pyaudio
import time

def send_video_audio(server_ip, video_port, audio_port):
    # Initialize video socket
    video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    video_socket.connect((server_ip, video_port))

    # Initialize audio socket
    audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    audio_socket.connect((server_ip, audio_port))

    # Initialize camera
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Error: Cannot access the camera.")
        return

    # Initialize audio stream
    audio = pyaudio.PyAudio()
    audio_stream = audio.open(format=pyaudio.paInt16,
                              channels=1,
                              rate=44100,
                              input=True,
                              frames_per_buffer=1024)

    def send_video():
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

                # Send the frame size first (4 bytes)
                video_socket.send(len(frame_data).to_bytes(4, 'big'))
                # Send the actual frame
                video_socket.sendall(frame_data)

                time.sleep(0.03)  # ~30 FPS
        except Exception as e:
            print(f"Video Error: {e}")
        finally:
            camera.release()
            video_socket.close()

    def send_audio():
        try:
            while True:
                audio_data = audio_stream.read(1024)
                # Send the audio chunk size first (4 bytes)
                audio_socket.send(len(audio_data).to_bytes(4, 'big'))
                # Send the actual audio data
                audio_socket.sendall(audio_data)
        except Exception as e:
            print(f"Audio Error: {e}")
        finally:
            audio_stream.stop_stream()
            audio_stream.close()
            audio_socket.close()

    # Start video and audio threads
    video_thread = threading.Thread(target=send_video, daemon=True)
    audio_thread = threading.Thread(target=send_audio, daemon=True)
    video_thread.start()
    audio_thread.start()

    # Prevent main thread from exiting
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping client...")
        camera.release()
        audio_stream.stop_stream()
        audio_stream.close()


import queue


def start_multi_connections():
    servers_queue = queue.Queue()  # Thread-safe queue for adding new servers dynamically
    threads = []  # Keep track of client threads

    def handle_new_connections():
        """Continuously check for new servers in the queue and start threads."""
        while True:
            try:
                # Wait for a new server to be added to the queue
                server_ip, video_port, audio_port = servers_queue.get()
                print(f"Connecting to new server: {server_ip}:{video_port}, {audio_port}")

                # Start a new thread for the client connection
                thread = threading.Thread(target=send_video_audio, args=(server_ip, video_port, audio_port),
                                          daemon=True)
                thread.start()
                threads.append(thread)

                # Mark the task as done
                servers_queue.task_done()
            except Exception as e:
                print(f"Error handling new connection: {e}")

    # Start a thread to handle new connections
    threading.Thread(target=handle_new_connections, daemon=True).start()

    # Add new servers dynamically
    while True:
        try:
            # Simulate user input or API to add a new server
            new_server_ip = input("Enter server IP (or type 'exit' to quit): ")
            if new_server_ip.lower() == "exit":
                print("Exiting...")
                break
            new_video_port = int(input("Enter video port: "))
            new_audio_port = int(input("Enter audio port: "))

            # Add the new server to the queue
            servers_queue.put((new_server_ip, new_video_port, new_audio_port))
        except Exception as e:
            print(f"Error adding server: {e}")

    # Wait for all threads to finish (optional, for graceful shutdown)
    for thread in threads:
        thread.join()


start_multi_connections()

# send_video_audio('192.168.253.103', 9999, 8888)
#
# # send_video_audio('192.168.253.134', 9999, 8888)

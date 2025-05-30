import socket
import threading
import time

from PIL import Image, ImageTk
import io
from tkinter import Tk, Label
import pyaudio
import queue

def student_client(server_ip, video_port, audio_port):
    # Initialize sockets
    video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    video_socket.connect((server_ip, video_port))

    audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    audio_socket.connect((server_ip, audio_port))

    # Initialize audio playback
    audio = pyaudio.PyAudio()
    audio_stream = audio.open(format=pyaudio.paInt16,
                              channels=1,
                              rate=44100,
                              output=True,
                              frames_per_buffer=1024)

    def receive_video():
        frame_data_queue = queue.Queue()

        def update_gui():
            if not frame_data_queue.empty():
                frame_data = frame_data_queue.get()
                try:
                    byte_stream = io.BytesIO(frame_data)
                    img = Image.open(byte_stream)
                    img = img.resize((640, 480))
                    photo = ImageTk.PhotoImage(img)
                    lbl.config(image=photo)
                    lbl.image = photo
                except Exception as e:
                    print(f"Error updating video frame: {e}")
            root.after(10, update_gui)

        def fetch_video_frames():
            try:
                while True:
                    frame_size_data = video_socket.recv(4)
                    if not frame_size_data:
                        print("Disconnected from video server.")
                        break
                    frame_size = int.from_bytes(frame_size_data, 'big')
                    frame_data = video_socket.recv(frame_size)
                    while len(frame_data) < frame_size:
                        frame_data += video_socket.recv(frame_size - len(frame_data))

                    frame_data_queue.put(frame_data)
            except Exception as e:
                print(f"Video Error: {e}")
            finally:
                video_socket.close()

        # Start thread to fetch video frames
        threading.Thread(target=fetch_video_frames, daemon=True).start()

        # Initialize Tkinter GUI
        root = Tk()
        root.title("Teacher Video")
        lbl = Label(root)
        lbl.pack()

        # Schedule periodic GUI updates
        root.after(10, update_gui)
        root.mainloop()

    def receive_audio():
        try:
            while True:
                chunk_size_data = audio_socket.recv(4)
                if not chunk_size_data:
                    print("Disconnected from audio server.")
                    break
                chunk_size = int.from_bytes(chunk_size_data, 'big')
                audio_data = audio_socket.recv(chunk_size)
                while len(audio_data) < chunk_size:
                    audio_data += audio_socket.recv(chunk_size - len(audio_data))

                audio_stream.write(audio_data)
        except Exception as e:
            print(f"Audio Error: {e}")
        finally:
            audio_socket.close()
            audio_stream.stop_stream()
            audio_stream.close()

    # Start threads for video and audio
    threading.Thread(target=receive_video, daemon=True).start()
    threading.Thread(target=receive_audio, daemon=True).start()

    # Keep main thread running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down client...")
        video_socket.close()
        audio_socket.close()

# Example usage
student_client('192.168.33.154', 9999, 8888)

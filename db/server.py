import socket
import threading
import queue
from PIL import Image, ImageTk
import io
from tkinter import Tk, Label
import pyaudio

def receive_video_audio(server_ip, video_port, audio_port):
    # Initialize sockets
    video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    video_socket.bind((server_ip, video_port))

    audio_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    audio_socket.bind((server_ip, audio_port))

    # Initialize audio playback
    audio = pyaudio.PyAudio()
    audio_stream = audio.open(format=pyaudio.paInt16,
                              channels=1,
                              rate=44100,
                              output=True,
                              frames_per_buffer=1024)

    frame_queue = queue.Queue()

    def update_gui():
        if not frame_queue.empty():
            frame_data = frame_queue.get()
            try:
                byte_stream = io.BytesIO(frame_data)
                img = Image.open(byte_stream)
                img = img.resize((640, 480))
                photo = ImageTk.PhotoImage(img)
                lbl.config(image=photo)
                lbl.image = photo
            except Exception as e:
                print(f"Frame processing error: {e}")
        root.after(10, update_gui)

    def receive_video():
        expected_sequence_number = 0
        frame_buffer = b''
        try:
            while True:
                packet, _ = video_socket.recvfrom(65000)
                sequence_number = int.from_bytes(packet[:4], 'big')
                data = packet[4:]

                if sequence_number == expected_sequence_number:
                    if data == b'EOF':  # End of frame
                        if frame_buffer:
                            frame_queue.put(frame_buffer)  # Add complete frame to queue
                            frame_buffer = b''  # Clear buffer for the next frame
                        expected_sequence_number = (expected_sequence_number + 1) % (2 ** 32)
                    else:
                        frame_buffer += data
                else:
                    print(f"\nOut-of-order frame: received {sequence_number}, expected {expected_sequence_number}")
        except Exception as e:
            print(f"Video Error: {e}")
        finally:
            video_socket.close()

    def receive_audio():
        try:
            while True:
                packet, _ = audio_socket.recvfrom(1400)  # Match the sender's packet size
                print(f"Received audio packet of size: {len(packet)}")
                if packet:
                    audio_stream.write(packet)
        except Exception as e:
            print(f"Audio Error: {e}")
        finally:
            audio_stream.stop_stream()
            audio_stream.close()
            audio_socket.close()

    # Start video and audio threads
    threading.Thread(target=receive_video, daemon=True).start()
    threading.Thread(target=receive_audio, daemon=True).start()

    # Set up GUI
    root = Tk()
    root.title("Video Chat")
    lbl = Label(root)
    lbl.pack()
    root.after(10, update_gui)
    root.mainloop()

# Example usage
receive_video_audio('0.0.0.0', 9999, 8888)


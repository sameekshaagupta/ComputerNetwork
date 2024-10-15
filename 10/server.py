import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class Server:
    def __init__(self):
        # Create a UDP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = '127.0.0.1'
        self.port = 12345
        self.server_socket.bind((self.host, self.port))

        self.client_address = None  # Store client's address to send back data

        self.root = tk.Tk()
        self.root.title("UDP Server")

        self.text_area = scrolledtext.ScrolledText(self.root, state='disabled', width=50, height=20)
        self.text_area.pack(pady=10)

        self.thread = threading.Thread(target=self.receive_messages)
        self.thread.start()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def receive_messages(self):
        while True:
            try:
                # Receive message from client
                data, self.client_address = self.server_socket.recvfrom(1024)
                message = data.decode()
                
                if not message:
                    break

                # Split the message to extract the two numbers
                numbers = message.split()
                if len(numbers) == 2:
                    try:
                        num1 = int(numbers[0])
                        num2 = int(numbers[1])
                        result = num1 + num2

                        # Update the server UI
                        self.text_area.config(state='normal')
                        self.text_area.insert(tk.END, f"Received: {num1} + {num2} = {result}\n")
                        self.text_area.config(state='disabled')

                        # Send result back to client
                        self.server_socket.sendto(str(result).encode(), self.client_address)
                    except ValueError:
                        self.text_area.config(state='normal')
                        self.text_area.insert(tk.END, "Invalid numbers received\n")
                        self.text_area.config(state='disabled')

            except Exception as e:
                print(f"Error: {e}")
                break

    def on_closing(self):
        self.server_socket.close()
        self.root.destroy()

if __name__ == "__main__":
    Server()

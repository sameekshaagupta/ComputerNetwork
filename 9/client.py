import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '127.0.0.1'
        self.port = 12345

        self.root = tk.Tk()
        self.root.title("Client")

        self.text_area = scrolledtext.ScrolledText(self.root, state='disabled', width=50, height=20)
        self.text_area.pack(pady=10)

        self.entry = tk.Entry(self.root, width=50)
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.send_message)

        self.connect_to_server()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def connect_to_server(self):
        try:
            self.client_socket.connect((self.host, self.port))
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except ConnectionRefusedError:
            self.text_area.config(state='normal')
            self.text_area.insert(tk.END, "Unable to connect to server.\n")
            self.text_area.config(state='disabled')

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if not message:
                    break
                self.text_area.config(state='normal')
                self.text_area.insert(tk.END, f"Server: {message}\n")
                self.text_area.config(state='disabled')
            except:
                break

    def send_message(self, event=None):
        message = self.entry.get()
        if message:
            self.client_socket.send(message.encode())
            self.text_area.config(state='normal')
            self.text_area.insert(tk.END, f"Client: {message}\n")
            self.text_area.config(state='disabled')
            self.entry.delete(0, tk.END)

    def on_closing(self):
        self.client_socket.close()
        self.root.destroy()

if __name__ == "__main__":
    Client()

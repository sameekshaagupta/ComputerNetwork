import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '127.0.0.1'
        self.port = 12345
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        self.conn = None
        self.addr = None

        self.root = tk.Tk()
        self.root.title("Server")

        self.text_area = scrolledtext.ScrolledText(self.root, state='disabled', width=50, height=20)
        self.text_area.pack(pady=10)

        self.entry = tk.Entry(self.root, width=50)
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.send_message)

        self.thread = threading.Thread(target=self.accept_connections)
        self.thread.start()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def accept_connections(self):
        self.conn, self.addr = self.server_socket.accept()
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, f"Connection established with {self.addr}\n")
        self.text_area.config(state='disabled')
        self.receive_messages()

    def receive_messages(self):
        while True:
            try:
                message = self.conn.recv(1024).decode()
                if not message:
                    break
                self.text_area.config(state='normal')
                self.text_area.insert(tk.END, f"Client: {message}\n")
                self.text_area.config(state='disabled')
            except:
                break

    def send_message(self, event=None):
        message = self.entry.get()
        if message:
            self.conn.send(message.encode())
            self.text_area.config(state='normal')
            self.text_area.insert(tk.END, f"Server: {message}\n")
            self.text_area.config(state='disabled')
            self.entry.delete(0, tk.END)

    def on_closing(self):
        self.conn.close()
        self.server_socket.close()
        self.root.destroy()

if __name__ == "__main__":
    Server()

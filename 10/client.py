import socket

def udp_client():
    server_address = ('127.0.0.1', 12345)

    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Input two numbers
        num1 = input("Enter first number: ")
        num2 = input("Enter second number: ")

        message = f"{num1} {num2}"
        
        # Send the numbers to the server
        client_socket.sendto(message.encode(), server_address)
        
        # Receive the sum from the server
        data, _ = client_socket.recvfrom(1024)
        print(f"Sum from server: {data.decode()}")
    
    finally:
        client_socket.close()

if __name__ == "__main__":
    udp_client()

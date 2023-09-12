import socket
import threading

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
server_address = ('192.168.0.82', 1337)

# Connect to the server
client_socket.connect(server_address)

# Function to send messages to the server
def send_message():
    while True:
        message = input("You: ")
        client_socket.send(message.encode())

# Function to receive messages from the server
def receive_message():
    while True:
        try:
            message = client_socket.recv(1024)
            print("\nReceived:", message.decode())
        except:
            print("Connection closed.")
            break

# Function to handle a client's messages
def handle_client(client_socket):
    while True:
        try:
            # Receive data from the client
            message = client_socket.recv(1024)
            if message:
                print("Received:", message.decode())
                # Broadcast the message to all clients
                broadcast(message, client_socket)
            else:
                # Remove the client if no data is received
                remove(client_socket)
        except Exception as e:
            print("Error in handle_client:", e)
            # Remove the client if there's an issue
            remove(client_socket)


# Create threads for sending and receiving messages
send_thread = threading.Thread(target=send_message)
receive_thread = threading.Thread(target=receive_message)

# Start the threads
send_thread.start()
receive_thread.start()

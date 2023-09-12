import socket
import threading

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
server_address = ('192.168.0.82', 1337)

# Bind the socket to the server address
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(5)

print("Waiting for a client to connect...")

# List to store connected clients
clients = []

# Function to broadcast messages to all clients
def broadcast(message, client_socket):
    for client in clients:
        # Send the message to everyone except the sender
        if client != client_socket:
            try:
                client.send(message)
            except:
                # Remove the client if there's an issue
                remove(client)

# Function to remove a client from the list
def remove(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

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

while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print("Connection established with:", client_address)
    
    # Add the client to the list
    clients.append(client_socket)
    
    # Create a thread to handle the client's messages
    client_thread = threading.Thread(target=lambda: handle_client(client_socket))
    client_thread.start()

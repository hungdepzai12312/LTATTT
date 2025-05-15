import socket  # Import the socket module to handle network connections
import threading  # Import threading to handle multiple clients concurrently

# Define the server IP and port
IP = '0.0.0.0'  # This means the server will listen on all available network interfaces
PORT = 9998  # The port number where the server will accept connections

def main():
    """
    Main function to set up the server and listen for incoming connections.
    """
    # Create a socket object using IPv4 (AF_INET) and TCP (SOCK_STREAM)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the specified IP and port
    server.bind((IP, PORT))

    # Start listening for incoming connections (backlog of 5 clients)
    server.listen(5)
    print(f'[*] Listening on {IP}:{PORT}')

    while True:
        # Accept a new client connection
        client, address = server.accept()
        print(f'[*] Accepted connection from {address[0]}:{address[1]}')

        # Create a new thread to handle the client request
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()  # Start the thread, allowing multiple clients to connect simultaneously

def handle_client(client_socket):
    """
    Function to handle a client connection.
    """
    # Use the 'with' statement to ensure the socket is properly closed
    with client_socket as sock:
        # Receive data from the client (up to 1024 bytes)
        request = sock.recv(1024)
        print(f'[*] Received: {request.decode("utf-8")}')

        # Send an acknowledgment response back to the client
        sock.send(b'ACK')

# Check if the script is run directly (not imported as a module)
if __name__ == '__main__':
    main()
    


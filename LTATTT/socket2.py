import socket  # Importing the socket module to enable network communication

# Define the target server's IP address and port number
target_host = "172.20.10.5"  # IP address of the target machine
target_port = 9998  # Port number where the server is listening

# Create a socket object using IPv4 (AF_INET) and TCP (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Establish a connection to the target server
client.connect((target_host, target_port))

# Send an HTTP request to the server
# The 'b' before the string converts it into bytes (required for sending data over a socket)
client.send(b"GET / HTTP/1.1\r\nHost: 172.20.10.2\r\n\r\n")

# Receive up to 4096 bytes of data from the server
response = client.recv(4096)

# Print the received response after decoding it from bytes to string
print(response.decode())

# Close the connection to free up resources
client.close()


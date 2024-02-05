import socket
import time
import sys

HOST = 'localhost'  # Replace with the server IP address
PORT = 1238

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print(f"[*] Connected to {HOST}:{PORT}")

while True:
    # Send 'ping' command to the server
    client_socket.send("/ping".encode())
    print(f"Sending: /ping")
    
    # Receive response from the server
    response = client_socket.recv(1024).decode()

    # Check if the response is '/ping' and send '/pong' back to the server
    if response == "/pong":
        print(f"Received: {response}")
        
    sys.stdout.flush()
    
    # Wait for 30 seconds before sending the next 'ping' command
    time.sleep(30)

# Close the client socket (This won't be reached in this example)
client_socket.close()
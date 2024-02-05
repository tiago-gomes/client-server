import socket
import select
import sys

HOST = '0.0.0.0'
PORT = 1238

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"[*] Listening on {HOST}:{PORT}")
sys.stdout.flush()

# List to keep track of connected clients
client_sockets = [server_socket]
client_addresses = {}

try:
    while True:
        # Use select to monitor sockets for reading
        read_sockets, _, _ = select.select(client_sockets, [], [])
        
        for sock in read_sockets:
            # Accept new connection
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                client_sockets.append(client_socket)
                client_addresses[client_socket] = client_address
                print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")
                sys.stdout.flush()
            
            # Receive command from the client
            else:
                try:
                    data = sock.recv(1024).decode()
                    if data:
                        print(f"Received from {client_addresses[sock][0]}:{client_addresses[sock][1]}: {data}")
                        sys.stdout.flush()
                        
                        # Check if the command is "/clients"
                        if data.strip() == "/clients":
                            # Prepare list of connected clients and their IPs
                            client_list = [f"{client_addresses[client][0]}:{client_addresses[client][1]}" for client in client_sockets[1:]]
                            response = "\n".join(client_list)
                        elif data.strip() == "/ping":
                            response = "/pong"
                        else:
                            response = "c4"
                        
                        if response != "c4":
                            # Send the response back to the client
                            sock.send(response.encode())
                            print(f"sending to {client_addresses[sock][0]}:{client_addresses[sock][1]}: {response}")
                            sys.stdout.flush()
                        
                    else:
                        # Close the connection if no data received
                        sock.close()
                        client_sockets.remove(sock)
                        print(f"[!] Connection closed from {client_addresses[sock][0]}:{client_addresses[sock][1]}")
                        del client_addresses[sock]
                except ConnectionResetError:
                    # Handle connection reset by peer error
                    sock.close()
                    client_sockets.remove(sock)
                    print(f"[!] Connection closed from {client_addresses[sock][0]}:{client_addresses[sock][1]}")
                    del client_addresses[sock]
                except OSError:
                    # Handle socket error
                    sock.close()
                    client_sockets.remove(sock)
                    print(f"[!] Connection closed from {client_addresses[sock][0]}:{client_addresses[sock][1]}")
                    del client_addresses[sock]
        
        # Print the current number of connected clients
        print(f"[*] Currently {len(client_sockets) - 1} client(s) connected")
        sys.stdout.flush()

except KeyboardInterrupt:
    print("\n[!] Server interrupted. Closing all connections.")
    sys.stdout.flush()

finally:
    # Close all client sockets
    for sock in client_sockets:
        sock.close()

    # Close the server socket
    server_socket.close()
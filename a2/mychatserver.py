from socket import *
import threading

host = 'localhost'
serverPort = 12000
bufferSize = 1024

clients = []
lock = threading.Lock()


def handle_client (client_socket, addr):
    print(f"New connection from {addr[1]}")
    with lock:
        clients.append((client_socket, addr))

    try:
        while True:
            try:
                message = client_socket.recv(bufferSize).decode()
                if not message:
                    # Client disconnected abruptly (Ctrl+C or closed app)
                    print(f"Client {addr[1]} disconnected unexpectedly.")
                    break
                if message.strip().lower() == 'exit':
                    break
                else:
                    print(f'{addr[1]}: {message}')
                    broadcast(f'{addr[1]}: {message}', client_socket)
            except (ConnectionResetError, ConnectionAbortedError, OSError) as e:
                print(f"Connection lost with {addr[1]}: {e}")
                break

    except Exception as e:
        print(f"Error at {addr[1]}: {e}")
    finally:
        print(f'Client {addr[1]} has left the chat.')
        client_socket.close()
        clients.remove((client_socket, addr))


def broadcast(message, sender_socket):
    with lock:
        for client_socket, _ in clients:
            if client_socket != sender_socket:
                try:
                    client_socket.send(message.encode())
                except Exception as e:
                    print(f'Error. Failed to send to client {e}')
                    client_socket.close()
                    clients.remove((client_socket, _))


# Create TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Bind socket to port
serverSocket.bind(('', serverPort))

# listen for incoming connections
serverSocket.listen()  # arbitrary number of max clients

print(f"Server listening on {host} {serverPort}")


while True:  # unlimited clients
    # accept a connection from client
    connectionSocket, addr = serverSocket.accept()

    thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))
    thread.start()


serverSocket.close() # do NOT put this in while loop
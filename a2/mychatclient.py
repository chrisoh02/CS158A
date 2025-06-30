from socket import *
import threading

serverName = 'localhost'    # ip address
serverPort = 12000          # port number
bufferSize = 1024

def receive_messages(client):
    try:
        while True:
            data = client.recv(bufferSize).decode()
            if not data:
                print("Error getting message from server")
                break
            print(data)

    except Exception:
        pass
    finally:
        client.close()


# TCP Socket Stream
clientSocket = socket(AF_INET, SOCK_STREAM)

# Connect to Server
clientSocket.connect((serverName, serverPort))
print("Connected to chat server. Type \'exit\' to leave.")

threading.Thread(target=receive_messages, args=(clientSocket,), daemon=True).start()

try:
    while True:
        message = input()
        clientSocket.send(message.encode())
        if message.strip().lower() == 'exit':
            break

except Exception as e:
    print("Exception")
finally:
    clientSocket.close()

print('Disconnected from server.')
# note to self, use command python3 myclient.py and python3 myserver.py

from socket import *

serverName = 'localhost'    # ip address
serverPort = 12000          # port number

# TCP Socket Stream
clientSocket = socket(AF_INET, SOCK_STREAM)

# Connect to Server
# replace serverName with class router IP 192.168.1.2
clientSocket.connect((serverName, serverPort))

sentence = input('Input lowercase sentence: ')

# Send sentence to server
clientSocket.send(sentence.encode())    # str.encode() is serialization

# receive the modified sentence from server
modifiedSentence = clientSocket.recv(64)    # 64 is the buffer size

print('From Server: ', modifiedSentence.decode())

# Close Socket
clientSocket.close()


# note to self, use command python3 myclient.py and python3 myserver.py
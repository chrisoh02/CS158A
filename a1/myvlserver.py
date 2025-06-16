from socket import *

serverPort = 12000

# Create TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Bind socket to port
serverSocket.bind(('', serverPort))

# listen for incoming connections
serverSocket.listen(1)  # only listening for 1 client

while True:  # unlimited clients
    # accept a connection from client
    connectionSocket, addr = serverSocket.accept()
    print(f'Connection from {addr}')

    # receive sentence from client and decode it back to string
    sentence = connectionSocket.recv(64).decode()

    # Grabs number of length n
    messageLength = int(sentence[:2])
    print(f'msg_len: {messageLength}')
    sentence = sentence[2:]
    print('processed: ', sentence)


    # remove extra characters if message is longer than given length
    #if len(sentence) > messageLength:
    #    sentence = sentence[:messageLength - len(sentence)]

    # process, convert the sentence to all uppercase
    capSentence = sentence.upper()

    # send, make sure to serialize with encode
    connectionSocket.send(capSentence.encode())
    print(f'msg_len_sent: {messageLength}')

    # close
    connectionSocket.close()
    print("Connection closed")


serverSocket.close() # do NOT put this in while loop

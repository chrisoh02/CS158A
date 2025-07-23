from socket import *
import threading
import uuid
import json
import time
import sys

class Node:
    def __init__(self, sip, sp, cip, cp, log_name):
        self.ip = sip
        self.port = sp
        self.next_ip = cip
        self.next_port = cp
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket = None
        self.log = open(log_name, 'w')      # log file
        self.uuid = uuid.uuid4()
        self.candidate = Message(self.uuid, 0)
        self.shutdown_event = threading.Event()

    def start(self):
        self.setup_server()
        self.connect_to_next()
        print("started")

        self.sendMessage(self.candidate.serialize())
        self.log_sent()
        print("sent initial message")

        listening = threading.Thread(target=self.listen)
        listening.start()

        try:
            while listening.is_alive():
                listening.join()
        finally:
            self.shutdown_event.set()
            self.finish()
            listening.join()


    def setup_server(self):
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(2)

    def connect_to_next(self):
        while True:
            try:
                self.client_socket = socket(AF_INET, SOCK_STREAM)
                self.client_socket.connect((self.next_ip, self.next_port))
                break
            except Exception:
                self.client_socket.close()
                time.sleep(2)

    def sendMessage(self, message_dict_form):
        message = json.dumps(message_dict_form) + "\n"
        self.client_socket.send(message.encode())

    def handleMessage(self, message):
        if message.uuid > self.uuid:  # pass along vote
            self.candidate = message
            self.log_received(message, 'greater')
            self.sendMessage(self.candidate.serialize())
            self.log_sent()
        elif message.uuid < self.uuid:  # vote for self
            self.sendMessage(self.candidate.serialize())
            self.log_received(message, 'smaller')
        else:  # declare that this node has been elected
            self.candidate.elected()
            self.log_received(message, 'equal')
            self.log.write(f'{self.candidate.uuid} has been elected leader.\n')
            self.sendMessage(self.candidate.serialize())
            self.log_sent()


    def listen(self):
        connection = None
        try:
            connection, _ = self.server_socket.accept()
            connection.settimeout(2)
            buffer = ''

            while not self.shutdown_event.is_set() and self.candidate.flag == 0:
                try:
                    data = connection.recv(1024)
                    if not data:
                        break
                    buffer = buffer + data.decode()

                    while '\n' in buffer:
                        line, buffer = buffer.split("\n", 1)
                        if not line.strip():
                            continue

                        received_message = Message.deserialize(json.loads(line))
                        self.handleMessage(received_message)
                except timeout:
                    continue
        except Exception as e:
            print(f'Error while listening: {e}]')
        finally:
            if connection:
                connection.close()

    def log_sent(self):
        self.log.write(f'Sent: uuid={self.candidate.uuid}, flag={self.candidate.flag}\n')

    def log_received(self, message, comparison):
        self.log.write(f'Received: uuid={message.uuid}, flag={message.flag}, {comparison}, {self.candidate.flag}\n')
        if self.candidate.flag == 1:
            self.log.write(f'Leader\'s uuid={message.uuid}\n')

    def finish(self):
        if self.server_socket:
            self.server_socket.close()
        if self.client_socket:
            self.client_socket.close()
        self.log.close()


class Message:
    def __init__(self, uuid=uuid.uuid4(), flag=0):
        self.uuid = uuid
        self.flag = flag

    def elected(self):
        self.flag = 1

    def serialize(self):
        return {"uuid": str(self.uuid), "flag": int(self.flag)}

    @classmethod
    def deserialize(cls, data):
        return cls(uuid=uuid.UUID(data['uuid']), flag=data['flag'])


def read_config(filename='config.txt'):
    with open(filename, 'r') as f:
        server = f.readline().strip().split(',')
        client = f.readline().strip().split(',')
    serverIP = server[0]
    serverPort = int(server[1])
    clientIP = client[0]
    clientPort = int(client[1])
    return serverIP, serverPort, clientIP, clientPort




sip, sp, cip, cp = read_config('config1.txt')
node = Node(sip, sp, cip, cp, 'log1.txt')
node.start()
print('done')

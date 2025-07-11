from socket import *
import pickle
import threading
import uuid


class Node:
    def __init__(self, port, serverPort, host='localhost'):
        self.host = host
        self.port = port
        self.uuid = uuid.uuid4()
        self.next = serverPort
        self.server_thread = threading.Thread(target=self.server)

    def sendMessage(self, message):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(self.next)
                s.send(pickle.dump(message))
        except Exception as e:
            print(f"{self.port}: Error {e}")

    def receiveMessage(self, message):
        if message.flag == 0:
            if message.uuid > self.uuid:  # pass along vote
                self.sendMessage(message)
            elif message.uuid < self.uuid:  # vote for self
                self.sendMessage(Message(self.uuid))
            else:  # declare that this node has been elected
                self.sendMessage(Message(self.uuid, 1))
        else:  # flag == 0, leader elected
            if message.uuid != self.uuid:
                self.sendMessage(message)

    def start(self):
        self.server_thread.start()

    def server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.host, self.port)
            s.listen(1)
            self.start

    def print(self):
        print(self.host, " ", self.port, " ", self.next)


class Message:
    def __init__(self, node_id, flag=0):
        self.uuid = node_id  # vote
        self.flag = flag  # 0 = election, 1 = leader chosen

    def elected(self):
        self.flag = 1


def read_config(file):
    addrs = []
    with open(file, 'r') as f:
        for line in f:
            addr = line.strip().split(',')
            addr[1] = int(addr[1])
            addrs.append(addr)
    nodes = [(Node(addrs[0][1], addrs[-1][1], addrs[0][0]))]
    for i in range(len(addrs) - 1, 0, -1):
        nodes.append(Node(addrs[i][1], addrs[i - 1][1], addrs[i][0]))
    return nodes


def run():
    config = read_config('config.txt')


run()







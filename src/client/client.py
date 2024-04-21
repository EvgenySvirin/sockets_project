import socket
import sys
from time import time
from selectors import EpollSelector, EVENT_READ


class Client:
    def __init__(self, ip: str, port: int,
                 server_ip: str, server_port: int,
                 block_size: int):
        self.ip = ip
        self.port = port

        self.server_ip = server_ip
        self.server_port = server_port

        self.socket = socket.socket(socket.AF_INET,  # Internet
                                    socket.SOCK_DGRAM)  # UDP
        self.socket.setblocking(False)
        self.socket.bind((ip, port))

        self.block_size = block_size
        self.block = (socket.inet_aton(ip) + port.to_bytes(4, 'big')).zfill(block_size)

        self.creation_time = time()
        self.bytes_received = 0

    def read(self):
        print("SAMUYU VAZHNUYU")
        data = self.socket.recv(self.block_size)
        assert self.block == data
        self.bytes_received += len(data)

    def speed_bits_seconds(self):
        return self.bytes_received * 8 / (time() - self.creation_time)

    def write(self):
        print((self.server_ip, self.server_port))
        print("SENDING")
        self.socket.sendto(self.block, (self.server_ip, self.server_port))

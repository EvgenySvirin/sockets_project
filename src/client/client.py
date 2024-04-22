import socket
import sys
from time import time
from selectors import EpollSelector, EVENT_READ


class Client:
    def __init__(self, client_ip: str, client_port: int,
                 server_ip: str, server_port: int,
                 block_size: int):
        """
        Client object contains attributes for networking, client speed evaluating
        and block of data to send.
        :param client_ip:
        :param client_port:
        :param server_ip:
        :param server_port:
        :param block_size:
        """
        self.client_ip = client_ip
        self.client_port = client_port

        self.server_ip = server_ip
        self.server_port = server_port

        self.socket = socket.socket(socket.AF_INET,  # Internet
                                    socket.SOCK_DGRAM)  # UDP
        self.socket.setblocking(False)
        self.socket.bind((client_ip, client_port))

        self.block_size = block_size
        logical_address = (socket.inet_aton(client_ip) + client_port.to_bytes(4, 'big'))
        self.block = logical_address.zfill(block_size)

        self.bytes_received = 0
        self.creation_time = time()

    def read(self) -> None:
        """
        Reads data came from server and checks that equals to sent data.
        :return:
        """
        data = self.socket.recv(self.block_size)
        assert self.block == data
        self.bytes_received += len(data)

    def speed_bits_seconds(self) -> float:
        """
        Returns average speed of the client since time of client object creation.
        """
        return self.bytes_received * 8 / (time() - self.creation_time)

    def write(self) -> None:
        """
        Writes to server data, that starts with client logical address
        and the rest filled to fit block size.
        :return:
        """
        self.socket.sendto(self.block, (self.server_ip, self.server_port))

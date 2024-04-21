import select
import socket
import subprocess
import typing
from ipaddress import ip_address

from echo_server.echo_server import EchoServer
from client.client import Client
from time import time, sleep
from threading import Thread, Lock


def create_ip_port(ip: str, port: int, label: int):
    """
    Creates address in lo.
    :param ip:
    :param port:
    :param label:
    :return:
    """
    subprocess.run(
        ["sudo", "ip", "addr", "add", f"{str(ip)}/{port}", "brd", "+", "dev", "lo", "label",
         f"lo:{label}"])


class ProgramState:
    def __init__(self,
                 ips_filename: str,
                 client_speed_limit: int,
                 echo_server_ip: str,
                 echo_server_port: int,
                 block_size: int = 125 * 4):
        """
        :param ips_filename: filename where ips situated
        :param client_speed_limit: speed for any client
        :param echo_server_ip: ip of echo server
        :param echo_server_port: port of echo server
        :param block_size: size of data blocks to send and receive
        """

        self.ips_filename = ips_filename
        self.client_speed_limit = client_speed_limit
        self.block_size = block_size

        self.client_port = echo_server_port
        self.echo_server_ip = echo_server_ip
        self.echo_server_port = echo_server_port
        self.label = 100
        create_ip_port(ip=echo_server_ip, port=echo_server_port, label=self.label)
        self.label += 1
        self.echo_server = EchoServer(server_ip=echo_server_ip, server_port=echo_server_port, block_size=block_size)

        self.ips_revision_sleep_time = 3
        self.ips_clients = dict()
        self.sockets_clients = dict()
        self.sockets = []

        self.ips_generator_enabled = False
        self.file_mutex = Lock()
        self.time_start = None

    def run(self) -> None:
        """
        Runs echo server and ips updating function in two separate threads
        and clients work function based on select.
        :return:
        """
        self.time_start = time()
        server_thread = Thread(target=self.__run_echo_server)
        server_thread.start()

        ips_file_thread = Thread(target=self.__update_ips)
        ips_file_thread.start()

        self.__run_clients(self.sockets_clients)

    def __run_clients(self, sockets_clients: typing.Dict[socket.socket, Client]) -> None:
        print("he5re")
        print(sockets_clients.keys())
        while True:
            r_sockets, w_sockets, x_sockets = select.select(sockets_clients.keys(),
                                                            sockets_clients.keys(),
                                                            sockets_clients.keys(),
                                                            1)
            print("he6re")
            print(r_sockets)

            for r in r_sockets:
                sockets_clients[r].read()
            for w in w_sockets:
                client = sockets_clients[w]
                if client.speed_bits_seconds() <= self.client_speed_limit:
                    client.write()

            for x in x_sockets:
                print("Removing socket")

                client = sockets_clients[x]
                sockets_clients.pop(x)

                self.ips_clients.pop(client.client_ip)

    def __run_echo_server(self) -> None:
        self.echo_server.run()

    def __update_ips(self) -> None:
        while True:
            try:
                with open(self.ips_filename) as file:
                    while line := file.readline():
                        try:
                            ip = str(ip_address(line.rstrip()))
                        except ValueError:
                            print(f"{line.rstrip()} is not correct ip")
                            continue

                        if ip not in self.ips_clients.keys():
                            self.__create_client(ip)
            except FileNotFoundError:
                print(f"No such file or directory {self.ips_filename}")
            sleep(self.ips_revision_sleep_time)

    def __create_client(self, ip: str) -> None:
        print("YA RODILSYA")
        create_ip_port(ip, self.client_port, self.label)
        self.label += 1
        client = Client(client_ip=ip, client_port=self.client_port,
                        server_ip=self.echo_server_ip,
                        server_port=self.echo_server_port,
                        block_size=self.block_size)
        self.ips_clients[ip] = client
        self.sockets_clients[client.socket] = client

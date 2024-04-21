import socket


class EchoServer:
    def __init__(self, server_ip: str, server_port: int, block_size: int):
        """
        :param server_ip: ip of udp server
        :param server_port: port to receive data from
        """
        self.server_ip = server_ip
        self.server_port = server_port
        self.block_size = block_size
        print("HERE0", self.server_ip, self.server_port)

        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP
        self.sock.bind((server_ip, server_port))

    def run(self) -> None:
        """
        runs echo server listening to udp_port
        :return: None
        """
        while True:
            print("HERE1", self.server_ip, self.server_port)
            data = self.sock.recv(self.block_size)

            print("HERE2")

            client_ip = socket.inet_ntoa(data[self.block_size - 8: self.block_size - 4])
            client_port = int.from_bytes(data[self.block_size - 4: self.block_size], "big")

            self.sock.sendto(data, (client_ip, client_port))
            print(f"CLIENT IP AND PORT ON SERVER: {client_ip}, {client_port}")

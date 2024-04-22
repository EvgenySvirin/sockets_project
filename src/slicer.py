import sys
from ipaddress import ip_address

from program_state import ProgramState


def start_slicer():
    args_amount = 5
    assert len(sys.argv) == args_amount, "Arguments are: ips filename, client speed, echo server ip, echo server port"
    ips_filename = sys.argv[1]
    client_speed_limit = int(sys.argv[2])

    try:
        echo_server_ip = str(ip_address(sys.argv[3]))
    except ValueError:
        print(f"{sys.argv[3]} is not correct ip, program is closing.")
        return

    echo_server_port = int(sys.argv[4])

    program_state = ProgramState(ips_filename=ips_filename,
                                 client_speed_limit_kbs=client_speed_limit,
                                 echo_server_ip=echo_server_ip,
                                 echo_server_port=echo_server_port)
    program_state.run()


if __name__ == "__main__":
    start_slicer()

import socket
import threading

print_lock = threading.Lock()


def scan_port(ip, port, type_protocol):
    sock = None

    if type_protocol == "TCP":
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    elif type_protocol == "UDP":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.settimeout(0.5)
    try:
        connect = sock.connect((ip, port))

        print_lock.acquire()
        print(type_protocol, " Port:", port, "it is open")
        print_lock.release()

        sock.close()
    except TimeoutError as e:
        pass
    except OSError as e:
        pass


def scan_tcp_ports(ip, range_port_nums):
    for i in range_port_nums:
        thread = threading.Thread(target=scan_port, args=(ip, i, "TCP"))
        thread.start()


def scan_udp_ports(ip, range_port_nums):
    for i in range_port_nums:
        thread = threading.Thread(target=scan_port, args=(ip, i, "UDP"))
        thread.start()


def start_port_scanner(ip, range_port_nums):
    scan_tcp_ports(ip, range_port_nums)
    scan_udp_ports(ip, range_port_nums)


if __name__ == '__main__':
    start_port_scanner("127.0.0.1", range(1000))


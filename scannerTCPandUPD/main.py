import socket
import threading


def scan_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    try:
        connect = sock.connect((ip, port))
        print("Port:", port, "it is open")
        sock.close()
    except Exception as e:
        pass


def scan_ports(ip, range_port_nums):
    for i in range_port_nums:
        thread = threading.Thread(target=scan_port, args=(ip, i))
        thread.start()


if __name__ == '__main__':
    scan_ports("127.0.0.1", range(500))


import binascii
import socket
import sys

from Cache import *
from DnsResponse import *


def check_cache(name_domain, msg_type, cache):
    rec = cache.get_record(name_domain, msg_type)
    message = ""

    if rec is not None:
        current_time = int(round(time()))
        if current_time - rec.time_record >= rec.ttl:
            message = "recording time expired"
            cache.remove_record(rec.name_domain, rec.resp_type)
            rec = None
        else:
            message = "data from cache"
    return rec, message


def proceed_query(sock, cache, ip_target_server):
    sock.settimeout(1)
    data = ""

    while True:
        try:
            data, addr = sock.recvfrom(4096)
            data = binascii.hexlify(data).decode("utf-8")
            break
        except TimeoutError:
            return

    dns_request = DnsRequest(data)

    if len(dns_request.questions) > 0:
        name_domain = dns_request.questions[0].name
        msg_type = dns_request.questions[0].q_type
        rec, message = check_cache(name_domain, msg_type, cache)
        if message != "":
            print(message)
        if rec is not None:
            print(rec.get_string())
            print('.............................................................')
            return

    print('Request sent to server')
    data = data.replace("\n", "").replace(" ", "")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock_for_request:
        sock_for_request.settimeout(2)
        try:
            sock_for_request.sendto(binascii.unhexlify(data), (ip_target_server, 53))
            response_from_server, _ = sock_for_request.recvfrom(4096)
            response_from_server = binascii.hexlify(response_from_server).decode("utf-8")
        except Exception as e:
            print(e)
            result = None
        else:
            result = response_from_server

    if result is not None:
        response = DnsResponse(result)
        answer = response.get_answer()
        cache.add_record(answer.name, answer.a_type, response.get_data_answers(), answer.time)
        print(cache.get_record(answer.name, answer.a_type).get_string())
        sock.sendto(binascii.unhexlify(result), addr)

    print('.............................................................')


def start_server(ip_target_server):
    ip = '127.0.0.1'
    port = 53
    cache = Cache()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))

    print('Server launched on ' + ip + ' port ' + str(port))
    print('.............................................................')

    while True:
        try:
            proceed_query(sock, cache, ip_target_server)
        except KeyboardInterrupt:
            print("stop server")
            sys.exit(0)


if __name__ == '__main__':
    args = sys.argv
    target_ip = "8.8.8.8"

    if len(args) > 1:
        target_ip = args[1]
    print("ip target server " + target_ip)
    start_server(target_ip)

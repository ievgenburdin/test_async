import socket
import time

from threading import Thread


def make_request():
    start_time = time.time()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8000))
    request_data = b'I need your clothes, boots and a motorcycle.'
    print("Client: ", request_data)
    sock.send(request_data)
    responce_data = sock.recv(100)
    print("Server: ", responce_data)
    sock.close()
    end_time = time.time()
    print("Close connection", end_time - start_time)


def do_request_forever():
    while True:
        make_request()


if __name__ == "__main__":
    t1 = Thread(target=do_request_forever)
    t2 = Thread(target=do_request_forever)
    t3 = Thread(target=do_request_forever)
    t1.start()
    t2.start()
    t3.start()

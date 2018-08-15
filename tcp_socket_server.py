import socket
import asyncio
from collections import deque
from threading import Thread

tasks = deque()
stopped = {}


def some_long_process():
    print("start slow function")
    process_time = 5.0
    yield from asyncio.sleep(process_time)
    print("end slow function")


class SocketServer:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port

    def do_some_logic(self, data):
        some_long_process()
        if data == b'I need your clothes, boots and a motorcycle.':
            data = b'Sorry. You are not terminator.'
        else:
            data = b'Simple response data.'
        return data

    def run(self, host=None, port=None):
        # Create a TCP/IP socket
        if not host:
            host = self.host
        if not port:
            port = self.port

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        server_address = (host, port)
        print('starting up on %s port %s' % server_address)
        sock.bind(server_address)
        # Listen for incoming connections
        sock.listen(1)

        while True:
            # Wait for a connection
            print('waiting for a connection')
            connection, client_address = sock.accept()
            try:
                print('connection from', client_address)
                # Get data process it and transmit responce
                while True:
                    data = connection.recv(100)
                    if data:
                        print('received "%s"' % data)
                        data = self.do_some_logic(data)
                        print('sending "%s"' % data)
                        connection.sendall(data)
                    else:
                        print('Connection are closed. No more data from', client_address)
                        break
            finally:
                # Clean up the connection
                connection.close()


app = SocketServer()

if __name__ == "__main__":
    app = SocketServer()
    app.run()



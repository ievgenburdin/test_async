import socket
import select
import time
import queue

from collections import deque
from threading import Thread


def some_long_process():
    print("start slow function")
    process_time = 5.0
    time.sleep(process_time)
    print("end slow function")


class SocketServer:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(0)
        self.inputs = [self.server]
        self.outputs = []
        self.exceptions = []
        self.message_queues = {}

    def run(self, host=None, port=None):
        # Create a TCP/IP socket
        if not host:
            host = self.host
        if not port:
            port = self.port
        # Bind the socket to the port
        server_address = (host, port)
        print('starting up on %s port %s' % server_address)
        self.server.bind(server_address)
        # Listen for incoming connections
        self.server.listen(5)
        print('waiting for a connection')
        self.accept_connections()

    @staticmethod
    def do_some_logic(data):
        if data == b'I need your clothes, boots and a motorcycle.':
            data = b'Sorry. You are not terminator.'
        else:
            data = b'Simple response data.'
        return data

    def accept_connections(self):
        # Wait for a connection
        while True:
            readable, writable, exceptional = select.select(
                self.inputs, self.outputs, self.inputs)

            for s in readable:
                if s is self.server:
                    connection, client_address = s.accept()
                    connection.setblocking(0)
                    self.inputs.append(connection)
                    self.message_queues[connection] = queue.Queue()

                else:
                    data = s.recv(1024)
                    if data:
                        if s not in self.outputs:
                            self.outputs.append(s)
                        print('received "%s"' % data)
                        # Meke some big blocking logic
                        resp_data = self.do_some_logic(data)
                        self.message_queues[s].put(resp_data)
                    else:
                        if s in self.outputs:
                            self.outputs.remove(s)
                        self.inputs.remove(s)
                        s.close()
                        del self.message_queues[s]

            for s in writable:
                print(len(self.inputs), len(self.outputs), len(self.inputs))
                try:
                    next_msg = self.message_queues.get(s)
                    if next_msg:
                        data = next_msg.get_nowait()
                    print('sending "%s"' % data)
                except queue.Empty:
                    self.outputs.remove(s)
                else:
                    s.sendall(data)

            for s in exceptional:
                self.inputs.remove(s)
                if s in self.outputs:
                    self.outputs.remove(s)
                s.close()
                del self.message_queues[s]


if __name__ == "__main__":
    app = SocketServer()
    app.run()



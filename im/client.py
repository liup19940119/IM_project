import socket
from select import epoll
import select,  threading
import json
import sys


class ClientCallback:
    def on_connect(self, *args, **kwargs):
        pass

    def on_disconnect(self, *args, **kwargs):
        pass

    def on_message(self, *args, **kwargs):
        pass

    def on_login(self, contacts):
        pass


class Client(threading.Thread):

    def __init__(self, callback=None, *args, **kwargs):
        super().__init__()
        self.message = {}
        self.callback = callback  # callback是一个ClientCallback对象
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.setDaemon(True)
        try:
            self.sock.connect(('10.1.0.117', 3000))
            self.callback.on_connect()
        except:
            self.callback.on_disconnect()

    def run(self):
        ep = epoll()
        ep.register(self.sock.fileno(), select.EPOLLIN)
        while True:
            try:
                events = ep.poll()
                for fd, ev in events:
                    if fd == self.sock.fileno():
                        data = self.sock.recv(4096)
                        if data is None or len(data) == 0:
                            raise ConnectionRefusedError
                        data = data.decode('utf-8')
                        data = json.loads(data)
                        # print(data)
                        if data['code'] == 'Register success':
                            self.callback.on_register()

                        if data['code'] == 'Login success':
                            # print(data)
                            self.callback.on_login(data['contact'])

                        if data['code'] == 'no':
                            return data['code']

                        if data['code'] == 1:
                            # print(data)
                            self.callback.on_message(data['message'], data['sender'])

            except ConnectionRefusedError:
                break
        ep.unregister(self.sock.fileno())
        self.sock.close()

    def send_message(self, username, message):
        data = {'command': 'message', 'receiver': username, 'message': message}
        self.sock.send(json.dumps(data).encode('utf-8'))

    def login(self, username, password):
        data = {'command': 'login', 'username': username, 'password': password}
        self.sock.send(json.dumps(data).encode('utf-8'))

    def register(self, username, password, mobile, sex):
        data = {'command': 'register', 'username': username, 'password': password, 'mobile': mobile, 'sex': sex}
        self.sock.send(json.dumps(data).encode('utf-8'))



import socket
from select import poll
import select, threading
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
            self.sock.connect(('10.1.0.230', 4000))
            self.callback.on_connect()
        except:
            self.callback.on_disconnect()

    def run(self):
        ep = poll()
        ep.register(self.sock.fileno(), select.POLLIN)
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
                        print(data)
                        if data['code'] == 1002 or data['code'] == 1001 or data['code'] == 1003:
                            # register
                            self.callback.on_register(data)

                        if data['code'] == 2002:
                            # login success
                            self.callback.on_login(data)

                        if data['code'] == 2001:
                            # login failure
                            self.callback.not_login(data)

                        if data['code'] == 3001 or data['code'] == 3002:
                            # send message
                            self.callback.on_message(data['message'], data['sender'], data['receiver'])

                        if data['code'] == 4001 or data['code'] == 4002 or data['code'] == 4003:
                            # add user
                            self.callback.on_add_user(data)

                        if data['code'] == 5001:
                            self.callback.on_show_info(data)

            except ConnectionRefusedError:
                break
        ep.unregister(self.sock.fileno())
        self.sock.close()

    def send_message(self, receiver_name, message):
        data = {'command': 'message', 'receiver': receiver_name, 'message': message}
        self.sock.send(json.dumps(data).encode('utf-8'))

    def login(self, username, password):
        data = {'command': 'login', 'username': username, 'password': password}
        self.sock.send(json.dumps(data).encode('utf-8'))

    def register(self, username, password, mobile, sex):
        data = {'command': 'register', 'username': username, 'password': password, 'mobile': mobile, 'sex': sex}
        self.sock.send(json.dumps(data).encode('utf-8'))

    def add_user(self, add_name):
        data = {'command': 'add', 'add_name': add_name}
        self.sock.send(json.dumps(data).encode('utf-8'))

    def show_info(self):
        data = {'command': 'show_info'}
        self.sock.send(json.dumps(data).encode('utf-8'))

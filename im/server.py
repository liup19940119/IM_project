import json
import socket, select
import webbrowser
from select import poll
import threading
import requests
import pymysql


class Handler:
    online_user_sock = {}

    def __init__(self, data, c_sock):
        # super().__init__(data, c_sock)
        self.contacts = []
        self.data = data
        self.c_sock = c_sock
        self.c_sock_name = None
        self.conn_db = pymysql.connect(host='127.0.0.1',
                                       port=3306,
                                       user='liupeng',
                                       password='123456',
                                       database='userim',
                                       cursorclass=pymysql.cursors.DictCursor,
                                       autocommit=1, )

        self.handle()

    def handle(self):
        for k, v in Handler.online_user_sock.items():
            if self.c_sock == v:
                self.c_sock_name = k
                break

        data = self.data
        data = json.loads(data.decode('utf-8'))
        if data['command'] == 'login':
            Handler.online_user_sock[data['username']] = self.c_sock
            self.login(data)

        if data['command'] == 'register':
            self.register(data)

        if data['command'] == 'message':
            self.message(data)

        if data['command'] == 'add':
            self.add_user(data)

        if data['command'] == 'show_info':
            self.show_info()

    def login(self, data):
        username = data['username']
        password = data['password']

        cursor = self.conn_db.cursor()
        if cursor.execute("select * from user where username='{}' and password='{}'".format(username, password)):
            cursor.execute("select username,avatar from user where id in "
                           "(select contacts_id from contact where user = '{}')".format(username))
            result = cursor.fetchall()
            for c in result:
                self.contacts.append({'username': c['username'], 'avatar': c['avatar']})
            send_data = {'code': 2002, 'contacts': self.contacts, 'username': username}
            return self.c_sock.send(json.dumps(send_data).encode('utf-8'))

        send_data = {'code': 2001, 'error_message': 'User Not Exist or Input Error'}
        # print('==', send_data)
        self.c_sock.send(json.dumps(send_data).encode('utf-8'))

    def register(self, data):
        response = requests.request('get', 'http://127.0.0.1:8000/imuser/register', params=data)
        # print(response.content)
        self.c_sock.send(response.content)

    def message(self, data):
        receiver = data['receiver']
        if receiver in Handler.online_user_sock.keys():
            receiver_sock = Handler.online_user_sock[receiver]
            data = {'code': 3001, 'sender': receiver, 'receiver': self.c_sock_name, 'message': data['message']}
            # print('===send_data:', data, receiver_sock)
            receiver_sock.send(json.dumps(data).encode('utf-8'))
        else:
            data = {'code': 3002, 'sender': '对方', 'message': '检测到对方未上线', 'receiver': self.c_sock_name}
            self.c_sock.send(json.dumps(data).encode('utf-8'))

    def add_user(self, data):
        data['username'] = self.c_sock_name
        response = requests.request('get', 'http://127.0.0.1:8000/imuser/add_user', params=data)
        self.c_sock.send(response.content)

    def show_info(self):
        data = {'code': 5001, 'username': self.c_sock_name}
        self.c_sock.send(json.dumps(data).encode('utf-8'))


class Server(threading.Thread):
    def __init__(self):
        super().__init__()
        self.s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.s_sock.setblocking(False)
        self.s_sock.bind(('10.1.0.230', 4000))
        self.s_sock.listen(1024)

        self.fd2obj = {}

    def run(self):
        epoll = poll()
        epoll.register(self.s_sock.fileno(), select.EPOLLIN)
        while True:
            events = epoll.poll()
            for fd, ev in events:
                if self.s_sock.fileno() == fd:
                    if ev == select.EPOLLIN:
                        c_sock, addr = self.s_sock.accept()
                        epoll.register(c_sock.fileno(), select.EPOLLIN)
                        self.fd2obj[c_sock.fileno()] = c_sock
                        print('{} has collected'.format(addr))

                else:
                    if ev == select.EPOLLIN:
                        c_sock = self.fd2obj[fd]
                        try:
                            data = c_sock.recv(4096)
                            if data == None or len(data) == 0:
                                raise Exception

                            Handler(data, c_sock)

                        except Exception:
                            del self.fd2obj[fd]
                            epoll.unregister(fd)
                            c_sock.close()


server = Server()
server.start()

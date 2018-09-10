import tkinter
from tkinter import messagebox
import sys, queue

from pythonliu.im.client import Client, ClientCallback
from pythonliu.im.test_message import MessageWindow


class Signal:
    def __init__(self, tk):
        self.tk = tk
        self.queue = queue.Queue()
        assert isinstance(self.tk, tkinter.Tk)
        self.tk.after(10, self._read_from_queue)
        self._sig_map = {}

    def register_signal(self, signal, func):
        assert callable(func)
        self._sig_map[signal] = func

    def send_signal(self, signal):
        self.queue.put(signal)

    def _read_from_queue(self):
        try:
            signal = self.queue.get_nowait()
            func = self._sig_map[signal]
            func()
        except:
            pass
        self.tk.after(10, self._read_from_queue)


class LoginWindow(ClientCallback):
    def __init__(self):
        self.client = None
        self.root = tkinter.Tk()
        self.signal = Signal(self.root)
        self.signal.register_signal("login", self.show_message_window)
        self.root.title('登录')
        self.root.geometry('400x200+100+100')

        self.varName = tkinter.StringVar(value='')
        self.varPwd = tkinter.StringVar(value='')
        self.labelName = tkinter.Label(self.root, text='User Name:', justify=tkinter.RIGHT, width=80)
        self.labelName.place(x=10, y=5, width=80, height=50)
        self.entryName = tkinter.Entry(self.root, width=80, textvariable=self.varName)
        self.entryName.place(x=100, y=5, width=250, height=50)

        self.labelPwd = tkinter.Label(self.root, text='User Pwd:', justify=tkinter.RIGHT, width=80)
        self.labelPwd.place(x=10, y=80, width=80, height=50)
        self.entryPwd = tkinter.Entry(self.root, show='*', width=80, textvariable=self.varPwd)
        self.entryPwd.place(x=100, y=80, width=250, height=50)

        self.buttonOk = tkinter.Button(self.root, text='Login', command=self.login)
        self.buttonOk.place(x=100, y=150, width=50, height=30)
        self.buttonCancel = tkinter.Button(self.root, text='Cancel', command=self.cancel)
        self.buttonCancel.place(x=300, y=150, width=50, height=30)

        self.client = Client(self)
        self.client.start()

        self.root.mainloop()

    def login(self):
        username = self.entryName.get()
        password = self.entryPwd.get()

        if not (username and password):
            messagebox.showinfo('Python tkinter', message='Error')
            return

        self.client.login(username, password)

    def show_message_window(self):
        self.root.destroy()
        global messageWin
        messageWin = MessageWindow(self.contacts, self.client)

    def on_login(self, contacts):
        setattr(self, "contacts", contacts)
        self.signal.send_signal("login")
        # print('=================', self.contacts)

    def on_connect(self):
        pass

    def on_disconnect(self):
        messagebox.showinfo('服务器无响应', message='Can\'t connect to server')

    def cancel(self):
        sys.exit(0)

# login = LoginWindow()

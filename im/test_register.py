import tkinter
import sys, time
from tkinter import messagebox

from client import Client, ClientCallback
from test_login import LoginWindow, Signal


class RegisterWindow(ClientCallback):
    def __init__(self):
        self.result = None
        self.root = tkinter.Tk()
        self.signal = Signal(self.root)
        self.signal.register_signal('register', self.get_register_result)
        self.root.title('注册')
        self.root.geometry('380x350+400+100')

        self.varName = tkinter.StringVar(value='')
        self.varPwd = tkinter.StringVar(value='')
        self.varMob = tkinter.StringVar(value='')
        self.varSex = tkinter.IntVar()

        self.labelName = tkinter.Label(self.root, text='User Name:', justify=tkinter.RIGHT, width=80)
        self.labelName.place(x=10, y=5, width=80, height=50)
        self.entryName = tkinter.Entry(self.root, width=80, textvariable=self.varName)
        self.entryName.place(x=100, y=5, width=250, height=50)

        self.labelMob = tkinter.Label(self.root, text='Mobile:', justify=tkinter.RIGHT, width=80)
        self.labelMob.place(x=10, y=80, width=80, height=50)
        self.entryMob = tkinter.Entry(self.root,  width=80, textvariable=self.varMob)
        self.entryMob.place(x=100, y=80, width=250, height=50)

        self.labelPwd = tkinter.Label(self.root, text='User Pwd:', justify=tkinter.RIGHT, width=80)
        self.labelPwd.place(x=10, y=160, width=80, height=50)
        self.entryPwd = tkinter.Entry(self.root,  width=80, textvariable=self.varPwd)
        self.entryPwd.place(x=100, y=160, width=250, height=50)

        self.labelSex = tkinter.Label(self.root, text='Sex:', justify=tkinter.RIGHT, width=80)
        self.labelSex.place(x=10, y=240, width=80, height=50)

        self.entryMale = tkinter.Radiobutton(self.root, text='Male', value=1, variable=self.varSex)
        self.entryMale.place(x=100, y=240, width=80, height=50)
        self.entryFemale = tkinter.Radiobutton(self.root, text='Female', value=2, variable=self.varSex)
        self.entryFemale.place(x=200, y=240, width=80, height=50)

        self.buttonOk = tkinter.Button(self.root, text='Register', command=self.submit)
        self.buttonOk.place(x=60, y=300, width=70, height=30)
        self.buttonCancel = tkinter.Button(self.root, text='Cancel', command=self.cancel)
        self.buttonCancel.place(x=270, y=300, width=70, height=30)

        self.client = Client(self)
        self.client.start()

        self.root.mainloop()

    def submit(self):
        username = self.entryName.get()
        password = self.entryPwd.get()
        mobile = self.entryMob.get()
        if self.varSex.get() == 1:
            sex = 'Male'
        else:
            sex = 'Female'

        if not (username and password and mobile and sex):
            messagebox.showinfo('错误信息', message='Every item cannot be empty')
            return

        self.client.register(username, password, mobile, sex)

    def get_register_result(self):
        if self.result['code'] == 1002:
            messagebox.showinfo('注册成功', message=self.result['error_message'])
            self.root.destroy()
            global loginWin
            loginWin = LoginWindow()
        else:

            messagebox.showinfo('注册失败', message=self.result['error_message'])

    def on_connect(self):
        pass

    def on_disconnect(self):
        messagebox.showinfo('服务器无响应', message='Can\'t connect to server')

    def on_register(self, data):
        self.result = data
        self.signal.send_signal('register')

    def cancel(self):
        sys.exit(0)


# rw = RegisterWindow()



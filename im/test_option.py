import tkinter
import sys

from test_login import LoginWindow
from test_register import RegisterWindow


class OptionWindow:

    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title('聊天选项菜单')
        self.window.geometry('300x300+500+200')

        self.loginButton = tkinter.Button(self.window, text='login', command=self.login_event)
        self.registerButton = tkinter.Button(self.window, text='register', command=self.register_event)
        self.exitButton = tkinter.Button(self.window, text='exit', command=self.exit_event)

        self.loginButton.place(x=120, y=40, width=60, height=40)
        self.registerButton.place(x=120, y=120, width=60, height=40)
        self.exitButton.place(x=120, y=200, width=60, height=40)

        self.window.mainloop()

    def login_event(self):
        self.window.destroy()
        global loginWin
        loginWin = LoginWindow()

    def register_event(self):
        self.window.destroy()
        global registerWin
        registerWin = RegisterWindow()

    def exit_event(self):
        sys.exit(0)


option = OptionWindow()




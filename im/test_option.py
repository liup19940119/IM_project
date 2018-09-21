import tkinter
import sys
import webbrowser

from PIL import Image
from tkinter import PhotoImage
from test_login import LoginWindow
from test_register import RegisterWindow


class OptionWindow:

    def __init__(self):
        self.window = tkinter.Tk()
        self.cv = tkinter.Canvas(self.window, bg='black')
        self.cv.create_rectangle(0, 0, 300, 300, outline='white', width=5)
        self.cv.place(x=300, y=0, width=300, height=300)
        self.right_frame = tkinter.Frame(master=self.window, width=300, height=300, bg='green')
        self.right_frame.place(x=0, y=0)
        self.window.title('聊天选项菜单')
        self.window.geometry('600x300+500+200')

        self.loginButton = tkinter.Button(self.cv, text='登录', command=self.login_event)
        self.registerButton = tkinter.Button(self.cv, text='注册', command=self.register_event)
        self.exitButton = tkinter.Button(self.cv, text='退出', command=self.exit_event)
        self.web_registerButton = tkinter.Button(self.cv, text='网页注册', command=self.web_register_event)

        self.loginButton.place(x=120, y=40, width=60, height=40)
        self.registerButton.place(x=50, y=220, width=60, height=40)
        self.exitButton.place(x=120, y=120, width=60, height=40)
        self.web_registerButton.place(x=200, y=220, width=60, height=40)

        # img_jpg = Image.open('111.jpg')
        img = PhotoImage(master=self.right_frame, file='222.gif')
        self.label_img = tkinter.Label(master=self.right_frame, image=img)
        self.label_img.pack()

        self.window.mainloop()

    def login_event(self):
        self.window.destroy()
        global loginWin
        loginWin = LoginWindow()

    def register_event(self):
        self.window.destroy()
        global registerWin
        registerWin = RegisterWindow()

    def web_register_event(self):
        url = 'http://127.0.0.1:8000/imuser/web_register/'
        webbrowser.open(url, new=2, autoraise=True)

    def exit_event(self):
        sys.exit(0)


option = OptionWindow()




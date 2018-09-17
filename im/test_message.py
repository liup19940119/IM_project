from tkinter import *
import time
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from client import ClientCallback


class MessageWindow(ClientCallback):
    def __init__(self, data, client=None):
        self.data = data
        self.client = client
        self.client.callback = self
        self.add_win = None
        self.user_text = None
        self.root = Tk()
        self.root.title('聊天中')
        self.root.geometry('800x520+300+100')

        # 创建几个frame作为容器
        self.text_msglist = ScrolledText(width=75, height=20, bg='white')
        self.text_msg = ScrolledText(width=97, height=6)
        frame_left_bottom = Frame(width=200, height=200)
        frame_right = Frame(width=200, height=200, bg='green')

        self.button_sendmsg = Button(frame_left_bottom, text='发送', command=self.sendmessage)
        self.button_add = Button(frame_left_bottom, text='添加好友', command=self.show_add_win)

        # contact list
        self.scroLianxi = Scrollbar(frame_right, troughcolor="green", width=22)
        self.list_contact = Listbox(frame_right, width=21, height=15, selectmode=EXTENDED, bg='green')
        self.list_contact.pack(side=LEFT)
        self.scroLianxi.pack(side=RIGHT, fill=Y)

        for u in self.data:
            self.list_contact.insert(END, str(u))

        self.scroLianxi.config(command=self.list_contact.yview)  # scrollbar滚动时listbox同时滚动
        self.list_contact.config(yscrollcommand=self.scroLianxi.set)
        # self.list_contact.bind('<Button-1>', self.callback)

        # 创建一个message绿色的tag
        self.text_msglist.tag_config('green', foreground='#008B00')

        # 使用grid设置各个容器位置
        self.text_msglist.grid(row=0, column=0, padx=2, pady=5)
        frame_right.grid(row=0, column=1, padx=4, pady=5)
        self.text_msg.grid(row=1, columnspan=2, padx=2, pady=5)
        frame_left_bottom.grid(row=2, columnspan=2)

        # 把元素填充进frame
        self.button_sendmsg.place(x=10, y=5)
        self.button_add.place(x=100, y=5)

        # 主事件循环
        self.root.mainloop()

    # 发送按钮事件
    def sendmessage(self):
        # 在聊天内容上方加一行 显示发送人及发送时间
        username = self.callback(event='<Button-1>')
        self.root.title('与{}聊天中'.format(username))
        msgcontent_to = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' 我对' + username + '说：' + '\n '

        self.text_msglist.insert(END, msgcontent_to, 'green')
        message = self.text_msg.get('0.0', END)
        self.text_msglist.insert(END, message)
        self.text_msg.delete('0.0', END)

        # print(username, '==', message)
        self.client.send_message(username, message)

    def show_add_win(self):
        self.add_win = Toplevel()
        self.add_win.title('请输入好友名字')
        self.add_win.geometry('200x80+620+550')
        self.user_text = Entry(self.add_win)
        btn = Button(self.add_win, text='添加', command=self.add_user)

        btn.pack(side=BOTTOM)
        self.user_text.pack(side=TOP)

    def add_user(self):
        username = self.user_text.get()
        print('=', username)
        self.add_win.destroy()
        self.client.add_user(username)

    def callback(self, event):
        self.list_contact.curselection()
        user = self.list_contact.get(ACTIVE)
        return user

    def on_message(self, message, sender):
        if sender == '对方':
            self.text_msglist.insert(END, message + '\n')
        else:
            msgcontent_from = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + sender + ' 对我 ' + '说：' + '\n '
            self.text_msglist.insert(END, msgcontent_from)
            self.text_msglist.insert(END, message + '\n')

    def on_add_user(self, message, username):
        messagebox.showinfo('添加结果', message=message)
        if message == '添加成功':
            self.list_contact.insert(END, username)
# messageWin = MessageWindow(data)

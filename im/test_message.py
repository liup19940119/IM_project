import webbrowser
from tkinter import *
import time
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from client import ClientCallback
import sqlite3


class MessageWindow(ClientCallback):
    def __init__(self, data, username, client=None):
        self.username = username
        self.data = data
        self.client = client
        self.client.callback = self
        self.add_win = None
        self.user_text = None
        self.root = Tk()
        self.root.title('{}的聊天窗口'.format(self.username))
        self.root.geometry('800x520+300+100')

        # 创建几个frame作为容器
        self.text_msglist = ScrolledText(width=75, height=20, bg='white')
        self.text_msg = ScrolledText(width=97, height=6)
        frame_left_bottom = Frame(width=800, height=200)
        frame_right = Frame(width=200, height=200, bg='green')

        # 创建按钮并绑定事件
        self.button_sendmsg = Button(frame_left_bottom, text='发送', command=self.sendmessage)
        self.button_add = Button(frame_left_bottom, text='添加好友', command=self.show_add_win)
        self.button_info = Button(frame_left_bottom, text='个人信息', command=self.show_info)
        self.button_message = Button(frame_left_bottom, text='查看历史消息', command=self.show_message)

        # contact list
        self.scroLianxi = Scrollbar(frame_right, troughcolor="green", width=22)
        self.list_contact = Listbox(frame_right, width=21, height=15, selectmode=EXTENDED, bg='green')
        self.list_contact.pack(side=LEFT)
        self.scroLianxi.pack(side=RIGHT, fill=Y)

        # 联系人列表添加联系人
        for u in self.data:
            self.list_contact.insert(END, u['username'])

        # 将历史消息添加到message框
        self.show_default_msg()

        # scrollbar滚动时listbox同时滚动
        self.scroLianxi.config(command=self.list_contact.yview)
        self.list_contact.config(yscrollcommand=self.scroLianxi.set)
        # self.list_contact.bind('<Button-1>', self.callback)

        # 创建一个message绿色的tag
        self.text_msglist.tag_config('green', foreground='#008B00')

        # 使用grid设置各个容器位置
        self.text_msglist.grid(row=0, column=0, padx=2, pady=5)
        frame_right.grid(row=0, column=1, padx=4, pady=5)
        self.text_msg.grid(row=1, columnspan=2, padx=2, pady=5)
        frame_left_bottom.grid(row=2, columnspan=2)

        # 把按钮填充进frame
        self.button_sendmsg.place(x=350, y=5)
        self.button_add.place(x=620, y=5)
        self.button_info.place(x=710, y=5)
        self.button_message.place(x=5, y=5)

        # 主事件循环
        self.root.mainloop()

    def show_default_msg(self, num=5):
        con = sqlite3.connect('message.db')
        try:
            result = con.execute("select * from {} limit {}".format(self.username + '_tb', num))
            for c in result:
                sender = c[0]
                message = c[2]
                msg_time = c[3]
                if sender != self.username:
                    msg = msg_time + sender + '对我' + '说：' + '\n '

                else:
                    msg = msg_time + '我对' + sender + '说：' + '\n '

                self.text_msglist.insert(END, msg, 'green')
                self.text_msglist.insert(END, message)

            con.commit()
            con.close()
        except:
            pass

    # 发送按钮事件
    def sendmessage(self):
        # 在聊天内容上方加一行 显示发送人及发送时间
        receiver_name = self.callback(event='<Button-1>')
        # self.root.title('与{}聊天中'.format(username))
        msgcontent_to = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' 我对' + receiver_name + '说：' + '\n '
        message = self.text_msg.get('0.0', END)

        # 将发送的消息加入到sqlite
        con = sqlite3.connect('message.db')
        con.execute(
            "create table IF NOT EXISTS {}(sender varchar(50), receiver varchar(50), message varchar(255), "
            "msg_time varchar(100))".format(self.username + '_tb'))
        messageTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        con.execute("insert into {} values ('{}', '{}', '{}', '{}')"
                    .format((self.username + '_tb'), self.username, receiver_name, message, str(messageTime)))
        con.commit()
        con.close()

        self.text_msglist.insert(END, msgcontent_to, 'green')
        self.text_msglist.insert(END, message)
        self.text_msg.delete('0.0', END)

        self.client.send_message(receiver_name, message)

    # 添加按钮时间
    def show_add_win(self):
        self.add_win = Toplevel()
        self.add_win.title('请输入好友名字')
        self.add_win.geometry('200x80+620+550')
        self.user_text = Entry(self.add_win)
        btn = Button(self.add_win, text='添加', command=self.add_user)

        btn.pack(side=BOTTOM)
        self.user_text.pack(side=TOP)

    def add_user(self):
        add_name = self.user_text.get()
        print('=', add_name)
        self.add_win.destroy()
        self.client.add_user(add_name)

    # 个人信息按钮事件
    def show_info(self):
        self.client.show_info()

    # 查看历史消息事件
    def show_message(self):
        history_msg_win = Toplevel()
        history_msg_win.title('{}的历史消息记录'.format(self.username))
        history_msg_win.geometry('550x500+500+100')
        msglist = ScrolledText(master=history_msg_win, width=65, height=28)
        msglist.grid(row=0, column=0, padx=2, pady=5)

        con = sqlite3.connect('message.db')
        try:
            result = con.execute("select * from {}".format(self.username + '_tb'))
            for c in result:
                sender = c[0]
                message = c[2]
                msg_time = c[3]
                if sender != self.username:
                    msg = msg_time + sender + '对我' + '说：' + '\n '

                else:
                    msg = msg_time + '我对' + sender + '说：' + '\n '

                msglist.insert(END, msg, 'green')
                msglist.insert(END, message)

            con.commit()
            con.close()
        except:
            pass

    def callback(self, event):
        self.list_contact.curselection()
        user = self.list_contact.get(ACTIVE)
        return user

    def on_message(self, message, sender, receiver):
        if sender == '对方':
            messagebox.showinfo('未在线', message=message)
            # self.text_msglist.insert(END, message + '\n')
        else:
            con = sqlite3.connect('message.db')
            con.execute(
                "create table IF NOT EXISTS {}(sender varchar(50), receiver varchar(50), message varchar(255), "
                "msg_time varchar(100))".format(sender + '_tb'))
            messageTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            con.execute("insert into {} values ('{}', '{}', '{}', '{}')"
                        .format((sender + '_tb'), receiver, sender, message, str(messageTime)))
            con.commit()
            con.close()

            msgcontent_from = time.strftime("%Y-%m-%d %H:%M:%S",
                                            time.localtime()) + ' ' + receiver + ' 对我 ' + '说：' + '\n '
            self.text_msglist.insert(END, msgcontent_from)
            self.text_msglist.insert(END, message + '\n')

    def on_add_user(self, data):
        if data['code'] == 4001:
            self.list_contact.insert(END, data['add_name'])
            messagebox.showinfo('添加结果', message=data['message'])
        else:
            messagebox.showinfo('添加结果', message=data['message'])

    def on_show_info(self, data):
        url = 'http://127.0.0.1:8000/imuser/show_info?username={}'.format(data['username'])
        webbrowser.open(url, new=2, autoraise=True)


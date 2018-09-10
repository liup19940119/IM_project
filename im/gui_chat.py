from PyQt5.QtWidgets import QApplication, \
    QWidget, \
    QPushButton, \
    QTextEdit, \
    QLabel, \
    QMessageBox

import sys


class ChatWindow(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.chat()

    def chat(self):
        self.setGeometry(200, 200, 800, 500)
        self.setWindowTitle('聊天窗口')

        self.lableChat = QTextEdit(self)
        self.lableMessage = QtGui.QTextLayout()
        self.lableContact = QLabel(self)

        # self.lableMessage.setText('聊天中')


        self.lableChat.setGeometry(0, 300, 600, 200)
        # self.lableMessage.setGeometry(0, 0, 600, 300)
        self.lableContact.setGeometry(700, 200, 300, 500)

        self.show()


app = QApplication(sys.argv)
c = ChatWindow()
sys.exit(app.exec_())
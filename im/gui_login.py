from PyQt5.QtWidgets import QApplication, \
    QWidget, \
    QProgressBar, \
    QPushButton, \
    QTextEdit, \
    QLabel, \
    QMessageBox

import sys
from pythonliu.im.client import Client


class LoginWindow(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 500, 300)
        self.setWindowTitle("登录")
        self.labelUsername = QLabel(self)
        self.labelUsername.setText("用户名:")
        self.labelPasswd = QLabel(self)
        self.labelPasswd.setText("密码:")

        self.labelUsername.setGeometry(50, 100, 100, 30)
        self.labelPasswd.setGeometry(50, 150, 100, 30)

        self.txtUsername = QTextEdit(self)
        self.txtUsername.setGeometry(160, 100, 300, 30)

        self.txtPasswd = QTextEdit(self)
        self.txtPasswd.setGeometry(160, 150, 300, 30)

        self.btnCancel = QPushButton(self)
        self.btnCancel.setText("取消")
        self.btnCancel.setGeometry(160, 200, 100, 50)

        self.btnLogin = QPushButton(self)
        self.btnLogin.setText("登录")
        self.btnLogin.setGeometry(310, 200, 100, 50)

        self.btnCancel.clicked.connect(self.exit)
        self.btnLogin.clicked.connect(self.login)

        self.show()

    def login(self):
        username = self.txtUsername.toPlainText().strip()
        password = self.txtPasswd.toPlainText().strip()

        if not (username and password):
            m = QMessageBox(self)
            m.setText("用户名或密码不能为空")
            m.show()
            return
        # print(password, username)
        client = Client(username, password)
        client.start()
        return username, password

    def exit(self):
        sys.exit(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LoginWindow()

    sys.exit(app.exec_())

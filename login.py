from PySide2.QtWidgets import  QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QPixmap
# import main

import sqls # sqls是自己写的模块

class LogInWindow():
    def __init__(self):
        self.ui = QUiLoader().load('LogIn.ui')
        self.ui.setFixedSize(self.ui.width(), self.ui.height())
        self.ui.label.setPixmap(QPixmap('attachment/welcome.png'))
        self.ui.pushButton1.clicked.connect(self.loginfunction)
        self.ui.pushButton2.clicked.connect(self.registerfunction)
        self.sqloflogin = sqls.SqlF()

    def loginfunction(self):
        print('登录按钮已经按下')
        accountlist = []
        for i in self.sqloflogin.getAllaccount():
            accountlist.append(i[0])
        if self.ui.lineEdit1.text() == '':
            QMessageBox.about(self.ui, '错误', '您还没有输入账号')
        elif self.ui.lineEdit2.text() == '':
            QMessageBox.about(self.ui, '错误', '您还没有输入密码')
        elif self.ui.lineEdit1.text() in accountlist:
            prepassword = self.sqloflogin.loginAccountPassword(self.ui.lineEdit1.text())
            password = prepassword[0]
            if self.ui.lineEdit2.text() == password:
                QMessageBox.about(self.ui, '登录成功', '欢迎使用!')

                # mainwindow = main.MWindow()
                # mainwindow.mui.show()

                self.ui.hide()
            else:
                QMessageBox.about(self.ui, '错误', '账号或密码错误！')
        else:
            print(self.sqloflogin.getAllaccount())
            QMessageBox.about(self.ui, '错误', '账号或密码错误！')

    def registerfunction(self):
        print('注册按钮已经按下')


if __name__ == '__main__':
    app = QApplication([])
    loginwindow = LogInWindow()
    loginwindow.ui.show()
    app.exec_()
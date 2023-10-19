'''
逻辑无问题 数据库可以正常搜索 集成摄像头重启后以及训练模型后
所有摄像头的重启后 其名称地址都能表示正确 可以设置摄像头使用哪种显示类型
并且可以对指定的用户进行删除操作
可以全彩色显示
'''

from PySide2.QtWidgets import QApplication, QMessageBox, QTableWidgetItem, QHeaderView
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import Qt
import numpy as np
import cv2, threading, os, shutil
from PIL import Image
import ast
import datetime
import sqls # sqls是自己写的模块

systemLock = 0
totalUser = 0
faceSamples = []
idlists = []
userdic = {}

class MWindow():

    def __init__(self):
        self.mui = QUiLoader().load('MUi.ui')
        self.mui.setFixedSize(self.mui.width(), self.mui.height())
        self.mui.pushButton1.clicked.connect(self.start)
        self.mui.pushButton2.clicked.connect(self.close)
        self.mui.addButton.clicked.connect(self.addcam)
        self.mui.delButton.clicked.connect(self.delcam)
        self.mui.luruButton.clicked.connect(self.luru)
        self.mui.logButton.clicked.connect(self.log)
        self.mui.pushButtonSaveConfig.clicked.connect(self.saveconfig)

        self.busy1, self.busy2, self.busy3, self.busy4 = False, False, False, False
        self.cameraList = [] # 记录已经获取的摄像头 避免同一个摄像头重复获取

        ######### ↓↓↓以下代码为人脸识别数据初始化过程 ########
        global totalUser, faceSamples, idlists, userdic

        f = open('config/totalUser.txt')
        config_totalUser = f.read()
        totalUser = int(config_totalUser)
        f.close()
        print('totaluser:', totalUser, type(totalUser))

        f = open('config/idlists.txt')
        for line in f.readlines():
            line = line.strip('\n')
            idlists.append(int(line))
        f.close()
        print('idlists:', idlists, type(idlists))

        if os.path.getsize('config/userdic.txt') > 0:
            f = open('config/userdic.txt')
            config_userdic = f.read()
            userdic = ast.literal_eval(config_userdic)
            f.close()
            print('userdic:', userdic, type(userdic))

        for i in range(1, totalUser+1):
            if i in userdic:
                for ii in os.listdir('data' + '/' + userdic[i]):
                    img = Image.open('data/' + userdic[i] + '/' + ii).convert('L')
                    img_np = np.array(img)
                    detectorofInit = cv2.CascadeClassifier('attachment/haarcascade_frontalface_default.xml')
                    facesofInit = detectorofInit.detectMultiScale(img_np)
                    for (x, y, w, h) in facesofInit:
                        faceSamples.append(img_np[y:y + h, x:x + w])
        ######### ↑↑↑以上代码为人脸识别数据初始化过程 ########

        ######### ↓↓↓以下代码为显示初始化过程 ########
        global systemLock
        f = open('config/configwin1.txt')
        result1 = []
        for line in f.readlines():
            line = line.strip('\n')
            result1.append(line)
        f.close()

        f = open('config/configwin2.txt')
        result2 = []
        for line in f.readlines():
            line =  line.strip('\n')
            result2.append(line)
        f.close()

        f = open('config/configwin3.txt')
        result3 = []
        for line in f.readlines():
            line = line.strip('\n')
            result3.append(line)
        f.close()

        f = open('config/configwin4.txt')
        result4 = []
        for line in f.readlines():
            line = line.strip('\n')
            result4.append(line)
        f.close()

        if result1 == []:
            pass
        else:
            nameandplace = result1[0]
            displaymode = int(result1[1])
            url = result1[2]
            if url.isdigit():
                # 如果是摄像头id
                url = int(url)
                if url == 0:
                    if systemLock != 0:
                        QMessageBox.about(self.mui, '错误', '集成摄像头被占用！')
                        return
                    elif systemLock == 0:
                        systemLock = 1
            else:
                # 如果不是摄像头id
                pass
            self.mui.lineEdit11.setText(nameandplace)
            self.mui.comboBox1.setCurrentIndex(displaymode)
            self.mui.lineEdit12.setText(str(url))
            if url != '':
                self.start1(url, nameandplace, displaymode)

        if result2 == []:
            pass
        else:
            nameandplace = result2[0]
            displaymode = int(result2[1])
            url = result2[2]
            if url.isdigit():
                # 如果是摄像头id
                url = int(url)
                if url == 0:
                    if systemLock != 0:
                        QMessageBox.about(self.mui, '错误', '集成摄像头被占用！')
                        return
                    elif systemLock == 0:
                        systemLock = 2
            else:
                # 如果不是摄像头id
                pass
            self.mui.lineEdit21.setText(nameandplace)
            self.mui.comboBox2.setCurrentIndex(displaymode)
            self.mui.lineEdit22.setText(str(url))
            if url != '':
                self.start2(url, nameandplace, displaymode)

        if result3 == []:
            pass
        else:
            nameandplace = result3[0]
            displaymode = int(result3[1])
            url = result3[2]
            if url.isdigit():
                # 如果是摄像头id
                url = int(url)
                if url == 0:
                    if systemLock != 0:
                        QMessageBox.about(self.mui, '错误', '集成摄像头被占用！')
                        return
                    elif systemLock == 0:
                        systemLock = 3
            else:
                # 如果不是摄像头id
                pass
            self.mui.lineEdit31.setText(nameandplace)
            self.mui.comboBox3.setCurrentIndex(displaymode)
            self.mui.lineEdit32.setText(str(url))
            if url != '':
                self.start3(url, nameandplace, displaymode)

        if result4 == []:
            pass
        else:
            nameandplace = result4[0]
            displaymode = int(result4[1])
            url = result4[2]
            if url.isdigit():
                # 如果是摄像头id
                url = int(url)
                if url == 0:
                    if systemLock != 0:
                        QMessageBox.about(self.mui, '错误', '集成摄像头被占用！')
                        return
                    elif systemLock == 0:
                        systemLock = 4
            else:
                # 如果不是摄像头id
                pass
            self.mui.lineEdit41.setText(nameandplace)
            self.mui.comboBox4.setCurrentIndex(displaymode)
            self.mui.lineEdit42.setText(str(url))
            if url != '':
                self.start4(url, nameandplace, displaymode)

        ######### ↑↑↑以上代码为显示初始化过程 ########

    def saveconfig(self):  # 保存显示配置文件的函数
        f = open('config/configwin1.txt', 'w')
        nameAndLocation = self.mui.lineEdit11.text()
        displaymode = self.mui.comboBox1.currentIndex()
        url = self.mui.lineEdit12.text()
        result1 = nameAndLocation + '\n' + str(displaymode) + '\n' + url + '\n'
        f.write(result1)
        f.close()
        f = open('config/configwin2.txt', 'w')
        nameAndLocation = self.mui.lineEdit21.text()
        displaymode = self.mui.comboBox2.currentIndex()
        url = self.mui.lineEdit22.text()
        result2 = nameAndLocation + '\n' + str(displaymode) + '\n' + url + '\n'
        f.write(result2)
        f.close()
        f = open('config/configwin3.txt', 'w')
        nameAndLocation = self.mui.lineEdit31.text()
        displaymode = self.mui.comboBox3.currentIndex()
        url = self.mui.lineEdit32.text()
        result3 = nameAndLocation + '\n' + str(displaymode) + '\n' + url + '\n'
        f.write(result3)
        f.close()
        f = open('config/configwin4.txt', 'w')
        nameAndLocation = self.mui.lineEdit41.text()
        displaymode = self.mui.comboBox4.currentIndex()
        url = self.mui.lineEdit42.text()
        result4 = nameAndLocation + '\n' + str(displaymode) + '\n' + url + '\n'
        f.write(result4)
        f.close()

        QMessageBox.about(self.mui, '保存成功', '下次启动时会采用此次配置')

    def delcam(self):
        print('function of del camera'
              '显示删除摄像头的界面 显示需要删除的摄像头的链接')
        self.addwin = DelWindow()
        self.addwin.ui.show()

    def addcam(self):
        print('function of add camera'
              '显示添加摄像头的界面 显示需要添加的摄像头的链接')
        self.addwin = AddWindow()
        self.addwin.ui.show()

    def luru(self):
        print('function of luru face'
              '显示人脸录入界面 这里需要系统锁 人脸录入的优先级比display的优先级高')
        self.luruwin = LuruWindow()
        self.luruwin.ui.setWindowFlags(Qt.CustomizeWindowHint)
        self.luruwin.ui.show()

    def log(self):
        print('function of inquiry log')
        self.logwin = LogWindow()
        self.logwin.ui.show()

    def start(self):
        if self.busy1 == True:
            QMessageBox.about(self.mui, '错误', '窗口1忙碌，不可以添加视频流')
        else:
            self.cam1 = Camera('1 Danny MacAskill’s Wee Day Out.flv', self.mui.display1)
            threading.Thread(target=self.cam1.display).start()
            if self.cam1.cap.isOpened():
                self.busy1 = True

        if self.busy2 == True:
            QMessageBox.about(self.mui, '错误', '窗口2忙碌，不可以添加视频流')
        else:
            self.cam2 = Camera('1 Danny MacAskill’s Wee Day Out.flv', self.mui.display2)
            threading.Thread(target=self.cam2.display).start()
            if self.cam2.cap.isOpened():
                self.busy2 = True

        if self.busy3 == True:
            QMessageBox.about(self.mui, '错误', '窗口3忙碌，不可以添加视频流')
        else:
            self.cam3 = Camera('1 Danny MacAskill’s Wee Day Out.flv', self.mui.display3)
            threading.Thread(target=self.cam3.display).start()
            if self.cam3.cap.isOpened():
                self.busy3 = True

        if self.busy4 == True:
            QMessageBox.about(self.mui, '错误', '窗口4忙碌，不可以添加视频流')
        else:
            self.cam4 = Camera('1 Danny MacAskill’s Wee Day Out.flv', self.mui.display4)
            threading.Thread(target=self.cam4.display).start()
            if self.cam4.cap.isOpened():
                self.busy4 = True

    def start1(self, url, cameraNamePlace = '', displaymode = 0):
        global systemLock
        if self.busy1 == True:
            QMessageBox.about(self.mui, '错误', '窗口1忙碌，不可以添加视频流')
        elif url in self.cameraList:
            QMessageBox.about(self.mui, '错误', f'摄像头{url}忙碌，不可以重复使用')
        else:
            if url == 0:
                systemLock = 1  # 上锁
            self.cam1 = Camera(url, self.mui.display1)
            self.cam1.displayMode = displaymode
            if cameraNamePlace != '':
                self.cam1.nameAndLocation = cameraNamePlace
            if displaymode == 0:
                threading.Thread(target=self.cam1.display).start()
            elif displaymode == 1:
                threading.Thread(target=self.cam1.displaySimpleBrand).start()
            elif displaymode == 2:
                threading.Thread(target=self.cam1.displayJustdisplayBrand).start()
            if self.cam1.cap.isOpened():
                self.busy1 = True
                self.cameraList.append(url)

    def start2(self, url, cameraNamePlace = '', displaymode = 0):
        global systemLock
        if self.busy2 == True:
            QMessageBox.about(self.mui, '错误', '窗口2忙碌，不可以添加视频流')
        elif url in self.cameraList:
            QMessageBox.about(self.mui, '错误', f'摄像头{url}忙碌，不可以重复使用')
        else:
            if url == 0:
                systemLock = 2  # 上锁
            self.cam2 = Camera(url, self.mui.display2)
            self.cam2.displayMode = displaymode
            if cameraNamePlace != '':
                self.cam2.nameAndLocation = cameraNamePlace
            if displaymode == 0:
                threading.Thread(target=self.cam2.display).start()
            elif displaymode == 1:
                threading.Thread(target=self.cam2.displaySimpleBrand).start()
            elif displaymode == 2:
                threading.Thread(target=self.cam2.displayJustdisplayBrand).start()
            if self.cam2.cap.isOpened():
                self.busy2 = True
                self.cameraList.append(url)

    def start3(self, url, cameraNamePlace = '', displaymode = 0):
        global systemLock
        if self.busy3 == True:
            QMessageBox.about(self.mui, '错误', '窗口3忙碌，不可以添加视频流')
        elif url in self.cameraList:
            QMessageBox.about(self.mui, '错误', f'摄像头{url}忙碌，不可以重复使用')
        else:
            if url == 0:
                systemLock = 3  # 上锁
            self.cam3 = Camera(url, self.mui.display3)
            self.cam3.displayMode = displaymode
            if cameraNamePlace != '':
                self.cam3.nameAndLocation = cameraNamePlace
            if displaymode == 0:
                threading.Thread(target=self.cam3.display).start()
            elif displaymode == 1:
                threading.Thread(target=self.cam3.displaySimpleBrand).start()
            elif displaymode == 2:
                threading.Thread(target=self.cam3.displayJustdisplayBrand).start()
            if self.cam3.cap.isOpened():
                self.busy3 = True
                self.cameraList.append(url)

    def start4(self, url, cameraNamePlace = '', displaymode = 0):
        global systemLock
        if self.busy4 == True:
            QMessageBox.about(self.mui, '错误', '窗口4忙碌，不可以添加视频流')
        elif url in self.cameraList:
            QMessageBox.about(self.mui, '错误', f'摄像头{url}忙碌，不可以重复使用')
        else:
            if url == 0:
                systemLock = 4  # 上锁
            self.cam4 = Camera(url, self.mui.display4)
            self.cam4.displayMode = displaymode
            if cameraNamePlace != '':
                self.cam4.nameAndLocation = cameraNamePlace
            if displaymode == 0:
                threading.Thread(target=self.cam4.display).start()
            if displaymode == 1:
                threading.Thread(target=self.cam4.displaySimpleBrand).start()
            if displaymode == 2:
                threading.Thread(target=self.cam4.displayJustdisplayBrand).start()
            if self.cam4.cap.isOpened():
                self.busy4 = True
                self.cameraList.append(url)

    def close(self):
        if self.busy1 == True:
            if self.cam1.url in self.cameraList:
                self.cameraList.remove(self.cam1.url)
            self.mui.display1.setPixmap(QPixmap('./attachment/nosignal.png'))
            self.cam1.close()
            print('1close')
            self.busy1 = False
        if self.busy2 == True:
            if self.cam2.url in self.cameraList:
                self.cameraList.remove(self.cam2.url)
            self.mui.display2.setPixmap(QPixmap('./attachment/nosignal.png'))
            self.cam2.close()
            print('2close')
            self.busy2 = False
        if self.busy3 == True:
            if self.cam3.url in self.cameraList:
                self.cameraList.remove(self.cam3.url)
            self.mui.display3.setPixmap(QPixmap('./attachment/nosignal.png'))
            self.cam3.close()
            print('3close')
            self.busy3 = False
        if self.busy4 == True:
            if self.cam4.url in self.cameraList:
                self.cameraList.remove(self.cam4.url)
            self.mui.display4.setPixmap(QPixmap('./attachment/nosignal.png'))
            self.cam4.close()
            print('4close')
            self.busy4 = False

    def close1(self):
        if self.busy1 == True:
            if self.cam1.url in self.cameraList:
                self.cameraList.remove(self.cam1.url)
            self.cam1.close()
            print('1close')
            self.busy1 = False
            self.mui.display1.setPixmap(QPixmap('./attachment/nosignal.png'))
        else:
            QMessageBox.about(self.mui, '错误', '窗口1并没有打开')

    def close2(self):
        if self.busy2 == True:
            if self.cam2.url in self.cameraList:
                self.cameraList.remove(self.cam2.url)
            self.cam2.close()
            print('2close')
            self.busy2 = False
            self.mui.display2.setPixmap(QPixmap('./attachment/nosignal.png'))
        else:
            QMessageBox.about(self.mui, '错误', '窗口2并没有打开')

    def close3(self):
        if self.busy3 == True:
            if self.cam3.url in self.cameraList:
                self.cameraList.remove(self.cam3.url)
            self.cam3.close()
            print('3close')
            self.busy3 = False
            self.mui.display3.setPixmap(QPixmap('./attachment/nosignal.png'))
        else:
            QMessageBox.about(self.mui, '错误', '窗口3并没有打开')

    def close4(self):
        if self.busy4 == True:
            if self.cam4.url in self.cameraList:
                self.cameraList.remove(self.cam4.url)
            self.cam4.close()
            print('4close')
            self.busy4 = False
            self.mui.display4.setPixmap(QPixmap('./attachment/nosignal.png'))
        else:
            QMessageBox.about(self.mui, '错误', '窗口4并没有打开')

class AddWindow():

    def __init__(self):
        self.ui = QUiLoader().load('Add.ui')
        self.ui.setFixedSize(self.ui.width(), self.ui.height())
        self.ui.buttonBox.accepted.connect(self.ok)
        self.ui.buttonBox.rejected.connect(self.cancel)

    def ok(self):
        global systemLock
        print('push the ok button')
        print(self.ui.comboBox.currentText())

        if self.ui.comboBox.currentText() == '':
            QMessageBox.about(self.ui, '错误', '请在组合选择框中选择内容')

        else:
            if self.ui.comboBox.currentText() == 'win1':

                # print("我们将要打开窗口1")
                if self.ui.lineEdit.text() == '':
                    QMessageBox.about(self.ui, '错误', '请输入在文本框中输入内容')
                elif mainwindow.busy1 == False:
                    self.textCamUrl = self.ui.lineEdit.text()
                    print(type(self.textCamUrl))
                    if self.textCamUrl.isdigit():
                        self.textCamUrl = int(self.textCamUrl)
                        '''
                        如果不是视频格式 是摄像头的ID 则把他转换成int格式
                        '''
                        print(type(self.textCamUrl))

                        if self.textCamUrl == 0:

                            if systemLock != 0:
                                QMessageBox.about(self.ui, '错误', "集成摄像头被占用！")
                                return
                            elif systemLock == 0:
                                systemLock = 1
                                '''
                                这段代码是针对集成摄像头的占用检测，
                                集成摄像头涉及人脸录入
                                '''
                    else:
                        '''如果不是摄像头的ID
                        则什么都不做
                        '''
                        print(type(self.textCamUrl))
                        pass

                    if self.textCamUrl not in mainwindow.cameraList:
                        displaymodeIndex = self.ui.comboBox2.currentIndex()
                        mainwindow.start1(self.textCamUrl, displaymode=displaymodeIndex)
                        mainwindow.cam1.displayMode = displaymodeIndex
                        if self.ui.lineEdit2.text() == '':
                            # 如果没有输入摄像头的名称地址
                            mainwindow.cam1.nameAndLocation = 'Test Camera, Test Location'
                        else:
                            mainwindow.cam1.nameAndLocation = self.ui.lineEdit2.text()
                    else:
                        QMessageBox.about(self.ui, '错误', f'摄像头{self.textCamUrl}忙碌，不可以重复使用')

                else:
                    QMessageBox.about(self.ui, '错误', '窗口1忙碌，不可以添加视频流')

            if self.ui.comboBox.currentText() == 'win2':

                if self.ui.lineEdit.text() == '':
                    QMessageBox.about(self.ui, '错误', '请输入在文本框中输入内容')
                elif mainwindow.busy2 == False:
                    self.textCamUrl = self.ui.lineEdit.text()
                    print(type(self.textCamUrl))
                    if self.textCamUrl.isdigit():
                        self.textCamUrl = int(self.textCamUrl)
                        '''
                        如果不是视频格式 是摄像头的ID 则把他转换成int格式
                        '''
                        print(type(self.textCamUrl))

                        if self.textCamUrl == 0:

                            if systemLock != 0:
                                QMessageBox.about(self.ui, '错误', "集成摄像头被占用！")
                                return
                            elif systemLock == 0:
                                systemLock = 2
                                '''
                                这段代码是针对集成摄像头的占用检测，
                                集成摄像头涉及人脸录入
                                '''

                    else:
                        '''如果不是摄像头的ID
                        则什么都不做
                        '''
                        print(type(self.textCamUrl))
                        pass

                    if self.textCamUrl not in mainwindow.cameraList:
                        displaymodeIndex = self.ui.comboBox2.currentIndex()
                        mainwindow.start2(self.textCamUrl, displaymode=displaymodeIndex)
                        mainwindow.cam2.displayMode = displaymodeIndex
                        if self.ui.lineEdit2.text() == '':
                            # 如果没有输入摄像头的名称地址
                            mainwindow.cam2.nameAndLocation = 'Test Camera, Test Location'
                        else:
                            mainwindow.cam2.nameAndLocation = self.ui.lineEdit2.text()
                    else:
                        QMessageBox.about(self.ui, '错误', f'摄像头{self.textCamUrl}忙碌，不可以重复使用')

                else:
                    QMessageBox.about(self.ui, '错误', '窗口2忙碌，不可以添加视频流')

            if self.ui.comboBox.currentText() == 'win3':

                if self.ui.lineEdit.text() == '':
                    QMessageBox.about(self.ui, '错误', '请输入在文本框中输入内容')
                elif mainwindow.busy3 == False:
                    self.textCamUrl = self.ui.lineEdit.text()
                    print(type(self.textCamUrl))
                    if self.textCamUrl.isdigit():
                        self.textCamUrl = int(self.textCamUrl)
                        '''
                        如果不是视频格式 是摄像头的ID 则把他转换成int格式
                        '''
                        print(type(self.textCamUrl))

                        if self.textCamUrl == 0:

                            if systemLock != 0:
                                QMessageBox.about(self.ui, '错误', "集成摄像头被占用！")
                                return
                            elif systemLock == 0:
                                systemLock = 3
                                '''
                                这段代码是针对集成摄像头的占用检测，
                                集成摄像头涉及人脸录入
                                '''

                    else:
                        '''如果不是摄像头的ID
                        则什么都不做
                        '''
                        print(type(self.textCamUrl))
                        pass

                    if self.textCamUrl not in mainwindow.cameraList:
                        displaymodeIndex = self.ui.comboBox2.currentIndex()
                        mainwindow.start3(self.textCamUrl, displaymode=displaymodeIndex)
                        mainwindow.cam3.displayMode = displaymodeIndex
                        if self.ui.lineEdit2.text() == '':
                            # 如果没有输入摄像头的名称地址
                            mainwindow.cam3.nameAndLocation = 'Test Camera, Test Location'
                        else:
                            mainwindow.cam3.nameAndLocation = self.ui.lineEdit2.text()
                    else:
                        QMessageBox.about(self.ui, '错误', f'摄像头{self.textCamUrl}忙碌，不可以重复使用')

                else:
                    QMessageBox.about(self.ui, '错误', '窗口3忙碌，不可以添加视频流')

            if self.ui.comboBox.currentText() == 'win4':

                if self.ui.lineEdit.text() == '':
                    QMessageBox.about(self.ui, '错误', '请输入在文本框中输入内容')
                elif mainwindow.busy4 == False:
                    self.textCamUrl = self.ui.lineEdit.text()
                    print(type(self.textCamUrl))
                    if self.textCamUrl.isdigit():
                        self.textCamUrl = int(self.textCamUrl)
                        '''
                        如果不是视频格式 是摄像头的ID 则把他转换成int格式
                        '''
                        print(type(self.textCamUrl))

                        if self.textCamUrl == 0:

                            if systemLock != 0:
                                QMessageBox.about(self.ui, '错误', "集成摄像头被占用！")
                                return
                            elif systemLock == 0:
                                systemLock = 4
                                '''
                                这段代码是针对集成摄像头的占用检测，
                                集成摄像头涉及人脸录入
                                '''

                    else:
                        '''如果不是摄像头的ID
                        则什么都不做
                        '''
                        print(type(self.textCamUrl))
                        pass
                    if self.textCamUrl not in mainwindow.cameraList:
                        displaymodeIndex = self.ui.comboBox2.currentIndex()
                        mainwindow.start4(self.textCamUrl, displaymode=displaymodeIndex)
                        mainwindow.cam4.displayMode = displaymodeIndex
                        if self.ui.lineEdit2.text() == '':
                            # 如果没有输入摄像头的名称地址
                            mainwindow.cam4.nameAndLocation = 'Test Camera, Test Location'
                        else:
                            mainwindow.cam4.nameAndLocation = self.ui.lineEdit2.text()
                    else:
                        QMessageBox.about(self.ui, '错误', f'摄像头{self.textCamUrl}忙碌，不可以重复使用')

                else:
                    QMessageBox.about(self.ui, '错误', '窗口4忙碌，不可以添加视频流')

    def cancel(self):
        print('push the cancel button')


class DelWindow():
    def __init__(self):
        self.ui = QUiLoader().load('Del.ui')
        self.ui.setFixedSize(self.ui.width(), self.ui.height())
        self.ui.buttonBox.accepted.connect(self.ok)
        self.ui.buttonBox.rejected.connect(self.cancel)

    def ok(self):
        print('push the ok button')
        print(self.ui.comboBox.currentText())

        if self.ui.comboBox.currentText() == '':
            QMessageBox.about(self.ui, '错误', '请在组合选择框中选择试图关闭的窗口')

        else:
            if self.ui.comboBox.currentText() == 'win1':
                # print("我们将要关闭窗口1")
                mainwindow.close1()

            if self.ui.comboBox.currentText() == 'win2':
                mainwindow.close2()

            if self.ui.comboBox.currentText() == 'win3':
                mainwindow.close3()

            if self.ui.comboBox.currentText() == 'win4':
                mainwindow.close4()

    def cancel(self):
        print('push the cancel button')

class DelFaceWindow():

    def __init__(self):
        self.ui = QUiLoader().load('DelFace.ui')
        self.ui.buttonBox.accepted.connect(self.ok)
        self.ui.buttonBox.rejected.connect(self.cancel)
        for i in range(1, totalUser+1):
            if i in userdic:
                self.ui.comboBox.addItem(userdic[i])

    def ok(self):
        global totalUser
        global faceSamples
        global idlists
        global userdic
        print('将要对选定的人脸进行删除')
        faceTodel = self.ui.comboBox.currentText()
        print(faceTodel)
        # 删userdic
        for i in range(1, totalUser+1):
            if i in userdic.copy():
                if userdic[i] == faceTodel:
                    userdic.pop(i)
                    while i in idlists:
                        idlists.remove(i)
                        # 删idlists
        # 删除图片
        shutil.rmtree('data'+'/'+faceTodel)
        # faceSamples要置空 重新训练
        faceSamples = []
        for i in range(1, totalUser+1):
            if i in userdic:
                for ii in os.listdir('data' + '/' + userdic[i]):
                    img = Image.open('data/' + userdic[i] + '/' + ii).convert('L')
                    img_np = np.array(img)
                    detectorofInit = cv2.CascadeClassifier('attachment/haarcascade_frontalface_default.xml')
                    facesofInit = detectorofInit.detectMultiScale(img_np)
                    for (x, y, w, h) in facesofInit:
                        faceSamples.append(img_np[y:y + h, x:x + w])

        tag1, tag2, tag3, tag4 = False, False, False, False
        remeurl1, remeurl2, remeurl3, remeurl4 = '', '', '', ''
        remeplace1, remeplace2, remeplace3, remeplace4 = '', '', '', ''
        rememode1, rememode2, rememode3, rememode4 = '', '', '', ''
        if mainwindow.busy1 == True:
            tag1 = True
            remeurl1 = mainwindow.cam1.url
            remeplace1 = mainwindow.cam1.nameAndLocation
            rememode1 = mainwindow.cam1.displayMode
            mainwindow.close1()
            mainwindow.busy1 = False
            # 释放一号窗口 一号相机 设置为空闲 并保存了它的URL和名称地址、显示模式 以便后续重启操作
        if mainwindow.busy2 == True:
            tag2 = True
            remeurl2 = mainwindow.cam2.url
            remeplace2 = mainwindow.cam2.nameAndLocation
            rememode2 = mainwindow.cam2.displayMode
            mainwindow.close2()
            mainwindow.busy2 = False
            # 释放二号窗口 二号相机 设置为空闲 并保存了它的URL和名称地址、显示模式 以便后续重启操作
        if mainwindow.busy3 == True:
            tag3 = True
            remeurl3 = mainwindow.cam3.url
            remeplace3 = mainwindow.cam3.nameAndLocation
            rememode3 = mainwindow.cam3.displayMode
            mainwindow.close3()
            mainwindow.busy3 = False
            # 释放三号窗口 三号相机 设置为空闲 并保存了它的URL和名称地址、显示模式 以便后续重启操作
        if mainwindow.busy4 == True:
            tag4 = True
            remeurl4 = mainwindow.cam4.url
            remeplace4 = mainwindow.cam4.nameAndLocation
            rememode4 = mainwindow.cam4.displayMode
            mainwindow.close4()
            mainwindow.busy4 = False
            # 释放四号窗口 四号相机 设置为空闲 并保存了它的URL和名称地址、显示模式 以便后续重启操作
        self.recog = cv2.face.LBPHFaceRecognizer_create()
        # 初始化人脸识别算法
        self.recog.train(faceSamples, np.array(idlists))
        # 保存idlists数据 ----------------------------------
        f = open('config/idlists.txt', 'w')
        for i in idlists:
            f.write(str(i))
            f.write('\n')
        f.close()
        # 保存userdic数据 ------------------------------------
        f = open('config/userdic.txt', 'w')
        f.write(str(userdic))
        f.close()
        yml = 'model' + '/' + 'model' + '.yml'
        self.recog.write(yml)

        '''
                    下面的代码是以前关闭摄像头的重启操作
                    '''
        if tag1 == True:
            mainwindow.start1(remeurl1, remeplace1, rememode1)
        if tag2 == True:
            mainwindow.start2(remeurl2, remeplace2, rememode2)
        if tag3 == True:
            mainwindow.start3(remeurl3, remeplace3, rememode3)
        if tag4 == True:
            mainwindow.start4(remeurl4, remeplace4, rememode4)


    def cancel(self):
        print('push the cancel button')


class LuruWindow():

    def __init__(self):
        global systemLock
        self.ui = QUiLoader().load('Luru.ui')
        self.ui.setFixedSize(self.ui.width(), self.ui.height())

        self.ui.lurudisplay2.setPixmap(QPixmap('attachment/avatar.png'))

        self.ui.pushButton2.clicked.connect(self.closeQuit)
        self.ui.pushButton.clicked.connect(self.snap)
        self.ui.pushButton3.clicked.connect(self.trainModel)
        self.ui.pushButton4.clicked.connect(self.delAll)
        # 点击按钮四会执行模型重置操作，跳出弹窗
        self.ui.pushButton5.clicked.connect(self.delFace)

        self.integratedNamePlace = '' # 记录集成摄像头的名称和地点 以便于后续重启的设置
        self.integratedDisplaymode = 0 # 记录集成摄像头的显示模式

        if systemLock != 0:
            QMessageBox.about(self.ui, '警告', '集成相机被占用，即将解锁，监控将暂时中断，人脸录入结束后可自行恢复')
            if systemLock == 1:
                self.integratedNamePlace = mainwindow.cam1.nameAndLocation
                self.integratedDisplaymode = mainwindow.cam1.displayMode
                mainwindow.close1()
                systemLock = 1
                self.lurucam = Camera(0, self.ui.lurudisplay)
                self.luruThread = threading.Thread(target=self.lurucam.displayLuruBrand)
                # self.luruThread.setDaemon(True)
                self.luruThread.start()
            elif systemLock == 2:
                self.integratedNamePlace = mainwindow.cam2.nameAndLocation
                self.integratedDisplaymode = mainwindow.cam2.displayMode
                mainwindow.close2()
                systemLock = 2
                self.lurucam = Camera(0, self.ui.lurudisplay)
                self.luruThread = threading.Thread(target=self.lurucam.displayLuruBrand)
                # self.luruThread.setDaemon(True)
                self.luruThread.start()
            elif systemLock == 3:
                self.integratedNamePlace = mainwindow.cam3.nameAndLocation
                self.integratedDisplaymode = mainwindow.cam3.displayMode
                mainwindow.close3()
                systemLock = 3
                self.lurucam = Camera(0, self.ui.lurudisplay)
                self.luruThread = threading.Thread(target=self.lurucam.displayLuruBrand)
                # self.luruThread.setDaemon(True)
                self.luruThread.start()
            elif systemLock == 4:
                self.integratedNamePlace = mainwindow.cam4.nameAndLocation
                self.integratedDisplaymode = mainwindow.cam4.displayMode
                mainwindow.close4()
                systemLock = 4
                self.lurucam = Camera(0, self.ui.lurudisplay)
                self.luruThread = threading.Thread(target=self.lurucam.displayLuruBrand)
                # self.luruThread.setDaemon(True)
                self.luruThread.start()

        if systemLock == 0:
            systemLock = 55
            self.lurucam = Camera(0, self.ui.lurudisplay)
            self.luruThread = threading.Thread(target=self.lurucam.displayLuruBrand)
            # self.luruThread.setDaemon(True)
            self.luruThread.start()

    def delFace(self):
        self.delfacewin = DelFaceWindow()
        self.delfacewin.ui.show()

    def delAll(self):
        self.resetwin = ResetWindow()
        self.resetwin.ui.show()

    def trainModel(self):
        global totalUser
        global userdic
        global faceSamples
        global idlists

        print('训练模型按钮已经按下')
        # self.face_samples = []
        # self.lists = []
        li = []
        tag1, tag2, tag3, tag4 = False, False, False, False
        remeurl1, remeurl2, remeurl3, remeurl4 = '', '', '', ''
        remeplace1, remeplace2, remeplace3, remeplace4 = '', '', '', ''
        rememode1, rememode2, rememode3, rememode4 = '', '', '', ''

        if self.ui.lineEdit.text() == '':
            QMessageBox.about(self.ui, '错误', '你还没有输入姓名')
        elif not os.path.exists('data/' + self.ui.lineEdit.text()):
            QMessageBox.about(self.ui, '错误', '该用户不存在或未进行录入')
        else:

            '''
            因为在按下拍摄按钮后，主界面的display窗口就已经启动 > display()会检测yml文件的存在
            > 存在yml文件就会进行读取操作 > 此时的trainModel()可能刚被按下，模型尚未训练完成
            > 导致Camera.display()中的读取yml文件操作出现报错

            解决方法：
            训练过程中，释放Camera的cap 训练完成后再进行 start操作

            因为本系统为多摄像头的监控管理系统，应用中很有可能不止一个摄像头在使用yml模型进行人脸识别操作
            所以需要对正在忙碌的窗口所对应的Camera对象都进行release操作，并在模型训练完成后
            对应当进行重启的摄像头进行重启操作
            '''
            if mainwindow.busy1 == True:
                tag1 = True
                remeurl1 = mainwindow.cam1.url
                remeplace1 = mainwindow.cam1.nameAndLocation
                rememode1 = mainwindow.cam1.displayMode
                mainwindow.close1()
                mainwindow.busy1 = False
                # 释放一号窗口 一号相机 设置为空闲 并保存了它的URL和名称地址、显示模式 以便后续重启操作
            if mainwindow.busy2 == True:
                tag2 = True
                remeurl2 = mainwindow.cam2.url
                remeplace2 = mainwindow.cam2.nameAndLocation
                rememode2 = mainwindow.cam2.displayMode
                mainwindow.close2()
                mainwindow.busy2 = False
                # 释放二号窗口 二号相机 设置为空闲 并保存了它的URL和名称地址、显示模式 以便后续重启操作
            if mainwindow.busy3 == True:
                tag3 = True
                remeurl3 = mainwindow.cam3.url
                remeplace3 = mainwindow.cam3.nameAndLocation
                rememode3 = mainwindow.cam3.displayMode
                mainwindow.close3()
                mainwindow.busy3 = False
                # 释放三号窗口 三号相机 设置为空闲 并保存了它的URL和名称地址、显示模式 以便后续重启操作
            if mainwindow.busy4 == True:
                tag4 = True
                remeurl4 = mainwindow.cam4.url
                remeplace4 = mainwindow.cam4.nameAndLocation
                rememode4 = mainwindow.cam4.displayMode
                mainwindow.close4()
                mainwindow.busy4 = False
                # 释放四号窗口 四号相机 设置为空闲 并保存了它的URL和名称地址、显示模式 以便后续重启操作

            self.recog = cv2.face.LBPHFaceRecognizer_create()
            # 初始化人脸识别算法
            for i in os.listdir('data/' + self.ui.lineEdit.text()):
                # img = cv2.imread('data/' + self.ui.lineEdit.text() + '/' + i)
                img = Image.open('data/' + self.ui.lineEdit.text() + '/' + i).convert('L')

                print('当前训练的人脸图片路径：' + 'data/' + self.ui.lineEdit.text() + '/' + i)
                # id = int(i.split('.')[0])
                # self.ids.append(id)
                img_np = np.array(img)
                detectorOfTrain = cv2.CascadeClassifier('attachment/haarcascade_frontalface_default.xml')
                facesofTrain = detectorOfTrain.detectMultiScale(img_np)

                # li.append(totalUser+1)
                # print(li)

                for (x, y, w, h) in facesofTrain:
                    '''
                    注意！ 有的情况一张图会识别出两张人脸 这个需要处理一下
                    否则 在后面 recog.train()的faceSamples长度和idlists的长度会出现不匹配

                    解决方法：
                    将li.append()由for(x,y,w,h)循环外 转移至循环内 以保证faceSamples长度
                    与idlists长度的匹配
                    这样一来，人脸采集时 每个人的照片都是10张 但是获取的人脸样本有的人会大于10
                    因为有些照片 一张图片可能会识别出两个人脸样本
                    '''
                    faceSamples.append(img_np[y:y + h, x:x + w])
                    li.append(totalUser + 1)
                    print(li)
                    # 将获取的图片添加到face_samples这个list之中

            print(len(faceSamples))
            print(type(faceSamples))
            print(type(faceSamples[0]))
            print(type(faceSamples[0][0]))
            idlists = idlists + li
            print(idlists)

            # 保存idlists数据 ----------------------------------
            f = open('config/idlists.txt', 'w')
            for i in idlists:
                f.write(str(i))
                f.write('\n')
            f.close()

            self.recog.train(faceSamples, np.array(idlists))

            totalUser = totalUser + 1

            # 保存totalUser数据 ---------------------------------
            f = open('config/totalUser.txt', 'w')
            f.write(str(totalUser))
            f.close()

            userdic[totalUser] = self.ui.lineEdit.text()
            # 完成label标签和用户名的对应关系

            # 保存userdic数据 ------------------------------------
            f = open('config/userdic.txt', 'w')
            f.write(str(userdic))
            f.close()

            yml = 'model' + '/' + 'model' + '.yml'
            self.recog.write(yml)

            '''
            下面的代码是以前关闭摄像头的重启操作
            '''
            if tag1 == True:
                mainwindow.start1(remeurl1, remeplace1, rememode1)
            if tag2 == True:
                mainwindow.start2(remeurl2, remeplace2, rememode2)
            if tag3 == True:
                mainwindow.start3(remeurl3, remeplace3, rememode3)
            if tag4 == True:
                mainwindow.start4(remeurl4, remeplace4, rememode4)

    def closeQuit(self):
        global systemLock
        self.lurucam.cap.release()
        self.ui.close()
        if systemLock == 1 and mainwindow.busy1 == False:
            mainwindow.start1(0, self.integratedNamePlace, self.integratedDisplaymode)
        elif systemLock == 2 and mainwindow.busy2 == False:
            mainwindow.start2(0, self.integratedNamePlace, self.integratedDisplaymode)
        elif systemLock == 3 and mainwindow.busy3 == False:
            mainwindow.start3(0, self.integratedNamePlace, self.integratedDisplaymode)
        elif systemLock == 4 and mainwindow.busy4 == False:
            mainwindow.start4(0, self.integratedNamePlace, self.integratedDisplaymode)
        elif systemLock == 55:
            systemLock = 0

    def getNewface(self):
        print('正在从摄像头录入新的人脸信息\n' * 3)
        self.sampleNum = 0  # 已经获取的样本数量
        self.maxSampleNum = 10

        self.lurucam.cap.release()
        self.ui.lurudisplay.setPixmap(QPixmap('./attachment/nosignal.png'))

        self.lurucamReal = Camera(0, self.ui.lurudisplay)
        self.luruThreadReal = threading.Thread(target=self.getNewFaceDisplay)
        self.luruThreadReal.start()

    def getNewFaceDisplay(self):
        global systemLock

        print('人脸捕捉新线程已经开启' * 5)
        while self.lurucamReal.cap.isOpened():
            while True:
                success, frame = self.lurucamReal.cap.read()
                if success and self.sampleNum < self.maxSampleNum:
                    rawframe = cv2.resize(frame, (640, 360))
                    # cv2.imshow('raw', frame)
                    frame = cv2.cvtColor(rawframe, cv2.COLOR_BGR2GRAY)
                    # cv2.imshow('raw2', frame)
                    self.faces = self.lurucamReal.detector.detectMultiScale(frame, 1.3, 5)
                    # 其中gray为要检测的灰度图像，1.3为每次图像尺寸减小的比例，5为minNeighbors

                    # 框选人脸，for循环保证一个能检测的实时动态视频流
                    for (x, y, w, h) in self.faces:
                        # xy为左上角的坐标,w为宽，h为高，用rectangle为人脸标记画框
                        cv2.rectangle(rawframe, (x, y), (x + w, y + h), (0, 0, 255), thickness=2)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), thickness=2)
                        self.sampleNum = self.sampleNum + 1
                        cv2.imwrite('data' + '/' + self.filepath + '/' + str(self.sampleNum) + '.jpg', frame)
                        # 上面保存的一定还得是frame（即灰度图像的图片 否则faceSamples初始化加载时会出错）

                    rawframe = cv2.cvtColor(rawframe, cv2.COLOR_BGR2RGB)
                    img = QImage(rawframe.data, rawframe.shape[1],
                                 rawframe.shape[0], rawframe.shape[1]*3, QImage.Format_RGB888)

                    # print(self.lurucamReal.outLabel)
                    '''
                    循环输出self.outLabel对象，其目的是前期调试使用
                    '''
                    self.lurucamReal.outLabel.setPixmap(QPixmap.fromImage(img))
                    cv2.waitKey(10)
                else:
                    self.lurucamReal.cap.release()
                    print('lurucamReal  XXXXXXXXXXX released!' * 5)
                    self.sampleNum = 0

                    self.ui.lurudisplay.setPixmap(QPixmap('./attachment/nosignal.png'))
                    if systemLock == 1:
                        mainwindow.start1(0, self.integratedNamePlace, self.integratedDisplaymode)
                    elif systemLock == 2:
                        mainwindow.start2(0, self.integratedNamePlace, self.integratedDisplaymode)
                    elif systemLock == 3:
                        mainwindow.start3(0, self.integratedNamePlace, self.integratedDisplaymode)
                    elif systemLock == 4:
                        mainwindow.start4(0, self.integratedNamePlace, self.integratedDisplaymode)
                    elif systemLock == 55:
                        systemLock = 0
                    print("snap按下后应释放系统锁 不再有lurudisplay\n", 'systemlock:', systemLock)

                    break

    def snap(self):
        global systemLock
        if self.ui.lineEdit.text() == '':
            QMessageBox.about(self.ui, '错误', '你还没有输入姓名')
        else:
            self.filepath = self.ui.lineEdit.text()
            # 这里需要添加“文件中是否有重复人员的校验操作”
            print("拍照按钮按下 用户应该保证拍摄效果 \n" * 5)
            if not os.path.exists('data' + '/' + self.filepath):
                os.mkdir('data' + '/' + self.filepath)
            else:
                shutil.rmtree('data' + '/' + self.filepath)
                os.mkdir('data' + '/' + self.filepath)
                # 存在用户姓名目录就清空，不存在就创建，确保最后存在空的data目录

            self.getNewface()


class ResetWindow():

    def __init__(self):
        self.ui = QUiLoader().load('ResetQ.ui')
        self.ui.setFixedSize(self.ui.width(), self.ui.height())
        self.ui.buttonBox.accepted.connect(self.yes)
        self.ui.buttonBox.accepted.connect(self.no)

    def yes(self):
        global totalUser
        global userdic
        global idlists
        global faceSamples
        userdic = {}
        totalUser = 0
        idlists = []
        faceSamples = []

        print('重置按钮已经按下，会删除data目录、model目录下的所有文件，重置config')
        shutil.rmtree('data')
        os.mkdir('data')
        shutil.rmtree('model')
        os.mkdir('model')
        print('totalUser:', totalUser)

        # 以下代码是对config文件夹下的文件的操作
        f = open('config/idlists.txt', 'w')
        f.write('')
        f.close()

        f = open('config/totalUser.txt', 'w')
        f.write('0')
        f.close()

        f = open('config/userdic.txt', 'w')
        f.write('')
        f.close()


    def no(self):
        print('重置操作没有被确认，重置操作被取消')

class LogWindow():
    def __init__(self):
        self.ui = QUiLoader().load('Log.ui')
        self.ui.setFixedSize(self.ui.width(), self.ui.height())
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.pushButton.clicked.connect(self.inquiryDB)
        self.ui.pushButton2.clicked.connect(self.clearDB)

        # 将两个时间编辑框中的时间选定为当下的时间 方便用户进行调整
        nowdatetime = str(datetime.datetime.now()).split('.')[0]
        nowdatetime = datetime.datetime.strptime(nowdatetime, '%Y-%m-%d %H:%M:%S')
        print('datetimeEdit的时间为',nowdatetime,'类型为',type(nowdatetime))
        self.ui.dateTimeEdit1.setDateTime(nowdatetime)
        self.ui.dateTimeEdit2.setDateTime(nowdatetime)

        self.sqlofLog = sqls.SqlF()
        # 从sqls模块中创建一个SqlF()对象

        # 给姓名多选框添加数据
        allname = self.sqlofLog.getAllname()  # sql返回的是一个tuple
        # print('allname:',allname)
        for i in allname:
            self.ui.comboBox2.addItem(i[0])
        # 给地点多选框添加数据
        allplace = self.sqlofLog.getAllplace() # sql返回的是一个tuple
        # print('allplace', allplace)
        for i in allplace:
            self.ui.comboBox.addItem(i[0])

        results = self.sqlofLog.tableWidgetDisplay()
        x = 0
        for i in results:
            y = 0
            row_count = self.ui.tableWidget.rowCount()  # 返回当前行数(尾部)
            self.ui.tableWidget.insertRow(row_count)  # 尾部插入一行
            for ii in i:
                self.ui.tableWidget.setItem(x, y, QTableWidgetItem(str(results[x][y])))
                y += 1
            x += 1

    def clearDB(self):
        # 以下代码是对于数据库的操作
        self.sqlofLog.resetDB()
        # 下面是tableWidget刷新操作
        self.ui.tableWidget.setRowCount(0)
    def inquiryDB(self):
        print('日志窗口的查询按钮已经按下')
        peoplename = self.ui.comboBox2.currentText()
        place = self.ui.comboBox.currentText()
        starttime = self.ui.dateTimeEdit1.dateTime()
        starttime = starttime.toString("yyyy-MM-dd hh:mm:ss") # 现在是string格式
        starttime = datetime.datetime.strptime(starttime,'%Y-%m-%d %H:%M:%S') #转为datetime格式
        endtime = self.ui.dateTimeEdit2.dateTime()
        endtime = endtime.toString("yyyy-MM-dd hh:mm:ss") # 现在是string格式
        endtime = datetime.datetime.strptime(endtime,'%Y-%m-%d %H:%M:%S') #转为datetime格式
        # print('starttime', starttime)
        # print('endtime', endtime)

        if peoplename == '任何人员':
            if place == '任何地点':
                sql = '''
                select * from log
                where time between '%s' and '%s'
                ''' % (starttime, endtime)
            else:
                sql = '''
                select * from log
                where place = '%s' and time between '%s' and '%s'
                ''' % (place, starttime, endtime)
        else:
            if place == '任何地点':
                sql = '''
                select * from log
                where name = '%s' and time between '%s' and '%s'
                ''' % (peoplename, starttime, endtime)
            else:
                sql = '''
                select * from log
                where name = '%s' and place = '%s' and time between '%s' and '%s'
                ''' % (peoplename, place, starttime, endtime)

        self.sqlofLog.cursor.execute(sql)
        results = self.sqlofLog.cursor.fetchall()
        # 下面是tableWidget刷新操作
        self.ui.tableWidget.setRowCount(0)
        x = 0
        for i in results:
            y = 0
            row_count = self.ui.tableWidget.rowCount()  # 返回当前行数(尾部)
            self.ui.tableWidget.insertRow(row_count)  # 尾部插入一行
            for ii in i:
                self.ui.tableWidget.setItem(x, y, QTableWidgetItem(str(results[x][y])))
                y += 1
            x += 1


class Camera:
    '''摄像头对象'''

    def __init__(self, url, outLabel):
        self.nameAndLocation = 'Test Video, No Location' # 记录摄像头的名称和地址
        self.displayMode = 0 # 记录摄像头的显示模式
        self.url = url
        self.outLabel = outLabel
        self.cap = cv2.VideoCapture(self.url)
        self.detector = cv2.CascadeClassifier('attachment/haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

    def display(self):
        sqlofDisplay = sqls.SqlF()
        faceMaxNum = 5 # 人脸重复出现的上限为5 连续5次识别为某个人 则该人员需要留下记录
        facecountDic = {} # 用来记录人脸重复的次数
        faceList = [] # 保存当前帧的人脸数据
        tempfaceList = [] # 人脸存储列表，保存上一帧的人的姓名

        if os.path.exists('model/model.yml'):  # 表示为已经录入过人脸了，可以进行人脸识别操作了
            yml = 'model' + '/' + 'model.yml'
            self.recognizer.read(yml)
        '''
        yml文件比较大，避免反复的读取操作是必须的
        '''
        while self.cap.isOpened():
            while True:
                success, frame = self.cap.read()
                if success:
                    rawframe = cv2.resize(frame, (640, 360))
                    # cv2.imshow('raw', frame)
                    frame = cv2.cvtColor(rawframe, cv2.COLOR_BGR2GRAY)
                    # cv2.imshow('raw2', frame)
                    self.faces = self.detector.detectMultiScale(frame, 1.3, 5)
                    rawframe = cv2.putText(rawframe, self.nameAndLocation, (7, 20),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255),
                                        2)  # 这行代码是显示摄像头的名称和地点的
                    # 其中gray为要检测的灰度图像，1.3(scaleFactor)为每次图像尺寸减小的比例，5为minNeighbors
                    #  框选人脸，for循环保证一个能检测的实时动态视频流
                    # for (x, y, w, h) in self.faces:
                    #     # xy为左上角的坐标,w为宽，h为高，用rectangle为人脸标记画框
                    #     cv2.rectangle(frame, (x, y), (x + w, y + w), (255, 0, 0), thickness=2)
                    # 框选人脸，for循环保证一个能检测的实时动态视频流
                    for (x, y, w, h) in self.faces:
                        # xy为左上角的坐标,w为宽，h为高，用rectangle为人脸标记画框
                        cv2.rectangle(rawframe, (x, y), (x + w, y + h), (0, 0, 255), thickness=2)

                        if os.path.exists('model/model.yml'):  # 表示为已经录入过人脸了，可以进行人脸识别操作了
                            # yml = 'model' + '/' + 'model.yml'
                            # self.recognizer.read(yml)
                            idum, confidence = self.recognizer.predict(frame[y:y + h, x:x + w])
                            print('idum为', idum)
                            print('confidence；', confidence)
                            if confidence < 68:
                                cv2.putText(rawframe, userdic[idum], (x + 5, y + 15),
                                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                                            2)
                                # 人脸计数代码区--------
                                faceList.append(userdic[idum])
                                if userdic[idum] not in tempfaceList:
                                    facecountDic[userdic[idum]] = 1
                                else:
                                    facecountDic[userdic[idum]] += 1
                                # 人脸计数代码区--------

                            else:
                                cv2.putText(rawframe, 'unknown', (x + 5, y + 15),
                                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                                            2)

                    rawframe = cv2.cvtColor(rawframe,cv2.COLOR_BGR2RGB)
                    img = QImage(rawframe.data, rawframe.shape[1],
                                 rawframe.shape[0], rawframe.shape[1]*3, QImage.Format_RGB888)
                    # print(self.outLabel)
                    '''
                    循环输出self.outLabel对象，其目的是前期调试使用
                    '''
                    self.outLabel.setPixmap(QPixmap.fromImage(img))

                    # 人脸计数代码区--------
                    for name,count in facecountDic.items():
                        if count >= faceMaxNum:
                            # 如果出现次数超过faceMaxNum
                            nowdatetime = str(datetime.datetime.now()).split('.')[0]
                            nowdatetime = datetime.datetime.strptime(nowdatetime, '%Y-%m-%d %H:%M:%S')
                            sqlofDisplay.saveNameTimePic(name, self.nameAndLocation, nowdatetime)
                            facecountDic[name] = 0 # 归零操作
                    tempfaceList = faceList # 当前帧变为上一帧
                    faceList = [] # 当前帧置零等待接收
                    # 人脸计数代码区--------

                    cv2.waitKey(10)
                else:
                    self.cap.release()
                    self.outLabel.setPixmap(QPixmap('./attachment/nosignal.png'))
                    print('released!')
                    break

    def displaySimpleBrand(self):
        '''
        只进行人脸检测的版本
        '''
        while self.cap.isOpened():
            while True:
                success, frame = self.cap.read()
                if success:
                    rawframe = cv2.resize(frame, (640, 360))
                    # cv2.imshow('raw', frame)
                    frame = cv2.cvtColor(rawframe, cv2.COLOR_BGR2GRAY)
                    # cv2.imshow('raw2', frame)
                    faces = self.detector.detectMultiScale(frame, 1.3, 5)
                    # 其中gray为要检测的灰度图像，1.3为每次图像尺寸减小的比例，5为minNeighbors
                    rawframe = cv2.putText(rawframe, self.nameAndLocation, (7, 20),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255),
                                        2)  # 这行代码是显示摄像头的名称和地点的

                    # 框选人脸，for循环保证一个能检测的实时动态视频流
                    for (x, y, w, h) in faces:
                        # xy为左上角的坐标,w为宽，h为高，用rectangle为人脸标记画框
                        cv2.rectangle(rawframe, (x, y), (x + w, y + h), (0, 0, 255), thickness=2)

                    rawframe = cv2.cvtColor(rawframe,cv2.COLOR_BGR2RGB)
                    img = QImage(rawframe.data, rawframe.shape[1],
                                 rawframe.shape[0], rawframe.shape[1]*3, QImage.Format_RGB888)

                    # print(self.outLabel)
                    '''
                    循环输出self.outLabel对象，其目的是前期调试使用
                    '''
                    self.outLabel.setPixmap(QPixmap.fromImage(img))
                    cv2.waitKey(10)
                else:
                    self.cap.release()
                    self.outLabel.setPixmap(QPixmap('./attachment/nosignal.png'))
                    print('released!')
                    break

    def displayJustdisplayBrand(self):
        '''
        displayJustdisplayBrand是只进行播放视频帧的版本 没有人脸检测和人脸识别
        '''
        while self.cap.isOpened():
            while True:
                success, frame = self.cap.read()
                if success:
                    rawframe = cv2.resize(frame, (640, 360))
                    rawframe = cv2.putText(rawframe, self.nameAndLocation, (7, 20),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255),
                                        2)  # 这行代码是显示摄像头的名称和地点的
                    rawframe = cv2.cvtColor(rawframe,cv2.COLOR_BGR2RGB)
                    img = QImage(rawframe.data, rawframe.shape[1],
                                 rawframe.shape[0], rawframe.shape[1]*3, QImage.Format_RGB888)
                    self.outLabel.setPixmap(QPixmap.fromImage(img))
                    cv2.waitKey(10)
                else:
                    self.cap.release()
                    self.outLabel.setPixmap(QPixmap('./attachment/nosignal.png'))
                    print('released!')
                    break

    def displayLuruBrand(self):
        '''
        displayLuruBrand是Camera对象针对录入界面的定制版本，没有实时的人脸识别以及
        识别文字表示功能，更符合录入界面的应用场景需要
        '''
        while self.cap.isOpened():
            while True:
                success, frame = self.cap.read()
                if success:
                    rawframe = cv2.resize(frame, (640, 360))
                    # cv2.imshow('raw', frame)
                    frame = cv2.cvtColor(rawframe, cv2.COLOR_BGR2GRAY)
                    # cv2.imshow('raw2', frame)
                    faces = self.detector.detectMultiScale(frame, 1.3, 5)
                    # 其中gray为要检测的灰度图像，1.3为每次图像尺寸减小的比例，5为minNeighbors
                    rawframe = cv2.putText(rawframe, 'enroll in facial recognition', (7, 20),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255),
                                        2)  # 这行代码是显示摄像头的名称和地点的

                    # 框选人脸，for循环保证一个能检测的实时动态视频流
                    for (x, y, w, h) in faces:
                        # xy为左上角的坐标,w为宽，h为高，用rectangle为人脸标记画框
                        cv2.rectangle(rawframe, (x, y), (x + w, y + h), (0, 0, 255), thickness=2)

                    rawframe = cv2.cvtColor(rawframe, cv2.COLOR_BGR2RGB)
                    img = QImage(rawframe.data, rawframe.shape[1],
                                 rawframe.shape[0], rawframe.shape[1]*3, QImage.Format_RGB888)

                    # print(self.outLabel)
                    '''
                    循环输出self.outLabel对象，其目的是前期调试使用
                    '''
                    self.outLabel.setPixmap(QPixmap.fromImage(img))
                    cv2.waitKey(10)
                else:
                    self.cap.release()
                    self.outLabel.setPixmap(QPixmap('./attachment/nosignal.png'))
                    print('released!')
                    break

    def close(self):
        global systemLock
        if self.url == 0:
            systemLock = 0  # 解锁
        self.cap.release()


class LogInWindow():
    def __init__(self):
        self.ui = QUiLoader().load('LogIn.ui')
        self.ui.setFixedSize(self.ui.width(), self.ui.height())
        self.ui.label.setPixmap(QPixmap('attachment/welcome.png'))
        self.ui.pushButton1.clicked.connect(self.loginfunction)
        self.ui.pushButton2.clicked.connect(self.registerfunction)
        self.StartSignal = False
        self.sqloflogin = sqls.SqlF()

    def loginfunction(self):
        print('登录按钮已经按下')
        self.sqloflogin.dbclose()
        self.sqloflogin.__init__()
        self.accountlist = []
        for i in self.sqloflogin.getAllaccount():
            self.accountlist.append(i[0])
        if self.ui.lineEdit1.text() == '':
            QMessageBox.about(self.ui, '错误', '您还没有输入账号')
        elif self.ui.lineEdit2.text() == '':
            QMessageBox.about(self.ui, '错误', '您还没有输入密码')
        elif self.ui.lineEdit1.text() in self.accountlist:
            prepassword = self.sqloflogin.loginAccountPassword(self.ui.lineEdit1.text())
            password = prepassword[0]
            if self.ui.lineEdit2.text() == password:
                QMessageBox.about(self.ui, '登录成功', '欢迎使用!')
                self.StartSignal = True
                print(self.StartSignal)
                self.ui.close()
            else:
                QMessageBox.about(self.ui, '错误', '账号或密码错误！')
        else:
            print(self.sqloflogin.getAllaccount())
            QMessageBox.about(self.ui, '错误', '账号或密码错误！')

    def registerfunction(self):
        print('注册按钮已经按下')
        self.registerwin = RegisterWindow()
        self.registerwin.ui.show()


class RegisterWindow():
    def __init__(self):
        self.ui = QUiLoader().load('Register.ui')
        self.ui.buttonBox.accepted.connect(self.ok)
        self.ui.buttonBox.rejected.connect(self.cancel)
        self.sqlofregister = sqls.SqlF()
    def ok(self):
        accountlist = []
        adminpassword = self.sqlofregister.loginAccountPassword('admin')[0]
        for i in self.sqlofregister.getAllaccount():
            accountlist.append(i[0])
        if self.ui.lineEdit1.text() not in accountlist:
            if self.ui.lineEdit3.text() == adminpassword:
                newaccount = self.ui.lineEdit1.text()
                newpassword = self.ui.lineEdit2.text()
                self.sqlofregister.register(newaccount, newpassword)
                QMessageBox.about(self.ui, '欢迎', '新用户注册成功，请记好账号密码！')
                start_login.accountlist.append(newaccount)
            else:
                QMessageBox.about(self.ui, '错误', '超级管理员密码错误！')
        else:
            QMessageBox.about(self.ui, '错误', '该账户已经存在！')

    def cancel(self):
        print('取消注册新用户')


app = QApplication([])
start_login = LogInWindow()
start_login.ui.show()
app.exec_()

if start_login.StartSignal == True:
    mainwindow = MWindow()
    mainwindow.mui.show()
    app.exec_()

# 临时入口用于调试
# app = QApplication([])
# mainwindow = MWindow()
# mainwindow.mui.show()
# app.exec_()
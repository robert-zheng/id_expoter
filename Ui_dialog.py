# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\workspace_py\id_export\dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(397, 301)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 20, 120, 30))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 60, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 100, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(30, 140, 70, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(30, 180, 100, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.lineEdit_host = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_host.setGeometry(QtCore.QRect(150, 20, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_host.setFont(font)
        self.lineEdit_host.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.lineEdit_host.setObjectName("lineEdit_host")
        self.lineEdit_user = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_user.setGeometry(QtCore.QRect(150, 60, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_user.setFont(font)
        self.lineEdit_user.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.lineEdit_user.setObjectName("lineEdit_user")
        self.lineEdit_passwd = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_passwd.setGeometry(QtCore.QRect(150, 100, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lineEdit_passwd.setFont(font)
        self.lineEdit_passwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_passwd.setObjectName("lineEdit_passwd")
        self.lineEdit_port = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_port.setGeometry(QtCore.QRect(150, 140, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_port.setFont(font)
        self.lineEdit_port.setObjectName("lineEdit_port")
        self.cBox_database = QtWidgets.QComboBox(Dialog)
        self.cBox_database.setGeometry(QtCore.QRect(150, 180, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.cBox_database.setFont(font)
        self.cBox_database.setObjectName("cBox_database")
        self.cBox_database.addItem("")
        self.cBox_database.addItem("")
        self.cBox_database.addItem("")
        self.cBox_database.addItem("")
        self.Button_yes = QtWidgets.QPushButton(Dialog)
        self.Button_yes.setGeometry(QtCore.QRect(130, 240, 93, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Button_yes.setFont(font)
        self.Button_yes.setObjectName("Button_yes")
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.lineEdit_host.raise_()
        self.lineEdit_user.raise_()
        self.lineEdit_port.raise_()
        self.cBox_database.raise_()
        self.Button_yes.raise_()
        self.lineEdit_passwd.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "数据库设置"))
        self.label.setText(_translate("Dialog", "主机地址:"))
        self.label_2.setText(_translate("Dialog", "用户名:"))
        self.label_3.setText(_translate("Dialog", "密码:"))
        self.label_4.setText(_translate("Dialog", "端口:"))
        self.label_5.setText(_translate("Dialog", "数据库:"))
        self.lineEdit_host.setText(_translate("Dialog", "101.132.158.171"))
        self.lineEdit_user.setText(_translate("Dialog", "test_read"))
        self.lineEdit_port.setText(_translate("Dialog", "3306"))
        self.cBox_database.setItemText(0, _translate("Dialog", "xjlcdbnew"))
        self.cBox_database.setItemText(1, _translate("Dialog", "zztestdb"))
        self.cBox_database.setItemText(2, _translate("Dialog", "zzlcdb"))
        self.cBox_database.setItemText(3, _translate("Dialog", "lqtestdb"))
        self.Button_yes.setText(_translate("Dialog", "确定"))

'''
Author: ylzheng zyl_js@126.com
Date: 2023-09-13 21:21:05
LastEditors: ylzheng zyl_js@126.com
LastEditTime: 2023-09-13 21:45:06
FilePath: \id_export\dialog.py
Description: 

Copyright (c) 2023 by ${git_name_email}, All Rights Reserved. 
'''
from PyQt5 import QtWidgets
from Ui_dialog import Ui_Dialog
from PyQt5.QtCore import pyqtSignal

class MyDialog(QtWidgets.QDialog, Ui_Dialog):
    signal_data=pyqtSignal(dict)
    def __init__(self,cfg):
        super(MyDialog, self).__init__()
        self.setupUi(self)
        self.my_sql_config = {"host":cfg["host"],"user":cfg["user"],"passwd":cfg["passwd"],"port":cfg["port"],"db":cfg["db"]}
        self.Button_yes.clicked.connect(self.get_data)
        self.lineEdit_host.setText(self.my_sql_config["host"])
        self.lineEdit_user.setText(self.my_sql_config["user"])
        self.lineEdit_passwd.setText(self.my_sql_config["passwd"])
        self.lineEdit_port.setText(str(self.my_sql_config["port"]))
        self.cBox_database.addItem(self.my_sql_config["db"])


    def get_data(self):
        self.my_sql_config["host"]=self.lineEdit_host.text()
        self.my_sql_config["user"]=self.lineEdit_user.text()
        self.my_sql_config["passwd"]=self.lineEdit_passwd.text()
        self.my_sql_config["port"]=int(self.lineEdit_port.text())
        self.my_sql_config["db"]=self.cBox_database.currentText()
        self.signal_data.emit(self.my_sql_config)
        self.close()
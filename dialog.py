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
    def __init__(self):
        super(MyDialog, self).__init__()
        self.setupUi(self)
        self.my_sql_config = {"host":"","user":"","passwd":"","port":"","database":"zztestdb"}
        self.Button_yes.clicked.connect(self.get_data)

    def get_data(self):
        self.my_sql_config["host"]=self.lineEdit_host.text()
        self.my_sql_config["user"]=self.lineEdit_user.text()
        self.my_sql_config["password"]=self.lineEdit_passwd.text()
        self.my_sql_config["port"]=int(self.lineEdit_port.text())
        self.my_sql_config["database"]=self.cBox_database.currentText()
        self.signal_data.emit(self.my_sql_config)
        self.close()
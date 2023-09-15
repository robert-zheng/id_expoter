from PyQt5 import QtWidgets,QtSql
from Ui_mainwindow import  Ui_MainWindow
from Ui_dialog import Ui_Dialog
from PyQt5.QtCore import QTimer,Qt,QSize,QThread,pyqtSignal
from PyQt5.QtGui import QColor
import sys
import time
import os
import logging
import threading
import pymysql
import datetime
import numpy as np
import openpyxl
from openpyxl import Workbook
from pyqtgraph import GraphicsLayoutWidget
from openpyxl.chart import (
    LineChart,
    Reference,
)
from dialog import MyDialog
import json

class MyWindowShow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindowShow, self).__init__()
        self.setupUi(self)
        # self.layout=QtWidgets.QGridLayout()
        self.setWindowTitle("数据库查询 V1.0")
        self.log_init()
        # 定义子窗口
        self.child_dialog = MyDialog()
        self.actionset.triggered.connect(self.child_dialog.show)
        #绑定QT信号槽
        self.child_dialog.signal_data.connect(self.get_database_config)
        self.Button_connect.clicked.connect(self.mysql_connect)
        self.Button_export.clicked.connect(self.export_excel)
        try:
            f = open("config.json",encoding="utf-8")
            self.cfg = json.load(f,encoding="utf-8")
            f.close()
        except OSError as reason:
            logging.info(str(reason))

    def mysql_connect(self,):
        logging.info("mysql_connect()...")
        if self.Button_connect.text()=="连接":
            try:
                self.conn = pymysql.connect(
                            host = self.cfg["host"],
                            user = self.cfg["user"],
                            password = self.cfg["passwd"],
                            port = self.cfg["port"],
                            database = self.cfg["db"],
                            charset = "utf8")
                self.cursor_Xj=self.conn.cursor()
                self.statusBar.showMessage("主机已连接%s" %self.cfg["host"])
                logging.info("主机已连接%s" %self.cfg["host"])
                self.Button_connect.setText("断开连接")
                # 获取所有存在的批次，添加到批次下拉框中
                self.get_pc()
            except OSError as reason:
                self.statusBar.showMessage("服务器连接失败..."+str(reason))
                logging.info("服务器连接失败...%s" %str(reason))
        else:
            self.conn.close()
            logging.info("已经断开连接%s" %self.cfg["host"])
            self.statusBar.showMessage("已经断开连接%s" %self.cfg["host"])
            self.Button_connect.setText("连接")

    def get_pc(self):
        """
        get_pc:获取所有生产批次，添加到下拉框界面中...
        """
        logging.info("正在执行'get_pc'...")
        sql="""select pc from t_pc ORDER BY intime desc"""
        self.cursor_Xj.execute(sql)
        self.pc_list=list(self.cursor_Xj.fetchall())
        logging.info(self.pc_list)
        self.cBox_pc_filter.clear()
        self.cBox_pc_filter.addItem("请选择批次")
        for each in self.pc_list:
            self.cBox_pc_filter.addItems(each)
        

    def export_excel(self,):
        logging.info("export_excel()...")
        mid_start = self.Edit_MidStart.text()
        mid_end = self.Edit_MidEnd.text()
        if len(mid_start)==22 and len(mid_end)==22:
            pass

    def log_init(self):    
        if not(os.path.exists("LogFile")):
            os.mkdir("LogFile")
        time_str = time.strftime('%Y_%m%d-%H%M%S', time.localtime())
        log_file_name = ".\\LogFile\\"+time_str+".txt"
        logging.basicConfig(filename=log_file_name,format="%(asctime)s %(name)s:%(levelname)s-->%(message)s",level='DEBUG',)

    def get_database_config(self,config):
        self.cfg["host"] = config["host"]
        self.cfg["user"] = config["user"]
        self.cfg["passwd"] = config["password"]
        self.cfg["port"] = config["port"]
        self.cfg["db"] = config["database"]
        self.save_config()
    
    def save_config(self):
        f = open("config.json",'w',encoding="utf-8")
        json.dump(self.cfg,f,indent=4)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindowShow()
    window.show()
    sys.exit(app.exec_())
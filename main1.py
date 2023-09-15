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
import json
import make_report1

class MyWindowShow(QtWidgets.QMainWindow, Ui_MainWindow):

    power_header_number=[4,116,117,118,119,120]
    pin_header_number=[4,20,21,22,23,24,25,26,27,28,29,30,31]
    freq_header_number=[4,114,115]
    my_sql_config = {"host":"","user":"","passwd":"","port":"","database":"zztestdb"}
    testresult = []
    testdata = []
    count_switch=False
    cmd2="""select max({param}),min({param}),avg({param}),std({param}) from t_testdata where pc='{pc}' and result='1' and tstep='0'"""
    cmd3="""select max({param}),min({param}),avg({param}),std({param}) from t_testdata where pc='{pc}' and result='1' and barcode='{barcode}' and tstep='0'"""
    # 统计模块数量
    cmd4="""SELECT COUNT(*) FROM t_testdata WHERE pc='{pc}' and tstep='0' and {param}=1"""
    # 统计测试次数
    cmd5="""SELECT COUNT(*) FROM t_testdata WHERE pc='{pc}' and tstep='0' and {param}=2"""
    cmd6="""SELECT COUNT(*) FROM t_testdata WHERE pc='{pc}' and tstep='0' """
    # 统计模块数量
    cmd7="""SELECT COUNT(DISTINCT(barcode)) FROM t_testdata WHERE pc='{pc}' and tstep='0' """
    cmd8= """SELECT COUNT(DISTINCT(barcode)) FROM t_testdata WHERE pc='{pc}' and tstep='0' and {param}={value}"""
    cmd9= """SELECT COUNT(DISTINCT(barcode)) FROM t_testresult WHERE pc='{pc}'  and {param}={value}"""
    pc = None
    step=0
    def __init__(self):
        super(MyWindowShow, self).__init__()
        self.setupUi(self)
        # self.layout=QtWidgets.QGridLayout()
        self.setWindowTitle("数据库查询 V1.0")
        # 定义子窗口
        self.child_dialog = MyDialog()
        self.actionset.triggered.connect(self.child_dialog.show)
        #绑定QT信号槽
        self.child_dialog.signal_data.connect(self.get_database_config)
        self.Button_connect.clicked.connect(self.mysql_connect)
        self.Button_consult.clicked.connect(self.consult)
        self.Button_export.clicked.connect(self.export_excel)
        self.table_data.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.actionexit.triggered.connect(QtWidgets.qApp.quit)
        self.cBox_workid.currentTextChanged.connect(self.workid_filter)
        self.cBox_pc_filter.currentIndexChanged.connect(self.select_pc)
        self.tabWidget.currentChanged.connect(self.filter)
        self.line_barcode.editingFinished.connect(self.read_by_barcode)
        self.tb_res.itemClicked.connect(self.tb_res_clicked)
        # 初始化图表
        self.pyqt_graph_init()
        # 显示/隐藏表头
        # self.table_data.horizontalHeader().setVisible(True)
        self.host=""
        self.user=""
        self.password=""
        self.port=""
        self.cursor_Xj=""
        self.conn=""
        self.log_init()
        logging.info("程序初始化...")
        self.table_dict=self.get_dict()
        try:
            f = open("config.json",encoding="utf-8")
            self.cfg = json.load(f,encoding="utf-8")
        except OSError as reason:
            logging.info(str(reason))

    def pyqt_graph_init(self):
        '''
        @description: 
        @param {*}
        @return {*}
        @author: zhengyanlong
        '''        
        self.gv_static = self.gl_1.addPlot(title="静态功耗")
        self.gv_dynamic = self.gl_1.addPlot(title="动态功耗")
        self.gl_1.nextRow()
        self.gv_snr = self.gl_1.addPlot(title="SNR")
        self.gv_rssi = self.gl_1.addPlot(title="RSSI")
        self.gv_static.setLabel('left', '静态功耗', units='mA')
        self.gv_dynamic.setLabel('left', '动态功耗', units='mA')
        self.gv_snr.setLabel('left','接收SNR',units='dB')
        self.gv_rssi.setLabel('left','接收RSSI',units='dB')
        self.gv_static.setYRange(30,60)
        self.gv_dynamic.setYRange(70,100)
        self.gv_snr.setYRange(30,70)
        self.gv_rssi.setYRange(-70,-50)
        self.gv_static.showGrid(x=True, y=True)
        self.gv_dynamic.showGrid(x=True, y=True)
        self.gv_snr.showGrid(x=True, y=True)
        self.gv_rssi.showGrid(x=True, y=True)

    def log_init(self):
        '''
        @description: 初始化log
        @param {None}
        @return {None}
        @author: zhengyanlong
        '''        
        if not(os.path.exists("LogFile")):
            os.mkdir("LogFile")
        time_str = time.strftime('%Y_%m%d-%H%M%S', time.localtime())
        log_file_name = ".\\LogFile\\"+time_str+".txt"
        logging.basicConfig(filename=log_file_name,format="%(asctime)s %(name)s:%(levelname)s-->%(message)s",level='DEBUG',)

    def select_pc(self):
        '''
        @description: 
        @param {*}
        @return {*}
        @author: zhengyanlong
        '''
        self.pc = self.cBox_pc_filter.currentText()

    def get_dict(self):
        """
        翻译表testdata字段
        """
        logging.info("正在执行'get_dict'...")
        table_dict={}
        try:
            f_dict = open("dict.txt",'r', encoding='utf-8')
            list_name=f_dict.read().split('\n')
            for each in list_name:
                list1=each.split(':')
                table_dict[list1[0]]=list1[1]
        except Exception as reason:
            self.statusBar.showMessage("配置文件打开失败,%s" % reason)
            logging.debug("配置文件打开失败,%s" % reason)
        return table_dict

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
        for each in self.pc_list:
            self.cBox_pc_filter.addItems(each)

    def get_workid(self):
        """
        获取该批次的所有工装号
        """
        logging.info("正在执行get_workid")
        sql="""select distinct(workid) from t_testdata where pc='{pc}'""".format(pc=self.pc)
        logging.info(sql)
        self.cursor_Xj.execute(sql)
        self.workid_list=self.cursor_Xj.fetchall()
        self.cBox_workid.clear()
        self.cBox_workid.addItem("工装ID")
        for each in self.workid_list:
            self.cBox_workid.addItems(each)

    def workid_filter(self):
        '''
        @description:根据工装ID筛选框筛选测试结果 
        @param {*}
        @return {*}
        @author: zhengyanlong
        '''
        logging.info("正在执行workid_filter...")
        workid = self.cBox_workid.currentText()
        logging.info(workid)
        logging.info(self.pc)
        if workid!="工装ID":
            self.consult(workid)
        

    def mysql_connect(self):
        '''
        @description: 连接MySQL数据库
        @param {*}
        @return {*}
        @author: zhengyanlong
        '''
        logging.info("正在执行'mysql_connect'...")
        if self.Button_connect.text()=="连接":
            try:
                self.conn = pymysql.connect(
                            host = self.my_sql_config["host"],
                            user = self.my_sql_config["user"],
                            password = self.my_sql_config["password"],
                            port = self.my_sql_config["port"],
                            database = self.my_sql_config["database"],
                            charset = "utf8")
                self.cursor_Xj=self.conn.cursor()
                self.statusBar.showMessage("主机已连接%s" %self.my_sql_config["host"])
                logging.info("主机已连接%s" %self.my_sql_config["host"])
                self.Button_connect.setText("断开连接")
                # 获取所有存在的批次，添加到批次下拉框中
                self.get_pc()
                self.UI_set(True)
            except OSError as reason:
                self.statusBar.showMessage("服务器连接失败..."+str(reason))
                logging.info("服务器连接失败...%s" %str(reason))

        else:
            self.conn.close()
            logging.info("已经断开连接%s" %self.my_sql_config["host"])
            self.UI_set(False)


    def UI_set(self,connect):
        """
        连接/断开数据库后,更新UI界面的按钮使能...
        """
        logging.info("正在执行UI_set,connect==%s" %connect)
        if connect:
            self.Button_consult.setEnabled(True)
            self.Button_filter.setEnabled(True)
            self.table_data.setColumnCount(len(self.cfg["testdatasub"]))      # 设定表格列数
            logging.info("testdata")
            # table_header_convert=[]
            # for each in self.cfg['trans']:
            #     try:
            #         table_header_convert.append(self.table_dict[each])
            #     except OSError as reason:
            #         logging.info(reason)               
            self.table_data.setHorizontalHeaderLabels(self.cfg['testdatasub'])
        else:
            self.Button_connect.setText("连接")
            self.Button_consult.setEnabled(False)
            self.Button_filter.setEnabled(False)
            self.statusBar.showMessage("服务器已经断开连接...")

    def UI_update(self,result):
        logging.info("开始向窗口更新测试结果...")
        self.table_result.setRowCount(len(result))
        for each in result:
            row = result.index(each)
            counter = 0
            for data in each:
                QItem = QtWidgets.QTableWidgetItem(str(data))
                column = counter
                self.table_result.setItem(row,column,QItem)
                counter = counter+1


    def consult(self,workid=None):
        """
        查询数据库
        """
        logging.info("开始查询数据库...")
        self.pc = self.cBox_pc_filter.currentText()
        self.get_workid()
        logging.info("t_testdata一共有%d个字段" %len(self.table_header))
        logging.info("t_testdata字段:"+str(self.table_header))
        result=[]
        result.append(['3.3V电压值:',]+self.get_count('z3_11'))
        result.append(['1.2V电压值:',]+self.get_count('z3_9'))
        result.append(['静态功耗(mA):',]+self.get_count('z7_3'))
        result.append(['动态功耗(mA):',]+self.get_count('z7_4'))
        result.append(['RX SNR(dB):',]+self.get_count('z5_2'))
        result.append(['RX RSSI:',]+self.get_count('z5_37'))
        result.append(['TX SNR(dB):',]+self.get_count('z5_41'))
        result.append(['TX RSSI:',]+self.get_count('z5_76'))
        result.append(['CAP电压:',]+self.get_count('z10_4'))
        result.append(['Boost电压:',]+self.get_count('z10_6'))
        result.append(['频偏(ppm):',]+self.get_count('z6_1'))
        test_count = self.excute_cmd(self.cmd6)                 # 总的测试测试
        result.append(['测试次数:',test_count])
        pass_count = self.excute_cmd(self.cmd4,"result")
        fail_count = self.excute_cmd(self.cmd5,"result")
        mod_count = self.excute_cmd(self.cmd7)
        pass_mod_count = self.excute_cmd(self.cmd8,"result",'1')        
        fail_mod_count = self.excute_cmd(self.cmd8,"result",'2')
        final_fail_mod_count = self.excute_cmd(self.cmd9,"tresult",'2')
        # 不良模块占总的模块比例
        final_fail_mod_percent = '{:.2%}'.format(final_fail_mod_count/mod_count)
        # 统计一次通过率
        one_pass_percent = '{:.2%}'.format((pass_mod_count-fail_mod_count+final_fail_mod_count)/mod_count)
        result.append(["测试成功次数",pass_count])
        result.append(["测试失败次数",fail_count])
        result.append(["测试模块数量",mod_count])
        result.append(["不良模块数量",final_fail_mod_count,final_fail_mod_percent])
        result.append(["一次通过率",one_pass_percent])
        result.append(["F107",self.excute_cmd(self.cmd5,"z4_0")])
        result.append(["F108",self.excute_cmd(self.cmd5,"z3_0")])
        result.append(["F109",self.excute_cmd(self.cmd5,"z5_0")])
        result.append(["F110",self.excute_cmd(self.cmd5,"z6_0")])
        result.append(["F111",self.excute_cmd(self.cmd5,"z7_0")])
        result.append(["F112",self.excute_cmd(self.cmd5,"z8_0")])
        result.append(["F113",self.excute_cmd(self.cmd5,"z10_0")])
        self.UI_update(result)


    def export_data(self):
        sql = """select * from t_testdata """
        self.pc = self.cBox_pc_filter.currentText()
        if self.pc == "选择批次":
            cond_1 = ""
        else:
            cond_1="where pc='%s' and tstep=0" %(self.pc)
        sql = sql+cond_1
        logging.info("执行SQL语句:%s" % sql)
        try:
            # 执行 sql 语句
            self.cursor_Xj.execute(sql)
            # 显示出所有数据
            self.data_result =self.cursor_Xj.fetchall()
            self.np_result=np.array(self.data_result)
            logging.info("shape:(%d,%d)" %(self.np_result.shape))
            self.statusBar.showMessage("查询到数据%d条···" % self.np_result.shape[0])
            logging.info("查询到数据%d条···" % self.np_result.shape[0])
        except:
            logging.info("Error: unable to fetch data")
        self.table_data.setRowCount(len(self.data_result))
        counter=0
        for row in self.data_result:
            column = 0
            for each in row:
                if isinstance(each,datetime.datetime):
                    each=each.strftime('%Y-%m-%d %H:%M:%S')
                if isinstance(each,int) or isinstance(each,float):
                    each=str(each)
                if each == None:
                    each="None"
                QItem = QtWidgets.QTableWidgetItem(each)
                self.table_data.setItem(counter,column,QItem)
                column = column+1
            counter=counter+1
        self.table_data.resizeColumnToContents()
        

    def get_result(self):
        """
        获取总结果，返回数据打印在数据表“测试数据”中...
        """
        logging.info("获取总结果，返回数据打印在数据表“测试数据”中...")
        result = []
        self.cursor_Xj.execute(self.cmd5.format(pc=self.pc))
        test_count =self.cursor_Xj.fetchone()[0]
        np_testresult = np.array(self.testresult)
        # logging.info("np_testresult shape:%d %d"%np_testresult.shape)
        fail_list = np.where(np_testresult[:,4]=='2')                # tresult==2
        result.append(["测试批次:",self.pc])
        result.append(["测试次数:",test_count])
        result.append(["测试模块数量:",len(modul_list)])
        result.append(["失败模块数量:",len(fail_list[0])])
        logging.info("Fail list:"+str(fail_list))
        result.append(["失败模块生产ID:"])
        for each in fail_list[0]:
            logging.info(type(np_testresult[each,0]))
            logging.info(np_testresult[each,0])
            logging.info(each)
            result.append(["-->",np_testresult[each][0]])
        # MySQL 查询最大值，最小值，平均值
        result.append(["测试项","最大值","最小值","平均值","方差"])
        result.append(['静态功耗(mA):',]+self.get_count('z7_3'))
        result.append(['动态功耗(mA):',]+self.get_count('z7_4'))
        result.append(['RX SNR(dB):',]+self.get_count('z5_2'))
        result.append(['RX RSSI:',]+self.get_count('z5_37'))
        result.append(['TX SNR(dB):',]+self.get_count('z5_41'))
        result.append(['TX RSSI:',]+self.get_count('z5_76'))
        result.append(["每个模块单独测试数据如下:"])
        
        if self.count_switch:
            modul_list = np.unique(self.np_result[:,4])
            for each in modul_list:
                result.append((each,))
                result.append(['静态功耗(mA):',]+self.get_mod_count('z7_3',str(each)))
                result.append(['动态功耗(mA):',]+self.get_mod_count('z7_4',str(each)))
                result.append(['RX SNR(dB):',]+self.get_mod_count('z5_2',str(each)))
                result.append(['RX RSSI:',]+self.get_mod_count('z5_37',str(each)))
                result.append(['TX SNR(dB):',]+self.get_mod_count('z5_41',str(each)))
                result.append(['TX RSSI:',]+self.get_mod_count('z5_76',str(each)))
        logging.info("get_result-->result:")
        logging.info(result)
        return result

    def get_count(self,name):
        """
        统计name的最大值,最小值,平均值...
        """
        sql = self.cmd2.format(param=name,pc=self.pc)
        logging.info(sql)
        try:
            self.cursor_Xj.execute(sql)
            res=self.cursor_Xj.fetchall()
            result=[]
            for each in res[0]:
                result.append(round(each,2))
        except:
            logging.info("SQL执行失败,%s"%sql)
        return result


    def excute_cmd(self,cmd,param=None,value='2'):
        sql=cmd.format(param=param,pc=self.pc,value=value)
        logging.info("SQL Command:"+sql)
        self.cursor_Xj.execute(sql)
        res=self.cursor_Xj.fetchone()[0]
        logging.info("counter:"+str(res))
        return res

    def get_mod_count(self,name,barcode):
        sql = self.cmd3.format(param=name,pc=self.pc,barcode=barcode)
        logging.info(sql)
        self.cursor_Xj.execute(sql)
        power_result=self.cursor_Xj.fetchall()
        result=[]
        for each in power_result[0]:
            if each !=None:
                result.append(round(each,2))
        return result

    def export(self):
        logging.info("开始导出测试报告...")
        report = make_report1.make_report(self.conn,self.pc)
        self.statusBar.showMessage("已经导出测试报告%s" %report)
        logging.info("已经导出测试报告%s" %report)
        

    def export_excel(self):
        '''
        @description: 启动后台线程输出到Excel文件
        @param {*}
        @return {*}
        @author: zhengyanlong
        '''
        self.export_thread=threading.Thread(target=self.export,args=[])
        self.export_thread.setDaemon(True)
        self.export_thread.start()

    def filter(self,index):
        '''
        @description: 通过pyqtgraph生成图表...
        @param {*}
        @return {*}
        @author: zhengyanlong
        '''
        logging.info("正在执行信息过滤...")
        if index==1 and self.pc!=None:
            logging.info("生成图表...")
            sql = """select z7_3,z7_4,z5_2,z5_37 from t_testdata where pc='{pc}' and result=1 and tstep=0""".format(pc=self.pc)
            self.cursor_Xj.execute(sql)
            temp = self.cursor_Xj.fetchall()
            data = np.array(temp)
            logging.info(data.shape)
            logging.info(data[:,0])
            self.gv_static.clear()
            self.gv_dynamic.clear()
            self.gv_snr.clear()
            self.gv_rssi.clear()
            self.gv_static.plot(data[:,0], pen='g',title="静态功耗")
            self.gv_dynamic.plot(data[:,1],pen='g')
            self.gv_snr.plot(data[:,2],)
            self.gv_rssi.plot(data[:,3],)
        if index==2 and self.pc!=None:
            logging.info("查询数据...")

    
    def tb_res_clicked(self,item):
        logging.info("select testdata..."+item.text())
        row = item.row()
        logging.info("点击了第%d行,第%d列,内容%s..."%(item.row(),item.column(),item.text()))
        id = self.res[row][0]
        logging.info("ID=%s"%id)
        sql = "select * from t_testdatasub where id='{id}'".format(id=id)
        cursor = self.conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        logging.info("开始向窗口更新测试结果...")
        self.table_data.setRowCount(len(result))
        for each in result:
            logging.info(each)
            row = result.index(each)
            counter = 0
            for data in each:
                if isinstance(data,str):
                    QItem = QtWidgets.QTableWidgetItem(data)
                else:
                    QItem = QtWidgets.QTableWidgetItem(str(data))
                column = counter
                if counter==2 and data=='2':
                    QItem.setForeground(QColor(100,111,30))
                QItem.setTextAlignment(Qt.AlignCenter)
                self.table_data.setItem(row,column,QItem)
                counter = counter+1
        self.tb_res.resizeColumnsToContents()


    def tb_res_update(self):
        logging.info("开始向窗口更新测试结果...")
        result = self.res
        self.tb_res.setRowCount(len(result))
        self.tb_res.setColumnCount(len(result[0])-1)
        self.tb_res.setVerticalHeaderLabels(["条形码","测试结果","工序","测试时间","错误码"])
        self.tb_res.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        for each_row in result:
            each = list(each_row)
            logging.info(each)
            row = result.index(each_row)
            counter = 0
            if each[2]=='2':
                item_color = QColor("red")
                each[2] = "失败"
            else:
                item_color = QColor("green")
                each[2] = "成功"
            if each[3]=='0':
                each[3] = "单板"
            else:
                each[3] = "写ID"
            for data in each[1:]:
                if isinstance(data,str):
                    QItem = QtWidgets.QTableWidgetItem(data)
                else:
                    QItem = QtWidgets.QTableWidgetItem(str(data))
                column = counter
                QItem.setTextAlignment(Qt.AlignCenter)
                QItem.setForeground(item_color)
                self.tb_res.setItem(row,column,QItem)
                counter = counter+1
        self.tb_res.resizeColumnsToContents()


    def read_by_barcode(self):
        '''
        @description: tab_2 查询测试结果
        @param {*}
        @return {*}
        @author: zhengyanlong
        '''
        logging.info("read_by_barcode...")
        barcode = self.line_barcode.text()
        self.statusBar.showMessage("生产ID:%s"%barcode)
        sql = "select id,barcode,result,tstep,intime,errcode from t_testdata where barcode='{barcode}' order by intime desc".format(barcode=barcode)     

        try:
            self.cursor_Xj.execute(sql)
            self.res = self.cursor_Xj.fetchall()
            self.tb_res_update()
        except OSError as reason:
            logging.info("read_by_barcode Fail..."+str(reason))


        sql = "select modulid,icid from t_modulids where barcode='{barcode}'".format(barcode=barcode)
        try:
            self.cursor_Xj.execute(sql)
            data = self.cursor_Xj.fetchone()
            self.line_modulid.setText(data[0])
            self.line_icid.setText(data[1])
        except OSError as reason:
            logging.info("read_by_barcode Fail..."+str(reason))
        

    def get_database_config(self,config):
        self.my_sql_config=config

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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindowShow()
    window.show()
    sys.exit(app.exec_())


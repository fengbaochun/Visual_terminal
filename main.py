import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QMessageBox
from PyQt5.QtCore import QTimer
#调用文件
from Ui_mainwindow import Ui_MainWindow  
from find_color_block import Find_color_block  
from Tool_box.Serial_tool import *



class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self,parent = None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        #设置软件title
        self.setWindowTitle("视觉终端")
        #在table中添加demo,并在类中实现功能
        table_1 = Find_color_block()
        self.tabWidget.insertTab(0,table_1,"色块识别")
        # 设置当前显示的界面 默认界面
        self.tabWidget.setCurrentWidget(table_1)

        ''' 设置主界面的内容 '''
        self.com = [] 
        for name in Com_dev.port_list:
            self.com.append(str(name).split("-")[0])
        
        self.Box_com.addItems(self.com)

        bps = ["9600", "115200"]
        self.Box_bps.addItems(bps)
        self.Box_bps.setCurrentIndex(1)

        check = ["无校检", "奇校检", "偶校检", "1校检", "0校检"]
        self.Box_check.addItems(check)
        self.Box_check.setCurrentIndex(0)

        stop_bit = ["1位","1.5位","2位"]
        self.Box_stop.addItems(stop_bit)
        self.Box_stop.setCurrentIndex(0)

        cam_num = ["0","1","2","3"]
        self.Box_cam.addItems(cam_num)
        self.Box_cam.setCurrentIndex(0)

        '''打开串口槽函数'''
        self.Button_opencom.clicked.connect(self.on_open_com)

        '''打开摄像头槽函数'''
        self.Button_open_cam.clicked.connect(self.on_open_cam)        

        '''定时器刷新串口'''
        self.timer = QTimer()  
        self.timer.timeout.connect(self.refresh_port)
        # self.timer.start(500)
    
    ''' 打开/关闭串口 '''
    def on_open_com(self):
        global Com_dev
        if self.Button_opencom.text() == "打开":
            self.Button_opencom.setText("关闭")
            # 获取界面配置
            com_x = str(self.Box_com.currentText()) 
            bps_x = str(self.Box_bps.currentText())
            # 设置串口相关信息
            Com_dev.set_com(com_x)
            Com_dev.set_bps(bps_x)
            # 尝试打开
            try:
                status = Com_dev.open()
                if status == False:
                    self.Button_opencom.setText("打开")
                    QMessageBox.question(self, "打开错误", "串口已被占用或不存在!!!", QMessageBox.Yes , QMessageBox.Yes)                                    
                    print("打开失败")
                    return 
                
                # Com_dev.send("M1111\r\n")   
                pass
            except:
                self.Button_opencom.setText("打开")
                QMessageBox.question(self, "打开错误", "串口已被占用或不存在!!!", QMessageBox.Yes , QMessageBox.Yes)                
                print("打开失败")
                return 
        else:
            # Com_dev.send("G0X280Y0Z0\r\n")  
            Com_dev.close()
            self.Button_opencom.setText("打开")
        pass

    def on_open_cam(self):
        if self.Button_open_cam.text() == "打开":
            self.Button_open_cam.setText("关闭")

            # 获取界面配置
            cam_x = str(self.Box_cam.currentText()) 
            # 设置摄像头ID
            
            # 尝试打开
            try:
                pass
            except:
                return 

            print("摄像头已打开")
        else:
            print("摄像头已关闭")
            self.Button_open_cam.setText("打开")
        pass

    ''' 串口刷新 '''
    def refresh_port(self):

        pass
        


        pass


if __name__ =='__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())

#参考资料
# https://www.jb51.net/article/156192.htm
# https://www.cnblogs.com/leokale-zz/p/13099815.html@
# https://blog.csdn.net/jia666666/article/details/81669092
# https://blog.csdn.net/Wang_Jiankun/article/details/83269859
# https://blog.csdn.net/qq_38161040/article/details/89742462
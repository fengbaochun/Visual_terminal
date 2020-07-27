import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QMessageBox
from PyQt5.QtCore import QTimer
#调用文件
from Ui_mainwindow import Ui_MainWindow  
from find_color_block import Find_color_block  
from Tool_box.Serial_tool import *
from Cam_dev import *
from find_color_block import *


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self,parent = None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        #设置软件title
        self.setWindowTitle("Vitual terminal")

        ''' 设置主界面的内容 '''
        self.com = [] 
        for name in Com_dev.port_list:
            self.com.append(str(name).split("-")[0])
        
        self.Box_com.addItems(self.com)

        bps = ["9600", "115200"]
        self.Box_bps.addItems(bps)
        self.Box_bps.setCurrentIndex(1)

        check = ["None", "奇校检", "偶校检", "1校检", "0校检"]
        self.Box_check.addItems(check)
        self.Box_check.setCurrentIndex(0)

        stop_bit = ["1","1.5","2"]
        self.Box_stop.addItems(stop_bit)
        self.Box_stop.setCurrentIndex(0)
        
        '''扫描摄像头设备，并将设备编号添加到控件'''
        cam_num = video.scan()
        print("当前摄像头状态："+str(video.status))

        self.Box_cam.addItems(cam_num)
        self.Box_cam.setCurrentIndex(0)

        '''打开串口槽函数'''
        self.Button_opencom.clicked.connect(self.on_open_com)
        self.Button_refresh.clicked.connect(self.refresh_port)

        '''打开摄像头槽函数'''
        self.Button_open_cam.clicked.connect(self.on_open_cam)        
        self.Button_cam_refresh.clicked.connect(self.cam_refresh_port) 

        '''在table中添加demo,并在类中实现功能'''
        table_1 = Find_color_block() 
        self.tabWidget.insertTab(0,table_1,"Color block recognition")
        # 设置当前显示的界面 默认界面
        self.tabWidget.setCurrentWidget(table_1)

    
    ''' 打开/关闭串口 '''
    def on_open_com(self):
        global Com_dev
        if self.Button_opencom.text() == "Open":
            self.Button_opencom.setText("Close")
            # 获取界面配置
            com_x = str(self.Box_com.currentText()) 
            bps_x = str(self.Box_bps.currentText())
            # 设置串口相关信息
            Com_dev.set_com(com_x)
            Com_dev.set_bps(bps_x)
            # 尝试打开
            try:
                status = Com_dev.open()
                
                Com_dev.send(gcode.init())
                Com_dev.send(gcode.home())                
                
                if status == False:
                    self.Button_opencom.setText("Open")
                    QMessageBox.question(self, "打开错误", "串口已被占用或不存在!!!", QMessageBox.Yes , QMessageBox.Yes)                                    
                    print("打开失败")
                    return 
                
                # Com_dev.send("M1111\r\n")   
                pass
            except:
                self.Button_opencom.setText("Open")
                QMessageBox.question(self, "打开错误", "串口已被占用或不存在!!!", QMessageBox.Yes , QMessageBox.Yes)                
                print("打开失败")
                return 
        else:
            # Com_dev.send("G0X280Y0Z0\r\n")  
            Com_dev.close()
            self.Button_opencom.setText("Open")
        pass

    def on_open_cam(self):
        if self.Button_open_cam.text() == "Open":
            # 获取界面配置
            cam_x = str(self.Box_cam.currentText()) 
            # 尝试打开 
            try:
                # video.open(int(cam_x),640,480)
                video.open(int(cam_x),800,600)
                print("摄像头已打开")
                self.Button_open_cam.setText("Close")
                pass
            except:
                QMessageBox.question(self, "打开错误", "请插入摄像头", QMessageBox.Yes , QMessageBox.Yes)                
                print("打开失败")
                pass             
        else:
            video.close()
            print("摄像头已关闭")
            print(Cam_dev.status)
            self.Button_open_cam.setText("Open")
        pass

    ''' 按键刷新串口设备 '''
    def refresh_port(self):
        Com_dev.scan()
        self.Box_com.clear()
        for i in range(0,len(Com_dev.port_list)):
            # print(str(Com_dev.port_list[i]).split("-")[0])
            self.Box_com.insertItem(i,str(Com_dev.port_list[i]).split("-")[0])
        pass

    ''' 按键刷新摄像头设备 '''
    def cam_refresh_port(self):
        video.scan()
        self.Box_cam.clear()
        for i in range(0,len(video.dev_list)):
            self.Box_cam.insertItem(i,str(video.dev_list[i]))
        pass


    pass


if __name__ =='__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    # 禁止修改窗口大小
    # myWin.setFixedSize(myWin.width(), myWin.height())
    myWin.show()
    sys.exit(app.exec_())

#参考资料
# https://www.jb51.net/article/156192.htm
# https://www.cnblogs.com/leokale-zz/p/13099815.html@
# https://blog.csdn.net/jia666666/article/details/81669092
# https://blog.csdn.net/Wang_Jiankun/article/details/83269859
# https://blog.csdn.net/qq_38161040/article/details/89742462

# https://www.cnblogs.com/daicw/p/11989499.html
# https://www.jianshu.com/p/33bc12c95350
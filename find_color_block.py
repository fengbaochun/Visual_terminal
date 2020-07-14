import sys
import cv2
import serial
import serial.tools.list_ports
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox,QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

from Ui_find_color_block import Ui_find_color_block

from Color_recognition.Color_block_recogn import Color_block_recogn
from Camera.Cam_dev import Cam_dev

tar_color = 'red'

color_dict ={   'red':      [127,197,188,60,197,255],
                'blue':     [50,197,188,80,197,255],
                'yellow':   [60,197,188,100,197,255],
              }   

# 子函数操作全局变量 需要加关键词
global red_hsv
global bule_hsv
global yellow_hsv

red_hsv=[50,50,50,50,50,50]
blue_hsv=[120,120,120,120,120,120]
yellow_hsv=[200,200,200,200,200,200]

class Find_color_block(QtWidgets.QWidget, Ui_find_color_block):

    hsv=[]
    num=0
    flag = True     #防止设置滑块位置时再次进入标志
    '''初始化'''
    def __init__(self):
        super(Find_color_block, self).__init__()
        self.setupUi(self)
       
        #滑块范围
        self.H_Slider_max.setRange(0,255)
        self.H_Slider_min.setRange(0,255)
        self.S_Slider_max.setRange(0,255)
        self.S_Slider_min.setRange(0,255)
        self.V_Slider_max.setRange(0,255)
        self.V_Slider_min.setRange(0,255)

        # 设置默认
        self.checkBox_Red.setCheckState(Qt.Checked)   

        # 设置默认为红色
        self.hsv=red_hsv
        self.H_Slider_max.setValue(self.hsv[0])
        self.H_Slider_min.setValue(self.hsv[1])
        self.S_Slider_max.setValue(self.hsv[2])
        self.S_Slider_min.setValue(self.hsv[3])
        self.V_Slider_max.setValue(self.hsv[4])
        self.V_Slider_min.setValue(self.hsv[5])
        self.TextEdit_hsv.insertPlainText(str(red_hsv))

        # 槽函数
        self.H_Slider_max.valueChanged.connect(self.Slider_change)   
        self.H_Slider_min.valueChanged.connect(self.Slider_change)   
        self.S_Slider_max.valueChanged.connect(self.Slider_change)   
        self.S_Slider_min.valueChanged.connect(self.Slider_change)   
        self.V_Slider_max.valueChanged.connect(self.Slider_change)   
        self.V_Slider_min.valueChanged.connect(self.Slider_change)   

        # 选择框
        self.checkBox_Red.clicked.connect(self.on_red_click) 
        self.checkBox_Yellow.clicked.connect(self.on_yellow_click) 
        self.checkBox_Blue.clicked.connect(self.on_blue_click) 
        
        # 初始化摄像头
        self.video = Cam_dev(0,640,480)
        # 初始化定时器
        self.timer = QTimer()  
        self.timer.timeout.connect(self.get_data_result)
        self.timer.start(10) #定时
        
        print("初始化 ok")
 
        pass

    
    '''更新数据到控件'''
    def fill_data_to_Slider(self,data=[]):
        self.flag = False
        print("--------设置滑块位置-------------------------"+str(data))
        # 设置滑块位置
        self.H_Slider_max.setValue(int(data[0]))
        self.H_Slider_min.setValue(int(data[1]))
        self.S_Slider_max.setValue(int(data[2]))
        self.S_Slider_min.setValue(int(data[3]))
        self.V_Slider_max.setValue(int(data[4]))
        self.V_Slider_min.setValue(int(data[5]))

        temp=[]
        temp.append(self.H_Slider_max.value())
        temp.append(self.H_Slider_min.value())
        temp.append(self.S_Slider_max.value())
        temp.append(self.S_Slider_min.value())
        temp.append(self.V_Slider_max.value())
        temp.append(self.V_Slider_min.value())
        print("--------设置完读取位置-------------------------"+str(temp))

        self.flag = True
        
        # 清除控件内容
        self.TextEdit_hsv.clear() 
        # 更新字符串到控件
        self.TextEdit_hsv.insertPlainText(str(data))
        pass

    '''滑块'''
    # @pyqtSlot()
    # @staticmethod
    @pyqtSlot()
    def Slider_change(self):
        global red_hsv
        global bule_hsv
        global yellow_hsv
        # 防止触发信号，进入槽函数
        if  self.flag == True:
            temp_hsv=[]

            # 获取滑块数值并更新到控件中
            temp_hsv.append(self.H_Slider_max.value())
            temp_hsv.append(self.H_Slider_min.value())
            temp_hsv.append(self.S_Slider_max.value())
            temp_hsv.append(self.S_Slider_min.value())
            temp_hsv.append(self.V_Slider_max.value())
            temp_hsv.append(self.V_Slider_min.value())
            
            print("当前滑块数值为"+str(temp_hsv))
            print("红色"+str(self.checkBox_Red.isChecked()))
            print("蓝色"+str(self.checkBox_Blue.isChecked()))
            print("黄色"+str(self.checkBox_Yellow.isChecked()))

            if self.checkBox_Red.isChecked():
                red_hsv[0]=temp_hsv[0]
                red_hsv[1]=temp_hsv[1]
                red_hsv[2]=temp_hsv[2]
                red_hsv[3]=temp_hsv[3]
                red_hsv[4]=temp_hsv[4]
                red_hsv[5]=temp_hsv[5]
            elif self.checkBox_Blue.isChecked():
                blue_hsv[0]=temp_hsv[0]
                blue_hsv[1]=temp_hsv[1]
                blue_hsv[2]=temp_hsv[2]
                blue_hsv[3]=temp_hsv[3]
                blue_hsv[4]=temp_hsv[4]
                blue_hsv[5]=temp_hsv[5]
            elif self.checkBox_Yellow.isChecked():
                yellow_hsv[0]=temp_hsv[0]
                yellow_hsv[1]=temp_hsv[1]
                yellow_hsv[2]=temp_hsv[2]
                yellow_hsv[3]=temp_hsv[3]
                yellow_hsv[4]=temp_hsv[4]
                yellow_hsv[5]=temp_hsv[5]

            self.TextEdit_hsv.clear()
            self.TextEdit_hsv.insertPlainText(str(temp_hsv))
            temp_hsv.clear()

        pass
    
    '''颜色选择槽函数'''
    @pyqtSlot()
    def on_red_click(self):
        self.checkBox_Yellow.setCheckState(Qt.Unchecked)
        self.checkBox_Blue.setCheckState(Qt.Unchecked)
        self.fill_data_to_Slider(red_hsv)
        print("on_red_click")
        pass

    @pyqtSlot()
    def on_blue_click(self):
        # 清除选中 并 修改滑块位置
        self.checkBox_Yellow.setCheckState(Qt.Unchecked)
        self.checkBox_Red.setCheckState(Qt.Unchecked)
        self.fill_data_to_Slider(blue_hsv)
        print("on_blue_click")
        pass

    @pyqtSlot()
    def on_yellow_click(self):
        self.checkBox_Blue.setCheckState(Qt.Unchecked)
        self.checkBox_Red.setCheckState(Qt.Unchecked)
        self.fill_data_to_Slider(yellow_hsv)
        print("on_yellow_click")
        pass
        
    '''定时器识别图像'''
    def get_data_result(self):
        # print(red_hsv)
        
        img = cv2.cvtColor(self.video.get_img(), cv2.COLOR_BGR2RGB) 
        inRange_hsv = cv2.inRange(img, np.array([127, 60, 171]),np.array([188, 197, 255]))

        # 显示 原图
        rows, cols, channels=img.shape
        bytesPerLine = channels * cols
        QImg = QImage(img.data, cols, rows, bytesPerLine, QImage.Format_RGB888)

        self.label_img.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.label_img.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


        # 显示 黑白图
        rows, cols=inRange_hsv.shape
        QImg = QImage(inRange_hsv.data, cols, rows,  QImage.Format_Grayscale8)
        self.label_img_gray.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.label_img_gray.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        cv2.waitKey(1)
        pass

    
    def init(self):

        pass


# https://www.cnblogs.com/komean/p/11209780.html
# https://blog.csdn.net/DerrickRose25/article/details/86744787
# https://blog.csdn.net/qq_42282163/article/details/86359302
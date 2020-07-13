import sys
import serial
import serial.tools.list_ports
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox,QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot

from Ui_find_color_block import Ui_find_color_block

from Color_recognition.Color_block_recogn import Color_block_recogn
from Camera import Cam_dev

tar_color = 'red'

color_dict ={   'red':      [127,197,188,60,197,255],
                'blue':     [50,197,188,80,197,255],
                'yellow':   [60,197,188,100,197,255],
              }   




class Find_color_block(QtWidgets.QWidget, Ui_find_color_block):
    # red_hsv=[127,197,188,60,197,255]
    # blue_hsv=[50,197,188,80,197,255]
    # yellow_hsv=[60,197,188,100,197,255]
    hsv=[]
    num=0
    '''初始化'''
    def __init__(self):
        super(Find_color_block, self).__init__()
        self.setupUi(self)
        self.red_hsv=[127,197,188,60,197,255]
        self.blue_hsv=[50,197,188,80,197,255]
        self.yellow_hsv=[60,197,188,100,197,255]
        
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
        self.hsv=self.red_hsv
        self.H_Slider_max.setValue(self.hsv[0])
        self.H_Slider_min.setValue(self.hsv[1])
        self.S_Slider_max.setValue(self.hsv[2])
        self.S_Slider_min.setValue(self.hsv[3])
        self.V_Slider_max.setValue(self.hsv[4])
        self.V_Slider_min.setValue(self.hsv[5])

        # 槽函数
        self.H_Slider_max.valueChanged.connect(self.Slider_change)   
        self.H_Slider_min.valueChanged.connect(self.Slider_change)   
        self.S_Slider_max.valueChanged.connect(self.Slider_change)   
        self.S_Slider_min.valueChanged.connect(self.Slider_change)   
        self.V_Slider_max.valueChanged.connect(self.Slider_change)   
        self.V_Slider_min.valueChanged.connect(self.Slider_change)   

        # 选择框
        self.checkBox_Red.clicked.connect(self.Checkboxclick) 
        self.checkBox_Yellow.clicked.connect(self.Checkboxclick) 
        self.checkBox_Blue.clicked.connect(self.Checkboxclick) 

        self.print_hsv_data(self.hsv,self.red_hsv)
        
        print("初始化 ok")

        self.timer = QTimer()  
 
        pass

    def print_hsv_data(self,temp,quanju):
        print(temp)
        print(quanju)        
        pass
    
    '''更新数据到控件'''
    def fill_data_to_Slider(self,data):

        self.H_Slider_max.setValue(data[0])
        self.H_Slider_min.setValue(data[1])
        self.S_Slider_max.setValue(data[2])
        self.S_Slider_min.setValue(data[3])
        self.V_Slider_max.setValue(data[4])
        self.V_Slider_min.setValue(data[5])

        pass

    '''滑块'''
    # @pyqtSlot()
    # @staticmethod
    def Slider_change(self):
        temp_hsv=[]
        # 获取滑块数值并更新到控件中
        temp_hsv.append(self.H_Slider_max.value())
        temp_hsv.append(self.H_Slider_min.value())
        temp_hsv.append(self.S_Slider_max.value())
        temp_hsv.append(self.S_Slider_min.value())
        temp_hsv.append(self.V_Slider_max.value())
        temp_hsv.append(self.V_Slider_min.value())

        # if self.checkBox_Red.isChecked():
        #     print("red_hsv"+str(self.red_hsv))
        #     print("temp_hasv"+str(temp_hsv))
        #     self.red_hsv=temp_hsv
        #     print("red_hsv"+str(self.red_hsv))
        #     print("temp_hasv"+str(temp_hsv))

        #     print("打印结束")

        #     # print("红色"+str(temp_hsv))
        # elif self.checkBox_Blue.isChecked():
        #     print("蓝色"+str(temp_hsv))
        # elif self.checkBox_Yellow.isChecked():                
        #     print("黄色"+str(temp_hsv))
        #     pass

        print("红色"+str(self.checkBox_Red.isChecked()))
        print("蓝色"+str(self.checkBox_Blue.isChecked()))
        print("黄色"+str(self.checkBox_Yellow.isChecked()))
        print(self.num)
        self.num=self.num+1

        if self.checkBox_Red.isChecked():
            self.red_hsv=temp_hsv

        # print(hsv)
        self.TextEdit_hsv.clear()
        self.TextEdit_hsv.insertPlainText(str(temp_hsv))
        temp_hsv.clear()

        pass

    '''颜色选择'''
    @pyqtSlot()
    def Checkboxclick(self):
        # 控件名字
        name = self.sender().objectName()
        print(self.num)
        self.num=self.num+1
        
        if name == self.checkBox_Blue.objectName():
            # 清除
            self.TextEdit_hsv.clear()
            # 修改滑块位置
            self.fill_data_to_Slider(self.blue_hsv)
            # 清除选中
            self.checkBox_Yellow.setCheckState(Qt.Unchecked)
            self.checkBox_Red.setCheckState(Qt.Unchecked)
            print("蓝色")
            return

        elif name == self.checkBox_Red.objectName():
            self.TextEdit_hsv.clear()
            self.fill_data_to_Slider(self.red_hsv)

            self.checkBox_Yellow.setCheckState(Qt.Unchecked)
            self.checkBox_Blue.setCheckState(Qt.Unchecked)
            print("红色")
            return

        elif name == self.checkBox_Yellow.objectName():
            
            self.TextEdit_hsv.clear()
            self.fill_data_to_Slider(self.yellow_hsv)

            self.checkBox_Blue.setCheckState(Qt.Unchecked)
            self.checkBox_Red.setCheckState(Qt.Unchecked)
            print("黄色")
            return
            

        pass

    
    def init(self):

        pass

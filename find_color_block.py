import sys
import serial
import serial.tools.list_ports
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox,QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import Qt

from Ui_find_color_block import Ui_find_color_block

from Color_recognition.Color_block_recogn import Color_block_recogn
from Camera import Cam_dev

# 目标颜色
# tar_color = 'red'

# color_dict ={   'red':      [127,197,188,60,197,255],
#                 'blue':     [50,197,188,80,197,255],
#                 'yellow':   [60,197,188,100,197,255],
#               }   

tar_color = 'red'

color_dict ={   'red':      [127,197,188,60,197,255],
                'blue':     [50,197,188,80,197,255],
                'yellow':   [60,197,188,100,197,255],
              }   

red_hsv=[127,197,188,60,197,255]
blue_hsv=[50,197,188,80,197,255]
yellow_hsv=[60,197,188,100,197,255]


class Find_color_block(QtWidgets.QWidget, Ui_find_color_block):
   
    '''初始化'''
    def __init__(self):
        super(Find_color_block, self).__init__()
        self.setupUi(self)

        #滑块测试
        self.H_Slider_max.setRange(0,255)
        self.H_Slider_min.setRange(0,255)
        self.S_Slider_max.setRange(0,255)
        self.S_Slider_min.setRange(0,255)
        self.V_Slider_max.setRange(0,255)
        self.V_Slider_min.setRange(0,255)

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
        
        print("初始化 ok")
        pass

    def read_Slider(self):
        
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
    def Slider_change(self):
        hsv=[]
        # 获取滑块数值并更新到控件中
        hsv.append(self.H_Slider_max.value())
        hsv.append(self.H_Slider_min.value())
        hsv.append(self.S_Slider_max.value())
        hsv.append(self.S_Slider_min.value())
        hsv.append(self.V_Slider_max.value())
        hsv.append(self.V_Slider_min.value())

        print(hsv)

        # # # 将滑块数据更新到字典        
        # if self.checkBox_Red.isChecked():
        #     red_hsv = hsv
        # elif self.checkBox_Blue.isChecked():
        #     blue_hsv = hsv
        # elif self.checkBox_Yellow.isChecked():
        #     yellow_hsv = hsv


        self.TextEdit_hsv.clear()
        self.TextEdit_hsv.insertPlainText(str(hsv))

        pass

    '''颜色选择'''
    def Checkboxclick(self):
        # 控件名字
        name = self.sender().objectName()
        
        if name == self.checkBox_Blue.objectName():
            # 清除
            self.TextEdit_hsv.clear()
            # 修改滑块位置
            # self.fill_data_to_Slider(color_dict["blue"])
            self.fill_data_to_Slider(blue_hsv)
            # 清除选中
            self.checkBox_Yellow.setCheckState(Qt.Unchecked)
            self.checkBox_Red.setCheckState(Qt.Unchecked)

        elif name == self.checkBox_Red.objectName():
            self.TextEdit_hsv.clear()
            # self.fill_data_to_Slider(color_dict["red"])
            self.fill_data_to_Slider(red_hsv)

            self.checkBox_Yellow.setCheckState(Qt.Unchecked)
            self.checkBox_Blue.setCheckState(Qt.Unchecked)


        elif name == self.checkBox_Yellow.objectName():
            
            self.TextEdit_hsv.clear()
            # self.fill_data_to_Slider(color_dict["yellow"])
            self.fill_data_to_Slider(yellow_hsv)

            self.checkBox_Blue.setCheckState(Qt.Unchecked)
            self.checkBox_Red.setCheckState(Qt.Unchecked)


        pass
    
    def init(self):

        pass

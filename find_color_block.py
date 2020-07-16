import sys
import cv2
import time
import serial
import serial.tools.list_ports
import numpy as np
import math
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox,QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from Tool_box.Serial_tool import *



from Ui_find_color_block import Ui_find_color_block

from Color_recognition.Color_block_recogn import Color_block_recogn

from Camera.Cam_dev import Cam_dev

tar_color = 'red'

color_dict ={   'red':      [127,197,188,60,197,255],
                'blue':     [50,197,188,80,197,255],
                'yellow':   [60,197,188,100,197,255],
              }   

# 子函数操作全局变量 需要加关键词
''' HSV 色彩空间 '''
global red_hsv
global bule_hsv
global yellow_hsv

''' 默认HSV '''
red_hsv = [108, 190, 59, 255, 121, 255]
blue_hsv = [74, 131, 107, 241, 146, 255]
yellow_hsv = [30, 83, 125, 209, 143, 255]

'''特征参数,长 宽 边缘阈值'''
feature_param=[50,50,100,250]

''' rect 颜色'''
rgb_param=[0,0,255]

''' 目标所有信息 '''
obj_all_info = {
            "red":{},
            "blue":{},
            "yellow":{}
            }

'''
    最高位置的标定参数
    可以根据据情况调整
'''
# obj_fact_size = 30 # mm
# obj_img_size = 69 # 像素

obj_fact_size = 29 # mm
obj_img_size = 69 # 像素

obj_p = float(obj_img_size)/float(obj_fact_size) 
# obj_p = 2
print(obj_p)

'''放置位置 [ x , y ] '''
red_place = [280,180]
blue_place = [200,180]
yellow_place = [140,180]
place_pos = [red_place,blue_place,yellow_place]

class Find_color_block(QtWidgets.QWidget, Ui_find_color_block):

    hsv=[]
    num=0
    flag = True     #防止设置滑块位置时再次进入标志
    data_status = True

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

        # 按键槽函数
        self.Button_arm_start.clicked.connect(self.Arm_work)  

        # 选择框
        self.checkBox_Red.clicked.connect(self.on_red_click) 
        self.checkBox_Yellow.clicked.connect(self.on_yellow_click) 
        self.checkBox_Blue.clicked.connect(self.on_blue_click) 
        
        '''初始化摄像头以及识别相关的'''
        self.video = Cam_dev(0,640,480)
        self.revogn = Color_block_recogn(red_hsv,feature_param,rgb_param)

        self.timer = QTimer()  
        self.timer.timeout.connect(self.get_data_result)
        self.timer.start(10) #定时
        
        self.G = Gcode()

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

    '''根据图像坐标转换为实际坐标'''
    def get_ARM_pos(self,x,y):
        # 基准坐标为中心坐标
        y = math.ceil(float((y-320)*1000) / float(obj_p) / float(1000))
        x = math.ceil(float((x-240)*1000) / float(obj_p) / float(1000))   
        return [x,y]

    '''搬运逻辑'''
    def move_obj(self):

        index = ["red","blue","yellow"]
        for j in range(len(index)):
            for i in range(len(obj_all_info[index[j]]["center"])):
                y = obj_all_info[index[j]]["center"][i][0]
                x = obj_all_info[index[j]]["center"][i][1]     
                temp = self.get_ARM_pos(x,y)
                #到达目标位置
                Com_dev.send(self.G.XYZ(int(215-temp[0]),int(0-temp[1]),0))
                # 下降
                Com_dev.send(self.G.Z(-20))
                # 吸气
                Com_dev.send(self.G.M100x(0))
                # 上升 一定高度
                Com_dev.send(self.G.Z(20))
                # 到放置位置上方
                Com_dev.send(self.G.XYZ(place_pos[j][0],place_pos[j][1],120))
                #下降Z
                Com_dev.send(self.G.Z(50))
                #漏气
                Com_dev.send(self.G.M100x(2))
                sleep(1)
                # #漏气完抬高一下
                # send_gcode_Z( Gcode_Z + 2 + Z_val*index + 10)
            time.sleep(1)
        
        Com_dev.send(self.G.M100x(2))

        pass

    '''机械臂工作'''
    def Arm_work(self):
        
        if Com_dev.status == True:
            if self.Button_arm_start.text() == "开始工作":
                self.Button_arm_start.setText("正在工作")
                # 关掉图像处理及收集数据
                self.data_status = False
                print(obj_all_info)
                
                self.move_obj()
                
                print("正在工作")
            else:
                # Com_dev.send(self.G.init())
                Com_dev.send(self.G.home())
                print("结束工作")
                self.Button_arm_start.setText("开始工作")
                # 开启图像处理及收集数据
                self.data_status = True
        else:
            QMessageBox.question(self, '警告', '请先打开串口再操作', QMessageBox.Yes, QMessageBox.Yes)        
        pass

    '''滑块'''
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
        self.revogn.set_hsv(red_hsv)
        self.revogn.set_rect_rgb([0,0,255])
        
        print("on_red_click")
        pass

    @pyqtSlot()
    def on_blue_click(self):
        # 清除选中 并 修改滑块位置
        self.checkBox_Yellow.setCheckState(Qt.Unchecked)
        self.checkBox_Red.setCheckState(Qt.Unchecked)
        self.fill_data_to_Slider(blue_hsv)
        # 设置识别算法的参数
        self.revogn.set_hsv(blue_hsv)
        self.revogn.set_rect_rgb([255,0,0])

        print("on_blue_click")
        pass

    @pyqtSlot()
    def on_yellow_click(self):
        self.checkBox_Blue.setCheckState(Qt.Unchecked)
        self.checkBox_Red.setCheckState(Qt.Unchecked)
        self.fill_data_to_Slider(yellow_hsv)
        self.revogn.set_hsv(yellow_hsv)
        self.revogn.set_rect_rgb([0,255,0])

        print("on_yellow_click")
        pass
    
    '''保存识别信息，方便使用与机械臂搬运
        根据不同的选项分别保存，强制使用者必须所有都要调整后，才能点击 “开始工作”
    '''
    def save_obj_info(self):
        if self.checkBox_Red.isChecked():
            obj_all_info["red"].update(self.revogn.tar_info)
        elif self.checkBox_Blue.isChecked():
            obj_all_info["blue"].update(self.revogn.tar_info)
        elif self.checkBox_Yellow.isChecked():
            obj_all_info["yellow"].update(self.revogn.tar_info)
        # print(obj_all_info)
        pass

    '''对图像画标识，辅助校准'''
    def draw_pos(self,img):
        size = 20
        # 画十字
        cv2.line(img,(320-size,240), (320+size,240), (0, 0, 0), 2)
        cv2.line(img,(320,240-size), (320,240+size), (0, 0, 0), 2)
        pass
        
    '''定时器识别图像'''
    def get_data_result(self):
        if self.data_status == True:
            img_src , inrange_img = self.revogn.get_target_img(self.video.get_img(1))
            img = cv2.cvtColor(img_src, cv2.COLOR_BGR2RGB) 
            
            # 画十字
            self.draw_pos(img)

            # 显示原图
            rows, cols, channels=img.shape
            bytesPerLine = channels * cols
            QImg = QImage(img.data, cols, rows, bytesPerLine, QImage.Format_RGB888)

            self.label_img.setPixmap(QPixmap.fromImage(QImg).scaled(
                self.label_img.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

            # 显示黑白图
            rows, cols=inrange_img.shape
            QImg = QImage(inrange_img.data, cols, rows,  QImage.Format_Grayscale8)
            self.label_img_gray.setPixmap(QPixmap.fromImage(QImg).scaled(
                self.label_img_gray.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            
            # 更新识别结果到控件中
            self.show_recong_result.clear()
        
            pos = []
            for i in range(self.revogn.tar_info["num"]):
                pos.insert(i,str(np.array(self.revogn.tar_info["center"])[i]))

            angle = []
            for i in range(self.revogn.tar_info["num"]):
                angle.insert(i,str(np.array(self.revogn.tar_info["angle"])[i]))

            temp = "数量:"+str(self.revogn.tar_info["num"])+"\n位置:"+str(pos)+"\n角度:"+str(angle)

            self.show_recong_result.insertPlainText(str(temp))
    

            self.save_obj_info()

        cv2.waitKey(1)
        pass

    pass

'''
gcode 封装
'''
class Gcode(object):
    datum = [210,0,-10]
    '''初始化'''
    def __init__(self):
        pass

    def init(self):
        return "M1111\r\n"
    
    '''机械臂最高位置'''
    def home(self):
        return self.XYZ(255,0,180)
    
    def Z(self,z):
        temp = "G0"+"Z"+str(z)+"\r\n"
        return temp        
        pass

    def X(self):
        pass

    def Y(self):
        pass

    def XYZ(self,x,y,z):
        temp = "G0"+"X"+str(x)+"Y"+str(y)+"Z"+str(z)+"\r\n"
        return temp

    def XY(self,x,y):
        temp = "G0"+"X"+str(x)+"Y"+str(y)+"\r\n"
        return temp

    def M100x(self,x):
        return "M100"+str(x)+"\r\n"

    pass

# https://www.cnblogs.com/komean/p/11209780.html
# https://blog.csdn.net/DerrickRose25/article/details/86744787
# https://blog.csdn.net/qq_42282163/article/details/86359302
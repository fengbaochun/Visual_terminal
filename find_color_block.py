import sys
import cv2
import time
import serial
import serial.tools.list_ports
import numpy as np
import math
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox,QApplication,QSpinBox
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from Tool_box.Serial_tool import *

from Ui_find_color_block import Ui_find_color_block

from Color_recognition.Color_block_recogn import Color_block_recogn

from Cam_dev import *


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
red_hsv = [108, 190, 59, 255, 70, 255]
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

# obj_p = float(obj_img_size)/float(obj_fact_size) 
# print(obj_p)
obj_p = 2.15

# # Z = -21
# # 图像偏置 特别准
# obj_y = 2.75
# obj_x = 2.61

# Z = -21
# 图像偏置
# obj_y = 2.65
# obj_x = 2.48

obj_y = 2.55
obj_x = 2.48


'''放置位置 [ x , y ,z] 只使用xy,z用来占位，调整的时候使用 '''
red_place = [280,180,0]
blue_place = [200,180,0]
yellow_place = [140,180,0]
place_pos = {   "red":red_place,
                "blue":blue_place,
                "yellow":yellow_place
            }

''' 机械臂位置 '''
# 机械臂最高点
MAX_HIGH=[295,0,175]
# 地面视角中心点
VIEW_CENTER=[215,0,-45]

class Find_color_block(QtWidgets.QWidget, Ui_find_color_block):

    hsv=[]
    num=0
    flag = True     #防止设置滑块位置时再次进入标志
    data_status = True
    change_pos = [280,0,0]
    demo_index = 1  #默认demo为木块
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

        # 调整机械臂目标位置
        self.show_red_place.clear()
        self.show_red_place.insertPlainText(str(place_pos["red"]))
        self.show_blue_place.insertPlainText(str(place_pos["blue"]))
        self.show_yellow_place.insertPlainText(str(place_pos["yellow"]))
        # 设置当前数值为10
        self.spinBox.setValue(10)

        self.Button_x_add.clicked.connect(self.change_ARM_tar_pos) 
        self.Button_x_less.clicked.connect(self.change_ARM_tar_pos) 
        self.Button_y_add.clicked.connect(self.change_ARM_tar_pos) 
        self.Button_y_less.clicked.connect(self.change_ARM_tar_pos) 
        self.Button_z_add.clicked.connect(self.change_ARM_tar_pos) 
        self.Button_z_less.clicked.connect(self.change_ARM_tar_pos) 
        self.Button_rest.clicked.connect(self.change_ARM_tar_pos)
        self.Button_home.clicked.connect(self.change_ARM_tar_pos)

        ''' 同一类别中进行demo区分 '''
        '''demo 木块 and 豆子'''
        self.demo = ["None","Block", "Beans"]
        self.Boxdemo.addItems(self.demo)
        self.Boxdemo.setCurrentIndex(0)     
        self.Boxdemo.currentIndexChanged.connect(self.change_demo)          
        
        '''初始化摄像头以及识别相关的'''
        self.revogn = Color_block_recogn(red_hsv,feature_param,rgb_param)

        self.timer = QTimer()  
        self.timer.timeout.connect(self.get_data_result)
        self.timer.start(10) #定时
        
        self.G = Gcode()

        print("初始化 ok")
 
        pass

    
    '''选择demo 切换相应的参数'''
    def change_demo(self):
        current_demo = str(self.Boxdemo.currentText())
        print(str(self.Boxdemo.currentIndex()))
        # demo 选择索引
        self.demo_index = self.Boxdemo.currentIndex()
        # 木块
        if current_demo == self.demo[1]:
            print(str(self.demo[1]))
            pass
        # 木块
        elif current_demo == self.demo[2]:
            print(str(self.demo[2]))
            pass        
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
        x = VIEW_CENTER[0] - math.ceil(float((x-300)*1000) / float(obj_x) / float(1000))   
        y = VIEW_CENTER[1] - math.ceil(float((y-400)*1000) / float(obj_y) / float(1000))
        return [x,y]
        # return [x,y]

    '''搬运逻辑 （木块）'''
    def move_obj(self):

        for dict_name in obj_all_info:
            try:
                for i in range(len(obj_all_info[dict_name]["center"])):
                    y = obj_all_info[dict_name]["center"][i][0]
                    x = obj_all_info[dict_name]["center"][i][1]     
                    temp = self.get_ARM_pos(x,y)
                    #到达目标位置
                    Com_dev.send(self.G.XYZ(int(temp[0]),int(temp[1]),0))
                    Com_dev.read()
                    # 下降
                    Com_dev.send(self.G.Z(-20))
                    Com_dev.read()
                    # 吸气
                    Com_dev.send(self.G.M100x(0))
                    sleep(0.1)
                    # Com_dev.read()
                    # 上升 一定高度
                    Com_dev.send(self.G.Z(20))
                    Com_dev.read()
                    # 到放置位置上方
                    Com_dev.send(self.G.XYZ(place_pos[dict_name][0],place_pos[dict_name][1],-5+30*i+40))
                    Com_dev.read()
                    #下降Z
                    Com_dev.send(self.G.Z(-5+30*i))
                    Com_dev.read()
                    #漏气
                    Com_dev.send(self.G.M100x(2))
                    # Com_dev.read()
                    sleep(0.1)
                    # 上升，避免撞到
                    Com_dev.send(self.G.Z(-5+30*i+40))
                    Com_dev.read()
                    
                    # #漏气完抬高一下
                    # send_gcode_Z( Gcode_Z + 2 + Z_val*index + 10)        

            except:
                print(dict_name+"没有选择")
                pass
        pass

    '''移动小物体'''
    def move_min_obj(self):
        for dict_name in obj_all_info:
            try:
                for i in range(len(obj_all_info[dict_name]["center"])):
                    y = obj_all_info[dict_name]["center"][i][0]
                    x = obj_all_info[dict_name]["center"][i][1]     
                    temp = self.get_ARM_pos(x,y)
                    print(temp)
                    
                    #到达目标位置
                    # Com_dev.send(self.G.XYZ(int(225-temp[0]),int(0-temp[1]),0))
                    Com_dev.send(self.G.XYZ(int(temp[0]),int(temp[1]),0))
                    Com_dev.read()
                    
                    # 下降
                    # Com_dev.send(self.G.Z(-21))
                    Com_dev.send(self.G.Z(-45))
                    Com_dev.read()
                    
                    # 吸气
                    Com_dev.send(self.G.M100x(0))
                    sleep(0.1)
                    # Com_dev.read()
                    # 上升 一定高度
                    Com_dev.send(self.G.Z(20))
                    Com_dev.read()
                    # 到放置位置上方
                    # Com_dev.send(self.G.XYZ(place_pos[dict_name][0],place_pos[dict_name][1],-5+30*i+40))
                    Com_dev.send(self.G.XYZ(place_pos[dict_name][0],place_pos[dict_name][1],-5+30*2+40))
                    Com_dev.read()
                    #下降Z
                    Com_dev.send(self.G.Z(-5+30*2))
                    Com_dev.read()
                    #漏气
                    Com_dev.send(self.G.M100x(2))
                    # Com_dev.read()
                    sleep(0.1)
                    # 上升，避免撞到
                    # Com_dev.send(self.G.Z(-5+30*i+40))
                    Com_dev.send(self.G.Z(-5+30*2+40))
                    Com_dev.read()
                    '''
                    '''
                    # #漏气完抬高一下
                    # send_gcode_Z( Gcode_Z + 2 + Z_val*index + 10)        

            except:
                print(dict_name+"没有选择")
                pass
        pass


    '''获取机械臂当前位置，下位机暂时没有支持'''
    def get_current_ARM_pos(self):
        "G0X280Y0Z0"
        return [280,0,0]
        pass
    
    '''获取调整后的数值'''
    def get_change_val(self,sender,index):
        
        val = self.spinBox.value()
        if Com_dev.status == True:
            QMessageBox.question(self, "打开错误", "请先打开串口再操作!!!", QMessageBox.Yes , QMessageBox.Yes)  
        else:
            if sender == "X+":
                place_pos[index][0] = place_pos[index][0] + val            
            elif sender == "X-":
                place_pos[index][0] = place_pos[index][0] - val     
            elif sender == "Y+":
                place_pos[index][1] = place_pos[index][1] + val 
            elif sender == "Y-":
                place_pos[index][1] = place_pos[index][1] - val  
            elif sender == "Z+":
                place_pos[index][2] = place_pos[index][2] + val 
            elif sender == "Z-":
                place_pos[index][2] = place_pos[index][2] - val 
            elif sender == "REST":
                place_pos["red"] = [280,180,0]
                place_pos["blue"] = [200,180,0]
                place_pos["yellow"] = [140,180,0]

            print(place_pos[index])
        
        '''同步控件内容'''
        self.show_red_place.clear()
        self.show_red_place.insertPlainText(str(place_pos["red"]))
        self.show_blue_place.clear()
        self.show_blue_place.insertPlainText(str(place_pos["blue"]))
        self.show_yellow_place.clear()
        self.show_yellow_place.insertPlainText(str(place_pos["yellow"]))
        pass
    
    '''修改'''
    def change_ARM_tar_pos(self):
        sender = self.sender().text()
        print(sender+ ' 是发送者')
        if sender == "HOME":
            try:
                # 回到home调整 颜色
                Com_dev.send(self.G.home())
                Com_dev.read()                    
            except :
                QMessageBox.question(self, "打开错误", "请先打开串口再操作!!!", QMessageBox.Yes , QMessageBox.Yes)    
        else:
            # 调整要放的位置
            try:
                if self.checkBox_Red.isChecked():
                    self.get_change_val(sender,"red")
                    Com_dev.send(self.G.XYZ(place_pos["red"][0],place_pos["red"][1],place_pos["red"][2]))
                    Com_dev.read()
                elif self.checkBox_Blue.isChecked():
                    self.get_change_val(sender,"blue")
                    Com_dev.send(self.G.XYZ(place_pos["blue"][0],place_pos["blue"][1],place_pos["blue"][2]))
                    Com_dev.read()
                elif self.checkBox_Yellow.isChecked():
                    self.get_change_val(sender,"yellow")
                    Com_dev.send(self.G.XYZ(place_pos["yellow"][0],place_pos["yellow"][1],place_pos["yellow"][2]))
                    Com_dev.read()      
            except:              
                '''没有打开串口需要提示'''
                place_pos["red"] = [280,180,0]
                place_pos["blue"] = [200,180,0]
                place_pos["yellow"] = [140,180,0]
                QMessageBox.question(self, "打开错误", "请先打开串口再操作!!!", QMessageBox.Yes , QMessageBox.Yes)              
                print("打开失败")
                pass   
            print(place_pos)

        pass

   
    ''' 选择 demo '''
    def chose_demo(self,index):
        # 木块
        if index == 1:
            self.move_obj()
            pass
        # 豆子
        elif index == 2:
            self.move_min_obj()
            pass
        pass
   
    '''机械臂工作'''
    def Arm_work(self):
        
        if Com_dev.status == True:
            if self.Button_arm_start.text() == "Start":
                # 关掉图像处理及收集数据
                self.data_status = False
                print(obj_all_info)
                
                # 搬运 木块和豆子选择，可拓展其他搬运逻辑
                self.chose_demo(self.Boxdemo.currentIndex())
                
                for i in obj_all_info:
                    obj_all_info[i].clear()

                print(obj_all_info)

                Com_dev.send(self.G.home())
                self.data_status = True
                print("工作结束")
            else:
                # Com_dev.send(self.G.init())
                Com_dev.send(self.G.home())
                print("结束工作")
                self.Button_arm_start.setText("Start")
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
        size = 15
        line_w = 2
        img_half_w = 400
        img_half_h = 300

        # 画中心十字
        cv2.line(img,(img_half_w-size,img_half_h), (img_half_w+size,img_half_h), (0, 0, 0), line_w)
        cv2.line(img,(img_half_w,img_half_h-size), (img_half_w,img_half_h+size), (0, 0, 0), line_w)

        # 画中心偏移的十字
        
        diff=[220,220]
        cv2.line(img,(img_half_w-size-diff[0],img_half_h), (img_half_w+size-diff[0],img_half_h), (0, 0, 0), line_w)
        cv2.line(img,(img_half_w-diff[1],img_half_h-size), (img_half_w-diff[1],img_half_h+size), (0, 0, 0), line_w)    

        diff=[-220,-220]
        cv2.line(img,(img_half_w-size-diff[0],img_half_h), (img_half_w+size-diff[0],img_half_h), (0, 0, 0), line_w)
        cv2.line(img,(img_half_w-diff[1],img_half_h-size), (img_half_w-diff[1],img_half_h+size), (0, 0, 0), line_w)    

        diff=[220,220]
        cv2.line(img,(img_half_w-size,img_half_h-diff[0]), (img_half_w+size,img_half_h-diff[0]), (0, 0, 0), line_w)
        cv2.line(img,(img_half_w,img_half_h-size-diff[1]), (img_half_w,img_half_h+size-diff[1]), (0, 0, 0), line_w)    

        diff=[-220,-220]
        cv2.line(img,(img_half_w-size,img_half_h-diff[0]), (img_half_w+size,img_half_h-diff[0]), (0, 0, 0), line_w)
        cv2.line(img,(img_half_w,img_half_h-size-diff[1]), (img_half_w,img_half_h+size-diff[1]), (0, 0, 0), line_w)    
   

        pass
        
    '''定时器识别图像'''
    def get_data_result(self):
        # 摄像头打开标志
        # print("video.status"+str(video.status))
        # print("self.data_status"+str(self.data_status))
        if video.status == True:

            if self.data_status == True:
                # 放置畸变校正出问题，出问题使用没有畸变校正的图像
                try:
                    img_src , inrange_img = self.revogn.get_target_img(video.get_img(1),self.demo_index)
                except :
                    img_src , inrange_img = self.revogn.get_target_img(video.get_img(0),self.demo_index)
                    pass
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

                # temp = "数量:"+str(self.revogn.tar_info["num"])+"\n位置:"+str(pos)+"\n角度:"+str(angle)
                temp = "num:"+str(self.revogn.tar_info["num"])+"\npos:"+str(pos)+"\nangle:"+str(angle)

                self.show_recong_result.insertPlainText(str(temp))
        

                self.save_obj_info()

            cv2.waitKey(1)
        pass


    pass

'''
gcode 封装
'''
class Gcode(object):
    '''初始化'''
    def __init__(self):
        pass

    def init(self):
        return "M1111\r\n"
    
    '''机械臂最高位置'''
    def home(self):
        return self.XYZ(MAX_HIGH[0],MAX_HIGH[1],MAX_HIGH[2])
    
    def Z(self,z):
        temp = "G0"+"Z"+str(z)+"\r\n"
        return temp        
        pass

    def X(self):
        pass

    def Y(self):
        pass

    def XYZ(self,x,y,z):
        temp = "G0"+"X"+str(x)+"Y"+str(y)+"Z"+str(z)+"F5000"+"\r\n"
        return temp

    def XY(self,x,y):
        temp = "G0"+"X"+str(x)+"Y"+str(y)+"\r\n"
        return temp

    def M100x(self,x):
        return "M100"+str(x)+"\r\n"
    
    def speed(self,val):
        return "G0F"+str(val)+"\r\n"

    pass

gcode = Gcode()

# https://www.cnblogs.com/komean/p/11209780.html
# https://blog.csdn.net/DerrickRose25/article/details/86744787
# https://blog.csdn.net/qq_42282163/article/details/86359302
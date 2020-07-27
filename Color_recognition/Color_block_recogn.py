import cv2
import numpy as np
import math

from Cam_dev import *

# 目标颜色
tar_color = 'green'
color_dict = {'red': {'Lower': np.array([127, 60, 171]), 'Upper': np.array([188, 197, 255])},
              'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
              'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
              }              

red_hsv = [108, 190, 120, 255, 163, 223]
blue_hsv = [74, 131, 107, 241, 146, 255]
yellow_hsv = [30, 83, 60, 209, 156, 255]

''' 特征参数,长 宽 边缘阈值 边框差值 '''
feature_param=[40,40,60,250,20]

''' rect 颜色'''
rgb_param=[0,0,255]


'''色块识别类'''
class Color_block_recogn():
    tar_num = 0

    tar_info = {"num":0,
            "center":[],
            "angle":[]}
    
    '''初始化参数'''
    def __init__(self,color_list=[],fea_list=[],rect_rgb_list=[]):
        self.hsv = color_list
        self.fea_p = fea_list
        self.rect_rgb = rect_rgb_list
        print("参数如下:")
        print("色彩hsv"+str(self.hsv))
        print("目标特征"+str(self.fea_p))
        print("矩形边框"+str(self.rect_rgb))
        pass
    
    ''' 设置颜色参数,参数直接决定识别'''
    def set_hsv(self,tar_list=[]):
        self.hsv = tar_list
        pass

    ''' 设置识别目标的特征（目标主要为色块一类的obj）'''
    def set_fea(self,tar_list=[]):
        self.fea_p = tar_list
        pass

    ''' 设置目标框\点的颜色 '''
    def set_rect_rgb(self,tar_list=[]):
        self.rect_rgb = tar_list
        pass

    ''' 按照索引获取识别目标的信息 '''
    def get_target_img(self,img,condition_index):
        
        # 临时缓存
        temp_tar_info = {"num":0,
        "center":[],
        "angle":[]}
        temp_num = 0

        # 高斯模糊
        gs_img = cv2.GaussianBlur(img, (5, 5), 0)                     
        # 转成 HSV 图
        hsv_img = cv2.cvtColor(gs_img, cv2.COLOR_BGR2HSV)
        # 转为二值化
        inRange_hsv = cv2.inRange(hsv_img, np.array([self.hsv[0],self.hsv[2],self.hsv[4]]), np.array([self.hsv[1],self.hsv[3],self.hsv[5]]))
        # 均值滤波
        average_val_img = cv2.blur(inRange_hsv,(3,3))
        #边缘识别
        canny_img = cv2.Canny(average_val_img,128,255,3)
        # 轮廓提取
        _,contours, hierarchy = cv2.findContours(canny_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        try:
            for i in range(len(contours)):
                # if (len(contours[i])>self.fea_p[2]) and (len(contours[i])<self.fea_p[3]):
                # if (len(contours[i])>self.fea_p[2]):
                if (len(contours[i])>35):
                    # 最小外接矩形
                    min_rect = cv2.minAreaRect(contours[i])

                    # 条件选择
                    if condition_index == 1:
                        # 识别条件
                        result = (min_rect[1][0]>35 and min_rect[1][1]>35)and(abs(min_rect[1][0]-min_rect[1][1])<25)
                    elif condition_index == 2:
                        result = (min_rect[1][0] * min_rect[1][1]) > 670

                    # 矩形长宽
                    # if (min_rect[1][0]>35 and min_rect[1][1]>35)and(abs(min_rect[1][0]-min_rect[1][1])<25):
                    # if ((min_rect[1][0] * min_rect[1][1]) > 670):
                    if result:
                        # 矩形坐标
                        box_points = cv2.boxPoints(min_rect)
                        # 标出中心点以及矩形
                        cv2.circle(img,(int(min_rect[0][0]),int(min_rect[0][1])) ,2,(self.rect_rgb[0],self.rect_rgb[1], self.rect_rgb[2]),4)
                        cv2.drawContours(img, [np.int0(box_points)], 0, (self.rect_rgb[0],self.rect_rgb[1], self.rect_rgb[2]), 2)        
                        
                        # 加入缓存字典               
                        temp_tar_info["center"].insert(temp_num,np.int0(min_rect[0]))
                        temp_tar_info["angle"].insert(temp_num,np.int0(min_rect[2]))  

                        temp_num = temp_num + 1
                        # print("中心坐标："+str(np.int0(min_rect[0]))+" "+"矩形长宽："+str(np.int0(min_rect[1]))+" "+"旋转角度："+str(np.int0(min_rect[2])))
                        # print("矩形长宽："+str(np.int0(min_rect[1])))

            temp_tar_info["num"]=temp_num

            # 将缓存字典更新到类变量中
            self.tar_info.clear()
            self.tar_info = temp_tar_info
            # print(self.tar_info)
        except:
            print("error------------->")

        #返回图像以及目标参数 
        return img,inRange_hsv

    ''' 获取目标 参数 '''
    def get_tar_info(self):
        pass
    
    pass


''' 识别 demo '''
def recogn_main():
    
    video.open(1,640,480)
    revogn = Color_block_recogn(red_hsv,feature_param,rgb_param)
    while True:
        img,inRange_hsv = revogn.get_target_img(video.get_img(1))
        # 显示图像
        cv2.imshow('inRange_hsv', inRange_hsv)
        cv2.imshow('src_img', img)

        cv2.waitKey(30)
    pass


if __name__ == "__main__":
    recogn_main()
    pass

# https://www.cnblogs.com/yiyi20120822/p/11506970.html
# https://blog.csdn.net/weixin_45875105/article/details/103902777?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.nonecase&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.nonecase
# https://blog.csdn.net/weixin_41115751/article/details/84137783
# https://www.jb51.net/article/164341.htm
# https://blog.csdn.net/lanyuelvyun/article/details/76614872

# https://blog.csdn.net/fang_zz/article/details/51530839?utm_medium=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.nonecase&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.nonecase
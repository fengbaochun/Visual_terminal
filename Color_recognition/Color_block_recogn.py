import cv2
import numpy as np
from Cam_dev import Cam_dev

# 目标颜色
tar_color = 'red'
color_dict = {'red': {'Lower': np.array([127, 60, 171]), 'Upper': np.array([188, 197, 255])},
              'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
              'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
              }              


'''色块识别类'''
class Color_block_recogn():
    tar_num = 0
    targe_contour=[]
    # inRange_hsv = None
    # img = None
    # src_img
    # inRang_img
    '''初始化参数'''
    def __init__(self,color_dict):
        self.color_thd = color_dict
        pass
    
    ''' 设置参数'''
    def set_param(self,tar_dict,index):

        pass
    
    # def get_img(self):
    #     return self.img
    #     pass

        ''' 按照索引获取识别目标的信息 '''
    def get_target_info(self,img,index):
        # 高斯模糊
        gs_img = cv2.GaussianBlur(img, (5, 5), 0)                     
        # 转成 HSV 图
        hsv_img = cv2.cvtColor(gs_img, cv2.COLOR_BGR2HSV)
        # 转为二值化
        inRange_hsv = cv2.inRange(hsv_img, self.color_thd[index]['Lower'], self.color_thd[index]['Upper'])
        # 均值滤波
        average_val_img = cv2.blur(inRange_hsv,(3,3))
        #边缘识别
        canny_img = cv2.Canny(average_val_img,128,255,3)
        # 轮廓提取
        _,contours, hierarchy = cv2.findContours(canny_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        num = 0
        for i in range(len(contours)):
            if len(contours[i])>100 and len(contours[i])<250:
                # 最小外接矩形
                min_rect = cv2.minAreaRect(contours[i])
                # 矩形长宽
                if min_rect[1][0]>50 and min_rect[1][1]>50:
                    num = num + 1
                    self.targe_contour.insert(i,contours[i])      
                    # 矩形坐标
                    box_points = cv2.boxPoints(min_rect)
                    # 标出中心点以及矩形
                    cv2.circle(img,(int(min_rect[0][0]),int(min_rect[0][1])) ,2,(0,0,213),4)
                    cv2.drawContours(img, [np.int0(box_points)], 0, (0, 255, 255), 2)              
                    self.tar_num = self.tar_num+1
                
                    # print("中心坐标："+str(np.int0(min_rect[0]))+" "+"矩形长宽："+str(np.int0(min_rect[1]))+" "+"旋转角度："+str(np.int0(min_rect[2])))

        self.tar_num = num
        print("目标数量"+str(self.tar_num))

        # 显示图像
        cv2.imshow('inRange_hsv', inRange_hsv)
        cv2.imshow('src_img', img)
        pass
    

    def get_img(self):

        pass

    pass


def recogn_main():
    
    video = Cam_dev(0,640,480)
    revogn = Color_block_recogn(color_dict)
    while True:
        frame = video.get_img()
        # cv2.imshow('src_img', frame)
        revogn.get_target_info(frame,tar_color)
        cv2.waitKey(30)
    pass


if __name__ == "__main__":
    # cam_main()
    recogn_main()
    pass

# https://www.cnblogs.com/yiyi20120822/p/11506970.html
# https://blog.csdn.net/weixin_45875105/article/details/103902777?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.nonecase&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.nonecase
# https://blog.csdn.net/weixin_41115751/article/details/84137783
# https://www.jb51.net/article/164341.htm
# https://blog.csdn.net/lanyuelvyun/article/details/76614872

# https://blog.csdn.net/fang_zz/article/details/51530839?utm_medium=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.nonecase&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.nonecase
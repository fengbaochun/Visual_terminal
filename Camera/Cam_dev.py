import cv2
import yaml
import numpy as np

'''摄像头调用类'''
class Cam_dev():
    #设备列表
    port_list = []  
    # 状态
    status = False
    # 畸形矫正参数
    cameraMatrix = np.array([
                            [ 7.9641507015667764e+02, 0., 3.1577913194699374e+02], 
                            [0.,7.9661307355876215e+02, 2.1453452136833957e+02], 
                            [0., 0., 1. ]
                            ])

    distCoeffs = np.array([
                        [ -1.1949335317713690e+00,
                        1.8078010700662486e+00,
                        4.9410258870084744e-03, 
                        2.8036176641915598e-03,
                        -2.0575845684235938e+00]
                        ])  

    ''' 设置摄像头分辨率参数 '''
    def __init__(self):
        # 扫描摄像头设备
        self.scan()
        # 打开摄像头
        # self.open(dev_id,cap_w,cap_h)
        pass
    
    ''' 打开摄像头 '''
    def open(self,dev_id,cap_w,cap_h):
        self.cap = cv2.VideoCapture(dev_id)

        if self.cap.isOpened():
            print("打开摄像头成功")
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_w)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_h)
            self.status = True
            print("摄像头参数设置成功")
        else:
            print("打开摄像头失败")  
        pass


    '''扫描摄像头端口 最大支持10个扫描'''
    def scan(self):
        self.dev_list = []
        num = 0
        for i in range(10):
            try:
                temp_cap = cv2.VideoCapture(i)
                if temp_cap.isOpened():
                    self.dev_list.append(str(num))
                    num = num + 1
                    temp_cap.release()
            except:
                pass

        print("摄像头设备："+str(self.dev_list))
        return self.dev_list
        pass

    ''' 关闭摄像头 释放资源 '''
    def close(self):
        self.cap.release()
        self.status = False
        print("摄像头已释放")        
        pass

    ''' 获取摄像头图像 '''
    ''' img_type : 0 原始图像 '''
    ''' img_type : 1 矫正的图像 '''
    def get_img(self,img_type):
        if img_type==0:
            ret, img = self.cap.read()
        elif img_type==1:
            ret, img = self.cap.read()
            img = cv2.undistort(img, self.cameraMatrix, self.distCoeffs, None)
        return img
    
    pass

# 摄像头类
global video
video = Cam_dev()                
             
'''摄像头调用demo'''
def cam_main():
    video.scan()
    # print("矫正参数:")
    # print("matrix:\n",str(video.cameraMatrix))
    # print("Coeffs:\n", str(video.distCoeffs))

    dev_id = input("请输入摄像头ID:")
    video.open(int(dev_id),640,480)
    # 100张照片后自动释放 关闭
    num =100
    while num:

        cv2.imshow("dis_img", video.get_img(1))
        cv2.imshow("src_img", video.get_img(0))
        # num =num -1
        cv2.waitKey(1)
        
    video.close()
    pass

'''主函数'''
if __name__ == "__main__":
    cam_main()
    pass
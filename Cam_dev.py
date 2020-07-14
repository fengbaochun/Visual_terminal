import cv2
import yaml
import numpy as np
'''
import cv2
video = cv2.VideoCapture(0)  # 0 700 701 'f:/tmp/src2.f4v'
# 设置摄像头参数 
video.set(cv2.CAP_PROP_FRAME_WIDTH, 1080) # 宽度 
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 960) # 高度
video.set(cv2.CAP_PROP_FPS, 30) # 帧数
video.set(cv2.CAP_PROP_BRIGHTNESS, 1) # 亮度 1
video.set(cv2.CAP_PROP_CONTRAST,40) # 对比度 40
video.set(cv2.CAP_PROP_SATURATION, 50) # 饱和度 50
video.set(cv2.CAP_PROP_HUE, 50) # 色调 50
video.set(cv2.CAP_PROP_EXPOSURE, 50) # 曝光 50
'''
 

'''摄像头调用类'''
class Cam_dev():
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
    def __init__(self,dev_id,cap_w,cap_h):
        
        self.cap = cv2.VideoCapture(dev_id)

        if self.cap.isOpened():
            print("打开摄像头成功")
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_w)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_h)
            print("摄像头参数设置成功")
        else:
            print("打开摄像头失败")  

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
                                     

'''摄像头调用demo'''
def cam_main():
 
    video = Cam_dev(0,640,480)
    print("矫正参数")
    print("matrix:\n",str(video.cameraMatrix))
    print("Coeffs:\n", str(video.distCoeffs))

    while True:

        cv2.imshow("dis_img", video.get_img(1))
        cv2.imshow("src_img", video.get_img(0))

        cv2.waitKey(1)
    pass

'''主函数'''
if __name__ == "__main__":
    cam_main()
    pass
import cv2
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
    def get_img(self):
        ret, img = self.cap.read()
        return img

    pass


'''摄像头调用demo'''
def cam_main():
    video = Cam_dev(0,640,480)
    while True:
        cv2.imshow('camera', video.get_img())
        cv2.waitKey(1)
    pass

'''主函数'''
if __name__ == "__main__":
    cam_main()
    pass
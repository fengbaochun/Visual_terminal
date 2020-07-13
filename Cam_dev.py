import cv2

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

    ''' 摄像头状态'''
    def status(self):
        return self.cap.isOpened()
        pass
    

    pass


'''摄像头调用demo'''
def cam_main():
    video = Cam_dev(0,640,480)
    while video.status():
        cv2.imshow('camera', video.get_img())
        cv2.waitKey(1)
    pass

'''主函数'''
if __name__ == "__main__":
    cam_main()
    pass
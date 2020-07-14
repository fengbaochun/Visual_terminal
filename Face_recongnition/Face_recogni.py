import cv2
import dlib
import numpy as np


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
                                     

# '''摄像头调用demo'''
# def cam_main():
 
#     video = Cam_dev(0,640,480)
#     print("矫正参数")
#     print("matrix:\n",str(video.cameraMatrix))
#     print("Coeffs:\n", str(video.distCoeffs))

#     while True:

#         cv2.imshow("dis_img", video.get_img(1))
#         cv2.imshow("src_img", video.get_img(0))

#         cv2.waitKey(1)
#     pass

# '''主函数'''
# if __name__ == "__main__":
#     cam_main()
#     pass

predictor_path  = "./shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
#相撞
predicator = dlib.shape_predictor(predictor_path)
win = dlib.image_window()
ret,img1 = cv2.imread("./example.jpg")​
cv2.imshow("img1", img1)

# dets = detector(img1,1)
# print("Number of faces detected : {}".format(len(dets)))
# for k,d in enumerate(dets):
#     print("Detection {}  left:{}  Top: {} Right {}  Bottom {}".format(
#         k,d.left(),d.top(),d.right(),d.bottom()
#     ))
#     lanmarks = [[p.x,p.y] for p in predicator(img1,d).parts()]
#     for idx,point in enumerate(lanmarks):
#         point = (point[0],point[1])
#         cv2.circle(img1,point,5,color=(0,0,255))
#         font = cv2.FONT_HERSHEY_COMPLEX_SMALL
#         cv2.putText(img1,str(idx),point,font,0.5,(0,255,0),1,cv2.LINE_AA)
#         #对标记点进行递归；
# ​
# cv2.namedWindow("img",cv2.WINDOW_NORMAL)
# cv2.imshow("img",img1)
# cv2.waitKey(0)
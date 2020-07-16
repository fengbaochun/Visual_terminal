import serial 
import serial.tools.list_ports
import threading
from time import sleep
from PyQt5.QtWidgets import QApplication,QMainWindow,QMessageBox


class Serial_dev(object):

    status = False
    bps = 115200
    def __init__(self):
        self.scan()
        pass
    
    ''' 扫描串口 '''
    def scan(self):
        self.port_list = list(serial.tools.list_ports.comports())
        if len(self.port_list) == 0:
            print("无可用串口")
        else:
            print("当前串口设备:")
            for i in range(0,len(self.port_list)):
                print(self.port_list[i])
        pass
    
    ''' 打开串口 '''
    # def open(self, temp_port , temp_bps):
    def open(self):
        try:
            # 打开串口获取对象
            self.ser_v = serial.Serial(self.port,self.bps,timeout=3000)
            if self.ser_v.is_open:
                print("串口"+str(self.port)+"已打开")
                print("波特率为："+str(self.bps))
                self.status = True
                # threading.Thread(target=self.read(), args=(self.ser_v,)).start()
            else:
                print("打开失败")
                self.status = False
            pass
        except:
            print("打开失败,请重新检查串口是否被占用!!!")  
            self.status = False
            pass

        return self.status
        

    ''' 关闭串口 '''
    def close(self):
        self.ser_v.close()
        self.status = False
        print(str(self.port)+"已关闭")
        pass

    ''' 发送数据 '''
    def send(self,data):
        # 判断串口状态
        if self.status:
            self.ser_v.write(data.encode("gbk"))
            print(str(len(data))+" 字节已发送成功")

        pass

    ''' 读取数据 '''
    def read(self):
        # while True:
        #     data = self.ser_v.read_all()
        #     print(data)
        #     # if data == '':
        #     #     continue
        #     # else:
        #     #     break
        #     sleep(0.02)

        pass
    
    ''' 设置波特率 '''
    def set_bps(self,val):
        self.bps = val
        pass

    ''' 设置端口号 '''
    def set_com(self,num):
        self.port = num
        pass


    pass

'''用于给其他类调用'''
global Com_dev
Com_dev = Serial_dev()



def main():
    Gcode1="M1111\r\n"
    Gcode2="G0X255Y0Z180\r\n"

    dev = Serial_dev()
    dev.set_com("COM6")
    dev.set_bps(115200)
    dev.open()
    dev.send(Gcode2)
    dev.read()
    dev.close()
    # dev.scan()
    pass

if __name__ == "__main__":
    main()    
    pass

# https://www.jianshu.com/p/b5ba170a25aa
# https://www.cnblogs.com/mangojun/p/10558069.html
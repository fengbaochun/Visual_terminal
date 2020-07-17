import serial,time
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
    def open(self):
        try:
            # 打开串口获取对象
            self.ser_v = serial.Serial(self.port,self.bps,timeout=3000)
            if self.ser_v.is_open:
                print("串口"+str(self.port)+"已打开")
                print("波特率为："+str(self.bps))
                self.status = True
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

            # print(data)
            # while self.ser_v.inWaiting() == 0:

            #     n = self.ser_v.inWaiting()#获取接收到的数据长度
            #     if n: 
            #         #读取数据并将数据存入data
            #         rev_data = self.ser_v.read(n)
            #         #输出接收到的数据
            #         print('get data from serial port:', rev_data)

            
            # time.sleep(1)
        pass

        pass

    ''' 读取数据 '''
    def read(self):
        status = True
        while status:
            n = self.ser_v.inWaiting()
            if n > 0:
                # data = self.ser_v.read_all()
                data = self.ser_v.read_until()
                if "ok" in str(data):
                    print(str(data))
                    sleep(1)
                    return 

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


'''

import os
import serial
import time
import threading
 
class SerialPort:
	message='' 
	def __init__(self,port,buand):
		super(SerialPort, self).__init__()
		self.port=serial.Serial(port,buand)
		self.port.close()
		if not self.port.isOpen():
			self.port.open()
	def port_open(self):
		if not self.port.isOpen():
			self.port.open()
	def port_close(self):
		self.port.close()
	def send_data(self):
			data = input("请输入要发送的数据（非中文）并同时接收数据: ")
			n=self.port.write((data+'\n').encode())
			return n
	def read_data(self):
		while True:
			self.message=self.port.readline()
			print(self.message)
 
serialPort="COM6"   #串口
baudRate=115200       #波特率
 
if __name__=='__main__':
    
	mSerial=SerialPort(serialPort,baudRate)
	t1=threading.Thread(target=mSerial.read_data) 
    
	t1.start()
	while True:
         time.sleep(1)
         mSerial.send_data()  


'''
# https://www.jianshu.com/p/b5ba170a25aa
# https://www.cnblogs.com/mangojun/p/10558069.html
# https://www.jb51.net/article/162891.htm
# https://www.jb51.net/article/162891.htm
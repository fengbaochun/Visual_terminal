import sys
from PyQt5.QtWidgets import QApplication,QMainWindow
#调用文件
from Ui_mainwindow import Ui_MainWindow  
from find_color_block import Find_color_block  

 
class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self,parent = None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        #设置软件title
        self.setWindowTitle("视觉终端")
        #在table中添加demo,并在类中实现功能
        table_1 = Find_color_block()
        self.tabWidget.insertTab(0,table_1,"色块识别")
        # 设置当前显示的界面 默认界面
        self.tabWidget.setCurrentWidget(table_1)


if __name__ =='__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())

#参考资料
# https://www.jb51.net/article/156192.htm
# https://www.cnblogs.com/leokale-zz/p/13099815.html@
# https://blog.csdn.net/jia666666/article/details/81669092
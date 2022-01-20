import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5 import uic
from bs4 import BeautifulSoup
import requests

def get_channels(file):
    f = open(file, 'r', encoding='UTF8')
    text = f.read()

    soup = BeautifulSoup(text, "html.parser")
    channels = soup.find_all("a", attrs={"class":"channel-link"})
    ch_list = []
    for i,channel in enumerate(channels):
        if i%2 == 0:
            ch_list.append(str(channel["href"]))
    return ch_list


#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("main.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.Button1.clicked.connect(self.file_open)

    def file_open(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        self.file_path.setText(filename[0])	
        ch_list = get_channels(filename[0])
        for i in range(len(ch_list)):
            self.channel_list.append("youtube.com"+ch_list[i])	
    


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
import sys
from tkinter.tix import Tree
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5 import uic
from bs4 import BeautifulSoup
import pyperclip
import requests
import pyautogui
import time

def my_write(text):
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")

def copy():
    w = pyautogui.getWindowsWithTitle("YouTube - Chrome")[0]
    if w.isActive == False:
        w.activate()
    if w.isMaximized == False:
        w.maximize()
    f = open("channel_list.txt", 'r', encoding='UTF8')
    lines = f.readlines()
    for line in lines:
        QApplication.processEvents()
        pyautogui.press("f6")
        my_write(line)
        pyautogui.press("enter")
        time.sleep(3)
        btn = pyautogui.locateOnScreen("subscribe_btn.png", grayscale=True, confidence=0.9)
        title = w.title
        title = title.replace("YouTube - Chrome", "")
        if btn is not None:
            pyautogui.click(btn)
            myWindow.show_execution(title+"ok")
        else:
            myWindow.show_execution(title+"pass")
            continue
    myWindow.show_execution("complete!")
    f.close

def get_channels(file):
    f = open(file, 'r', encoding='UTF8')
    text = f.read()

    soup = BeautifulSoup(text, "html.parser")
    channels = soup.find_all("a", attrs={"class":"channel-link"})
    ch_list = []
    for i,channel in enumerate(channels):
        if i%2 == 0:
            ch_list.append(str(channel["href"]))
    f.close
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
        self.open_btn.clicked.connect(self.file_open)
        self.copy_Button.clicked.connect(copy)

    def file_open(self):
        try:
            filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
            self.file_path.setText(filename[0])	
            ch_list = get_channels(filename[0])
            f = open("channel_list.txt", 'w', encoding='UTF8')
            for i in range(len(ch_list)):
                self.channel_list.append("youtube.com"+ch_list[i])	
                f.write("youtube.com"+ch_list[i]+"\n")
            f.close
        except:
            return 0

    def show_execution(self, text):
        self.execution_textBrowser.append(text)
        self.execution_textBrowser.repaint()
    


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
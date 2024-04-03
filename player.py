import time

from playerui import Ui_Form
from PyQt5.QtWidgets import QDialog,QLCDNumber
from PyQt5.QtCore import Qt,QUrl,QTimer
from PyQt5.QtMultimedia import QMediaContent,QMediaPlayer
import os
class PlayerWidget(QDialog):
    def __init__(self,acolor=[0,128,255],bcolor=[255,128,0],dtime=180.0,tbuf=0.5,discolor=[80,80,80],parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.showFullScreen()
        self.resize(1920,1080)
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.repaint)
        self.timer.start()
        self.acolor = acolor
        self.bcolor = bcolor
        self.dtime = dtime
        self.tbuf = tbuf
        self.discolor = discolor
        # self.windowsize = [850,450]
        self.setStyleSheet("background-color:rgb(0,0,0);")
        self.ui.Atimer.setStyleSheet("border: 0px; color: rgb(%d,%d,%d);"%(discolor[0],discolor[1],discolor[2]))
        self.ui.Btimer.setStyleSheet("border: 0px; color: rgb(%d,%d,%d);"%(discolor[0],discolor[1],discolor[2]))
        self.ui.Acache.setStyleSheet("border: 0px; color: rgb(%d,%d,%d);"%(discolor[0],discolor[1],discolor[2]))
        self.ui.Bcache.setStyleSheet("border: 0px; color: rgb(%d,%d,%d);"%(discolor[0],discolor[1],discolor[2]))
        self.ui.Atimer.setSegmentStyle(QLCDNumber.Flat)
        self.ui.Btimer.setSegmentStyle(QLCDNumber.Flat)
        self.ui.Acache.setSegmentStyle(QLCDNumber.Flat)
        self.ui.Bcache.setSegmentStyle(QLCDNumber.Flat)
        self.keepgoing = True
        self.mixer = QMediaPlayer()
        self.mixer.setMedia(QMediaContent(QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__),"ding.mp3"))))
        self.mixer.setVolume(50)
        self.user = 0
        self.atime = dtime
        self.atimel = dtime
        self.abuf = tbuf
        self.btime = dtime
        self.btimel = dtime
        self.bbuf = tbuf
        self.t0 = time.time()
        self.status = 2
    def keyPressEvent(self,event):
        if event.key() == Qt.Key.Key_Escape:
            self.keepgoing = False
            self.close()
        elif event.key() == Qt.Key.Key_Space:
            if self.status == 0:
                self.status = 3
                self.atimel = self.atime
                self.t0 = time.time()
            elif self.status == 1:
                self.status = 2
                self.btimel = self.btime
                self.t0 = time.time()
    def paintEvent(self,event):
        self.ui.Atimer.setStyleSheet("border: 0px; color: rgb(%d,%d,%d);"%(self.discolor[0],self.discolor[1],self.discolor[2]))
        self.ui.Btimer.setStyleSheet("border: 0px; color: rgb(%d,%d,%d);"%(self.discolor[0],self.discolor[1],self.discolor[2]))
        self.ui.Acache.setStyleSheet("border: 0px; color: rgb(%d,%d,%d);"%(self.discolor[0],self.discolor[1],self.discolor[2]))
        self.ui.Bcache.setStyleSheet("border: 0px; color: rgb(%d,%d,%d);"%(self.discolor[0],self.discolor[1],self.discolor[2]))
        self.ui.Aprogress.setStyleSheet("QProgressBar{text-align: center;color: #FFFFFF;}QProgressBar::chunk{background-color: rgb(%d,%d,%d);}"%(self.discolor[0],self.discolor[1],self.discolor[2]))
        self.ui.Bprogress.setStyleSheet("QProgressBar{text-align: center;color: #FFFFFF;}QProgressBar::chunk{background-color: rgb(%d,%d,%d);}"%(self.discolor[0],self.discolor[1],self.discolor[2]))
        if self.status == 0:
            self.ui.Atimer.setStyleSheet("border: 0px; color: rgb(%d,%d,%d);"%(self.acolor[0],self.acolor[1],self.acolor[2]))
            self.ui.Aprogress.setStyleSheet("QProgressBar{text-align: center;color: #FFFFFF;}QProgressBar::chunk{background-color: rgb(%d,%d,%d);}"%(self.acolor[0],self.acolor[1],self.acolor[2]))
            self.atime = self.atimel + self.t0 - time.time()
            if self.atime < 0:
                self.t0 = time.time()
                self.status = 3
                self.atime = self.atimel = 0
        elif self.status == 1:
            self.ui.Btimer.setStyleSheet("border: 0px; color: rgb(%d,%d,%d);"%(self.bcolor[0],self.bcolor[1],self.bcolor[2]))
            self.ui.Bprogress.setStyleSheet("QProgressBar{text-align: center;color: #FFFFFF;}QProgressBar::chunk{background-color: rgb(%d,%d,%d);}"%(self.bcolor[0],self.bcolor[1],self.bcolor[2]))
            self.btime = self.btimel + self.t0 - time.time()
            if self.btime < 0:
                self.t0 = time.time()
                self.status = 2
                self.btime = self.btimel = 0
        elif self.status == 2:
            self.ui.Acache.setStyleSheet("border: 0px; color: rgb(%d,%d,%d);"%(self.acolor[0],self.acolor[1],self.acolor[2]))
            self.abuf = self.tbuf + self.t0 - time.time()
            if self.abuf < 0:
                self.t0 = time.time()
                self.status = 0
                self.abuf = self.tbuf
                self.mixer.stop()
                self.mixer.play()
            if self.atime == 0 and self.btime == 0:
                self.mixer.stop()
                self.mixer.play()
                self.keepgoing = False
                self.close()
        elif self.status == 3:
            self.ui.Bcache.setStyleSheet("border: 0px; color: rgb(%d,%d,%d);"%(self.bcolor[0],self.bcolor[1],self.bcolor[2]))
            self.bbuf = self.tbuf + self.t0 - time.time()
            if self.bbuf < 0:
                self.t0 = time.time()
                self.status = 1
                self.bbuf = self.tbuf
                self.mixer.stop()
                self.mixer.play()
            if self.atime == 0 and self.btime == 0:
                self.mixer.stop()
                self.mixer.play()
                self.keepgoing = False
                self.close()
            # ats = resources["FiraCode Bold 300"].render("%.1f"%atime,True,acolor if status == 0 else discolor)
            # bts = resources["FiraCode Bold 300"].render("%.1f"%btime,True,bcolor if status == 1 else discolor)
            # abus = resources["FiraCode Bold 100"].render("%.2f"%abuf,True,acolor if status == 2 else discolor)
            # bbus = resources["FiraCode Bold 100"].render("%.2f"%bbuf,True,bcolor if status == 3 else discolor)
            # screen.blit(ats,[(size[0]/2-ats.get_width())/2,200])
            # screen.blit(bts,[(size[0]/2-bts.get_width())/2 + size[0]/2,200])
            # screen.blit(abus,[(size[0]/2-abus.get_width())/2,600])
            # screen.blit(bbus,[(size[0]/2-bbus.get_width())/2 + size[0]/2,600])
        self.ui.Atimer.display("%.1f"%self.atime)
        self.ui.Btimer.display("%.1f"%self.btime)
        self.ui.Acache.display("%.2f"%self.abuf)
        self.ui.Bcache.display("%.2f"%self.bbuf)
        self.ui.Aprogress.setValue(int(self.atime*100/self.dtime))
        self.ui.Bprogress.setValue(int(self.btime*100/self.dtime))
        # self.close()
        # time.sleep(1)
    def resizeEvent(self,event):
        size = [event.size().width(),event.size().height()]
        self.ui.Atimer.setGeometry(size[0]*3//17,size[1]*8//45,size[0]*4//17,size[1]*4//15)
        self.ui.Btimer.setGeometry(size[0]*10//17,size[1]*8//45,size[0]*4//17,size[1]*4//15)
        self.ui.Acache.setGeometry(size[0]*19//85,size[1]*22//45,size[0]*12//85,size[1]//9)
        self.ui.Bcache.setGeometry(size[0]*11//17,size[1]*22//45,size[0]*12//85,size[1]//9)
        self.ui.Aprogress.setGeometry(size[0]*13//85,size[1]*31//45,size[0]*24//85,30)
        self.ui.Bprogress.setGeometry(size[0]*48//85,size[1]*31//45,size[0]*24//85,30)
    def close(self):
        time.sleep(1)
        return super().close()
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(["argtimer"])
    w = PlayerWidget()
    w.show()
    app.exec_()
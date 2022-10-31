from ctypes import windll
from subprocess import PIPE, Popen
from sys import exit, argv
from sqlite3 import connect
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from requests import get

import config
import function
from shutil import copy
from getpass import getuser


def clickedStart():
    con = connect('bd')
    cur = con.cursor()
    home = cur.execute(f"""SELECT * FROM homeInfo""").fetchall()[0]
    path = 'resurse/weather.jpg'
    if home[5] == 0:
        if home[3]:
            data = get(f"http://api.openweathermap.org/data/2.5/weather?"
                       f"q={home[0]}&type=like&APPID={config.appid}").json()
            weather = data['weather'][0]['main']
        else:
            data = get(f"http://api.openweathermap.org/data/2.5/weather?"
                       f"lat={home[1]}&lon={home[2]}&type=like&APPID={config.appid}").json()
            weather = data['weather'][0]['main']
        path = cur.execute(f"""SELECT path FROM pathToImage WHERE title='{weather}'""").fetchall()[0][0]
        con.close()
    elif home[5] == 1:
        cmd = 'python telegramGeneratePhoto.py'
        p = Popen(cmd, stdout=PIPE, shell=True)
        p.wait()

    windll.user32.SystemParametersInfoW(20, 0, path, 0)


class MyWidget(QMainWindow):
    wither = {'witherBut_1': 'Rain',
              'witherBut_2': 'Clouds',
              'witherBut_3': 'Drizzle',
              'witherBut_4': 'Snow',
              'witherBut_5': 'Thunderstorm',
              'witherBut_6': 'Clear'}

    def __init__(self):
        super().__init__()
        uic.loadUi('mainWindow.ui', self)
        self.setWindowTitle('Wall')
        self.pushButtonCity.clicked.connect(self.clickedButtonCity)
        self.pushButtonCoords.clicked.connect(self.clickedButtonCoords)
        self.pushButton.clicked.connect(self.clickedButtonTime)
        self.witherBut_1.clicked.connect(self.clickedWeatherButton)
        self.witherBut_2.clicked.connect(self.clickedWeatherButton)
        self.witherBut_3.clicked.connect(self.clickedWeatherButton)
        self.witherBut_4.clicked.connect(self.clickedWeatherButton)
        self.witherBut_5.clicked.connect(self.clickedWeatherButton)
        self.witherBut_6.clicked.connect(self.clickedWeatherButton)
        self.pushButton.clicked.connect(clickedStart)
        self.butAutoload.clicked.connect(self.clickedAutoload)
        self.butAIImage.clicked.connect(self.clickedAIImage)

    def clickedAIImage(self):
        if self.sender().isChecked():
            con = connect('bd')
            cur = con.cursor()
            cur.execute(f"""UPDATE homeInfo SET
                                                type_1=1
                                                                WHERE true""")
            con.commit()
            con.close()
        else:
            con = connect('bd')
            cur = con.cursor()
            cur.execute(f"""UPDATE homeInfo SET
                                                type_1=0
                                                                WHERE true""")
            con.commit()
            con.close()

    def clickedAutoload(self):
        USER_NAME = getuser()
        bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\start.lnk' % USER_NAME
        copy(r'start.exe - Ярлык.lnk', bat_path)

    def clickedButtonTime(self):
        con = connect('bd')
        cur = con.cursor()
        cur.execute(f"""UPDATE homeInfo SET 
                                    time={int(self.spinTime.text()) * 3600} 
                                                    WHERE true""")
        con.commit()
        con.close()

    def clickedWeatherButton(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')[0]
        con = connect('bd')
        cur = con.cursor()
        cur.execute(f"""
                    UPDATE pathToImage SET path='{fname}'
                     WHERE title='{self.sender().objectName()}'""").fetchall()
        con.commit()
        con.close()

    def clickedButtonCity(self):
        a = function.weatherNowCity(self.lineEditCity.text())
        if a:
            self.warningCity.setText(' ')
            con = connect('bd')
            cur = con.cursor()
            cur.execute(f"""UPDATE homeInfo SET 
                            title='{self.lineEditCity.text()}', type=1 
                                            WHERE true""")
            con.commit()
            con.close()
        else:
            self.warningCity.setText('Данный город не предусмотрен')

    def clickedButtonCoords(self):
        a = function.weatherNowCoords(self.lineEditX.text(),
                                      self.lineEditY.text())
        if a:
            self.warningCoords.setText(' ')
            con = connect('bd')
            cur = con.cursor()
            cur.execute(f"""UPDATE homeInfo SET 
                            X='{self.lineEditX.text()}',
                            Y='{self.lineEditY.text()}',
                            type = 0
                                         WHERE true""")
            con.commit()
            con.close()
        else:
            self.warningCoords.setText('Координаты не корректны')


if __name__ == '__main__':
    app = QApplication(argv)
    ex = MyWidget()
    ex.show()
    exit(app.exec_())

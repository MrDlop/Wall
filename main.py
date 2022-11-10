import datetime
from ctypes import windll
from subprocess import PIPE, Popen
from sys import exit, argv
from sqlite3 import connect
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from requests import get
from shutil import copy
from getpass import getuser
from googletrans import LANGCODES, Translator, LANGUAGES

import config
import function

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

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
        con = connect('bd')
        cur = con.cursor()
        lang = cur.execute("""SELECT language FROM homeInfo""").fetchall()[0][0]
        con.close()

        translator = Translator()

        self.languageBox.setCurrentIndex(self.languageBox.findText(LANGUAGES[lang]))

        self.label_city.setText(translator.translate(self.label_city.text(), dest=lang).text)
        self.label_coords.setText(translator.translate(self.label_coords.text(), dest=lang).text)
        self.label_latitude.setText(translator.translate(self.label_latitude.text(), dest=lang).text)
        self.label_length.setText(translator.translate(self.label_length.text(), dest=lang).text)
        self.label_clock.setText(translator.translate(self.label_clock.text(), dest=lang).text)
        self.radioStatic.setText(translator.translate(self.radioStatic.text(), dest=lang).text)

        self.setWindowTitle('Wall')
        self.pushButtonCity.clicked.connect(self.clickedButtonCity)
        self.pushButtonCoords.clicked.connect(self.clickedButtonCoords)
        self.pushButton.clicked.connect(self.clickedButtonTime)
        for i in range(1, 7):
            a = eval(f'self.witherBut_{i}')
            b = eval(f'self.label_wither_{i}')
            a.clicked.connect(self.clickedWeatherButton)
            a.setText(translator.translate(a.text(), dest=lang).text)
            b.setText(translator.translate(b.text(), dest=lang).text)

        self.pushButton.clicked.connect(self.clickedStart)
        self.pushButton.setText(translator.translate(self.pushButton.text(), dest=lang).text)

        self.butAutoload.clicked.connect(self.clickedAutoload)
        self.butAutoload.setText(translator.translate(self.butAutoload.text(), dest=lang).text)

        self.butAIImage.clicked.connect(self.clickedAIImage)
        self.butAIImage.setText(translator.translate(self.butAIImage.text(), dest=lang).text)

        self.radioStatic.clicked.connect(self.radioStatic_)

        for i in LANGCODES:
            self.languageBox.addItem(i)

    def clickedStart(self):
        con = connect('bd')
        cur = con.cursor()
        cur.execute(f"""
        UPDATE homeInfo SET language='{LANGCODES[self.languageBox.currentText()]}'
        """)
        con.commit()
        lang = self.languageBox.currentText()

        translator = Translator()

        self.butAIImage.setText(translator.translate(self.butAIImage.text(), dest=lang).text)
        self.butAutoload.setText(translator.translate(self.butAutoload.text(), dest=lang).text)
        self.pushButton.setText(translator.translate(self.pushButton.text(), dest=lang).text)
        self.label_city.setText(translator.translate(self.label_city.text(), dest=lang).text)
        self.label_coords.setText(translator.translate(self.label_coords.text(), dest=lang).text)
        self.label_latitude.setText(translator.translate(self.label_latitude.text(), dest=lang).text)
        self.label_length.setText(translator.translate(self.label_length.text(), dest=lang).text)
        self.label_clock.setText(translator.translate(self.label_clock.text(), dest=lang).text)
        self.radioStatic.setText(translator.translate(self.radioStatic.text(), dest=lang).text)
        for i in range(1, 7):
            a = eval(f'self.witherBut_{i}')
            b = eval(f'self.label_wither_{i}')
            a.setText(translator.translate(a.text(), dest=lang).text)
            b.setText(translator.translate(b.text(), dest=lang).text)

        home = cur.execute(f"""SELECT * FROM homeInfo""").fetchall()[0]

        path = 'resurse/weather.jpg'
        if home[3]:
            data = get(f"http://api.openweathermap.org/data/2.5/weather?"
                       f"q={home[0]}&type=like&APPID={config.appid}").json()
            weather = data['weather'][0]['main']
        else:
            data = get(f"http://api.openweathermap.org/data/2.5/weather?"
                       f"lat={home[1]}&lon={home[2]}&type=like&APPID={config.appid}").json()
            weather = data['weather'][0]['main']
        if home[7]:
            t = datetime.datetime.now().day
            with open("data.csv", "a") as f:
                f.write(f"\n{t}.{datetime.datetime.now().month}."
                        f"{datetime.datetime.now().year};{data['main']['temp']};{weather}")
                f.close()
        if home[5] == 0:
            path = cur.execute(f"""SELECT path FROM pathToImage WHERE title='{weather}'""").fetchall()[0][0]
            con.close()
        elif home[5] == 1:
            cmd = 'python telegramGeneratePhoto.py'
            p = Popen(cmd, stdout=PIPE, shell=True)
            p.wait()

        windll.user32.SystemParametersInfoW(20, 0, path, 0)

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

    def radioStatic_(self):
        if self.sender().isChecked():
            con = connect('bd')
            cur = con.cursor()
            cur.execute(f"""UPDATE homeInfo SET
                                                                static=1
                                                                                WHERE true""")
            con.commit()
            con.close()
        else:
            con = connect('bd')
            cur = con.cursor()
            cur.execute(f"""UPDATE homeInfo SET
                                                static=0
                                                                WHERE true""")
            con.commit()
            con.close()

    def clickedAutoload(self):
        flag = QMessageBox.question(self, "Предупреждение", "Вы точно хотите "
                                                            "поставить программу на автозагрузку")
        if flag == QMessageBox.Yes:
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
        path = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')[0]
        con = connect('bd')
        cur = con.cursor()
        cur.execute(f"""
                    UPDATE pathToImage SET path='{path}'
                     WHERE title='{self.sender().objectName()}'""").fetchall()
        con.commit()
        con.close()

    def clickedButtonCity(self):
        if function.findCity(self.lineEditCity.text()):
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
        if function.findCityForCoords(self.lineEditX.text(),
                                      self.lineEditY.text()):
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

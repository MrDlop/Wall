import json
import sys
from sqlite3 import connect
from sys import exit, argv
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from googletrans import Translator

import function


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('weatherWidgetWindow.ui', self)

        con = connect('bd')
        cur = con.cursor()
        lang = cur.execute("""SELECT language FROM homeInfo""").fetchall()[0][0]
        con.close()

        translator = Translator()

        self.arr = ['weather', 'temperature', 'speed_wind', 'humidity', 'pressure']
        self.config = json.load(open("Config/settings.json"))

        color_nameLabel = [self.graphicColor('purple'),
                           self.graphicColor('red'),
                           self.graphicColor('yellow'),
                           self.graphicColor('green'),
                           self.graphicColor('orange')]
        color_textLabel = [self.graphicColor('purple'),
                           self.graphicColor('red'),
                           self.graphicColor('yellow'),
                           self.graphicColor('green'),
                           self.graphicColor('orange')]
        for i, j in zip(self.arr, color_nameLabel):
            a = eval(f'self.label_{i}_1')
            text = a.text()
            a.setText(translator.translate(text, dest=lang).text)
            a.setGraphicsEffect(j)
            a.setStyleSheet(f"font: {self.config['day-month-year_font_size']}pt \"UniSansBold\";\n"
                            "color: rgb(255, 255, 255);")
            a.setAlignment(QtCore.Qt.AlignCenter)
        for i, j in zip(self.arr, color_textLabel):
            a = eval(f'self.label_{i}')

            a.setGraphicsEffect(j)
            a.setStyleSheet(f"font: {self.config['day-month-year_font_size']}pt \"UniSansBold\";\n"
                            "color: rgb(255, 255, 255);")
            a.setAlignment(QtCore.Qt.AlignCenter)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        timer = QTimer(self)
        timer.timeout.connect(self.start)
        timer.start(1000)

    def graphicColor(self, color):
        return QGraphicsDropShadowEffect(self,
                                         blurRadius=15.0,
                                         color=QtGui.QColor(color),
                                         offset=QtCore.QPointF(0.0, 0.0)
                                         )

    def start(self):
        con = connect('bd')
        cur = con.cursor()
        home = cur.execute(f"""SELECT * FROM homeInfo""").fetchall()[0]
        con.close()
        if home[3]:
            data = function.infoCity(home[0])
        else:
            data = function.infoCoords(home[1], home[2])
        forecast = [data['weather'][0]['description'],
                    data['main']['temp'],
                    data['wind']['speed'],
                    data['main']['humidity'],
                    data['main']['pressure']]
        for i, j in zip(self.arr, forecast):
            a = eval(f'self.label_{i}')
            if i == 'temperature':
                a.setText(str(round(float(j) - 273.15, 2)) + "°C")
            elif i == 'weather':
                con = connect('bd')
                cur = con.cursor()
                lang = cur.execute("""SELECT language FROM homeInfo""").fetchall()[0][0]
                con.close()

                translator = Translator()

                a.setText(translator.translate(j, dest=lang).text)
            else:
                a.setText(str(j))


if __name__ == '__main__':
    app = QApplication(argv)
    ex = MyWidget()
    ex.show()
    if sys.platform == 'win32':
        from ctypes import windll
        import win32gui, win32con

        win32gui.SetWindowPos(ex.winId(), win32con.HWND_BOTTOM, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)

        hwnd = win32gui.GetWindow(win32gui.GetWindow(windll.user32.GetTopWindow(0), win32con.GW_HWNDLAST),
                                  win32con.GW_CHILD)
        win32gui.SetWindowLong(ex.winId(), win32con.GWL_HWNDPARENT, hwnd)
    exit(app.exec_())

import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QMessageBox, QTableWidgetItem, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import Qt, QSize
from design_for_sign_up import Ui_MainWindow1
from design_for_victorina import Ui_MainWindow2
from design_for_rank import Ui_MainWindow3


class MyWidget(QMainWindow, Ui_MainWindow1):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('python_embl1.jpg'))
        self.setFixedSize(354, 380)

        window = self.frameGeometry()
        window_central = QDesktopWidget().availableGeometry().center()
        window.moveCenter(window_central)
        self.move(window.topLeft())

        self.pushButton.clicked.connect(self.sign_up)

        self.pixmap = QPixmap('python_embl1.jpg')
        self.label_5.setFixedSize(150, 120)
        self.label_5.move(90, 80)
        self.label_5.setPixmap(self.pixmap)

        # self.con = sqlite3.connect("db/birthday.db")

        nImage = QImage("020 New Life.png")
        sImage = nImage.scaled(QSize(374, 390))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

    def sign_up(self):
        self.window1 = Victorina()
        self.hide()
        self.window1.show()


class UserError(Exception):  # создание собствнных ошибок
    pass


class EmptyValue(UserError):
    pass


class ExistingValue(UserError):
    pass


class Victorina(QMainWindow, Ui_MainWindow2):  # класс для добавления в БД информации о новом человеке
    def __init__(self):
        super(Victorina, self).__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('python_embl1.jpg'))
        self.setFixedSize(639, 312)

        window = self.frameGeometry()
        window_central = QDesktopWidget().availableGeometry().center()
        window.moveCenter(window_central)
        self.move(window.topLeft())

        self.pushButton.clicked.connect(self.start)
        self.pushButton_2.clicked.connect(self.check)

        oImage = QImage("020 New Life.png")
        sImage = oImage.scaled(QSize(639, 312))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

    def start(self):
        pass

    def question(self):
        pass

    def check(self):
        # self.finish()
        pass

    def finish(self):
        self.window2 = Rank()
        self.hide()
        self.window2.show()


class Rank(QMainWindow, Ui_MainWindow3):
    def __init__(self):
        super(Rank, self).__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('python_embl1.jpg'))
        self.setFixedSize(428, 423)

        window = self.frameGeometry()
        window_central = QDesktopWidget().availableGeometry().center()
        window.moveCenter(window_central)
        self.move(window.topLeft())

        # self.con = sqlite3.connect("db/birthday.db")

        self.pushButton.clicked.connect(self.load)

        oImage = QImage("020 New Life.png")
        sImage = oImage.scaled(QSize(428, 423))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

    def load(self):
        pass
        # cur = self.con.cursor()
        # self.res_id_hor = f"SELECT horoscope FROM information WHERE name='{name}'"
        # id = cur.execute(self.res_id_hor)
        # id = list(id)
        # id = id[0][0]
        # if not id:
        #     self.label_4.setText('Error: Запись не найдена')
        #     self.label_5.setText('')
        #     self.listWidget.clear()
        #     return
        # else:
        #     self.label_4.setText('')
        #     self.res_descr_hor = f"SELECT description FROM horoscope_bd WHERE id = {id}"
        #     self.res_descr_hor = cur.execute(self.res_descr_hor).fetchall()
        #     self.res_title_hor = f"SELECT title FROM horoscope_bd WHERE id = {id}"
        #     self.res_title_hor = cur.execute(self.res_title_hor).fetchall()
        #     self.label_5.setText(self.res_title_hor[0][0])
        #     need = self.res_descr_hor[0][0].split('*')
        #     self.listWidget.addItems(need)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())

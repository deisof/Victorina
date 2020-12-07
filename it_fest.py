import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QIcon, QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize
from design_for_sign_up import Ui_MainWindow1
from design_for_victorina import Ui_MainWindow2
from design_for_rank import Ui_MainWindow3


class UserError(Exception):  # создание собствнных ошибок
    pass


class EmptyValue(UserError):
    pass


class ExistingValue(UserError):
    pass


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

        self.con = sqlite3.connect("project.db")

        nImage = QImage("020 New Life.png")
        sImage = nImage.scaled(QSize(374, 390))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

    def sign_up(self):
        name = self.lineEdit.text()
        cur = self.con.cursor()
        try:
            if name:
                check = f"SELECT id FROM record WHERE name='{name}'"
                result = cur.execute(check).fetchall()
                if result:
                    raise ExistingValue
            else:
                raise EmptyValue
        except EmptyValue:
            self.label_4.setText('Error: Введите имя')
            return
        except ExistingValue:
            self.label_4.setText('Error: Пользователь с таким именем уже есть')
            return
        cur.execute(
            "INSERT INTO record(name, score) VALUES (?, ?)",
            (name, 0))
        self.con.commit()
        self.new_window()

    def new_window(self):
        self.window1 = Victorina()
        self.hide()
        self.window1.show()


class Victorina(QMainWindow, Ui_MainWindow2):
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
        with open('tests.txt', encoding='utf8') as f:
            self.text = f.read().split('\\')
        self.text = [value for value in self.text if value]
        self.question = []
        self.answer = []
        self.explanation = []
        q = 1
        for i in range(len(self.text)):
            if i % 3 == 0:
                self.question.append(self.text[i])
            elif i == q:
                self.answer.append(self.text[i])
                q += 3
            else:
                self.explanation.append(self.text[i])
        self.x = 0
        self.y = 0
        self.lcdNumber.display(self.x)
        self.pushButton.clicked.connect(self.start)
        self.pushButton_2.clicked.connect(self.check)

        oImage = QImage("020 New Life.png")
        sImage = oImage.scaled(QSize(639, 312))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

    def start(self):
        if self.y != len(self.question):
            if self.y == 0:
                self.label_3.setText(f'{self.y + 1}/10')
            self.listWidget.clear()
            self.listWidget.addItem(self.question[self.y])
        else:
            self.finish()

    def question(self):
        pass

    def check(self):
        ans = self.lineEdit.text()
        if ans == self.answer[self.y]:
            message = QMessageBox.information(self, '', "Вы ответили правильно, так держать", QMessageBox.Ok)
            if message == QMessageBox.Ok:
                self.x += 1
                self.lcdNumber.display(self.x)
                self.y += 1
                self.label_3.setText(f'{self.y + 1}/10')
                self.lineEdit.clear()
                self.start()
        else:
            message = QMessageBox.information(self, '', "Вы ответили неверно, хотети увидеть объяснение", QMessageBox.Yes, QMessageBox.No)
            if message == QMessageBox.Yes:
                message = QMessageBox.information(self, '', self.explanation[self.y], QMessageBox.Ok)
                if message == QMessageBox.Ok:
                    self.y += 1
                    self.label_3.setText(f'{self.y + 1}/10')
                    self.lineEdit.clear()
                    self.start()
            else:
                self.y += 1
                self.label_3.setText(f'{self.y + 1}/10')
                self.lineEdit.clear()
                self.start()



    def finish(self):
        self.window2 = Rank(self.x)
        self.hide()
        self.window2.show()


class Rank(QMainWindow, Ui_MainWindow3):
    def __init__(self, x):
        super(Rank, self).__init__()
        self.x = x
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('python_embl1.jpg'))
        self.setFixedSize(428, 423)

        window = self.frameGeometry()
        window_central = QDesktopWidget().availableGeometry().center()
        window.moveCenter(window_central)
        self.move(window.topLeft())
        self.con = sqlite3.connect("project.db")
        self.label_3.setText(f'{self.x}')
        self.pushButton.clicked.connect(self.load)

        oImage = QImage("020 New Life.png")
        sImage = oImage.scaled(QSize(428, 423))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

    def load(self):
        self.queue = f"SELECT name, score FROM record"
        cur = self.con.cursor()
        result = cur.execute(self.queue).fetchall()
        result = sorted(result, key=lambda x: x[1], reverse=True)
        if not result:
            pass
        else:
            self.tableWidget.setRowCount(len(result))
            self.tableWidget.setColumnCount(len(result[0]))
            column = (el[0] for el in cur.description)
            column = tuple(column)
            self.tableWidget.setHorizontalHeaderLabels(column)
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())

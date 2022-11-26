import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class AnotherWindow(QMainWindow):
    def __init__(self):
        super(AnotherWindow, self).__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton.clicked.connect(self.change)
        self.con = sqlite3.connect('cofee.sqlite')
        self.cur = self.con.cursor()

    def change(self):
        info = [self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text(),
                self.lineEdit_5.text(), self.lineEdit_6.text(), self.lineEdit_7.text()]
        if info:
            if int(info[0]) in [elem[0] for elem in self.cur.execute("""SELECT id FROM info""").fetchall()]:

                self.cur.execute(
                    f'UPDATE info SET name = "{info[1]}", degree = "{info[2]}", type = "{info[3]}", taste = "{info[4]}", price = "{info[5]}", size = "{info[6]}" WHERE id = "{info[0]}"')
                self.con.commit()
            else:

                self.cur.execute(
                    f'INSERT INTO info (id, name, degree, type, taste, price,size) VALUES("{info[0]}", "{info[1]}", "{info[2]}", "{info[3]}", "{info[4]}", "{info[5]}", "{info[6]}")')
                self.con.commit()
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('design.ui', self)
        self.con = sqlite3.connect("cofee.sqlite")
        self.cur = self.con.cursor()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.update_btn.clicked.connect(self.update)
        self.pushButton.clicked.connect(self.show_new_window)

    def update(self):
        self.tableWidget.setHorizontalHeaderLabels(['id', 'name', 'degree', 'type', 'taste', 'price', 'size'])
        try:
            res = self.cur.execute("""SELECT id, name, degree, type, taste, price, size FROM info""").fetchall()
        except sqlite3.OperationalError:
            res = ['НЕТ', 'НИКАКИХ', 'ДАННЫХ', 'ВАМ', 'НУЖНО', 'ДОБАВИТЬ', 'ИХ']
            self.cur.execute("CREATE TABLE info (id     INTEGER, name   TEXT, degree TEXT, type   TEXT, taste  TEXT,"
                             " price  TEXT, size   TEXT);")
            self.con.commit()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(7)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def show_new_window(self, checked):
        self.other = AnotherWindow()
        self.other.show()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()

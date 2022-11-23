import sqlite3
import sys


from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from design import Ui_MainWindow

class Main(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        con = sqlite3.connect("cofee.sqlite")
        cur = con.cursor()
        self.setupUi(self)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        res = cur.execute("""SELECT id, name, degree, type, taste, price, size FROM info""").fetchall()
        for i, row in enumerate(res):
            tmp = i
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
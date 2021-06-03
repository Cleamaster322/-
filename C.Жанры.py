import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QTableWidget, QHBoxLayout
from PyQt5.QtGui import QColor
import csv
import sqlite3
    
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.loadUI()

        self.loadTable('students.csv')

    def loadUI(self):
        self.setGeometry(100, 100, 750, 550)
        self.lay = QHBoxLayout()
        self.table = QTableWidget()
        self.lay.addWidget(self.table)
        self.setLayout(self.lay)

    def loadTable(self, table_name):
        con = sqlite3.connect("films.db")
        cur = con.cursor()
        
        

        # with open(table_name, encoding="utf8") as csvfile:
        #     title = ["№","Название","Год","Жанр"]
        #     self.table.setColumnCount(len(title))
        #     self.table.setHorizontalHeaderLabels(title)
        #     self.table.setRowCount(0)
        #     result = cur.execute("""SELECT * FROM Films
        #     WHERE genre = 1""").fetchall()
        #     for i, row in enumerate(result):
        #         self.table.setRowCount(self.table.rowCount() + 1)
        #         for j, elem in enumerate(row):
        #             self.table.setItem(i,j, QTableWidgetItem(str(elem)))
        #         if i == 199:
        #             break
        # self.table.resizeColumnsToContents()
        # con.close() 

    
app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
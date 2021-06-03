import sys
from test import SecondForm
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QTableWidgetItem, QTableWidget, QHBoxLayout,QComboBox,QVBoxLayout, QMainWindow
from PyQt5.QtGui import QColor
import csv
import sqlite3

class FirstForm(QMainWindow):
    def __init__(self):
        super().__init__()

        self.loadUI()
        self.loadTable()

    def loadUI(self):
        self.setGeometry(100, 100, 130, 200)

    def loadTable(self):
        
        con = sqlite3.connect("films.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM genres""").fetchall()
        self.hor_layout = QVBoxLayout()

        self.label = QLabel(self)
        self.label.setText("Выберите жанр")
        self.label.move(25,0)

        self.btn = QComboBox(self)
        for elem in result:
                self.btn.addItem(elem[1])

        self.btn.move(15,30)

        self.btn1 = QPushButton("Найти",self)
        self.btn1.clicked.connect(self.ret_genre)
        
        self.btn1.move(15,70)

    def ret_genre(self):
        print(self.btn.currentText())
        self.second_form = SecondForm(self,"")
        self.second_form.show()


# class MyWidget(QWidget):
    # def __init__(self,*args):
    #     super().__init__()

    #     self.loadUI()

    #     self.loadTable('students.csv')

    # def loadUI(self):
    #     # self.lay = QHBoxLayout()
    #     self.table = QTableWidget()
    #     self.setGeometry(100, 100, 130, 200)
    #     # self.lay.addWidget(self.table)
    #     # self.setLayout(self.lay)

    # def loadTable(self, table_name):
        
    #     con = sqlite3.connect("films.db")
    #     cur = con.cursor()

    #     with open(table_name, encoding="utf8") as csvfile:
    #         title = ["№","Название","Год","Жанр"]
    #         self.table.setColumnCount(len(title))
    #         self.table.setHorizontalHeaderLabels(title)
    #         self.table.setRowCount(0)
    #         result = cur.execute("""SELECT * FROM Films
    #         WHERE genre = 1""").fetchall()
    #         for i, row in enumerate(result):
    #             self.table.setRowCount(self.table.rowCount() + 1)
    #             for j, elem in enumerate(row):
    #                 self.table.setItem(i,j, QTableWidgetItem(str(elem)))
    #             if i == 199:
    #                 break
    #     self.table.resizeColumnsToContents()
    #     con.close() 

class SecondForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Вторая форма')
        self.lbl = QLabel(args[-1], self)
        self.lbl.adjustSize()
    
app = QApplication(sys.argv)
ex = FirstForm()
ex.show()
sys.exit(app.exec_())
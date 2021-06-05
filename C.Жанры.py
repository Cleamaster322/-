import sys
from PyQt5.QtWidgets import QApplication, QBoxLayout, QPushButton, QWidget, QTableWidgetItem, QTableWidget, QHBoxLayout,QVBoxLayout,QComboBox
from PyQt5.QtGui import QColor
import csv
import sqlite3
    
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.loadUI()
        self.loadTable()
        

    def loadUI(self):
        self.setGeometry(100, 100, 750, 550)
        self.lay = QHBoxLayout()
        self.table = QTableWidget()
        self.allBtn = QVBoxLayout()
        self.all = QVBoxLayout()
        self.lay.addWidget(self.table)
        self.all.addLayout(self.allBtn)
        self.all.addLayout(self.lay)
        self.setLayout(self.all)

    def loadTable(self):
        con = sqlite3.connect("films.db")
        cur = con.cursor()
        allGenres = {}
        genre =cur.execute("""SELECT * FROM genres""").fetchall()

        for elem in genre:
            allGenres[elem[0]] = elem[1]
        self.btn_genre = QComboBox(self)

        for i in allGenres:
            self.btn_genre.addItem(allGenres[i])
        self.btn = QPushButton("Найти",self)

        self.allBtn.addWidget(self.btn_genre)
        self.allBtn.addWidget(self.btn)

        
        
        
        title = ["№","title","year","genre","Duration"]
        self.table.setColumnCount(len(title))
        self.table.setHorizontalHeaderLabels(title)
        self.table.setRowCount(0)
        
        result = cur.execute("""SELECT * FROM Films""").fetchall()
        for i, row in enumerate(result):
            self.table.setRowCount(self.table.rowCount() + 1)
            for j, elem in enumerate(row):
                if j == 3:
                    self.table.setItem(i,j, QTableWidgetItem(str(allGenres[elem])))
                else:
                    self.table.setItem(i,j, QTableWidgetItem(str(elem)))
            if i == 199:
                break
        
        self.table.resizeColumnsToContents()
        con.close() 
    
    def get_genre(self):
        self


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
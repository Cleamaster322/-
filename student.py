import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QTableWidget, QHBoxLayout
from PyQt5.QtGui import QColor
import csv

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
        self.max_bal = 920

    def loadTable(self, table_name):
        with open(table_name, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            title = next(reader)
            print(title)
            self.table.setColumnCount(len(title))
            self.table.setHorizontalHeaderLabels(title)
            self.table.setRowCount(0)
            for i, row in enumerate(reader):
                self.table.setRowCount(self.table.rowCount() + 1)
                summ = 0
                for j, elem in enumerate(row):
                    if row[j] != '' and (j>1 and j!=11):
                        summ += float(row[j])
                    self.table.setItem(i, j, QTableWidgetItem(elem))
                if summ >= self.max_bal*0.95:
                    self.table.item(i,1).setBackground(QColor("#98fb98"))
                elif summ >=self.max_bal*0.80:
                    self.table.item(i,1).setBackground(QColor("#ffff00"))
                elif summ >= self.max_bal*0.60:
                    self.table.item(i,1).setBackground(QColor("#ff0000"))
                
        self.table.resizeColumnsToContents()


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())

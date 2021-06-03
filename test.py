import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QComboBox
import sqlite3

class Test(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        con = sqlite3.connect("films.db")
        cur = con.cursor()
        
        self.setGeometry(200, 200, 300, 300)
        self.setWindowTitle('First program') 
        self.btn = QComboBox(self)   
        result = cur.execute("""SELECT * FROM genres""").fetchall()
        for elem in result:
            self.btn.addItem(elem[1])
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Test()
    ex.show()
    sys.exit(app.exec())

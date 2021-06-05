import sys

from PyQt5.QtWidgets import QApplication, QLineEdit, QWidget, QPushButton, QPlainTextEdit,QGridLayout,QVBoxLayout


class Test(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.initUI()
        self.allNum = []
        self.answ = ''
        self.flag = 0

    def initUI(self):
        self.setWindowTitle('Калькулятор')

        grid = QWidget()
        grid.setLayout(QGridLayout())


        self.result_field = QLineEdit()

        btn0 = QPushButton('0', clicked = lambda: self.pushed())
        btn1 =QPushButton("1")
        btn1.clicked.connect(self.pushed)
        btn2 =QPushButton("2")
        btn2.clicked.connect(self.pushed)
        btn3 =QPushButton("3")
        btn3.clicked.connect(self.pushed)
        btn4 =QPushButton("4")
        btn4.clicked.connect(self.pushed)
        btn5 =QPushButton("5")
        btn5.clicked.connect(self.pushed)
        btn6 =QPushButton("6")
        btn6.clicked.connect(self.pushed)
        btn7 =QPushButton("7")
        btn7.clicked.connect(self.pushed)
        btn8 =QPushButton("8")
        btn8.clicked.connect(self.pushed)
        btn9 =QPushButton("9")
        btn9.clicked.connect(self.pushed)
        btnLeftBrace =QPushButton("(")
        btnLeftBrace.clicked.connect(self.pushed)
        btnRightBrace =QPushButton(")")
        btnPlus = QPushButton("+")
        btnPlus.clicked.connect(self.pushed)
        btnSub = QPushButton("-")
        btnSub.clicked.connect(self.pushed)
        btnMult = QPushButton("*")
        btnMult.clicked.connect(self.pushed)
        btnDiv = QPushButton("\\")
        btnDiv.clicked.connect(self.pushed)
        btnRightBrace.clicked.connect(self.pushed)
        btnBack = QPushButton("Back")
        btnBack.clicked.connect(self.back)
        btnDel = QPushButton("Del")
        btnDel.clicked.connect(self.delete)
        btnPush = QPushButton("Push")
        btnPush.clicked.connect(self.push)
        btnPoint = QPushButton(",")
        btnPoint.clicked.connect(self.push)


        grid.layout().addWidget(self.result_field,0,0,1,4)
        grid.layout().addWidget(btnBack,1,0,1,2)
        grid.layout().addWidget(btnPush,1,2,1,2)
        grid.layout().addWidget(btnLeftBrace,2,0)
        grid.layout().addWidget(btnRightBrace,2,1)
        grid.layout().addWidget(btnDel,2,2)
        grid.layout().addWidget(btnPlus,2,3)
        grid.layout().addWidget(btn7,3,0)
        grid.layout().addWidget(btn8,3,1)
        grid.layout().addWidget(btn9,3,2)
        grid.layout().addWidget(btnSub,3,3)
        grid.layout().addWidget(btn4,4,0)
        grid.layout().addWidget(btn5,4,1)
        grid.layout().addWidget(btn6,4,2)
        grid.layout().addWidget(btnMult,4,3)
        grid.layout().addWidget(btn1,5,0)
        grid.layout().addWidget(btn2,5,1)
        grid.layout().addWidget(btn3,5,2)
        grid.layout().addWidget(btnDiv,5,3)
        grid.layout().addWidget(btn0,6,0,1,3)
        grid.layout().addWidget(btnPoint,6,3,1,1)


        self.layout().addWidget(grid)
    def pushed(self):
        sender = self.sender()
        self.allNum.append(str(sender.text()))
        self.result_field.setText(''.join(self.allNum))
        
        
    
    def back(self):
        if self.allNum == []:
            return
        sender = self.sender()
        self.allNum.pop()
        self.result_field.setText(''.join(self.allNum))
        
        

    def delete(self):
        sender = self.sender()
        self.allNum = []
        self.result_field.setText('')

    def push(self):
        if self.allNum == []:
            return
        try:
            sender = self.sender()
            self.result_field.setText(str(eval(''.join(self.allNum))))
            self.allNum = []
            self.answ = self.result_field.text()
        except:
            self.delete()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Test()
    ex.show()
    sys.exit(app.exec()) 
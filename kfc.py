import sys
from PyQt5.QtWidgets import QApplication, QSpinBox, QWidget,QLabel, QPlainTextEdit, QHBoxLayout, QCheckBox, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
from datetime import datetime
 
class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        self.setFixedSize(320,800)
        self.menu_layout = QVBoxLayout()
        self.print_layout = QHBoxLayout()
        self.out_layot = QVBoxLayout()
        self.setWindowTitle('KFC')
 
        self.cheque = []
        self.foods = ['Шефбургур', "Твистер", "Чизбургер", 'Боксмастер']
        self.img = ['pyqt\shef.jpg', 'pyqt\\twister.jpg','pyqt\chese.jpg','pyqt\\box.jpg']
        self.count = dict()
        self.input_window = QPlainTextEdit()
        self.input_window.setPlainText('')
        
 
        for i in self.foods:  # создание
            self.v_menu = QHBoxLayout()
           
            self.pixmap = QPixmap(self.img[self.foods.index(i)])
            self.image = QLabel(self)
            self.image.setPixmap(self.pixmap.scaledToWidth(100))

            self.checkb = QCheckBox(i, self)
            self.checkb.stateChanged.connect(self.checker)

            self.spinbox = QSpinBox(self)
            self.spinbox.setMaximum(10)

            self.count[i] = self.spinbox            

            self.v_menu.addWidget(self.image)
            self.v_menu.addWidget(self.checkb)
            self.v_menu.addWidget(self.spinbox)
            

            self.menu_layout.addLayout(self.v_menu)
        
        self.btn = QPushButton('Рассчет', self)
        self.btn.clicked.connect(self.print)
 
        self.print_layout.addWidget(self.input_window)
 
        self.out_layot.addLayout(self.menu_layout)
        self.out_layot.addWidget(self.btn)
        self.out_layot.addLayout(self.print_layout)
        self.setLayout(self.out_layot)
    
    def checker(self, state): # проверка на установку галки
        if self.checkb.sender().isChecked():
            self.cheque.append(self.checkb.sender().text())
        else:
            self.cheque.remove(self.checkb.sender().text())
 
    def print(self):  # просмотр списка и вывод
        spisok = self.cheque
        if len(spisok) == 0:
            self.input_window.setPlainText("                 Ваш заказ пуст")
            return
        lst = '######################\n    ВАШ ЧЕК   ' + str(datetime.now().strftime("%y.%w.%d %H:%M:%S\n"))
        count = 1
        for i in spisok:
            tmp = self.count.get(i).value()
            if tmp == 0:
                self.input_window.setPlainText("           Ошибка при заказе\nОбратите внимание на КОЛИЧЕСТВО")
                return
            lst += '\n#' + str(count) +'  ' + str(i) + ' - ' + str(tmp)
            count += 1
        lst += '\n\n' + '\n######################'
        self.input_window.setPlainText(lst)
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.resize(400,400)
    ex.show()
    sys.exit(app.exec())
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextBrowser, QPlainTextEdit


class Test(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setGeometry(500, 200, 800, 800)
        self.setWindowTitle('HTML редактор')   
        #Поле с вводом текста
        self.text = QPlainTextEdit(self)
        self.text.resize(750,350)
        self.text.move(25,10)
        #Отправить
        self.btn = QPushButton('Отправить', self)
        self.btn.resize(100, 30)
        self.btn.move(345, 365)
        self.btn.clicked.connect(self.pushed)
        #Поле вывода текста
        self.htmlText = QTextBrowser(self)
        self.htmlText.resize(750,350)
        self.htmlText.move(25,400)    
        self.htmlText.setOpenExternalLinks(True)
        
    def pushed(self):
        self.htmlText.setPlainText('') # Сброс текста в поле вывода
        text = self.text.toPlainText()
        self.htmlText.append(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Test()
    ex.show()
    sys.exit(app.exec())



# <!DOCTYPE HTML>
# <html>
#  <head>
#   <meta charset="utf-8">
#   <title>Тег H2</title>
#  </head>
#  <body>

#   <h1 align = "center">Lorem ipsum dolor sit amet</h1>
#   <p>Lorem ipsum dolor sit amet,<br>consectetuer adipiscing elit, sed diem 
#   nonummy nibh euismod tincidunt ut lacreet dolore magna 
#   aliguam erat volutpat.</p>

#   <h2>Ut wisis enim ad minim veniam</h2>
#   <p>Ut wisis enim ad minim veniam, quis nostrud exerci tution 
#   ullamcorper suscipit lobortis nisl ut aliquip ex ea 
#   commodo consequat.</p>

#  </body>
# </html>
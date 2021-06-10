import sys
from PyQt5.QtWidgets import QApplication, QBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QTableWidgetItem, QTableWidget, QHBoxLayout,QVBoxLayout,QComboBox
from PyQt5.QtGui import QColor
import csv
import sqlite3


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.loadUI()
        self.LoadBtn()
        

    def loadUI(self):
        self.setGeometry(0, 100, 1980, 980)
        self.lay = QHBoxLayout()
        self.table = QTableWidget()
        self.allBtn = QVBoxLayout()
        self.all = QVBoxLayout()
        self.lay.addWidget(self.table)
        self.all.addLayout(self.allBtn)
        self.all.addLayout(self.lay)
        self.setLayout(self.all)
        self.flagSave = 0 # флаг на существования кнопки Сохранить

    def LoadBtn(self):
        con = sqlite3.connect("films.db")
        cur = con.cursor()
        self.allGenres = {}
        genre =cur.execute("""SELECT * FROM genres""").fetchall()
        # Жанры
        for elem in genre:
            self.allGenres[elem[0]] = elem[1]
        self.btn_genre = QComboBox(self)
        self.btn_genre.addItem("Не важно")
        for i in self.allGenres:
            self.btn_genre.addItem(self.allGenres[i])
        # Длительность
        self.duration_lay = QHBoxLayout()
        self.duration1 =QLineEdit(self)
        self.duration2 =QLineEdit(self)
        self.text_dur1 = QLabel(self)
        self.text_dur2 = QLabel(self)
        self.text_dur1.setText('От')
        self.text_dur2.setText('До')
        self.duration_lay.addWidget(self.text_dur1)
        self.duration_lay.addWidget(self.duration1)
        self.duration_lay.addWidget(self.text_dur2)
        self.duration_lay.addWidget(self.duration2)

        # Год
        self.year_lay = QHBoxLayout()
        self.year1 =QLineEdit(self)
        self.year2 =QLineEdit(self)
        self.text_year1 = QLabel(self)
        self.text_year2 = QLabel(self)
        self.text_year1.setText('От')
        self.text_year2.setText('До')
        self.year_lay.addWidget(self.text_year1)
        self.year_lay.addWidget(self.year1)
        self.year_lay.addWidget(self.text_year2)
        self.year_lay.addWidget(self.year2)

        # Title
        self.title = QLineEdit(self)


        # найти
        self.btn_find = QPushButton("Найти",self)
        self.btn_find.clicked.connect(self.get_genre)

        # Заголовки
        self.label_Genre = QLabel(self)
        self.label_Genre.setText('Жанр')
        self.label_Duration = QLabel(self)
        self.label_Duration.setText('Длительность')
        self.label_Year = QLabel(self)
        self.label_Year.setText('Год')
        self.label_Title = QLabel(self)
        self.label_Title.setText('Название')
        
        # Добавляем кнопки
        self.allBtn.addWidget(self.label_Genre)
        self.allBtn.addWidget(self.btn_genre)
        self.allBtn.addWidget(self.label_Duration)
        self.allBtn.addLayout(self.duration_lay) 
        self.allBtn.addWidget(self.label_Year)
        self.allBtn.addLayout(self.year_lay)
        self.allBtn.addWidget(self.label_Title)
        self.allBtn.addWidget(self.title)
        self.allBtn.addWidget(self.btn_find)
        


    def loadTable(self):
        con = sqlite3.connect("films.db")
        cur = con.cursor()
        title = ["№","title","year","genre","Duration"]
        self.table.setColumnCount(len(title))
        self.table.setHorizontalHeaderLabels(title)
        self.table.setRowCount(0)
        
        result = cur.execute(f"""SELECT * FROM Films
        WHERE {self.genre_filter} {self.duration_filter} AND {self.year_filter} AND {self.title_filter} """).fetchall()
        for i, row in enumerate(result):
            self.table.setRowCount(self.table.rowCount() + 1)
            for j, elem in enumerate(row):
                if j == 3:
                    self.table.setItem(i,j, QTableWidgetItem(str(self.allGenres[elem])))
                else:
                    self.table.setItem(i,j, QTableWidgetItem(str(elem)))
        
        if self.flagSave == 0:
            self.flagSave = 1
            self.btn_save = QPushButton("Сохранить",self)
            self.btn_save.clicked.connect(self.change)
            self.allBtn.addWidget(self.btn_save)

            self.btn_add = QPushButton("Добавить",self)
            self.btn_add.clicked.connect(self.add)
            self.allBtn.addWidget(self.btn_add)

        self.table.resizeColumnsToContents()
        con.close() 

    
    def get_genre(self):
        duration_do = "0"
        duration_posle = "99999999"
        if self.duration1.text()!= "":
            duration_do = self.duration1.text()
        if self.duration2.text()!= "":
            duration_posle = self.duration2.text()
        if duration_do != '' and duration_posle != "":
            self.duration_filter = f"duration BETWEEN {duration_do} AND {duration_posle}"
        else:
            self.duration_filter = ""
        
        year_do = "0"
        year_posle = "2021"
        if self.year1.text()!= "":
            year_do = self.year1.text()
        if self.year2.text()!= "":
            year_posle = self.year2.text()
        if year_do != '' and year_posle != "":
            self.year_filter = f"year BETWEEN {year_do} AND {year_posle}"
        else:
            self.duration_filter = ""
        
        title = "%"
        if self.title.text()!= "":
            title = self.title.text()

        if title != "%":
            self.title_filter = f"title like '{title}_%'"
        else:
            self.title_filter = "title like '%'"

        
        genre = self.btn_genre.currentText()
        if genre == "Не важно":
            self.genre_filter = ""
            self.loadTable()
        else:
            for i in self.allGenres:
                if genre == self.allGenres[i]:
                    self.genre_filter = f"GENRE = {i} AND"
                    self.loadTable()
                    continue
    def change(self):
        con = sqlite3.connect("films.db")
        cur = con.cursor()
        column = self.table.columnCount()
        genre = ""
        for i in range(self.table.rowCount()):
            for j in self.allGenres:
                if self.table.item(i,3).text() == self.allGenres[j]:   
                    genre = f"{j}"
                        
            
            chan_bd = f"""UPDATE films set title = "{self.table.item(i,1).text()}", year = "{self.table.item(i,2).text()}", genre = "{genre}", duration = '{self.table.item(i,4).text()}' WHERE id = '{self.table.item(i,0).text()}'"""
            cur.execute(chan_bd)
            con.commit()
        con.close()

    def add(self):
        self.second_form = SecondForm(self)
        self.second_form.show()

class SecondForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Добавление')

        self.all = QVBoxLayout()
        self.btnTitleName = QLabel("Название")
        self.btnTitle = QLineEdit(self)
        self.all.addWidget(self.btnTitleName)
        self.all.addWidget(self.btnTitle)


        self.btnYearName = QLabel("Год")
        self.btnYear = QLineEdit(self)
        self.all.addWidget(self.btnYearName)
        self.all.addWidget(self.btnYear)

        con = sqlite3.connect("films.db")
        cur = con.cursor()
        self.allGenres = {}
        genre_bd =cur.execute("""SELECT * FROM genres""").fetchall()

        for elem in genre_bd:
            self.allGenres[elem[0]] = elem[1]
        self.btnGenre = QComboBox(self)
        for i in self.allGenres:
            self.btnGenre.addItem(self.allGenres[i])

        self.btnGenreName = QLabel("Жанр")
        
        self.all.addWidget(self.btnGenreName)
        self.all.addWidget(self.btnGenre)

        self.btnDurationName = QLabel("Длительность")
        self.btnDuration = QLineEdit(self)
        self.all.addWidget(self.btnDurationName)
        self.all.addWidget(self.btnDuration)

        self.btnAdd = QPushButton('Добавить')
        self.btnAdd.clicked.connect(self.add)
        self.all.addWidget(self.btnAdd)
        self.setLayout(self.all)

    def add(self):
        con = sqlite3.connect("films.db")
        cur = con.cursor()
        title = self.btnTitle.text()
        year = self.btnYear.text()
        for i in self.allGenres:
            if self.btnGenre.currentText() == self.allGenres[i]:
                genre = i
        duration = self.btnDuration.text()
        add_bd = f"""INSERT INTO films(title,year,genre,duration) VALUES('{title}','{year}','{genre}','{duration}')"""
        cur.execute(add_bd)
        con.commit()
        con.close()

app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
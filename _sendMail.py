import sys
import  module1 as m1
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5 import QtSql

# create Toolbar window and Main Window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setCentralWidget(Pencere())
        self.setUI()
    def setUI(self):
        toolbar = self.addToolBar("File")

        new = QAction("MailGönderme",self)
        toolbar.addAction(new)
        save = QAction("bilgiGüncelleme",self)
        toolbar.addAction(save)

        _print = QAction("kayitlikisibilgileri", self)
        toolbar.addAction(_print)

        toolbar.actionTriggered.connect(self.uygula)

        self.setWindowIcon(QIcon("mailIcon.png"))
        toolbar.setMovable(False)

        #self.setGeometry(400,100,350,500)
        self.setFixedHeight(500)
        self.setFixedWidth(400)
        self.setWindowTitle("meail gönderme")
        self.show()

    def uygula(self,q):
        if q.text() == "kayitlikisibilgileri":
            self.setCentralWidget(Customer())
        if q.text() == "MailGönderme":
            self.setCentralWidget(Pencere())
        if q.text() == "bilgiGüncelleme":
            self.setCentralWidget(Güncelleme())

#First window and send message
class Pencere(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    def init_ui(self):
        self.messageLabel = QtWidgets.QLabel("mesaj göndermek için bir adet mesaj giriniz ")
        self.message = QtWidgets.QTextEdit()


        self.messageButton = QtWidgets.QPushButton("mesajı gönder")

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.messageLabel)
        v_box.addWidget(self.message)
        v_box.addWidget(self.messageButton)

        self.messageButton.clicked.connect(self.messageSend)

        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch()
        h_box.addLayout(v_box)
        h_box.addStretch()
        self.setLayout(h_box)
    def messageSend(self):

        databasename = "mailDatabase.db"
        tablename = "userInformation"
        m1.sendMessageClass(self.message.toPlainText(),databasename,tablename)



#CustomerInformation
class Customer(QWidget):
    def __init__(self):
        super().__init__()
        self.setUI()
    def setUI(self):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('mailDatabase.db')

        if not db.open():
            QMessageBox.critical(self,'Hata','hata',QMessageBox.Cancel)

        self.model = QtSql.QSqlTableModel()
        self.model.setTable('customerInformation')
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.model.select()
        self.model.setHeaderData(0,Qt.Horizontal,'ID')
        self.model.setHeaderData(1,Qt.Horizontal,'USERNAME')

        view =QTableView()
        view.setModel(self.model)
        self.delrow = -1
        view.clicked.connect(self.satirAl)

        v_box =  QVBoxLayout()
        btn1 = QPushButton('Satır Ekle')
        btn2 = QPushButton("Satır Sil")
        print("bölge1")
        btn1.clicked.connect(self.satirEkle)
        btn2.clicked.connect(lambda :self.model.removeRow(view.currentIndex().row()))
        v_box.addWidget(view)
        v_box.addWidget(btn1)
        v_box.addWidget(btn2)
        widget = QWidget()
        self.setLayout(v_box)

    def satirEkle(self):
        self.model.insertRows(self.model.rowCount(), 1)

    def satirAl(self, i):
        print(i.row())
        self.delrow = i.row()



class Güncelleme(QWidget):
    def __init__(self):
        super().__init__()
        self.setUI()

    def setUI(self):
        self.usernameLabel = QtWidgets.QLabel("username :")
        self.usernameText = QtWidgets.QLineEdit()
        self.passwordLabel = QtWidgets.QLabel("password :")
        self.passwordText = QtWidgets.QLineEdit()

        self.updateBtn = QtWidgets.QPushButton("update")

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.usernameLabel)
        v_box.addWidget(self.usernameText)
        v_box.addWidget(self.passwordLabel)
        v_box.addWidget(self.passwordText)

        self.updateBtn.clicked.connect(self.updateClick)

        v_box.addWidget(self.updateBtn)
        v_box.addStretch()

        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch()
        h_box.addLayout(v_box)
        h_box.addStretch()

        self.setLayout(h_box)
    def updateClick(self):
        databasename = "mailDatabase.db"
        attributes1 = ("Update userInformation set _USERNAME = '{}' , _PASSWORD = '{}' where _ID = 1".format(self.usernameText.text(),self.passwordText.text()))

        m1.databaseUpdateOperation(databasename,attributes1)


def databaseCreate():
    databasename = "mailDatabase.db"
    tablename = "customerInformation"
    attributse = "(_ID INT,_USERNAME TEXT)"
    m1.database(databasename,tablename,attributse)
def main():
    app  = QApplication(sys.argv)
    mainwindow = MainWindow()
    database = databaseCreate()
    sys.exit(app.exec())
if __name__ == "__main__":
    main()

import sys
import sqlite3
import cryptocode
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox, QFormLayout, QLabel, QLineEdit, QPushButton, QWidget, QVBoxLayout, QMessageBox

class NewLoginDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(NewLoginDialog, self).__init__(parent)

        self.setFixedSize(300,150)
        self.setWindowTitle("Yeni Kullanıcı")
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.repassword = QLineEdit()
        newloginLayout = QFormLayout()
        newloginLayout.addRow("Kullanıcı Adı", self.username)
        newloginLayout.addRow("Şifre", self.password)
        newloginLayout.addRow("Şifre Kontrol", self.repassword)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.check)
        self.buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(newloginLayout)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def check(self):
        if str(self.password.text()) == str(self.repassword.text()): # girilen şifrelerin kontrolü
            kAdi=str(self.username.text())
            kSifre=str(self.password.text())
            baglanti = sqlite3.connect("database.db")
            self.cursor = baglanti.cursor()

            self.cursor.execute("Create Table If not exists kullanici (kullanıcı_adı TEXT,parola TEXT)")
            baglanti.commit()
            self.cursor.execute("INSERT INTO kullanici VALUES(?,?)",(kAdi,kSifre))
            baglanti.commit()
            baglanti.close()

            QMessageBox.information(self,'Bilgi','Kullanıcı başarılı bir şekilde oluşturuldu....')
            self.accept()
        else:
            QMessageBox.warning(self, 'Hata', 'Girdiğiniz şifreler eşleşmemektedir.')
            self.password.clear()
            self.repassword.clear()

    #geri dönüş yada programdan çıkış için gerekli parametreler
    def my_exception_hook(exctype, value, traceback):
        
        print(exctype, value, traceback)
        
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)


    sys._excepthook = sys.excepthook


    sys.excepthook = my_exception_hook

class LoginDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)
        #Kullanıcı adı ve parola kontrol penceresi
        self.setFixedSize(300,120)
        self.setWindowTitle("Kullanıcı Girişi")
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        loginLayout = QFormLayout()
        loginLayout.addRow("Kullanıcı Adı", self.username)
        loginLayout.addRow("Şifre", self.password)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.check)
        self.buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(loginLayout)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def check(self):
        
        baglanti = sqlite3.connect("database.db")
        self.cursor = baglanti.cursor()
        adi = self.username.text()
        par = self.password.text()
        self.cursor.execute("Select * From kullanici where kullanıcı_adı = ? and parola = ?",(adi,par))
        data = self.cursor.fetchall()
        baglanti.close()

        if len(data) != 0: 
            QMessageBox.information(self,'Bilgi','Giriş başarılı...')
            self.accept()
        else:
            QMessageBox.warning(self, 'Hata', 'Kullanıcı Adı veya Şifre hatası...')

    #geri dönüş yada programdan çıkış için gerekli parametreler
    def my_exception_hook(exctype, value, traceback):

        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    sys._excepthook = sys.excepthook
    sys.excepthook = my_exception_hook

#ana pencere 
class MainWindow(QtWidgets.QWidget):
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        siteNameLabel = QLabel('Site İsmi')
        siteUrlLabel = QLabel('Site URL')
        sitePasswordLabel = QLabel('Şifre')
        self.siteName = QLineEdit()
        self.siteUrl = QLineEdit()
        self.sitePassword = QLineEdit()
        self.temizle = QtWidgets.QPushButton("Temizle")
        self.ekle = QtWidgets.QPushButton("Yeni Kayıt")
        self.guncelle = QtWidgets.QPushButton("Kayıt Güncelle")
        self.sil = QtWidgets.QPushButton("Kayıt Sil")
        self.ara = QtWidgets.QPushButton("Kayıt Ara")

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(siteNameLabel, 1, 0)
        grid.addWidget(self.siteName, 1, 1)
        grid.addWidget(siteUrlLabel, 2, 0)
        grid.addWidget(self.siteUrl, 2, 1)
        grid.addWidget(sitePasswordLabel, 3, 0)
        grid.addWidget(self.sitePassword, 3, 1)
        grid.addWidget(self.ara,4,1)
        grid.addWidget(self.ekle,5,1)
        grid.addWidget(self.guncelle,6,1)
        grid.addWidget(self.sil,7,1)
        grid.addWidget(self.temizle,8,1)
        self.setFixedSize(500,300)
        self.setWindowTitle('Şifre Bankası')
        self.setLayout(grid)

        self.temizle.clicked.connect(self.click)
        self.ekle.clicked.connect(self.click)
        self.guncelle.clicked.connect(self.click)
        self.sil.clicked.connect(self.click)
        self.ara.clicked.connect(self.click)

        self.show()

    def click(self):
        sender = self.sender()
        siteA=str(self.siteName.text())
        siteU=str(self.siteUrl.text())
        siteP=str(self.sitePassword.text())

        baglanti = sqlite3.connect("database.db")
        self.cursor = baglanti.cursor()
        self.cursor.execute("Create Table If not exists siteBilgi (site_adı TEXT,site_URL TEXT,site_sifre TEXT)")
        baglanti.commit() 

        if sender.text() == "Kayıt Ara":
            if(siteA !=""):    
                try:
                    self.cursor.execute("Select * From siteBilgi where site_adı = ?",(siteA,))
                    data = self.cursor.fetchone()
                
                    baglanti.close()
                    if not data:
                        QMessageBox.information(self,'Bilgi','Aradığınız kayıt bulunamadı.')
                    else:
                        self.siteUrl.setText(str(data[1]))
                        self.sitePassword.setText(cryptocode.decrypt(str(data[2]), self.sifre) )
                except:
                    QMessageBox.warning(self,'Hata','Arama işlemi sırasında bir hata oluştu, lütfen tekrar deneyin.')
            else:
                QMessageBox.warning(self, 'Hata', 'Site adı boş geçilemez.')

        elif sender.text()=="Yeni Kayıt":
            if(siteA !="" and siteU !="" and siteP !=""):    
                try:
                    encoded = cryptocode.encrypt(siteP,self.sifre)

                    self.cursor.execute("INSERT INTO siteBilgi VALUES(?,?,?)",(siteA,siteU,encoded))
                    baglanti.commit()
                    baglanti.close()
                    QMessageBox.information(self,'Bilgi','Site bilgileri başarılı bir şekilde kayıt edildi.')
                    self.siteName.clear()
                    self.siteUrl.clear()
                    self.sitePassword.clear()
                except:
                    QMessageBox.warning(self,'Hata','Kayıt işlemi sırasında bir hata oluştu, lütfen tekrar deneyin.')
            else:
                QMessageBox.warning(
                self, 'Hata', 'Lütfen tüm alanları doldurun...')
            
        elif sender.text()=="Kayıt Güncelle":
            if(siteA !="" and siteU !="" and siteP !=""):    
                try:

                    encoded = cryptocode.encrypt(siteP,self.sifre)

                    self.cursor.execute("UPDATE siteBilgi SET site_URL=?  where site_adı=?",(siteU,siteA))
                    baglanti.commit()
                    self.cursor.execute("UPDATE siteBilgi SET site_sifre=?  where site_adı=?",(encoded,siteA))
                    baglanti.commit()
                    baglanti.close()
                    QMessageBox.information(self,'Bilgi','Site başarılı bir şekilde güncellendi.')
                    self.siteName.clear()
                    self.siteUrl.clear()
                    self.sitePassword.clear()
                except:
                    QMessageBox.warning(self,'Hata','Güncelleme işlemi sırasında bir hata oluştu, lütfen tekrar deneyin.')
            
            else:
                QMessageBox.warning(
                self, 'Hata', 'Lütfen tüm alanları doldurun...')
        elif sender.text()=="Kayıt Sil":
            
            if(siteA !="" and siteU !="" and siteP !=""):    
                
                try: 

                    ask_dialog = QMessageBox()
                    ask_dialog.setWindowTitle("Dikkat")
                    ask_dialog.setText("Site bilgilerini silmek istediğinizden emin misiniz?")
                    ask_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                    ask_dialog.setDefaultButton(QMessageBox.No)
                    ask_dialog.setIcon(QMessageBox.Question)
                    if ask_dialog.exec() == QMessageBox.Yes:
      
                        self.cursor.execute("DELETE From siteBilgi  where site_adı=?",(siteA,))
                        baglanti.commit()
                        baglanti.close()

                    QMessageBox.information(self,'Bilgi','Site başarılı bir şekilde silindi.')
                    self.siteName.clear()
                    self.siteUrl.clear()
                    self.sitePassword.clear()
                except:
                    QMessageBox.warning(self,'Hata','Silme işlemi sırasında bir hata oluştu, lütfen tekrar deneyin.')
            
            else:
                QMessageBox.warning(
                self, 'Hata', 'Lütfen tüm alanları kontrol edin...')
        else:
            self.siteName.clear()
            self.siteUrl.clear()
            self.sitePassword.clear()
            
    def setUsername(self, username,password):
        # Diğer nesneden username ve şifrenin dışarıdan alınması
        self.kAdi = username
        self.sifre = password
        
        


if __name__ == "__main__":
    app = QApplication(sys.argv)

    baglanti = sqlite3.connect("database.db")
        
    cursor = baglanti.cursor()

    cursor.execute("Create Table If not exists kullanici (kullanıcı_adı TEXT,parola TEXT)")       
    baglanti.commit()

    cursor.execute("""Select * From kullanici""")
    veri=cursor.fetchall()
    baglanti.close()
   
    #veri tabanı kontrolü sonrasında kullanıcı olmaması durumunda yeni kullanıcı eklemek için ilgili arayüz çağrılır.
    if not veri:
        newLogin=NewLoginDialog()
        if not newLogin.exec_():
            sys.exit(-1)
    
    #veri tabanında kullanıcı varsa kullanıcı girişinin yapılabilmesi çin pencere çağrılır.
    login = LoginDialog()
    if not login.exec_(): 
        sys.exit(-1)         

    #kullanıcı adı ve şifresi doğru ise ana pencere çağrılır.
    main = MainWindow()

    # ana pencereye kullanıcı adı ve şifre gönderilir.
    main.setUsername(login.username.text(),login.password.text())
    main.show()

    sys.exit(app.exec_())
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QRadioButton, QButtonGroup
from PyQt5.QtCore import Qt

class NewWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(700,300,500,500)
        self.Button1 = QRadioButton("Visa",self)
        self.Button2 = QRadioButton("MasterCard", self)
        self.Button3 = QRadioButton("SuperCard", self)
        self.Button4 = QRadioButton("Online", self)
        self.Button5 = QRadioButton("Cash", self)
        self.setWindowTitle("My second GUI")

        #button group declarations

        self.ButtonGroup1 = QButtonGroup(self)
        self.ButtonGroup1 = QButtonGroup(self)
        self.ButtonGroup1 = QButtonGroup(self)
        self.ButtonGroup2 = QButtonGroup(self)
        self.ButtonGroup2 = QButtonGroup(self)

        self.initUI()

    def initUI(self):
        self.Button1.setGeometry(5,0,300,50)
        self.Button2.setGeometry(5, 50, 300, 50)
        self.Button3.setGeometry(5, 100, 300, 50)
        self.Button4.setGeometry(5, 150, 300, 50)
        self.Button5.setGeometry(5, 200, 300, 50)

        self.setStyleSheet("QRadioButton{"
                                        "font-family: Arial;"
                                        "font-size: 30px;"
                                        "padding : 10px;"
                                        "}")
        self.ButtonGroup1.addButton(self.Button1)
        self.ButtonGroup1.addButton(self.Button2)
        self.ButtonGroup1.addButton(self.Button3)
        self.ButtonGroup2.addButton(self.Button4)
        self.ButtonGroup2.addButton(self.Button5)


        self.Button1.toggled.connect(self.ischanged)
        self.Button2.toggled.connect(self.ischanged)
        self.Button3.toggled.connect(self.ischanged)
        self.Button4.toggled.connect(self.ischanged)
        self.Button5.toggled.connect(self.ischanged)

    def ischanged(self,state):
        radio_button = self.sender()
        if radio_button.isChecked():
            print(f"{radio_button.text()} is selected")

def main():
    app = QApplication(sys.argv)
    window = NewWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
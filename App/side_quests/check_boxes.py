import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox
from PyQt5.QtCore import Qt

class NewWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(700,300,500,500)
        self.checkbox = QCheckBox("Do you like food?",self)
        self.setWindowTitle("My second GUI")
        self.initUI()


    def initUI(self):

        self.checkbox.setStyleSheet("font-size : 30px;"
                                    "font-family : Arial")

        self.checkbox.setGeometry(10,10,500,75)
        self.checkbox.setChecked(False)
        self.checkbox.stateChanged.connect(self.ischanged)



    def ischanged(self,state):
        if state == Qt.Checked:
            print("You like food")
        else:
            print("You donot like food!")

def main():
    app = QApplication(sys.argv)
    window = NewWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
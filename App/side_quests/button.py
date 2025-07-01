import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QLabel, QWidget, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class NewWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(700,300,500,500)
        self.setWindowTitle("My second GUI")
        self.Button = QPushButton("Click Here",self)
        self.label = QLabel("Hello" , self)
        self.label.setStyleSheet("font-size : 30px")
        
        self.initUI()

    def initUI(self):
        self.Button.setGeometry(150,200,200,100)
        self.Button.setStyleSheet("font-size: 30px")
        self.Button.clicked.connect(self.on_click)

        self.label.setGeometry(150,280,200,100)

    def on_click(self):
        print("Button Clicked")
        self.Button.setText("Clicked")
        self.Button.setDisabled(True)
        self.label.setText("Button clicked")



def main():
    app = QApplication(sys.argv)
    window = NewWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()



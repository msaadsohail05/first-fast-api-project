import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class NewWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(700,300,500,500)
        self.setWindowTitle("My second GUI")
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        label1 = QLabel("A#",self)
        label2 = QLabel("B#", self)
        label3 = QLabel("C#", self)
        label4 = QLabel("D#", self)
        label5 = QLabel("E#", self)

        #Allignment
        label1.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        label2.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        label3.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        label4.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        label5.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        label1.setStyleSheet("background-color: blue")
        label2.setStyleSheet("background-color: red")
        label3.setStyleSheet("background-color: yellow")
        label4.setStyleSheet("background-color: green")
        label5.setStyleSheet("background-color: pink")

        grid = QGridLayout()
        grid.addWidget(label1,0,0)
        grid.addWidget(label2, 0,1)
        grid.addWidget(label3, 1,0)
        grid.addWidget(label4, 1,1)
        grid.addWidget(label5, 2,0)

        central_widget.setLayout(grid)


def main():
    app = QApplication(sys.argv)
    window = NewWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()


# #magic methods
#
# class Book:
#     def __init__(self,t,a,n):
#         self._title = t
#         self._author = a
#         self._numPages = n
#
#     @property
#     def title(self):
#         return f"The title of the book is {self._title}"
#
#     @property
#     def author(self):
#         return f"The auhtor of this book is {self._author}"
#
#     @title.setter
#     def SetTitle(self,t):
#         if t == " ":
#             print("No input given")
#         else:
#             self._title = t
#
#     @author.setter
#     def SetAuthor(self,a):
#         if a == " ":
#             print("No input given")
#         else:
#             self._author = a
#
#     def __str__(self):
#         return f"{self.title} by {self.author} consisting of {self.numPages} pages."
#
#     def __eq__(self, other):
#         return self.numPages == other.numPages
#
#     def __lt__(self, other):
#         return self.numPages < other.numPages
#
#     def __gt__(self, other):
#         return self.numPages > other.numPages
#
#     def __contains__(self, item):
#         return item in self.title or item in self.author
#
#     def __getitem__(self, key):
#         if key == 'title':
#             return self.title
#         elif key == 'author':
#             return self.author
#         elif key == 'numPages':
#             return self.numPages
#         else:
#             return f"The key {key} was not found!"
#
#
# book1 = Book("1984", "George Orwell", 328)
# book2 = Book("Animal Farm", "George Orwell", 112)
#
#
#
# # print(book1)                     # Uses __str__
# # print(book1 > book2)            # True
# # print(book2 < book1)            # True
# # print(book1 == book2)           # False
# # print("Orwell" in book1)        # True
# # print("Farm" in book1)          # False
# # print(book1["title"])
#
# import json
# file_path = "file1.json"
# employee = {
#     "name" : "saad",
#     "age" : 20,
#     "eligibility"  : True
# }
# with open(file_path,'w') as file:
#     json.dump(employee,file)
#     print(f"data : {employee}")
#
# import requests
#
# base_url = "https://pokeapi.co/api/v2/"
#
# def get_pokemon_info(name):
#     url = f"{base_url}/pokemon/{name}"
#     data = requests.get(url)
#     if data.status_code == 200:
#         pData = data.json()
#         return pData
#     else:
#         print(f"Failed to retrive data {data.status_code}")
#
#
# name = input("Enter the name of the pokemon: ")
# returnData = get_pokemon_info(name)
#
# if name:
#     print(f"ID: {returnData["id"]}")
#     print(f"Name : {returnData["name"].capitalize()}")

import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QLabel
from PyQt5.QtGui import QIcon,QFont,QPixmap
from PyQt5.QtCore import Qt



class NewWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(700,300,500,500)
        self.setWindowTitle("My first GUI")
        self.setGeometry(0,0,500,500)
        self.setWindowIcon(QIcon("dg.jpg"))
        label = QLabel("Hello",self)

        self.setFont(QFont("Arial" , 50))
        label.setGeometry(0,0,500,75)
        label.setStyleSheet("color: Blue;"
                            "background-color: grey")
        label.setAlignment(Qt.AlignHCenter)
        label1 = QLabel(self)
        label1.setGeometry(100,100,250,250)
        mypixmap = QPixmap("dg.jpg")

        label1.setPixmap(mypixmap)
        label1.setScaledContents(True)

        label1.setGeometry((self.width() - label1.width() )//2,(self.height() - label1.height() )//2,label1.width(),label1.height())

def main():
    app = QApplication(sys.argv)
    window = NewWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
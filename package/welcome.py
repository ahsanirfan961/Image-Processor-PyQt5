from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from package.menu import Menu
from package.data import widget

# Welcome
class Welcome(QMainWindow):
    
    def __init__(self):
        super(Welcome, self).__init__()
        loadUi("assets/ui/welcome.ui", self)
        self.start.clicked.connect(self.goto_menu)
         
    def goto_menu(self):
        menu = Menu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

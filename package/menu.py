from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from package.data import widget
from package.negative import Negative
from package.brightness import Brightness
from package.burkes import Burkes
from package.gabor import Gabor
from package.sobel import Sobel
from package.resize import Resize

# Welcome
class Menu(QMainWindow):
    
    def __init__(self):
        super(Menu, self).__init__()
        loadUi("assets/ui/menu.ui", self)
        self.negative.clicked.connect(self.goto_negative)
        self.gabor.clicked.connect(self.goto_gabor)
        self.brightness.clicked.connect(self.goto_brightness)
        self.burkes.clicked.connect(self.goto_burkes)
        self.sobel.clicked.connect(self.goto_sobel)
        self.resize_btn.clicked.connect(self.goto_resize)
        
    def goto_negative(self):
        process = Negative()
        widget.addWidget(process)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goto_gabor(self):
        process = Gabor()
        widget.addWidget(process)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goto_brightness(self):
        process = Brightness()
        widget.addWidget(process)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goto_burkes(self):
        process = Burkes()
        widget.addWidget(process)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goto_sobel(self):
        process = Sobel()
        widget.addWidget(process)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goto_resize(self):
        process = Resize()
        widget.addWidget(process)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from package.data import widget
import os, threading
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap


# Welcome
class Process(QMainWindow):
    
    def __init__(self):
        super(Process, self).__init__()
        loadUi("assets/ui/process.ui", self)
        self.back.clicked.connect(self.go_back)
        self.selectimage.clicked.connect(self.select_image)
        self.applyfilter.clicked.connect(self.apply_filter)
        self.open.clicked.connect(self.openImage)
        self.open.setEnabled(False)
         
    def select_image(self):
        options = QFileDialog.Options()
        self.fileName, _ = QFileDialog.getOpenFileName(self, 'Select an image', '', 'JPEG IMG (*.jpg)', options=options)
        if self.fileName:
            # Get the filename without the path
            base_name = os.path.basename(self.fileName)
            # Copy the file to the specified directory
            self.save_path = "C:/Image Processor/" + base_name
            os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
            # Display the filename without the path
            self.imagename.setText("Selected Image: " + base_name)
            # Display the image
            pixmap = QPixmap(self.fileName)
            self.image.setPixmap(pixmap.scaled(400, 400, aspectRatioMode=True))
            self.image.setText('')
            self.applyfilter.setEnabled(True)
            self.open.setEnabled(False)

    def go_back(self):
        widget.removeWidget(widget.currentWidget())
    
    def apply_filter(self):
        if not hasattr(self, 'fileName'):
            self.result.setStyleSheet('color: red')
            self.result.setText('No file selected!')
            return
        self.result.setText('Applying filter...')
        if self.filter():
            self.result.setStyleSheet('color: green')
            self.result.setText('Saved at: ' + self.save_path)
            self.open.setEnabled(True)
            self.applyfilter.setEnabled(False)
        else:
            self.result.setStyleSheet('color: red')
            self.result.setText(self.result.text()+'Error applying filter!')
    
    def openImage(self):
        if hasattr(self, 'fileName'):
            try:
                os.startfile(self.save_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Warning", "No image selected!")
    
    def filter(self):
        pass
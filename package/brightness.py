from package.process import Process
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QSlider
from PyQt5.QtCore import Qt
import numpy as np
from package.gaussian import gaussian_filter
from PIL import Image

class Brightness(Process):
       
    def __init__(self):
        super(Brightness, self).__init__()
        self.filter_name.setText("Change Brightness")

        self.resize_label = QLabel("Brightness Value:", self.frame)
        self.resize_label.setGeometry(700, 190, 120, 16)

        self.slider = QSlider(Qt.Horizontal, self.frame)
        self.slider.setGeometry(680, 220, 180, 30)

        self.slider.setMinimum(-255)
        self.slider.setMaximum(255)
        self.slider.setValue(0)
        self.slider.setTickInterval(15)
        self.slider.setTickPosition(QSlider.TicksAbove)

        self.b_value = QLabel("0", self.frame)
        self.b_value.setGeometry(765, 260, 120, 16)

        self.slider.valueChanged.connect(self.update_brightness)

    def update_brightness(self):
        self.b_value.setText(str(self.slider.value()))
        self.applyfilter.setEnabled(True)
    
    def filter(self):
        with Image.open(self.fileName) as img:
            # Change brightness to 100
            if img.width != img.height:
                self.result.setText('Image must be square!')
                return False
            brigt_img = self.change_brightness(img, self.slider.value())
            brigt_img.save(self.save_path, format="jpeg")
            pixmap = QPixmap(self.save_path)
            self.image.setPixmap(pixmap.scaled(400, 400, aspectRatioMode=True))
        return True

    def change_brightness(self, img: Image, level: float) -> Image:
        """
        Change the brightness of a PIL Image to a given level.
        """

        def brightness(c: int) -> float:
            """
            Fundamental Transformation/Operation that'll be performed on
            every bit.
            """
            return level + c 

        if not -255.0 <= level <= 255.0:
            raise ValueError("level must be between -255.0 (black) and 255.0 (white)")
        return img.point(brightness)


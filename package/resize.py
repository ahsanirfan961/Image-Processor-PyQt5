from package.process import Process
from cv2 import imread, imwrite
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QLineEdit
import numpy as np

class Resize(Process):
        
    def __init__(self):
        super(Resize, self).__init__()
        self.filter_name.setText("Resize Image")

        self.resize_label = QLabel("To Resize", self.frame)
        self.resize_label.setGeometry(700, 190, 70, 16)

        self.width_input = QLineEdit(self.frame)
        self.width_input.setGeometry(700, 220, 120, 20)
        self.width_input.setStyleSheet("background-color: white;")
        self.width_input.setPlaceholderText("Enter Width")

        self.height_input = QLineEdit(self.frame)
        self.height_input.setGeometry(700, 250, 120, 20)
        self.height_input.setStyleSheet("background-color: white;")
        self.height_input.setPlaceholderText("Enter Height")
        
    
    def filter(self):
        img = imread(self.fileName, 1)
        if img.shape[0] != img.shape[1]:
            self.result.setText('Image must be square!')
            return False
        if not self.width_input.text().isdigit() or not self.height_input.text().isdigit():
            self.result.setText('Invalid width or height!')
            return False
        dst_w, dst_h = int(self.width_input.text()), int(self.height_input.text())
        n = NearestNeighbour(img, dst_w, dst_h)
        n.process()
        imwrite(self.save_path, n.output)
        pixmap = QPixmap(self.save_path)
        self.image.setPixmap(pixmap.scaled(400, 400, aspectRatioMode=True))
        return True
        

class NearestNeighbour:
    """
    Simplest and fastest version of image resizing.
    Source: https://en.wikipedia.org/wiki/Nearest-neighbor_interpolation
    """

    def __init__(self, img, dst_width: int, dst_height: int):
        if dst_width < 0 or dst_height < 0:
            raise ValueError("Destination width/height should be > 0")

        self.img = img
        self.src_w = img.shape[1]
        self.src_h = img.shape[0]
        self.dst_w = dst_width
        self.dst_h = dst_height

        self.ratio_x = self.src_w / self.dst_w
        self.ratio_y = self.src_h / self.dst_h

        self.output = self.output_img = (
            np.ones((self.dst_h, self.dst_w, 3), np.uint8) * 255
        )

    def process(self):
        for i in range(self.dst_h):
            for j in range(self.dst_w):
                self.output[i][j] = self.img[self.get_y(i)][self.get_x(j)]

    def get_x(self, x: int) -> int:
        """
        Get parent X coordinate for destination X
        :param x: Destination X coordinate
        :return: Parent X coordinate based on `x ratio`
        >>> nn = NearestNeighbour(imread("digital_image_processing/image_data/lena.jpg",
        ...                              1), 100, 100)
        >>> nn.ratio_x = 0.5
        >>> nn.get_x(4)
        2
        """
        return int(self.ratio_x * x)

    def get_y(self, y: int) -> int:
        """
        Get parent Y coordinate for destination Y
        :param y: Destination X coordinate
        :return: Parent X coordinate based on `y ratio`
        >>> nn = NearestNeighbour(imread("digital_image_processing/image_data/lena.jpg",
        ...                              1), 100, 100)
        >>> nn.ratio_y = 0.5
        >>> nn.get_y(4)
        2
        """
        return int(self.ratio_y * y)


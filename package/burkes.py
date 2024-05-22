from package.process import Process
from cv2 import imread, imwrite
from PyQt5.QtGui import QPixmap
import numpy as np

class Burkes(Process):
       
    def __init__(self):
        super(Burkes, self).__init__()
        self.filter_name.setText('Burkes Filter')
        self.threshold = 128
    
    def filter(self):
        img = imread(self.fileName)
        if img.shape[0] != img.shape[1]:
            self.result.setText('Image must be square!')
            return False
        img = self.process(img, self.threshold)
        imwrite(self.save_path, img)
        pixmap = QPixmap(self.save_path)
        self.image.setPixmap(pixmap.scaled(400, 400, aspectRatioMode=True))
        return True
    
    def process(self, input_img, threshold: int):
        self.min_threshold = 0
        # max greyscale value for #FFFFFF
        self.max_threshold = int(self.get_greyscale(255, 255, 255))

        if not self.min_threshold < threshold < self.max_threshold:
            msg = f"Factor value should be from 0 to {self.max_threshold}"
            raise ValueError(msg)

        self.input_img = input_img
        self.threshold = threshold
        self.width, self.height = self.input_img.shape[1], self.input_img.shape[0]

        # error table size (+4 columns and +1 row) greater than input image because of
        # lack of if statements
        self.error_table = [
            [0 for _ in range(self.height + 4)] for __ in range(self.width + 1)
        ]
        self.output_img = np.ones((self.width, self.height, 3), np.uint8) * 255

        for y in range(self.height):
            for x in range(self.width):
                greyscale = int(self.get_greyscale(*self.input_img[y][x]))
                if self.threshold > greyscale + self.error_table[y][x]:
                    self.output_img[y][x] = (0, 0, 0)
                    current_error = greyscale + self.error_table[y][x]
                else:
                    self.output_img[y][x] = (255, 255, 255)
                    current_error = greyscale + self.error_table[y][x] - 255
                """
                Burkes error propagation (`*` is current pixel):

                                 *          8/32        4/32
                2/32    4/32    8/32    4/32    2/32
                """
                self.error_table[y][x + 1] += int(8 / 32 * current_error)
                self.error_table[y][x + 2] += int(4 / 32 * current_error)
                self.error_table[y + 1][x] += int(8 / 32 * current_error)
                self.error_table[y + 1][x + 1] += int(4 / 32 * current_error)
                self.error_table[y + 1][x + 2] += int(2 / 32 * current_error)
                self.error_table[y + 1][x - 1] += int(4 / 32 * current_error)
                self.error_table[y + 1][x - 2] += int(2 / 32 * current_error)
        return self.output_img
        
        
    def get_greyscale(cls, blue: int, green: int, red: int) -> float:
        """
        >>> Burkes.get_greyscale(3, 4, 5)
        4.185
        >>> Burkes.get_greyscale(0, 0, 0)
        0.0
        >>> Burkes.get_greyscale(255, 255, 255)
        255.0
        """
        """
        Formula from https://en.wikipedia.org/wiki/HSL_and_HSV
        cf Lightness section, and Fig 13c.
        We use the first of four possible.
        """
        return 0.114 * blue + 0.587 * green + 0.299 * red


from package.process import Process
from cv2 import imread, imwrite
from PyQt5.QtGui import QPixmap
PI = 180
import numpy as np
from package.convolve import img_convolve

class Sobel(Process):
       
    def __init__(self):
        super(Sobel, self).__init__()
        self.filter_name.setText("Sobel Filter")
        
    
    def filter(self):
        img = imread(self.fileName, 0)
        if img.shape[0] != img.shape[1]:
            self.result.setText('Image must be square!')
            return False
        img, theta = self.sobel_filter(img)
        imwrite(self.save_path, img)
        pixmap = QPixmap(self.save_path)
        self.image.setPixmap(pixmap.scaled(400, 400, aspectRatioMode=True))
        return True
        
    def sobel_filter(self, image):
        kernel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        kernel_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])

        dst_x = np.abs(img_convolve(image, kernel_x))
        dst_y = np.abs(img_convolve(image, kernel_y))
        # modify the pix within [0, 255]
        dst_x = dst_x * 255 / np.max(dst_x)
        dst_y = dst_y * 255 / np.max(dst_y)

        dst_xy = np.sqrt((np.square(dst_x)) + (np.square(dst_y)))
        dst_xy = dst_xy * 255 / np.max(dst_xy)
        dst = dst_xy.astype(np.uint8)

        theta = np.arctan2(dst_y, dst_x)
        return dst, theta

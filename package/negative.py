from package.process import Process
from cv2 import imread, imwrite
from PyQt5.QtGui import QPixmap

class Negative(Process):
       
    def __init__(self):
        super(Negative, self).__init__()
        self.filter_name.setText("Convert to Negative")
        
    
    def filter(self):
        img = imread(self.fileName)
        if img.shape[0] != img.shape[1]:
            self.result.setText('Image must be square!')
            return False
        img = Negative.convert_to_negative(img)
        imwrite(self.save_path, img)
        pixmap = QPixmap(self.save_path)
        self.image.setPixmap(pixmap.scaled(400, 400, aspectRatioMode=True))
        return True
        
        
    def convert_to_negative(img):
        # getting number of pixels in the image
        pixel_h, pixel_v = img.shape[0], img.shape[1]

        # converting each pixel's color to its negative
        for i in range(pixel_h):
            for j in range(pixel_v):
                img[i][j] = [255, 255, 255] - img[i][j]

        return img


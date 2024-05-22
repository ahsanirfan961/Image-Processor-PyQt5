from package.process import Process
import numpy as np
from cv2 import COLOR_BGR2GRAY, CV_8UC3, cvtColor, filter2D, imread, imwrite
from PyQt5.QtWidgets import QLabel, QLineEdit, QCheckBox
from PyQt5.QtGui import QPixmap

class Gabor(Process):
        
    def __init__(self):
        super(Gabor, self).__init__()
        self.filter_name.setText("Gabor Filter")

        self.resize_label = QLabel("Options", self.frame)
        self.resize_label.setGeometry(700, 190, 70, 16)

        self.ksize_input = QLineEdit(self.frame)
        self.ksize_input.setGeometry(700, 220, 180, 20)
        self.ksize_input.setStyleSheet("background-color: white;")
        self.ksize_input.setPlaceholderText("Enter Kernal Size")

        self.sigma_input = QLineEdit(self.frame)
        self.sigma_input.setGeometry(700, 250, 180, 20)
        self.sigma_input.setStyleSheet("background-color: white;")
        self.sigma_input.setPlaceholderText("Enter Standard Deviation")

        self.lambda_input = QLineEdit(self.frame)
        self.lambda_input.setGeometry(700, 280, 180, 20)
        self.lambda_input.setStyleSheet("background-color: white;")
        self.lambda_input.setPlaceholderText("Enter size of wavelength")

        self.gamma_input = QLineEdit(self.frame)
        self.gamma_input.setGeometry(700, 310, 180, 20)
        self.gamma_input.setStyleSheet("background-color: white;")
        self.gamma_input.setPlaceholderText("Enter Gamma")

        self.psi_input = QLineEdit(self.frame)
        self.psi_input.setGeometry(700, 340, 180, 20)
        self.psi_input.setStyleSheet("background-color: white;")
        self.psi_input.setPlaceholderText("Enter Phase Offset")

        self.default_checkbox = QCheckBox("Use Default Values", self.frame)
        self.default_checkbox.setGeometry(700, 370, 180, 20)
        self.default_checkbox.stateChanged.connect(self.useDefaultValues)
    
    def useDefaultValues(self):
        if self.default_checkbox.isChecked():
            self.ksize_input.setText("10")
            self.sigma_input.setText("8")
            self.lambda_input.setText("10")
            self.gamma_input.setText("0")
            self.psi_input.setText("0")
            self.ksize_input.setDisabled(True)
            self.sigma_input.setDisabled(True)
            self.lambda_input.setDisabled(True)
            self.gamma_input.setDisabled(True)
            self.psi_input.setDisabled(True)
        else:
            self.ksize_input.setText("")
            self.sigma_input.setText("")
            self.lambda_input.setText("")
            self.gamma_input.setText("")
            self.psi_input.setText("")
            self.ksize_input.setDisabled(False)
            self.sigma_input.setDisabled(False)
            self.lambda_input.setDisabled(False)
            self.gamma_input.setDisabled(False)
            self.psi_input.setDisabled(False)

    def validate(self):
        if not self.default_checkbox.isChecked():
            if not self.ksize_input.text().isdigit() or not self.sigma_input.text().isdigit() or not self.lambda_input.text().isdigit() or not self.gamma_input.text().isdigit() or not self.psi_input.text().isdigit():
                self.result.setText('Invalid input!')
                return False
        return True

    def filter(self):
        if self.validate():
            img = imread(self.fileName)
            if img.shape[0] != img.shape[1]:
                self.result.setText('Image must be square!')
                return False
            gray = cvtColor(img, COLOR_BGR2GRAY)

            ksize = int(self.ksize_input.text()) 
            sigma = int(self.sigma_input.text())
            lambd = int(self.lambda_input.text())
            gamma = int(self.gamma_input.text())
            psi = int(self.psi_input.text())

            # Apply multiple Kernel to detect edges
            out = np.zeros(gray.shape[:2])
            for theta in [0, 30, 60, 90, 120, 150]:
                """
                ksize = 10  It determines the accuracy of detecting the pattern
                            Too small can result in loss of information
                            Too large can result in a lot of noise

                sigma = 8   It represents the standard deviation of the Gaussian function
                            It sets the width of the detected pattern
                            Too large increases the spread of the filter
                            Too small can result in loss of information

                lambd = 10  It represents the wavelength of the sinusoidal function
                            Shorter wavelength captures small details
                            Longer wavelength captures broader picture
                            Too large or small can result in loss of information

                gamma = 0   It defines the shape of the filter
                            A value of 0.5 results in a circular shape
                            A value of 1 results in an elliptical shape
                            A value of 2 results in a rectangular shape

                psi = 0     It represents the phase offset of the sinusoidal function
                            It sets the starting point of the filter
                            It can be used to shift the filter to detect different patterns
                """

                kernel_10 = self.gabor_filter_kernel(ksize, sigma, theta, lambd, gamma, psi)
                out += filter2D(gray, CV_8UC3, kernel_10)
            out = out / out.max() * 255
            out = out.astype(np.uint8)
            imwrite(self.save_path, out)
            pixmap = QPixmap(self.save_path)
            self.image.setPixmap(pixmap.scaled(400, 400, aspectRatioMode=True))
            return True
        return False
        
        
    def gabor_filter_kernel(self,
        ksize: int, sigma: int, theta: int, lambd: int, gamma: int, psi: int
    ) -> np.ndarray:
        """
        :param ksize:   The kernelsize of the convolutional filter (ksize x ksize)
        :param sigma:   standard deviation of the gaussian bell curve
        :param theta:   The orientation of the normal to the parallel stripes
                        of Gabor function.
        :param lambd:   Wavelength of the sinusoidal component.
        :param gamma:   The spatial aspect ratio and specifies the ellipticity
                        of the support of Gabor function.
        :param psi:     The phase offset of the sinusoidal function.

        >>> gabor_filter_kernel(3, 8, 0, 10, 0, 0).tolist()
        [[0.8027212023735046, 1.0, 0.8027212023735046], [0.8027212023735046, 1.0, \
    0.8027212023735046], [0.8027212023735046, 1.0, 0.8027212023735046]]

        """

        # prepare kernel
        # the kernel size have to be odd
        if (ksize % 2) == 0:
            ksize = ksize + 1
        gabor = np.zeros((ksize, ksize), dtype=np.float32)

        # each value
        for y in range(ksize):
            for x in range(ksize):
                # distance from center
                px = x - ksize // 2
                py = y - ksize // 2

                # degree to radiant
                _theta = theta / 180 * np.pi
                cos_theta = np.cos(_theta)
                sin_theta = np.sin(_theta)

                # get kernel x
                _x = cos_theta * px + sin_theta * py

                # get kernel y
                _y = -sin_theta * px + cos_theta * py

                # fill kernel
                gabor[y, x] = np.exp(-(_x**2 + gamma**2 * _y**2) / (2 * sigma**2)) * np.cos(
                    2 * np.pi * _x / lambd + psi
                )

        return gabor


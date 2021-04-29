from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import image as img
import numpy as np
from numpy.fft import ifft2, fft2, fftshift
import cmath
from PyQt5.QtGui import QImage, QPixmap, qRgb

gray_color_table = [qRgb(i, i, i) for i in range(256)]

def toQImage(im, copy=False):
    if im is None:
        return QImage()

    im = np.require(im, np.uint8, 'C')
    if im.dtype == np.uint8:
        if len(im.shape) == 2:
            qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_Indexed8)
            qim.setColorTable(gray_color_table)
            return qim.copy() if copy else qim

        elif len(im.shape) == 3:
            if im.shape[2] == 3:
                qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_RGB888)
                return qim.copy() if copy else qim
            elif im.shape[2] == 4:
                qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_ARGB32)
                return qim.copy() if copy else qim

class image(object):
    def __init__(self, inputImg, outputImg, outputSelector, imagePath):
        self.inputImg = inputImg
        self.outputImg = outputImg
        self.outputSelector = outputSelector
        self.imagePath = imagePath
        image = img.imread(imagePath, 0)
        fourier_coefficients = fft2(image)
        fshift = fftshift(fourier_coefficients)
        self.components = {}
        self.components['amplitude'] = np.abs(fshift)
        self.components['phase'] = np.angle(fshift) 
        self.components['real'] = np.real(fshift)
        self.components['imaginary'] = np.imag(fshift)
        self.display()

    def display(self):
        self.inputImg.setPixmap(QtGui.QPixmap(self.imagePath))
        self.outputImg.setPixmap(QtGui.QPixmap(toQImage(self.components[self.outputSelector.currentText()])))

class component(object):
    def __init__(self, img_selector, component_selector, ratio):
        self.ratio = ratio
        self.img_selector = img_selector
        self.component_selector = component_selector


# class Mixer(object):
#     def __init__(self, output1, output2, component1, component2, img1, img2):
#         self.output1 = output1
#         self.output2 = output2
#         self.component1 = component1
#         self.component2 = component2
#         self.img1 = img1
#         self.img2 = img2
    
#     def updateOutput(self):
        

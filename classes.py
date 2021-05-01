from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import image as img
import numpy as np
from numpy.fft import ifft2, fft2, fftshift
from PyQt5.QtGui import QImage, QPixmap, qRgb

mixerComponents = ['amplitude', 'phase', 'real', 'imaginary', 'unity Amplitude', 'zero Phase']
imgs = ['image 1', 'image 2']

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
    shape = None
    def __init__(self, imgWidgets, imagePath):
        image = img.imread(imagePath, 0)
        if self.__class__.shape is not None:
            if not self.__class__.shape == image.shape:
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.showMessage('two images must be same size!')
                return False
        self.__class__.shape = image.shape
        self.inputImg = imgWidgets[0]
        self.outputImg = imgWidgets[1]
        self.outputSelector = imgWidgets[2]
        self.imagePath = imagePath

        fourier_coefficients = fft2(image)
        # fshift = fftshift(fourier_coefficients)
        self.components = {}
        self.components['amplitude'] = np.abs(fourier_coefficients)
        self.components['phase'] = np.angle(fourier_coefficients) 
        self.components['real'] = np.real(fourier_coefficients)
        self.components['imaginary'] = np.imag(fourier_coefficients)
        self.components['unity Amplitude'] = np.array([1 for element in fourier_coefficients])
        self.components['zero Phase'] = np.array([0 for element in fourier_coefficients])
        self.display()

    def display(self):
        self.inputImg.setPixmap(QtGui.QPixmap(self.imagePath))
        self.outputImg.setPixmap(QtGui.QPixmap(toQImage(self.components[self.outputSelector.currentText()])))

class component(object):
    def __init__(self, img_selector, component_selector, ratio, slotFunction):
        self.ratio = ratio
        self.img_selector = img_selector
        self.component_selector = component_selector
        self.img_selector.activated.connect(slotFunction)
        self.component_selector.activated.connect(slotFunction)
        self.component_selector.addItems([component for component in mixerComponents])
        self.img_selector.addItems([img for img in imgs])

def mix(amplitude = None, phase = None, real = None, imaginary = None):
    if amplitude is not None and phase is not None:
        return np.real(ifft2(np.multiply(amplitude, np.exp(1j*phase))))
    elif real is not None and imaginary is not None:
        return np.real(ifft2(np.add(real, 1j * imaginary)))

class Mixer(object):
    def __init__(self, outputs, component1, component2, images, outputSelector):
        self.outputs = outputs
        self.component1 = component1
        self.component2 = component2
        self.images = images
        self.outputSelector = outputSelector
        self.display()

    def display(self):
        self.combinedImg = None
        if self.component1.component_selector.currentText() == 'amplitude':
            self.combinedImg = mix(amplitude= self.images[self.component1.img_selector.currentText()].components[self.component1.component_selector.currentText()],
                                   phase= self.images[self.component2.img_selector.currentText()].components[self.component2.component_selector.currentText()])
        elif self.component1.component_selector.currentText() == 'phase':
            self.combinedImg = mix(phase= self.images[self.component1.img_selector.currentText()].components[self.component1.component_selector.currentText()],
                                   amplitude= self.images[self.component2.img_selector.currentText()].components[self.component2.component_selector.currentText()])
        elif self.component1.component_selector.currentText() == 'real':
            self.combinedImg = mix(real= self.images[self.component1.img_selector.currentText()].components[self.component1.component_selector.currentText()],
                                   imaginary= self.images[self.component2.img_selector.currentText()].components[self.component2.component_selector.currentText()])
        elif self.component1.component_selector.currentText() == 'imaginary':
            self.combinedImg = mix(real= self.images[self.component1.img_selector.currentText()].components[self.component1.component_selector.currentText()],
                                   imaginary= self.images[self.component2.img_selector.currentText()].components[self.component2.component_selector.currentText()])

        if self.combinedImg is not None:
            self.outputs[self.outputSelector.currentText()].setPixmap(QtGui.QPixmap(toQImage(self.combinedImg)))
        else:
            print("there's an error in displaying the combined image!")
    
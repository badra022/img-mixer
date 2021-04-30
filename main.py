###########################################################
# authors: Ahmed Badra,
#          Hassan Hosni,
#          Yousof Elhely,
#          Moamen Gamal
#
# title: Biosignal viewer
#
# file: main program file (RUN THIS FILE)
############################################################

# libraries needed for main python file
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from gui import Ui_MainWindow
import os
import pathlib
from classes import image

imgComponents = ['amplitude', 'phase', 'real', 'imaginary']
mixerComponents = ['amplitude', 'phase', 'real', 'imaginary', 'unity Amplitude', 'zero Phase']
outputs = ['output 1', 'output 2']
imgs = ['image 1', 'image 2']

# class definition for application window components like the ui
class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.imgWidgets = []
        self.imgWidgets.append([self.ui.img1, self.ui.img1_component_display, self.ui.img1_display_selector])
        self.imgWidgets.append([self.ui.img2, self.ui.img2_component_display, self.ui.img2_display_selector])

        self.outputs = {'output 1': self.ui.output1_display, 'output 2': self.ui.output2_display}
        self.images = {}

        for widget in self.imgWidgets:
            widget[2].activated.connect(self.updateComponentDisplay)
            for component in imgComponents:
                widget[2].addItem(component)

        self.ui.component1_component_selector.addItems([component for component in mixerComponents])
        self.ui.component2_component_selector.addItems([component for component in mixerComponents])
        self.ui.component1_img_selector.addItems([img for img in imgs])
        self.ui.component2_img_selector.addItems([img for img in imgs])
        self.ui.output_selector.addItems([output for output in outputs])

        self.ui.actionopen.triggered.connect(self.open)
        self.ui.actionnew_window.triggered.connect(child_window)
        self.images = []

    def updateComponentDisplay(self):
        for image in self.images:
            image.display()

    def open(self):
            files_names = QtGui.QFileDialog.getOpenFileName( self, 'Open only jpeg', os.getenv('HOME') ,"jpeg(*.jpeg)" )
            for path in files_names:
                idx = 0
                if pathlib.Path(path).suffix == ".jpeg":
                    self.images['image ' + str(idx + 1)] = image(self.imgWidgets[idx] , path)
                    self.imgWidgets.pop(0)
                    idx = idx + 1
            if not self.imgWidgets:
                self.mixer = Mixer( outputs = self.outputs,
                                    component1 = self.ui.component1,
                                    component2 = self.ui.component2,
                                    images = self.images,
                                    outputSelector = self.ui.output_selector)

def child_window():
    win = ApplicationWindow()
    win.show()

# function for launching a QApplication and running the ui and main window
def window():
    app = QApplication(sys.argv)
    win = ApplicationWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    window()
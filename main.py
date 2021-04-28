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
from classes import image, Mixer

imgComponents = ['amplitude', 'phase', 'real', 'imaginary']
mixerComponents = ['amplitude', 'phase', 'real', 'imaginary', 'unity_amplitude', 'zero_phase']
outputs = ['output 1', 'output 2']

# class definition for application window components like the ui
class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.imgWidgets = []
        self.imgWidgets.append([self.ui.img1, self.ui.img1_component_display, self.ui.img1_display_selector])
        self.imgWidgets.append([self.ui.img2, self.ui.img2_component_display, self.ui.img2_display_selector])
        self.images = {'image 1': self.ui.output1_display, 'image 2': self.ui.output2_display}


        for widget in self.imgWidgets:
            widget[2].activated.connect(self.updateComponentDisplay)
            for component in imgComponents:
                widget[2].addItem(component)

        self.ui.component1_component_selector.addItem([component for component in mixerComponents])
        self.ui.component2_component_selector.addItem([component for component in mixerComponents])
        self.ui.component1_img_selector.addItem([img for img in self.images.keys()])
        self.ui.component2_img_selector.addItem([img for img in self.images.keys()])
        self.ui.output_selector.addItem([output for output in outputs])

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
                    self.images.append(image(self.imgWidgets[idx][0],
                                             self.imgWidgets[idx][1],
                                             self.imgWidgets[idx][2],
                                             path))
                    self.imgWidgets.pop(0)
                    idx = idx + 1
            if not self.imgWidgets:
                self.mixer = Mixer( output1 = self.ui.output1_display,
                                    output2 = self.ui.output2_display,
                                    component1 = self.ui.component1,
                                    component2 = self.ui.component2,
                                    img1 = self.images[0],
                                    img2 = self.images[1])

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
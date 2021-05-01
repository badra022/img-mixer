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
from classes import image, Mixer, component

imgComponents = ['amplitude', 'phase', 'real', 'imaginary']
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
        self.component1 = component(img_selector = self.ui.component1_img_selector ,
                               component_selector = self.ui.component1_component_selector,
                               ratio = self.ui.component1_slider_ratio, slotFunction = self.updateOutputDisplay)
        self.component2 = component(img_selector = self.ui.component2_img_selector ,
                        component_selector = self.ui.component2_component_selector,
                        ratio = self.ui.component2_slider_ratio, slotFunction = self.updateOutputDisplay)
        self.outputs = {'output 1': self.ui.output1_display, 'output 2': self.ui.output2_display}
        self.images = {}

        self.ui.output_selector.activated.connect(self.updateOutputDisplay)
        for widget in self.imgWidgets:
            widget[2].activated.connect(self.updateComponentDisplay)
            widget[2].addItems([component for component in imgComponents])
               
        self.ui.output_selector.addItems([output for output in outputs])
        self.ui.actionopen.triggered.connect(self.open)
        self.ui.actionnew_window.triggered.connect(self.child_window)
        self.idx = 0 

    def updateComponentDisplay(self):
        for image in self.images.values():
            image.display()

    def updateOutputDisplay(self):
        self.mixer.display()

    def open(self):
            files_names = QtGui.QFileDialog.getOpenFileName( self, 'Open only jpeg', os.getenv('HOME') ,"jpeg(*.jpeg)" )
            for path in files_names:
                if pathlib.Path(path).suffix == ".jpeg":
                    self.images['image ' + str(self.idx + 1)] = image(self.imgWidgets[0] , path)
                    self.imgWidgets.pop(0)
                    self.idx = self.idx + 1
            if not self.imgWidgets:
                self.mixer = Mixer( outputs = self.outputs,
                                    component1 = self.component1,
                                    component2 = self.component2,
                                    images = self.images,
                                    outputSelector = self.ui.output_selector)

    def child_window(self):
        self.child = ApplicationWindow()
        self.child.show()

# function for launching a QApplication and running the ui and main window
def window():
    app = QApplication(sys.argv)
    win = ApplicationWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    window()
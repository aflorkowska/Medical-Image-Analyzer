# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from PyQt5.QtWidgets import *
from PyQt5 import uic , QtGui


class MyGUI(QMainWindow):
    
    def __init__(self):
        super(MyGUI, self).__init__()
        
        #Loading UI
        uic.loadUi("imageviewer.ui", self)
        
        #Defining widgets
        self.label = self.findChild(QLabel, "label")
        
        #Defining actions
        self.actionLoad_images.triggered.connect(self.load_image)
        
        
        #Defining variables
        self.current_file = "healthy1.jpg"
        self.file_list = None
        self.file_counter = None
        
        
        
        #Default settings
        ### Default Windows
        self.setWindowTitle("Medical Images Analyzer")
        
        ### Default PixelLabel
        pixmap = QtGui.QPixmap(self.current_file)
        pixmap = pixmap.scaled(self.width(), self.height())
        self.label.setPixmap(pixmap)
        self.label.setMinimumSize(1,1)
        
        #Show the app
        self.show()
        
    def resizeEvent(self, event):
        try:
            pixmap = QtGui.QPixmap(self.current_file)
        except:
            pixmap = QtGui.QPixmap("healthy1.jpg") #ustawic jaks defaultowy 
        pixmap = pixmap = pixmap.scaled(self.width(), self.height())
        self.label.setPixmap(pixmap)
        self.label.resize(self.width(), self.height())
        
    def load_image(self):
        options = QFileDialog().Options()
        filename , _ = QFileDialog.getOpenFileName(self, "Open File", "", "Image Files (*.png, *.jpg)", options=options)
        
        if filename!= "":
            self.current_file = filename
            pixmap = QtGui.QPixmap(self.current_file)
            pixmap = pixmap.scaled(self.width(), self.height())
            self.label.setPixmap(pixmap)
        
def main():
    app = QApplication([])
    win = MyGUI()
    app.exec()

    

if __name__ == "__main__":
    main()
   
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import tensorflow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic , QtGui

defaultImage = "src/settings/default.jpg"
emptyImageError = "src/settings/error_image.jpg"
emptyDirectoryError = "src/settings/error_directory.jpg"

class MyGUI(QMainWindow):
    
    def __init__(self):
        super(MyGUI, self).__init__()
        
        #Loading UI
        uic.loadUi("imageviewer.ui", self)
        
        #Defining widgets
        self.label = self.findChild(QLabel, "label")
        self.nextButton = self.findChild(QPushButton, "pushButton")
        self.previousButton = self.findChild(QPushButton, "pushButton_2")
        
        #Defining actions
        self.actionLoad_images.triggered.connect(self.load_image)
        self.actionChoose_directory.triggered.connect(self.open_directory)
        self.previousButton.clicked.connect(self.previous_image)
        self.nextButton.clicked.connect(self.next_image)
        
        #Defining variables
        self.current_file = defaultImage
        self.file_list = None
        self.file_counter = None
        
        #Default settings
        ### Default Windows
        self.setWindowTitle("Medical Images Analyzer")
        self.setMinimumSize(500,750)
        self.setMaximumSize(600,900)
        
        ###Default PixelLabel
        self.set_image()
       # self.label.setMinimumSize(300,350)
       # self.label.setMaximumSize(600,800)
        
        #Show the app
        self.show()
        
    def resizeEvent(self, event):
        self.set_image()  
        self.label.resize(self.width(), self.height())
         
        
    def load_image(self):
        options = QFileDialog().Options()
        filename , _ = QFileDialog.getOpenFileName(self, "Open File", "", "Image Files (*.png)", options=options) 
        
        if filename != "":
            self.current_file = filename
        else:
            self.current_file = emptyImageError
            
        self.set_image()
            
    def open_directory(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.file_list = [directory + "/" + f for f in os.listdir(directory) if f.endswith(".jpg") or f.endswith(".png")]
       
        if len(self.file_list) > 0:
            self.file_counter = 0
            self.current_file = self.file_list[self.file_counter]
        else:
            self.current_file = emptyDirectoryError
            
        self.set_image()        
            
         
    def next_image(self):
        if self.file_counter is not None and len(self.file_list) > 0:
            self.file_counter += 1
            self.file_counter %= len(self.file_list)
            self.current_file = self.file_list[self.file_counter]
            self.set_image()
            
    def previous_image(self):
        if self.file_counter is not None and len(self.file_list) > 0:
            self.file_counter -= 1
            self.file_counter %= len(self.file_list)
            self.current_file = self.file_list[self.file_counter]
            self.set_image()
  
    def set_image(self):
        try:
            pixmap = QtGui.QPixmap(self.current_file)
        except:
            pixmap = QtGui.QPixmap(defaultImage) 
        pixmap = pixmap.scaled(self.width(), self.height())
        self.label.setPixmap(pixmap)   
            
def main():
    app = QApplication([])
    win = MyGUI()
    app.exec()

    
if __name__ == "__main__":
    main()
   
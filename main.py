# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic , QtGui


class MyGUI(QMainWindow):
    
    def __init__(self):
        super(MyGUI, self).__init__()
        
        #Loading UI
        uic.loadUi("imageviewer.ui", self)
        
        #Default settings
        ### Default Windows
        self.setWindowTitle("Medical Images Analyzer")
        #self.setMinimumSize(QSize(300, 300))
        
        #Defining widgets
        self.label = self.findChild(QLabel, "label")
        
        #Defining actions
        self.actionLoad_images.triggered.connect(self.load_image)
        self.actionChoose_directory.triggered.connect(self.open_directory)
        
        
        #Defining variables
        self.current_file = "default.jpg"
        self.file_list = None
        self.file_counter = None
        
        
    
        ### Default PixelLabel
        pixmap = QtGui.QPixmap(self.current_file)
        pixmap = pixmap.scaled(self.width(), self.height())
        self.label.setPixmap(pixmap)
        self.label.setMinimumSize(300,300)
        
        #Show the app
        self.show()
        
    def resizeEvent(self, event):
        try:
            pixmap = QtGui.QPixmap(self.current_file)
        except:
            pixmap = QtGui.QPixmap("default.jpg") 
            
        pixmap = pixmap = pixmap.scaled(self.width(), self.height())
        self.label.setPixmap(pixmap)
        self.label.resize(self.width(), self.height())
        
    def load_image(self):
        options = QFileDialog().Options()
        filename , _ = QFileDialog.getOpenFileName(self, "Open File", "", "Image Files (*.png)", options=options) 
        
        if filename != "":
            self.current_file = filename
        else:
            self.current_file = "error_image.jpg" #ERROR 
            
        pixmap = QtGui.QPixmap(self.current_file)
        pixmap = pixmap.scaled(self.width(), self.height())
        self.label.setPixmap(pixmap)
            
    def open_directory(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.file_list = [directory + "/" + f for f in os.listdir(directory) if f.endswith(".jpg") or f.endswith(".png")]
       
        if len(self.file_list) > 0:
            self.file_counter = 0
            self.current_file = self.file_list[self.file_counter]
        else:
            self.current_file = "error_directory.jpg"
            
        pixmap = QtGui.QPixmap(self.current_file)
        pixmap = pixmap.scaled(self.width(), self.height())
        self.label.setPixmap(pixmap)         
            
             
def main():
    app = QApplication([])
    win = MyGUI()
    app.exec()

    

if __name__ == "__main__":
    main()
   
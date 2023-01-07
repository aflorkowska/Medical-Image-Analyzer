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
from PyQt5.QtGui import *
import cv2, imutils
import numpy as np

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
        self.brightnessSlider = self.findChild(QSlider, "verticalSlider")
        self.sharpnessSlider = self.findChild(QSlider, "verticalSlider_2")
        
        #Defining actions
        self.actionLoad_images.triggered.connect(self.load_image)
        self.actionChoose_directory.triggered.connect(self.open_directory)
        self.previousButton.clicked.connect(self.previous_image)
        self.nextButton.clicked.connect(self.next_image)
        self.brightnessSlider.valueChanged['int'].connect(self.brightness_value)
        self.sharpnessSlider.valueChanged['int'].connect(self.sharpness_value)
        self.actionSharpening.triggered.connect(self.edgeDetectionSwitcher)
        #Defining variables
        self.current_file = defaultImage
        self.current_image = None
        self.file_list = None
        self.file_counter = None
        self.brightness_value = 0
        self.sharpness_value = 0 
        self.is_edge_detection_chosen = 0
        
        #Default settings
        ### Default Windows
        self.setWindowTitle("Medical Images Analyzer")
        self.setMinimumSize(500,750)
        self.setMaximumSize(600,900)
        
        ###Default PixelLabel
        self.set_image()
      
        
        #Show the app
        self.show()
        
    def resizeEvent(self, event):
        self.current_image = cv2.imread(self.current_file)
        self.set_image()  
        self.label.resize(self.width(), self.height())
         
        
    def load_image(self):
        options = QFileDialog().Options()
        filename , _ = QFileDialog.getOpenFileName(self, "Open File", "", "Image Files (*.png)", options=options) 
        
        if filename != "":
            self.current_file = filename
        else:
            self.current_file = emptyImageError
        
        self.current_image = cv2.imread(self.current_file)
        self.set_image()
            
    def open_directory(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.file_list = [directory + "/" + f for f in os.listdir(directory) if f.endswith(".jpg") or f.endswith(".png")]
       
        if len(self.file_list) > 0:
            self.file_counter = 0
            self.current_file = self.file_list[self.file_counter]
        else:
            self.current_file = emptyDirectoryError
        
        self.current_image = cv2.imread(self.current_file)
        self.set_image()        
            
         
    def next_image(self):
        if self.file_counter is not None and len(self.file_list) > 0:
            self.file_counter += 1
            self.file_counter %= len(self.file_list)
            self.current_file = self.file_list[self.file_counter]
            self.current_image = cv2.imread(self.current_file)
            self.set_image()
            
    def previous_image(self):
        if self.file_counter is not None and len(self.file_list) > 0:
            self.file_counter -= 1
            self.file_counter %= len(self.file_list)
            self.current_file = self.file_list[self.file_counter]
            self.current_image = cv2.imread(self.current_file)
            self.set_image()
  
    def set_image(self):
        
        try:
            image = imutils.resize(self.current_image, width = 600)
           
        except:
            self.current_image = cv2.imread(defaultImage)
            image = imutils.resize(self.current_image, width = 600)
        
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1],frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(image))   
      
    def brightness_value(self, value):
        self.brightness_value = value
        self.update()
      
    def changeBrightness(self, img, value):
        hsv  = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h,s,v = cv2.split(hsv)
        lim = 255 - value
        v[v>lim] = 255
        v[v<=lim] += value
        final_hsv = cv2.merge((h,s,v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img
              
    def changeSharpness(self, img, value):
        kernel_size = (value + 1, value + 1)
        img = cv2.blur(img, kernel_size)
        return img
    
    def sharpness_value(self, value):
        self.sharpness_value = value
        self.update()
      
    def edgeDetectionSwitcher(self):
        self.is_edge_detection_chosen = 1 if self.is_edge_detection_chosen == 0 else 0
        self.update()
        print("Edge switcher", self.is_edge_detection_chosen)
    
    def canny_edge_detection(self, img):
        # Setting parameter values
        t_lower = 50  # Lower Threshold
        t_upper = 150  # Upper threshold
          
        # Applying the Canny Edge filter
        edge = cv2.Canny(img, t_lower, t_upper)
        return edge
        
    def update(self):
        self.current_image = cv2.imread(self.current_file)
        img = self.changeBrightness(self.current_image, self.brightness_value)
        img = self.changeSharpness(img, self.sharpness_value)
        if(self.is_edge_detection_chosen):
            img = self.canny_edge_detection(img)
        self.current_image = img
        self.set_image()
    
        
    
if __name__ == "__main__":
    app = QApplication([])
    win = MyGUI()
    app.exec()
   
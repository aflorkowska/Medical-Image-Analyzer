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
from PIL import *
import torch
import torch.nn as nn
from torchvision import  transforms, datasets, models
from efficientnet_pytorch import EfficientNet


modelpath = "src/model.pth"
defaultImage = "src/settings/default.jpg"
emptyImageError = "src/settings/error_image.jpg"
emptyDirectoryError = "src/settings/error_directory.jpg"

class MyGUI(QMainWindow):
    
    def __init__(self):
        super(MyGUI, self).__init__()
        
        #Loading UI
        uic.loadUi("imageviewer_new.ui", self)
        
        #Defining widgets
        self.label = self.findChild(QLabel, "label")
        self.prediction = self.findChild(QLabel, "label_3")
        ###Buttons
        self.nextButton = self.findChild(QPushButton, "pushButton")
        self.previousButton = self.findChild(QPushButton, "pushButton_2")
        ###Sliders
        self.brightnessSlider = self.findChild(QSlider, "verticalSlider")
        self.sharpnessSlider = self.findChild(QSlider, "verticalSlider_2")
        self.contrastSlider = self.findChild(QSlider, "horizontalSlider")
        self.lowerEdgeDetectionSlider = self.findChild(QSlider, "horizontalSlider_2")
        self.upperEdgeDetectionSlider = self.findChild(QSlider, "horizontalSlider_3")
        ###Checbox
        self.edgeDetectionCheckBox = self.findChild(QCheckBox, "checkBox")
        self.contrastCheckBox = self.findChild(QCheckBox, "checkBox_2")
        self.brightnessCheckBox = self.findChild(QCheckBox, "checkBox_3")
        self.sharpnessCheckBox = self.findChild(QCheckBox, "checkBox_4")
        
       
        
        #Default settings
        ### Default Windows
        self.setWindowTitle("Medical Images Analyzer")
        self.setMinimumSize(500,750)
        self.setMaximumSize(800,1000)
        
        #Defining actions
        ###Menu
        self.actionLoad_images.triggered.connect(self.load_image)
        self.actionChoose_directory.triggered.connect(self.open_directory)
        self.actionSave_image.triggered.connect(self.save_image)
        self.actionQuit.triggered.connect(self.close) 
        self.actionGet_Results.triggered.connect(self.get_results_model_prediction)
        ###Buttons
        self.previousButton.clicked.connect(self.previous_image)
        self.nextButton.clicked.connect(self.next_image)
        ###Sliders
        self.brightnessSlider.valueChanged['int'].connect(self.brightness_value)
        self.sharpnessSlider.valueChanged['int'].connect(self.sharpness_value)
        self.contrastSlider.valueChanged['int'].connect(self.contrast_value)
        self.contrastSlider.valueChanged['int'].connect(self.contrast_value)
        self.lowerEdgeDetectionSlider.valueChanged['int'].connect(self.lowerThreshold_value)
        self.upperEdgeDetectionSlider.valueChanged['int'].connect(self.upperThreshold_value)
        
        #Defining variables
        self.current_file = defaultImage
        self.current_image = None
        self.file_list = None
        self.file_counter = None
        self.saved_images_counter = 0
        ###Sliders
        self.brightness_value = 0
        self.sharpness_value = 0 
        self.contrast_value = 0
        self.lowerThreshold_value = 0
        self.upperThreshold_value = 0
        ###Switchers
        self.is_edge_detection_chosen = 0
        
        ###Default PixelLabel
        self.set_image()
      
        #Show the app
        self.show()
        
        
   
    def resizeEvent(self, event):
        self.current_image = cv2.imread(self.current_file)
        self.set_image()  
        self.label.resize(self.width(), self.height())
         
    
    def get_results_model_prediction(self):
                
        
        classes = ['Healthy', 'Covid', 'Lung Opacity']
        
        model = EfficientNet.from_pretrained('efficientnet-b3', num_classes=3)
        device = "cpu" 
        model.load_state_dict(torch.load(modelpath,map_location=torch.device('cpu')))
        model.to(device)
        
        # 
        
        img = Image.open(self.current_file)
        transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x.repeat(3, 1, 1) ),
        transforms.Normalize((0.485,0.456, 0.406), (0.229 , 0.224, 0.225)) ])
        img_normalized = transform(img).float()
        img_normalized = img_normalized.unsqueeze_(0)
       
        #img_normalized = img_normalized.to(device)
        with torch.no_grad():
            model.eval()
            output = model(img_normalized)
            index = output.data.cpu().numpy().argmax()
            class_name = classes[index]
      

        ## NA SZTYWNO BO NIE DZIALA MODEL 
        #class_name = classes[0]  
        path_to_directory = self.current_file[0:len(self.current_file)-4]
        index  = path_to_directory.rfind("/")
        value = "Label: " + self.current_file[index + 1 : len(self.current_file)-4] + " ------ Model prediction: " + str(class_name)
        self.prediction.setText(str(value))
        
    def save_image(self):
        temp_path = self.current_file[0:len(self.current_file)-4]
        name = temp_path + "_ModifiedImg_" + str(self.saved_images_counter) + ".PNG"
        self.saved_images_counter += 1
        cv2.imwrite(name, self.current_image)
        
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
        
    def update(self):
        self.current_image = cv2.imread(self.current_file)
        img  = self.current_image
        
        if(self.brightnessCheckBox.isChecked()): 
            img = self.changeBrightness(img, self.brightness_value)
        if(self.sharpnessCheckBox.isChecked()): 
            img = self.changeSharpness(img, self.sharpness_value)
        if(self.contrastCheckBox.isChecked()): 
            img = self.changeContrast(img, self.contrast_value)
        if(self.edgeDetectionCheckBox.isChecked()):
            if(self.lowerThreshold_value < self.upperThreshold_value):
               img  = self.cannyEdgeDetection(img, self.lowerThreshold_value, self.upperThreshold_value)
           
        self.current_image = img
        self.set_image()
    
    #Sliders
    def brightness_value(self, value):
        self.brightness_value = value 
        self.update()
        
    def sharpness_value(self, value):
        self.sharpness_value = value / 10
        self.update()  
        
    def contrast_value(self, value):
        self.contrast_value = value
        self.update() 

    def lowerThreshold_value(self, value):
        self.lowerThreshold_value = value
        self.update()
        
    def upperThreshold_value(self, value):
        self.upperThreshold_value = value
        self.update()
        
        
        #Image Processing Methods
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
        kernel = np.array([[-1,-1,-1], [-1,value,-1], [-1,-1,-1]])
        img = cv2.filter2D(img, -1, kernel)
        return img

    def changeContrast(self, img, value):
        params = value * 0.1;
        clahe = cv2.createCLAHE(clipLimit = params) 
        grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cl_img = clahe.apply(grayimg)
        return cl_img
    
    def cannyEdgeDetection(self, img, lowerTh, upperTh):
        edge = cv2.Canny(img, lowerTh, upperTh)
        return edge
    
 
if __name__ == "__main__":
    app = QApplication([])
    win = MyGUI()
    app.exec()
   
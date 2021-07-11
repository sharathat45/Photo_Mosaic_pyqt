from PyQt4.QtCore import Qt
from PyQt4.QtGui import (QGridLayout, QPushButton, QLabel, QPixmap, QDialog, QIcon, QMessageBox)
import style_sheet
import webbrowser
from functools import partial
import sys
import os

def resource_path(relative_path):
   if hasattr(sys, '_MEIPASS'):
      return os.path.join(sys._MEIPASS, relative_path)
   return os.path.join(os.path.abspath("."), relative_path)

class PopUp(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(style_sheet.window_style)
        self.setWindowIcon(QIcon(resource_path('images/favicon.ico')))
        self.setWindowTitle("Photo Mosaic")
        self.setStandardButtons(QMessageBox.Ok)
        
    def empty_target_img(self):
        self.setIcon(QMessageBox.Warning)
        self.setText("No Target Image selected")
        self.setInformativeText("Please select a target image for mosaic")
        self.exec_()
   
    def empty_input_images(self):
        self.setIcon(QMessageBox.Warning)
        self.setText("No Input Images selected")
        self.setInformativeText("Please select folder containing of images for background of mosaic")
        self.exec_()

    def choose_output_path(self):
        self.setIcon(QMessageBox.Warning)
        self.setText("No Output Directory selected")
        self.setInformativeText("Please select folder to store output mosaic image")
        self.exec_()

    def error(self):
        self.setIcon(QMessageBox.Critical)
        self.setText("Something went wrong!!")
        self.setInformativeText("Close the application and try again")
        self.exec_()    

class ImagesWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(style_sheet.window_style) 
        self.setWindowIcon(QIcon(resource_path('images/favicon.ico')))
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('Example Mosaics')
        self.setMaximumWidth(800)
        self.setMaximumHeight(700) 
        
        self.images_layout = QGridLayout()
        self._imageWidget()
        self.setLayout(self.images_layout)

    def _imageWidget(self):
        self.image_0 = '<li>- Colour Mosaic</li> <li>- Focus on Target Image</li>'
        self.image_1 = '<li>- Grayscale Mosaic</li> <li>- Focus on Target Image</li>'
        self.image_2 = '<li>- Colour Mosaic</li> <li>- Focus on Background Images</li>'
        self.image_3 = '<li>- Colour Mosaic</li> <li>- More Focus on Background Images</li>'
        
        for iter,i in enumerate(['thumb_1.jpg','thumb_2.jpg', 'thumb_3.jpg', 'thumb_4.jpg']):    
            self.label = QLabel(self)
            self.pixmap = QPixmap(resource_path('images/'+i))
            self.pixmap = self.pixmap.scaled(200, 200, Qt.KeepAspectRatio)
            self.label.setPixmap(self.pixmap)    
            self.images_layout.addWidget(self.label,0,iter)
            
            self.images_layout.addWidget(QLabel(eval(f'self.image_{iter}')),1,iter)
            
            self.button = QPushButton("View Full Image", self)
            self.button.setToolTip("Image will load in web browser from internet")
            self.button.clicked.connect(partial(self.show_image, iter+1))
            self.images_layout.addWidget(self.button,2,iter)    
         
         
    def show_image(self, image_id: int):
        if image_id == 1: 
            webbrowser.open('https://drive.google.com/file/d/1urXQb9MNKSYaQA9j2nI5cbYvMp8Y4rOX/view')
        elif image_id == 2: 
            webbrowser.open('https://drive.google.com/file/d/1CaYolmyA7Ay5YtD41AdiBs2S4JMNuyNI/view')
        elif image_id == 3: 
            webbrowser.open('https://drive.google.com/file/d/12WXhPMCpSUCAXm2zUtb0Rm7YysLvb5Gp/view')
        elif image_id == 4: 
            webbrowser.open('https://drive.google.com/file/d/1L5hcB9CLEnbbgNNRtzNW2ug3AYTQbpIC/view')
            
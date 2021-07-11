from PyQt4.QtCore import Qt, QThread, pyqtSlot
from PyQt4.QtGui import (QWidget, QVBoxLayout, QGridLayout, QComboBox, QPushButton, QFileDialog, QProgressBar,
   QLabel, QFrame, QPixmap, QHBoxLayout, QIcon, QFontDatabase, QFont )
import os
import ntpath
import posixpath
import style_sheet 
from functools import partial
from popup_window import PopUp, ImagesWindow, resource_path 
from mosaic_worker import Worker

class window(QWidget):
   def __init__(self, parent = None):
      super(window, self).__init__(parent)
      self.setWindowIcon(QIcon(resource_path('images/favicon.ico')))
      self.setStyleSheet(style_sheet.window_style)   
      self.setWindowTitle('Photo Mosaic')
      self.setMaximumWidth(500)
      self.setMaximumHeight(300)
      
      self.target_image_directory = ""
      self.input_images_directory = ""
      self.output_directory = ""

      self.popup_window = PopUp()
      self.main_layout = QVBoxLayout()
      self._headerWidget()
      self._inputWidget()
      self._progress()
      self._completed_status()
      self._footerWidget()   
      self.setLayout(self.main_layout)
      
   def _headerWidget(self):     
      self.header_layout = QHBoxLayout()

      self.logo_img = QLabel(self)
      self.pixmap = QPixmap(resource_path('images/camera-solid.png'))
      self.logo_img.setPixmap(self.pixmap)
      self.logo_img.setAlignment(Qt.AlignCenter)
      self.header_layout.addWidget(self.logo_img)

      self.main_title = QLabel('PHOTO MOSAIC')
      self.main_title.setObjectName('MainTitle')
      self.main_title.setAlignment(Qt.AlignCenter)
      self.header_layout.addWidget(self.main_title)
      
      self.fontDB = QFontDatabase()
      self.fontDB.addApplicationFont(resource_path("fonts/Anurati-Regular.otf"))
      self.main_title.setFont(QFont("Anurati", style_sheet.title_font_size))
      
      self.main_layout.addLayout(self.header_layout)

   def _inputWidget(self):   
      self.input_buttons = QGridLayout()
      
      self.Image_option = QComboBox()
      self.Image_option.addItems(["Colour Mosaic", "Grayscale Mosaic"])
      self.Image_option.setToolTip("<b> Output Image colour </b> <br> \
                           <b>Colour Mosaic:</b> output image will be same as input image colour,\
                           <b>Grayscale Mosaic:</b> output image will be bi-tonal black & white")
      self.input_buttons.addWidget(self.Image_option,0,1)
      
      self.focus_option = QComboBox()
      self.focus_option.addItems(["Focus on Target Image", "Focus on Background Images", "More Focus on Background Images"])
      self.focus_option.setToolTip("<b> Focus on images </b> <br> \
                           Checkout Example images for more information on this")
      
      self.input_buttons.addWidget(self.focus_option,0,2)

      self.size_option = QComboBox()
      self.size_option.addItems(["Regular Size", "Regular Size +", "Regular Size ++"])
      self.size_option.setToolTip("<b> Output Image Size </b> <br> As Image size increases, \
                           it can accomodate more background images,\
                           but output Image size and computation time will increase")
      self.input_buttons.addWidget(self.size_option,0,3)

      self.target_img_button = QPushButton("Select Target Image", self)
      self.target_img_button.clicked.connect(partial(self.get_file, 1))
      self.input_buttons.addWidget(self.target_img_button,1,1)

      self.input_dir_button = QPushButton("Select Background Images Folder", self)
      self.input_dir_button.clicked.connect(partial(self.get_file, 2))
      self.input_buttons.addWidget(self.input_dir_button,1,2)

      self.output_dir_button = QPushButton("Select Output Folder", self)
      self.output_dir_button.setToolTip("Choose where output image to be saved")
      self.output_dir_button.clicked.connect(partial(self.get_file, 3))
      self.input_buttons.addWidget( self.output_dir_button,1,3)

      self.Mosaic = QPushButton("Compute Mosaic", self)
      self.Mosaic.clicked.connect(self.mosaic)
      self.input_buttons.addWidget(self.Mosaic,2,2)
      
      self.frame = QFrame()
      self.frame.setLayout(self.input_buttons)
      self.frame.show()
      self.main_layout.addWidget(self.frame)
   
   def _progress(self):
      self.progress = QProgressBar()
      
      self.progress.resize(self.width() - 200 - 10, 50)
      self.progress.setAlignment(Qt.AlignCenter)
      self.progress.setFormat('%p%')
      self.progress.setTextVisible(True)
      self.progress.setRange(0, 100)
      
      self.progress.setValue(2)
      self.progress.hide()
      self.main_layout.addWidget(self.progress)

   def _completed_status(self):
      self.completed_layout = QVBoxLayout()
      
      self.success_img = QLabel(self)
      self.success_pixmap = QPixmap(resource_path('images/check-solid.png'))
      self.success_img.setPixmap(self.success_pixmap)
      self.success_img.setAlignment(Qt.AlignCenter)
      self.completed_layout.addWidget(self.success_img)  
      
      self.completed_buttons = QHBoxLayout()
      self.open_image_button = QPushButton("Open Output Mosaic folder", self)
      self.open_image_button.setToolTip("Viewing the Image may take some time, <br> Please be patient!!")
      
      self.open_image_button.clicked.connect(self.open_folder)
      self.completed_buttons.addWidget(self.open_image_button)
      self.compute_again_button = QPushButton("Compute Mosaic for Other Image", self)
      self.compute_again_button.clicked.connect(self.display_home)
      self.completed_buttons.addWidget(self.compute_again_button)
      self.completed_layout.addLayout(self.completed_buttons)  
      
      self.completed_frame = QFrame()
      self.completed_frame.setLayout(self.completed_layout)
      self.completed_frame.hide()
      self.main_layout.addWidget(self.completed_frame)

   def _footerWidget(self):  
      self.example = QPushButton("View Example Images", self)
      self.images_win = ImagesWindow()
      self.example.clicked.connect(self.example_win)
      self.main_layout.addWidget(self.example) 

   def example_win(self):
      self.images_win.show()
      self.images_win.exec_()

   def mosaic(self): 
      if len(self.target_image_directory) == 0 or not os.path.isfile(self.target_image_directory):
         self.popup_window.empty_target_img()
      elif len(self.input_images_directory) == 0 or not os.path.exists(self.input_images_directory):
         self.popup_window.empty_input_images()
      elif len(self.output_directory) == 0 or not os.path.exists(os.path.split(self.output_directory)[0]):
         self.popup_window.choose_output_path()
      else:
         self.worker_inputs = {}
         self.worker_inputs['target_image_path'] = self.target_image_directory
         self.worker_inputs['bckgrnd_images_path'] = self.input_images_directory
         self.worker_inputs ['output_path'] = self.output_directory
         self.worker_inputs['image_colour_option'] = False if self.Image_option.currentText()=="Colour Mosaic" else True
         if self.focus_option.currentText()=="Focus on Target Image":
            self.worker_inputs['focus_option'] = 0.8
         elif self.focus_option.currentText()=="Focus on Background Images":            
            self.worker_inputs['focus_option'] = 0.7
         else:
            self.worker_inputs['focus_option'] = 0.6 

         if self.size_option.currentText()=="Regular Size ++":
            self.worker_inputs ['size_option'] = 3 
         elif self.size_option.currentText()=="Regular Size +":
            self.worker_inputs ['size_option'] = 2
         else:
            self.worker_inputs ['size_option'] = 1

         self.frame.hide()
         self.progress.show()

         self.thread = QThread()       # Create a QThread object
         self.worker = Worker(self.worker_inputs)    # Create a worker object 
         self.worker.moveToThread(self.thread)      # Move worker to the thread
         self.thread.started.connect(self.worker.run)
         self.worker.finished.connect(self.thread.quit)
         self.worker.finished.connect(self.worker.deleteLater)
         self.thread.finished.connect(self.thread.deleteLater)
         self.worker.progress.connect(self.reportProgress)

         self.thread.start() # Start the thread
         self.worker.finished.connect(self.done_processing )
         
   def display_home(self):
      self.completed_frame.hide()
      self.progress.setValue(2)
      self.progress.hide()
      self.frame.show()

   @pyqtSlot(int)
   def reportProgress(self,n):
      if n == 0:
         self.thread.quit()
         self.worker.deleteLater()
         self.thread.deleteLater()
         self.popup_window.error()
         self.display_home()      
      else:   
         self.progress.setValue(n)

   def done_processing(self):
      self.progress.hide()
      self.completed_frame.show()
      
   def open_folder(self):
      os.startfile(os.path.realpath(os.path.split(self.output_directory)[0]))
    
   def get_file(self, mode:int):
      if mode == 1:
         self.target_image_directory = QFileDialog.getOpenFileName(self, 'Choose target Image','./',"Image files (*.jpg *.png *.JPG *.PNG)")
      elif mode == 2:
         self.input_images_directory = QFileDialog.getExistingDirectory(self, "Choose Background Images folder", "./")
         self.input_images_directory = self.input_images_directory.replace(ntpath.sep,posixpath.sep)
      elif mode == 3:
         self.output_directory = QFileDialog.getSaveFileName(self,"Save Output Image","C:/PhotoMosaic.jpg","Image Files (*.jpg)")
         
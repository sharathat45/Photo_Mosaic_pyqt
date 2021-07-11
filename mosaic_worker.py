import cv2
import os
import random
import numpy as np
from PIL import Image,ImageOps
from pathlib import Path
from PyQt4.QtCore import ( QObject, pyqtSignal)

IMAGE_HIGHT_1 = 10000  
IMAGE_WIDTH_1 = 7200  
IMAGE_HIGHT_2 = 14000  
IMAGE_WIDTH_2 = 10000  
IMAGE_HIGHT_3 = 16000  
IMAGE_WIDTH_3 = 12500  

GRID_WIDTH_1 = 700
GRID_HIGHT_1 = 400
GRID_WIDTH_2 = 900
GRID_HIGHT_2 = 500
GRID_WIDTH_3 = 900
GRID_HIGHT_3 = 500

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    
    def __init__(self, worker_inputs):
        super().__init__()
        self.target_img_path = worker_inputs["target_image_path"]
        self.bckgrnd_imgs_path = worker_inputs["bckgrnd_images_path"]
        self.mosaic_img_path = worker_inputs["output_path"]

        self.grayscale_flag = worker_inputs["image_colour_option"]      
        self.blend_factor = worker_inputs["focus_option"]
        self.desired_width  = eval('IMAGE_WIDTH_'+ str(worker_inputs["size_option"]))
        self.desired_height = eval('IMAGE_HIGHT_'+ str(worker_inputs["size_option"]))
        self.progress_iter = 3
        self.grid_w = eval('GRID_WIDTH_'+ str(worker_inputs["size_option"])) 
        self.grid_h = eval('GRID_HIGHT_'+ str(worker_inputs["size_option"])) 
        self.ratio = (0.8,1.7)   #h/w ratio, if below lower threshold->landscape, above upper threshold->portrait, in between->square
    
    def run(self):   
        try:
            self.progress.emit(10)
            self._read_target_img()
            self.progress.emit(20)
            self._perform_mosaic(20)
            self.progress.emit(95)
            self._save_mosaic_img()
            self.progress.emit(100)
        except :
            self.progress.emit(0)

        self.finished.emit()

    def _read_target_img(self): # Read target image and resize
        if self.grayscale_flag:        
            self.target_img = cv2.imread(self.target_img_path,0)
            self.target_h,self.target_w = self.target_img.shape[:2]
        else:
            self.target_img = cv2.imread(self.target_img_path)
            self.target_h,self.target_w = self.target_img.shape[:2] 

        if(self.target_h/self.target_w  <= self.ratio[0]):  #if landscape image
            self.desired_height = self.desired_width
       
        hpercent = (self.desired_height/float(self.target_h))
        self.target_w = int((float(self.target_w)*float(hpercent)))
        self.target_h = self.desired_height        
        self.target_img = cv2.resize(self.target_img,(self.target_w, self.target_h), interpolation = cv2.INTER_CUBIC)
        
    def _save_mosaic_img(self): # Save the final image        
        cv2.imwrite(self.mosaic_img_path,self.target_img) 

    def _perform_mosaic(self,progress_val):
        files = list(Path(self.bckgrnd_imgs_path).rglob("*.[PpjJ][NnpP][gG]"))
        random.shuffle(files)
        
        images_list = []     #store extracted images
        images_list_iter = 0 #list iterator
        x=0                  # width
        y=0                  # height
        i = 0                #while loop iterator
        n = len(files)       #images to store/shift operation

        while True:
            if i<n:     #get from file,blend and store in list
                try:
                    if self.grayscale_flag:
                        imgdata = Image.open(files[i]).convert('L')
                    else:
                        imgdata = Image.open(files[i])
                except:
                    i+=1  
                    continue

                imgdata = ImageOps.exif_transpose(imgdata) #ignore metadata orientation
                imgdata.thumbnail((self.grid_w, self.grid_h))
                
                w,h = imgdata.size
                if(h/w >= self.ratio[1]):                   #if portrait image
                    input_img = imgdata
                elif(h/w <= self.ratio[0]):                 #if landscape image
                    input_img = imgdata.resize((self.grid_w,self.grid_h), Image.LANCZOS)
                    w,h = self.grid_w,self.grid_h
                else:                                       #if square image
                    input_img = imgdata.resize((self.grid_h,self.grid_h), Image.LANCZOS)
                    w,h = self.grid_h,self.grid_h
                
                input_img = np.array(input_img)
                if self.grayscale_flag==False:
                    input_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)

                images_list.append((input_img,w,h))

                i+=1  
                  
            elif i==n: # shuffle images list after extraction from file
                random.shuffle(images_list)
                input_img = images_list[images_list_iter][0]
                w,h = images_list[images_list_iter][1], images_list[images_list_iter][2]
                images_list_iter +=1
                i+=1

            else: # get the images from image list
                if images_list_iter == n:
                    random.shuffle(images_list)
                    images_list_iter = 0 
                
                input_img = images_list[images_list_iter][0]
                w,h = images_list[images_list_iter][1], images_list[images_list_iter][2]
                images_list_iter += 1
        
            if x+w > self.target_w:  # x1+x2 = w , x1 -> percent of img inside target_img frame (for edge background images)
                progress_val += self.progress_iter
                self.progress.emit(progress_val)

                x1_percent = (self.target_w-x)/w                
                if x1_percent <= 0.3:  # very small percent is inside then ignore and leave it empty space
                    x=0
                    y += h
                    if y >= self.target_h:
                        break
                else: # most percent is inside or outside then expand current img and fit to frame 
                    w = self.target_w-x
                    try: 
                        input_img = cv2.resize(input_img,(w,self.grid_h), interpolation = cv2.INTER_LINEAR)
                        self.target_img[y:y+h, x:x+w] = cv2.addWeighted(self.target_img[y:y+h, x:x+w],self.blend_factor,input_img,(1-self.blend_factor),0) 
                    except:
                        pass
                    x=0
                    y += h
                    if y >= self.target_h:
                        break 
                    else:
                        continue
            try: 
                self.target_img[y:y+h, x:x+w] = cv2.addWeighted(self.target_img[y:y+h, x:x+w],self.blend_factor,input_img,(1-self.blend_factor),0)  
            except:
                pass
            x += w 
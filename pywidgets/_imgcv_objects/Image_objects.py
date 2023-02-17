from tkinter import messagebox
from pywidgets._imgcv_objects.__origin import Img_cv,ALL_EXTENSIONS
import cv2
import numpy as np
from pycv2.img.utils import *
from tkinter import filedialog
from typing import Tuple
CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
class Cluster_Imgcv(Img_cv):
    def __init__(self, imgcv, mask=None, points=None ,kmeans=7):
        super().__init__(imgcv, mask=mask, points=points)
        self.kmeans=kmeans
    def cluster_image(self):
        Z = self.imgcv.reshape((-1,3))
        # convert to np.float32
        Z = np.float32(Z)
        # define criteria, number of clusters(K) and apply kmeans()

        ret,label,center=cv2.kmeans(Z,self.kmeans,None,CRITERIA,10,cv2.KMEANS_RANDOM_CENTERS)
        # Now convert back into uint8, and make original image
        center = np.uint8(center)
        res = center[label.flatten()]
        self.imgcv = res.reshape((self.imgcv.shape))
    def get_keys(self):
        the_dict=Img_cv.get_keys(self)
        the_dict["kmeans"]=self.kmeans
        return the_dict
class Brushed_Imgcv(Img_cv):
    def __init__(self, imgcv, mask=None, points=None ,radiusarea=3,flags=cv2.INPAINT_TELEA):
        super().__init__(imgcv, mask=mask, points=points)
        self.radiusArea=radiusarea
        self.flags=flags
    def in_paint_image(self):
        resultimg = cv2.inpaint(self.imgcv, self.mask, self.radiusArea, self.flags)
        self.imgcv=resultimg
    
    def get_keys(self):
        the_dict=Img_cv.get_keys(self)
        the_dict["radiusarea"]=self.radiusArea
        return the_dict
class Colored_Imgcv(Img_cv):
    def __init__(self, imgcv, mask=None, points=None ,coloerbackground=None,color=(255,255,255)):
        super().__init__(imgcv, mask=mask, points=points)
        self.color=color
        if coloerbackground is None:
            coloerbackground=np.zeros(self.imgcv.shape,"uint8")
            coloerbackground[:]=self.color
        self.colorBackground=coloerbackground
    def get_keys(self):
        val=Img_cv.get_keys(self)
        val["coloerbackground"]=self.colorBackground.copy()
        val["color"]=self.color
        return val
    def add_color_back_ground(self):
        colored_background=add_back_ground(self.imgcv, self.mask,
                            self.colorBackground)
        self.imgcv=colored_background

class Blurred_imgcv(Img_cv):
    def __init__(self, imgcv, mask=None, points=None ,blured=7):
        super().__init__(imgcv, mask=mask, points=points)
        self.blurred=blured
    def bluredimg(self):
        if self.blurred!=0:
            self.imgcv=bluring(self.imgcv, self.mask, self.blurred)    
    def get_keys(self):
        val=Img_cv.get_keys(self)
        val["blured"]=self.blurred
        return val
class Background_Img_cv(Img_cv):
    def __init__(self, imgcv, mask=None, points=None ,imported_backgrounds:list=[]):
        super().__init__(imgcv, mask=mask, points=points)
        self.imported_backgrounds:Tuple[Img_cv,tuple]=[]
        for background,_ in imported_backgrounds:
            self.import_img_back_ground(background)
    def get_keys(self):
        val=Img_cv.get_keys(self)
        val["imported_backgrounds"]=self.imported_backgrounds
        return val

    def get_imgbackground_file(self,**kwargs):
        filename=filedialog.asksaveasfilename(
            filetypes=ALL_EXTENSIONS,**kwargs
        )
        if filename!="":
            try:
                img=cv2.imread(filename,)
                if not img  is None:
                    #get one chanal from the image
                    mask=img.copy()[:,:,0]
                    mask[:]=255
                    self.import_img_back_ground(Img_cv(img,mask))
                else:
                    messagebox.showerror(str("FATAL ERROR"))
            except Exception as e:
                messagebox.showerror(str(e))
    def corr_background(self,box,imgcv):
        b=self.clamp_box(box)
        return cv2.resize(imgcv.copy().copy(),(b[2],b[3]),cv2.INTER_AREA)
    
    def corr_keep(self,box,img):
        main_h,main_w=box[2:]
        h,w=img.shape[:2]
        background=img.copy()
        if h>main_h:
            background=resize_img(background,height=main_h)
        h,w=background.shape[:2]
        if w>main_w:
            background=resize_img(background,width=main_w)
        return background
    
    def import_img_back_ground(self,imgcv_obj:Img_cv):
        "ADD unready image to imgbackground"
        h,w=self.imgcv.shape[:2]
        imgcv_obj["background"]=self.corr_keep([0,0,w,h],imgcv_obj["imgcv"])
        w,h=imgcv_obj["background"].shape[:2]
        box=[0,0,w,h]
        self.add_back_image(box,imgcv_obj)
  
    def add_back_image(self,box,imgcv_obj:Img_cv):
        box=self.clamp_box(box)
        imgcv_obj["background"]=self.corr_background(box,imgcv_obj["imgcv"])
        self.imported_backgrounds.append([imgcv_obj,box[:2]])
        return imgcv_obj
    def _background_for_object(self,finalimage,points,current_obj):
        b=self.clamp_box(pts_2_xywh(points))
        result_image=self.corr_background(b,current_obj["imgcv"])
        mask=cv2.resize(current_obj.mask.copy(),(b[2],b[3]),cv2.INTER_AREA).astype(np.bool)
        finalimage[b[1]:b[1]+b[3],b[0]:b[0]+b[2]][mask]=result_image[mask]
        current_obj["background"]=result_image.copy()
        def re_fix_circles(points):
            b=self.clamp_box(pts_2_xywh(points[:4].copy()))
            new_circles=xywh_2_pts(b)
            new_circles.append([b[0]+int(b[2]/2),b[1]+int(b[3]/2)])
            return new_circles
        new_circles=re_fix_circles(points)
        return finalimage,list(new_circles)   
    def finish_addbackGround(self):
        _added_backgrond=self.imgcv.copy()
        for background,pos in self.imported_backgrounds:
            h,w=background["background"].shape[:2]
            points=xywh_2_pts([pos[0],pos[1],w,h])
            _added_backgrond,_=self._background_for_object(_added_backgrond.copy(),points,background)
        self.imgcv=_added_backgrond
from tkinter import *
import numpy as np
import cv2
from pywidgets.tk.Img_editor.side_bar.slider import *

def _donothing(*args,**kwargs):pass

class Frame_erode(Slider_1_Reset):
    def __init__(self,app,mask,target,range=(1,30),**kwargs):
        super().__init__(app,1,range,**kwargs)
        self.mask=mask
        self.target=target
        self.var.trace_add("write",lambda f,s,t:self._minmizer())
    def _minmizer(self):
        self.erode(self.var.get())
    def erode(self,num):
        mask=self.mask.copy()
        kernal=np.ones((num,num))
        result=cv2.erode(self.mask,kernal)
        self.target(result)
        self.mask=mask.copy()
        
class Frame_dilite(Slider_1_Reset):
    def __init__(self,app,mask,target,range=(1,30),**kwargs):
        super().__init__(app,1,range,**kwargs)
        self.mask=mask
        self.target=target
        self.var.trace_add("write",lambda f,s,t:self._minmizer())
    def _minmizer(self):
        self.dialte(self.var.get())
    def dialte(self,num):
        mask=self.mask.copy()
        kernal=np.ones((num,num))
        result=cv2.dilate(self.mask,kernal)
        self.target(result)
        self.mask=mask.copy()
     
class Frame_Close(Slider_1_Reset):
    def __init__(self,app,mask,target,range=(1,30),**kwargs):
        super().__init__(app,1,range,**kwargs)
        self.mask=mask
        self.target=target
        
        self.var.trace_add("write",lambda f,s,t:self._minmizer())
    def _minmizer(self):
        self.close_mask(self.var.get())
    def close_mask(self,num):
        mask=self.mask.copy()
        kernel = np.ones((num,num))
        morph = cv2.morphologyEx(self.mask, cv2.MORPH_CLOSE, kernel)
        self.target(morph)
        self.mask=mask.copy()
        
class Frame_Open(Slider_1_Reset):
    def __init__(self,app,mask,target,range:tuple=(1,30),**kwargs):
        super().__init__(app,1,range,**kwargs)
        self.mask=mask
        self.target=target
        self.var.trace_add("write",lambda f,s,t:self._minmizer())
    def _minmizer(self):
        self.open_mask(self.var.get())
    def open_mask(self,num):
        mask=self.mask.copy()
        kernel = np.ones((num,num))
        morph = cv2.morphologyEx(self.mask, cv2.MORPH_OPEN, kernel)
        self.target(morph)
        self.mask=mask

class Thresholding_Frame(Frame):
    def __init__(self,app,src,target,defult_type=cv2.THRESH_BINARY,*args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.gray=src if len(src.shape) ==2 else cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
        self.target=target
        
        self.value_scale=Slider_2(self,range=(0,255))
        self.value_scale.scale_2.config(from_=0,to=1)
        self.columnconfigure(0,weight=1)
        self.value_scale.grid(row=0,column=0,sticky=NSEW)
        
        self.value_scale._minimer=self._minmizer
    def _minmizer(self):
        self.thresh(*self.value_scale.values())
    def thresh(self,thresh,type:int=None):
        type=type if not type is None else self.value_scale.var_2.get() 
        theresh_img=cv2.threshold(self.gray,thresh,255,type)[1]
        self.target(theresh_img)
        return theresh_img

class Adaptive_Tresh_Frame(Thresholding_Frame): 
    def __init__(self, app, src, target, defult_type=cv2.THRESH_BINARY, *args, **kwargs):
        super().__init__(app, src, target, defult_type=defult_type, *args, **kwargs)
        self.value_scale.scale_1.config(to=30)
    def adaptive_threshold(self, thresh,type:int=None):
        type_var=type if not type is None else self.value_scale.var_2.get()
        theresh_img=cv2.adaptiveThreshold(self.gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,type_var,11,thresh)
        self.target(theresh_img)
        return theresh_img

class Frame_Canny(Slider_2): 
    def __init__(self, app, src, target,range:tuple=(0,255), *args, **kwargs):
        super().__init__(app,range, *args, **kwargs)
        self.gray=cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
        self.target=target
    def _minimer(self):
        super()._minimer()
        self.canny(*self.values())
    def canny(self, thresh, maxthresh):
        theresh_img=cv2.Canny(self.gray,thresh,maxthresh)
        self.target(theresh_img)
        return theresh_img

class Bars_BGR(Slider_3x2):
    def __init__(self, app,imgcv,target, orient=..., range: tuple = ..., **kwargs):
        super().__init__(app=app, orient=orient, range=range, **kwargs)
        self.target=target
        self.imgcv=imgcv
        for scale in [self.side_1,self.side_1,self.side_1]:
            def minmizer():
                Slider_2._minimer(scale)
                self.mask_creator()
            scale._minimer=minmizer
    def values_low_upper(self):
        lower=[]
        upper=[]
        for var in [self.side_1,self.side_2,self.side_3]:
            minv,maxv =var.values()
            lower.append(minv)
            upper.append(maxv)
        return lower,upper
    
    def mask_creator(self,lower=None,upper=None):
        lower =lower if lower is None else np.array(self.values_low_upper()[0], dtype = "uint8")
        upper =upper if upper is None else np.array(self.values_low_upper()[1], dtype = "uint8")
        mask = cv2.inRange(self.imgcv, lower, upper)
        self.target(mask)

class Bars_HSV(Slider_3x2):
    def __init__(self, app,imgcv,target, orient=..., range: tuple = ..., **kwargs):
        super().__init__(app=app, orient=orient, range=range, **kwargs)
        self.target=target
        self.imgcv=cv2.cvtColor(imgcv,cv2.COLOR_BGR2HSV)
        for scale in [self.side_1,self.side_1,self.side_1]:
            def minmizer():
                Slider_2._minimer(scale)
                self.mask_creator()
            scale._minimer=minmizer
    def values_low_upper(self):
        lower=[]
        upper=[]
        for var in [self.side_1,self.side_2,self.side_3]:
            minv,maxv =var.values()
            lower.append(minv)
            upper.append(maxv)
        return lower,upper
    def mask_creator(self,lower=None,upper=None):
        lower =lower if lower is None else np.array(self.values_low_upper()[0], dtype = "uint8")
        upper =upper if upper is None else np.array(self.values_low_upper()[1], dtype = "uint8")
        mask = cv2.inRange(self.imgcv, lower, upper)
        self.target(mask)


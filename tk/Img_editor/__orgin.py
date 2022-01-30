import inspect

from pathlib import Path
from tkinter import *
from pywidgets.tk.Notebook import CusNotebook
import numpy as np
from pycv2.img.utils import *
from tkinter import filedialog
from pykeyboard import keyboard
from pykeyboard.keys import ENTER
ALL_EXTENSIONS=(
    ("ALL","*.*"),("PNG","*.png"),("JPEG",".jpg *.jpeg *.jp2"),("WEB","*.web"),
    ("Portable image","*.pbm *.pgm *.ppm *.pxm *.pnm"),("Windows bitmaps","*.bmp *.dib")
)
def INR(funct,*args,**kwargs):
    func_args = inspect.getargspec(funct).args
    the_dic={}
    for value in kwargs:
        if value in func_args:
            the_dic[value]=kwargs[value]
    return funct(*args,**the_dic)

class Img_cv():
    def __init__(self,imgcv,mask=None,box=None):
        if imgcv is None:
            raise "error in defining opencv image"
        if mask is None:
            mask = np.zeros(imgcv.shape[:2], dtype=np.uint8)
        if box is None:
            box = [0, 0, imgcv.shape[1], imgcv.shape[0]]
        self.imgcv=imgcv
        self.mask=mask
        self.box=box
    def __bool__(self):return True
    def __getitem__(self, name: str):
        return self.__dict__[name]
    def __setitem__(self,k,v):
        setattr(self,k,v)
    def get_keys(self):
        return{"imgcv":self.imgcv.copy(),"mask":self.mask.copy(),"box":self.box.copy()}
    
    def apppend(self,object):
        return object
 
    def __eq__(self, o:np.ndarray):
        return self.imgcv is o
    def clamp_box(self,box):
        return clamp_box(box,self.imgcv)
    def clamp_points(self,points):
            return clamp_points(points,self.imgcv)
    
    def clamp_point(self,pt):
        return clamp_point(pt,self.imgcv)
    def save_imgcv(self,**kwargs):
        filename=filedialog.asksaveasfilename(
            filetypes=ALL_EXTENSIONS,**kwargs
        )
        if filename!="":
            cv2.imwrite(filename,self.imgcv)
    
class Img_editor(Frame,Img_cv):
    def __init__(self,app,imgcv,mask=None,box=None,**kwargs):
        dicttion={}
        for value in inspect.getfullargspec(Frame.__init__).args:
            if value in kwargs:
                dicttion[value]=kwargs[value]
        if not hasattr(self,"mainnotebook"):
            Frame.__init__(self,app,**dicttion)
            Img_cv.__init__(self,imgcv,mask,box)
        self.zoomper=100
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.mainnotebook = CusNotebook(self)
        self.mainnotebook.grid(row=0, column=0, sticky=NSEW)
        #for a cancel button
  
    def __getitem__(self, key: str) :
        if key in Frame.keys(self):
            Frame.__getitem__(self,key)
        else:
            Img_cv.__getitem__(self,key)   
    
    def __setattr__(self, __name: str, __value):
        if __name=="mainnotebook":
            if not hasattr(self,__name):
                return super().__setattr__(__name,__value)
            else:
                return super().__getattribute__(__name)
        else:
            super().__setattr__(__name,__value)
    def _end_target(self,_=None):
        self.cancel()
        self.endtarget()
    
    def entered(self, target):
        self.endtarget=target
        if keyboard.checknow(ENTER):
            self.winfo_toplevel().bind_all("<KeyRelease-Return>",
                                    lambda e: self.winfo_toplevel().bind_all("<Return>", self._end_target))
        else:
            self.winfo_toplevel().bind_all("<Return>",self._end_target)
    #for cnacle button inw widgets
    def cancel(self):
        self._remove_enter_key()
    def _remove_enter_key(self):
        self.unbind_all("<Return>")
        self.unbind_all("<KeyRelease-Return>")
        

EXTENSIONS=[exten.split(".")[1] for _,root in ALL_EXTENSIONS for exten in root.split(" ")]
class EMViwerer(Img_editor):
    def __init__(self, app, imgcv, mask=None, box=None, **kwargs):
        super().__init__(app, imgcv, mask=mask, box=box, **kwargs)
    def show_viwers(self,state=True,colorimgstate=True,**kwargs):
        for var in kwargs:
            setattr(self,var,kwargs[var])
        #putting circles automaticly
        the_dict=self.get_keys()
        #this is for coloring imgcv
        the_dict["colorimgstate"]=colorimgstate
        if state and "circles" not in the_dict:
            the_dict["circles"]=xywh_2_pts(self.box)
            
        title=self.mainnotebook.actived_widget()
        if hasattr(title,"define_image"):
            INR(title.define_image,**the_dict)
    def remove_bind(self):
        self._remove_enter_key()
        for title in self.mainnotebook:
            if hasattr(title.widget,"canvas"):
                bindings=list(title.widget.canvas.bind())
                for binding in bindings:
                    title.widget.canvas.unbind(binding)

        
    
    


import numpy as np
from pycv2.img.utils import * 
from tkinter import filedialog
import inspect
ALL_EXTENSIONS=(
    ("ALL","*.*"),("PNG","*.png"),("JPEG","*.jpg *.jpeg *.jp2"),("WEB","*.web"),
    ("Portable image","*.pbm *.pgm *.ppm *.pxm *.pnm"),("Windows bitmaps","*.bmp *.dib")
)

EXTENSIONS=[".png",".jpg", ".jpeg" ".jp2",".web",".bmp",".dib",".pbm",".pgm",".ppm",".pxm" ,".pnm"]
DEFAULT_SAVE=dict(filetypes=ALL_EXTENSIONS,defaultextension=ALL_EXTENSIONS,)
def INR(funct,*args,**kwargs):
    func_args = inspect.getargspec(funct).args
    the_dic={}
    for value in kwargs:
        if value in func_args:
            the_dic[value]=kwargs[value]
    return funct(*args,**the_dic)

class Img_cv():
    def __init__(self,imgcv,mask=None,points=None):
        if imgcv is None:
            raise "error in defining opencv image"
        if mask is None:
            mask = np.zeros(imgcv.shape[:2], dtype=np.uint8)
        if points is None:
            points = xywh_2_pts([0, 0, imgcv.shape[1], imgcv.shape[0]])
        self.imgcv=imgcv
        self.mask=mask
        self.points=points
    @property
    def box(self):
        """The foo property."""
        return pts_2_xywh(self.points)
    @box.setter
    def box(self, value):
        self.points = xywh_2_pts(value)
    def __getitem__(self, name: str):
        #self.__dict__[name]
        return getattr(self,name)
    def __setitem__(self,k,v):
        
        setattr(self,k,v)
    def get_keys(self):
        return{"imgcv":self.imgcv.copy(),"mask":self.mask.copy(),"points":self.points.copy()}
    
 
    def __eq__(self, o:np.ndarray):
        return self.imgcv is o
    def clamp_box(self,box):
        return clamp_box(box,self.imgcv)
    def clamp_points(self,points):
        return clamp_points(points,self.imgcv)
    
    def clamp_point(self,pt):
        return clamp_point(pt,self.imgcv)
    def save_imgcv(self,**kwargs):
        kwargs=dict(**DEFAULT_SAVE,**kwargs)
        filename=filedialog.asksaveasfilename(**kwargs)
        if filename!="":
            cv2.imwrite(filename,self.imgcv)
    

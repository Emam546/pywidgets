from pycv2.img.utils import rgb_to_hex,hex_to_rgb
from tkinter import *
from PIL import Image,ImageTk
import numpy as np
DEFULT_COLORS=[(255,255,255),(200,200,200),(100,100,100),(70,70,70),(0,0,0),
            (255,0,0),(200,0,0),(100,0,0),(70,0,0),
            (0,255,0),(0,200,0),(0,100,0),(0,70,0),
            (0,0,255),(0,0,200),(0,0,100),(0,0,70),
            (255,0,255),(255,255,0),(0,255,255),
            ]
class Box_color_tracker(Frame):
    def __init__(self,app,target,text=None,width=60,height=60,*args,**kwargs):
        super().__init__(app,*args,**kwargs)
        self.dim=[height,width,3]
        self.last_bg=self["bg"]
        self.target=target
        self.showing_label=Label(self,text,bg=self["bg"])
        self.showing_label.pack(fill=BOTH,expand=YES)
        self._define_color(hex_to_rgb(self["bg"]))
    def _define_color(self,color):
        img=np.zeros(self.dim,"uint8")
        img[:]=color
        self.img=Image.fromarray(img)
        self.img=ImageTk.PhotoImage(self.img)
        
        self.config=self.configure
        self.showing_label.config(bg=rgb_to_hex(*color),image=self.img)
    def configure(self, **cnf):

        if "bg" in cnf:
            if self.last_bg!=cnf["bg"]:
                self.last_bg=cnf["bg"]
                color=list(hex_to_rgb(cnf["bg"]))
                self._define_color(color)
                color.reverse()
                self.target(color)
        if "text" in cnf:
            self.showing_label.config(text=cnf["text"])
            cnf.pop("text")
        super().configure(*cnf) 

class BOXS_COLOR(Frame):
    def __init__(self,app=None,rows=10,columns=3,defult_colors=DEFULT_COLORS,**Kwargs):
        super().__init__(self,**Kwargs)
        self.empty_box
        for row in range(rows):
            for column in range(columns):
                color=(255,255,255)
                if column+(row*columns) in range(len(defult_colors)):
                    color=defult_colors[column+(row*columns)]
                box=Box_color_tracker(self)
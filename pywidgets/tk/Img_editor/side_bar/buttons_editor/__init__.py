from tkinter import *
from PIL import Image,ImageTk
from pycv2.img.utils import newbox
import cv2,numpy as np
import json
import os
__FilePATH=os.path.dirname(__file__)
file=open(__FilePATH+"\\buttonsgrid.json","r")
BUTTON_COFIGURATION=json.load(file)
#it a list with dictionaries childs
for value in BUTTON_COFIGURATION:
    value["image"]=__FilePATH+"\\"+value["image"]
    order=value["order"]
    if type(order)==list:
        for child in order:
            child["image"]=__FilePATH+"\\"+child["image"]
file.close()
file=open(__FilePATH+"\\style.json","r")
STYLE_COFIGURATION=json.load(file)

file.close()
class Button_command(Button):
    def __init__(self,master,order="",*args,**kwargs):
        super().__init__(master,*args,**kwargs)
        self.order=order
class Buttons_Frame(Frame):
    def create(self,app:Widget,buttons:dict=BUTTON_COFIGURATION):
        style=self.style
        index=0
        rows,columns=self.row_colums
        for r in range(rows):
            for c in range(columns):
                if index >=len(buttons):break
                button=buttons[index]
                index+=1
                image=Image.open(button["image"])
                w,h=image.size
                h=self.width
                image=image.resize((self.width,h))
                image=ImageTk.PhotoImage(image)
                self.images.append(image)
                if type(button["order"])==str:
                    if hasattr(self,button["order"]):
                        command=getattr(self,button["order"])
                        button=Button_command(app,order=button["order"],image=image,command=command,**style["button_sidebar"])
                        button.grid(row=r,column=c,**style["button_sidebar.grid"])
        #self._configuration()
    def _configuration(self,):
        style=self.style
        rows,columns=self.row_colums
        index=0
        buttons=self.winfo_children()
        for r in range(rows):
            for c in range(columns):
                if index >=len(buttons):break
                button=buttons[index];index+=1
                
        
    def __init__(self,app,mask,target,box=None,style=STYLE_COFIGURATION,buttonconfigurations:dict=BUTTON_COFIGURATION,row_colums=(2,5),width=35,*args,**kwargs):
        super().__init__(app,*args,**kwargs)
        self.width=width
        self.style=style
        self.images=[]
        self.mask=mask
        self.target=target
        self.box=box
        self.row_colums=row_colums
        self.create(self,buttonconfigurations)
    def betwise_image(self):
        mask=cv2.bitwise_not(self.mask)
        self.target(mask)
    def make_box_thresh(self):
        box=newbox(self.mask,self.box)
        self.target(box=box)
    def clear_mask(self):
        mask=np.zeros_like(self.mask,"uint8")
        self.target(mask=mask)
    def fill_mask_spaces(self,mode=cv2.RETR_TREE):
        contours=cv2.findContours(self.mask,mode,cv2.CHAIN_APPROX_SIMPLE)[0]
        mask=self.mask.copy()
        if len(contours)>=1:
            #print("drawcntors")
            cv2.drawContours(mask, contours, -1, (255), cv2.FILLED)
        self.target(mask=mask)
    def reset_box(self):
        h,w=self.mask.shape[:2]
        b=[0,0,w,h]
        self.target(box=b)
    
     
    

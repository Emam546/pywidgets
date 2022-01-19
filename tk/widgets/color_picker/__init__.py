import os ,sys
__FILE_PATH=os.path.dirname(__file__)+"\\"
sys.path.append(__FILE_PATH)
from color_widgets import Box_color_tracker
from tkinter import *
from tkinter import colorchooser
from pykeyboard import keyboards
from pykeyboard.keys import LEFT_BUTTON_MOUSE
from PIL import Image,ImageTk,ImageGrab
from pycv2.img.utils import rgb_to_hex
import numpy as np
import cv2
import win32api
from win32api import GetSystemMetrics
import re
import time
import pyperclip as pc
from threading import Thread
import numpy as np
key=keyboards()
PHOTO = Image.open(__FILE_PATH+"icons\\copy_icon.png")
WIDTH=GetSystemMetrics(0)
HEIGHT=GetSystemMetrics(1)
def _vaildiation_digits_number(input):
    if input.isnumeric() or input == "":return True                  
    else:return False

class Colored_getting_box(Frame):
    def __init__(self,app,target,fg="black",defult_color="#ffffff",*args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.target=target
        reg=self.winfo_toplevel().register(_vaildiation_digits_number)
        def _track_color(color):
            self.__change()
            self.target(color)

        self.box=Box_color_tracker(self,_track_color,bg=defult_color)
        hex_Code_frame=Frame(self,bg=self["bg"],width=20)
        hex_Code_frame.rowconfigure(0,weight=1)
        box_col=Frame(self,bg=self["bg"],width=200,height=100)
        self.hex_color_var=StringVar()
        self.hex_entry=Entry(hex_Code_frame,font=40,textvariable=self.hex_color_var)
        
        self._copyting_image=PHOTO.resize((20,20))
        self._copyting_image=ImageTk.PhotoImage(self._copyting_image)
        Button(hex_Code_frame,image=self._copyting_image,compound=LEFT,bd=0,command=self._clip_hexcode).grid(row=0,column=1)
        
        Label(box_col,text="R",font=40,justify=CENTER,bg=self["bg"],fg=fg).grid(row=0,column=0)
        Label(box_col,text="G",font=40,justify=CENTER,bg=self["bg"],fg=fg).grid(row=0,column=1)
        Label(box_col,text="B",font=40,justify=CENTER,bg=self["bg"],fg=fg).grid(row=0,column=2)
        self.b_var,self.g_var,self.r_var=StringVar(),StringVar(),StringVar()
        self.r_box=Entry(box_col,width=5,font=10,validate ="key",
                    validatecommand =(reg, '%S'),textvariable=self.r_var,justify=CENTER)
        self.g_box=Entry(box_col,width=5,font=10,validate ="key",
                    validatecommand =(reg, '%S'),textvariable=self.g_var,justify=CENTER)
        self.b_box=Entry(box_col,width=5,font=10,validate ="key", validatecommand =(reg, '%S')
                    ,textvariable=self.b_var,justify=CENTER)

        self.box.pack(pady=6)
        hex_Code_frame.pack(pady=20)
        self.hex_entry.grid(row=0,column=0,sticky=NSEW)
        box_col.pack(padx=30)
        self.r_box.grid(row=1,column=0)
        self.g_box.grid(row=1,column=1,padx=5)
        self.b_box.grid(row=1,column=2)

        self.b_var.trace_add("write", lambda f,s,t:self._change_color())
        self.g_var.trace_add("write", lambda f,s,t:self._change_color())
        self.r_var.trace_add("write", lambda f,s,t:self._change_color())
        self.hex_color_var.trace_add("write",lambda f,s,t:self.hexcolorchanged_changed())
        Button(self,text="change color",command=self.ask_color).pack(pady=10)
        self.pick_color_button=Button(self,text="pick color",command=self.color_screen_picker)
        self.pick_color_button.pack(pady=10)
        self._start_focusing()
    
    def change_color_box(self,color):
        self.box.configure(bg=color[1],text=color[1])
        self.__change()
    
    def hexcolorchanged_changed(self):
        if  self.winfo_toplevel().focus_get()==self.hex_entry:
            hexcolor=self.hex_color_var.get()
            if len(hexcolor)==7:
                match=re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', str(hexcolor))
                if match:
                    self.box.config(bg=hexcolor,text=hexcolor)
    
    def _clip_hexcode(self):
        hexcolor=self.box["bg"]
        pc.copy(hexcolor)

    def color_screen_picker(self):
        if self["bg"]!="blue":
            Thread(target=self.__get_mouse_color).start()
    
    def __get_mouse_color(self):
        self["bg"]="blue"
        key.pressedkey(LEFT_BUTTON_MOUSE)
        last_time=time.time()
        while self.winfo_exists()==1 and self["bg"]=="blue":
            x_root,y_root=self.winfo_toplevel().winfo_x(),self.winfo_toplevel().winfo_y()
            root_width,root_height=self.winfo_toplevel().winfo_width(),self.winfo_toplevel().winfo_height()
            x, y = win32api.GetCursorPos()
            if key.pressedkey(LEFT_BUTTON_MOUSE):
                if time.time()-last_time>0.5:
                    last_time=time.time()
                    continue
                last_time=time.time()
                if self.winfo_toplevel().state()=="normal" and\
                    x in range(x_root,root_width+x_root) and y_root in range(y_root,root_height+y_root):
                    continue 
                
                img=ImageGrab.grab(bbox=(0,0,WIDTH,HEIGHT))
                img_np=np.array(img)
                img_final=cv2.cvtColor(img_np,cv2.COLOR_BGR2RGB)
                b,g,r=img_final[y,x]
                self["bg"]="black"
                self.change_color_box(((r,g,b),rgb_to_hex(r,g,b)))
                break 
        else:key.stop_checking_all()
    
    def ask_color(self):
        self.winfo_toplevel().focus()
        color=colorchooser.askcolor(self.box["bg"])
        if color!=(None,None):
            self.change_color_box(color)
    
    def _change_color(self):
        e=self.winfo_toplevel().focus_get()
        if e not in [self.r_box,self.b_box,self.g_box]:return
        b,g,r=self.b_var.get(),self.g_var.get(),self.r_var.get()
        if b=="":b=0
        if g=="":g=0
        if r=="":r=0
        r,g,b=int(r),int(g),int(b) 
        hex_color=rgb_to_hex(r,g,b)
        self.box.config(bg=hex_color,text=hex_color)

    def __change(self):
        e=self.winfo_toplevel().focus_get()
        if e!=self.hex_entry:
            h=self.box["bg"].lstrip("#")
            color=tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
            if e!=self.r_box:self.r_var.set(int(color[0]))
            if e!=self.g_box:self.g_var.set(int(color[1]))
            if e!=self.b_box:self.b_var.set(int(color[2]))
            self.hex_color_var.set(self.box["bg"])
    def _start_focusing(self):
        if self.winfo_exists()==1:
            self.__change()
            self.winfo_toplevel().after(1000,self._start_focusing)
        else:key.stop_checking_all()

class CoLor_Choser(Frame):
    def __init__(self,app,target,defult_color="#ffffff",*args, **kwargs):
        super().__init__(**kwargs)
    

def main():
    root=Tk()
    def do_nothing(*args,**kwargs):
        pass
    Colored_getting_box(root,do_nothing,bg="black").pack(fill=BOTH,expand=YES)
    root.mainloop()
if __name__=="__main__":
    main()
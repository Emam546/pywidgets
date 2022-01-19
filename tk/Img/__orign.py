from tkinter import *
import cv2
from PIL import Image,ImageTk
WIDTH_O="width"
HEIGHT_O="height"
BOTH_O="BOTH"
DISABLE_O="disable"

class Img(Frame):           
    def __init__(self,app,zoom=100,plusnumber:int=100,*args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.canvas=Canvas(self,bg=self["bg"])
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.canvas.grid(column=0,row=0,sticky=NSEW)
        self.zoom=zoom
        self.plusnum=plusnumber
        self.difference=False
        self.imgtk=None
    def bind(self,key=None,target=None,add=None):
        if key==None:
            return Canvas.bind(self.canvas)
        if target==None:return
        def binding(event):
            event.x=int((event.x/self.zoom)*100)
            event.y=int((event.y/self.zoom)*100)
            target(event)
        Canvas.bind(self.canvas,key,binding,add)
    def canvasx(self,x):
        x=(x*self.zoom)/100
        return ((Canvas.canvasx(self.canvas,x)/self.zoom)*100)   
    def canvasy(self,y):
        y=(y*self.zoom)/100
        return ((Canvas.canvasy(self.canvas,y)/self.zoom)*100)
    def define_image(self,img_cv):
        if self.winfo_exists()==TRUE and not img_cv is None:
            self.canvas.delete("all")
            if len(img_cv.shape)==2:
                img_cv=cv2.cvtColor(img_cv,cv2.COLOR_GRAY2BGR)
            elif img_cv.shape[2]==4:
                img_cv=cv2.cvtColor(img_cv,cv2.COLOR_BGRA2BGR)
            img=cv2.cvtColor(img_cv,cv2.COLOR_BGR2RGB)
            
            self.imgPI=Image.fromarray(img)
            
            self.resized()
    def resized(self):
        w,h=self.imgPI.size
        h=int((self.zoom*h)/100)
        w=int((self.zoom*w)/100)
        img= self.imgPI.resize((w,h))
        self.imgtk = ImageTk.PhotoImage(image=img)
        h,w=self.imgtk.height(),self.imgtk.width()
        self.canvas.create_image(0,0,image=self.imgtk,anchor=NW)
        self.difference=True
        self.canvas.config(scrollregion=(0,0,w+self.plusnum,h+self.plusnum))
        
    def zoomprecent(self,zoom):
        self.zoom=zoom
        self.resized()
        
class Img_with_scrollbar(Img):
    def __init__(self,app=None,*args,**kwargs):
        super().__init__(app,*args,**kwargs)
        vscroll=self.vscroll=Scrollbar(self,command=self.canvas.yview)
        hscroll=self.hscroll=Scrollbar(self,orient=HORIZONTAL,command=self.canvas.xview)
        self.canvas.config(xscrollcommand=hscroll.set, yscrollcommand=vscroll.set)
        
        self.bind("<Configure>",lambda e:self.configuration())
    def configuration(self):
        if self.imgtk==None:return
        w,h=self.imgtk.width()+100,self.imgtk.height()+100
        cw,ch=self.canvas.winfo_width(),self.canvas.winfo_height()
        if w>cw :
            if self.hscroll.winfo_ismapped()!=1:
                self.hscroll.grid(column=0,row=1,sticky="sew",columnspan=2)
        else:self.hscroll.grid_forget()
        if h>ch :
            if self.vscroll.winfo_ismapped()!=1:
                self.vscroll.grid(column=1,row=0,sticky=NSEW)
        else:self.vscroll.grid_forget() 
    def resized(self):
        super().resized()
        self.configuration()
class Image_with_slider(Img_with_scrollbar):
    def add_track_bar(self,obj,__name,__value:int=0,range=(0,100),*args,**kwargs):
        #array of setiing attributes of the slider
        #each value is a dictionary of name and defult value and defult range
        
        #setting slider in the Frame

        int_var=IntVar()
        def __update():
            setattr(obj,__name,int_var.get())
        self.add_tracker(int_var,range,*args,**kwargs)
        int_var.set(__value)
        int_var.trace_add("write",lambda *args:__update())
        #to be abled to stihc in the botton
        self.rowconfigure(self.grid_size()[1],weight=1)
    def add_tracker(self,int_var:IntVar,range=(0,100),*args,**kwargs):
        _scaler=Scale(self,variable=int_var,from_=range[0],to=range[1],orient=HORIZONTAL,*args,**kwargs)
        _grid_row=max(2,self.grid_size()[1])
        _scaler.grid(row=_grid_row,column=0,sticky="sew")
        self.rowconfigure(_grid_row,weight=1)

        
def the_right_value(dim,dim2):
    w,h=dim
    cw,ch=dim2
    return int((h*cw)/ch),int((w*ch)/cw)     
class Resized_with_image(Img_with_scrollbar):
    def __init__(self, app=None,orinet=WIDTH_O,out=False, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.orient=orinet
        self.out=out
    def define_image(self,img_cv,orient=None):
        if orient in [WIDTH_O,HEIGHT_O,BOTH_O,DISABLE_O]:
            self.orient=orient
        super().define_image(img_cv)
        
    def width(self,dim):
        w,h=dim
        cw,ch=self.canvas.winfo_width(),self.canvas.winfo_height()
        return w,int((w*ch)/cw)
    def height(self,dim):
        w,h=dim
        cw,ch=self.canvas.winfo_width(),self.canvas.winfo_height()
        return int((h*cw)/ch),h
    
    def resized(self):
        if self.orient==WIDTH_O:
            w,h=self.width(self.imgPI.size)  
        elif self.orient==HEIGHT_O:
            w,h=self.width(self.imgPI.size)
        elif self.orient==BOTH_O:
            w,h=self.canvas.winfo_width(),self.canvas.winfo_height()
        else:
            w,h=self.imgPI.size
        if not self.out:
            cw,ch=self.canvas.winfo_width(),self.canvas.winfo_height()
            if cw<w:
                w=cw
                h=the_right_value((w,h),(cw,ch))[1]
            if ch<h:
                h=ch
                w=the_right_value((w,h),(cw,ch))[0]
        h=int((self.zoom*h)/100)
        w=int((self.zoom*w)/100)
        img= self.imgPI.resize((w,h))
        
        self.imgtk = ImageTk.PhotoImage(image=img)
        h,w=self.imgtk.height(),self.imgtk.width()
        self.canvas.create_image(0,0,image=self.imgtk,anchor=NW) 
        self.canvas.config(scrollregion=(0,0,w+self.plusnum,h+self.plusnum))
        self.configuration()
    def stop(self):
        self.recording=False

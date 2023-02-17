from functools import partial
import os
import json
from tkinter import *
from PIL import Image,ImageTk
__FilePATH=os.path.dirname(__file__)
CANCEL_BUTTON_COFIGURATIONS=[
    {
        "image":"icons\\enter_button.png",
        "order":"_end_target"
    },
    {
        "image":"icons\\cancel.png",
        "order":"cancel"
    }
]
file=open(__FilePATH+"\\buttonsgrid.json","r")
BUTTON_COFIGURATION=json.load(file)
for diction in [BUTTON_COFIGURATION,CANCEL_BUTTON_COFIGURATIONS]:
    for value in diction:
        
        value["image"]=__FilePATH+"\\"+value["image"]
        order=value["order"]
        if type(order)==list:
            for child in order:
                child["image"]=__FilePATH+"\\"+child["image"]
file.close()
file=open(__FilePATH+"\\style.json","r")
STYLE_COFIGURATION=json.load(file)
file.close()


class frame_poped_up(Frame):
    def __init__(self,app:Widget,*args,**kwargs):
        super().__init__(app.winfo_toplevel(),*args,**kwargs)
        def check(event):
            if event.widget not in self.winfo_children():
                self.place_forget()
        
        self.bind_all("<Button-1>",check,add="+")
    def popup(self,x,y):
        self.place(anchor=NW,x=x,y=y)

class buttonpoped(frame_poped_up):
    def __init__(self,app:Widget,*args,**kwargs):
        self.button=b=Label(app,*args,**kwargs)
        super().__init__(app.winfo_toplevel(),bg=b["bg"])
        def check(event):
            if event.widget!=self.button:
                self.place_forget()
        self.bind_all("<Button-3>",check,add="+")
        self.button.bind("<Button-3>",lambda e:self.poped_menu())
    def grid(self,*args,**kwargs):
        self.button.grid(*args,**kwargs)
    def pack(self,*args,**kwargs):
        self.button.pack(*args,**kwargs)    
    def poped_menu(self):
        def right_pos(widget:Widget):
            x,y=widget.winfo_x(),widget.winfo_y()
            root=widget.winfo_toplevel()
            parent=widget.nametowidget(widget.winfo_parent())
            while root!=parent:
                x+=parent.winfo_x()
                y+=parent.winfo_y()
                parent=widget.nametowidget(parent.winfo_parent())
            return x,y
        x,y=right_pos(self.button)
        x+=self.button.winfo_width()
        self.popup(x,y)
    def define_button(self,button,command):
        self.place_forget()
        (lambda :self.winfo_toplevel().tk.call(command))()
        #self.button["image"]=button["image"]
        #self.button["command"]=command
        #self.button["text"]=button["text"]
    def update(self):
        for btn in self.winfo_children():
            btn.config( 
                command=partial(self.define_button,btn,btn["command"])
            )
class Button_command(Button):
    def __init__(self,master,order="",*args,**kwargs):
        super().__init__(master,*args,**kwargs)
        self.order=order
            
class Buttonsmenu(Frame):
    def create(self,app:Widget,imgeditor,buttons:dict=BUTTON_COFIGURATION):
        style=self.style.copy()
        grid=style.pop("grid")
        for button in buttons:
            image=Image.open(button["image"])
            w,h=image.size
            #h=int((self.width*h)/w)
            h=self.width
            image=image.resize((self.width,h))
            image=ImageTk.PhotoImage(image)
            if image not in self.images:
                self.images.append(image)
            
            if type(button["order"])==list and \
                 self.__avalible_buttons(imgeditor,button["order"])>0:
                the_button=buttonpoped(app,image=image,**style)
                the_button.grid(row=app.grid_size()[1],**grid)
                self.create(the_button,imgeditor,button["order"])
                the_button.update()
            elif type(button["order"])==str:
                if hasattr(imgeditor,button["order"]):
                    command=getattr(imgeditor,button["order"])
                    Button_command(app,order=button["order"],image=image,command=command,**style).grid(
                        row=app.grid_size()[1],**grid
                    )
    
    @staticmethod 
    def __avalible_buttons(imgeditor,buttons):
        count=0
        for button in buttons:
            if type(button["order"])==list:
                count+=Buttonsmenu.__avalible_buttons(imgeditor,buttons)
            elif type(button["order"])==str:
                if hasattr(imgeditor,button["order"]):  
                    count+=1    
        return count    
            
    def re_create(self,imgeditor,buttons:dict=BUTTON_COFIGURATION):
        for widg in self.winfo_children():
            widg.destroy()
        self.create(self,imgeditor,buttons=buttons)
        self.update()
    def __init__(self,app,style:dict=STYLE_COFIGURATION,width=35,*args,**kawrgs):
        super().__init__(app,*args,**kawrgs)
        self.images=[]
        self.width=width
        self.style=style

class Active_Cancel_Button(Frame):
    def create(self,app:Widget,imgeditor,buttons:dict=CANCEL_BUTTON_COFIGURATIONS):
        style=self.style.copy()
        style.pop("grid")
        for button in buttons:
            image=Image.open(button["image"])
            w,h=image.size
            #h=int((self.width*h)/w)
            h=self.width
            image=image.resize((self.width,h))
            image=ImageTk.PhotoImage(image)
            if image not in self.images:
                self.images.append(image)
            if type(button["order"])==str:
                if hasattr(imgeditor,button["order"]):
                    command=getattr(imgeditor,button["order"])
                    Button_command(app,order=button["order"],image=image,command=command,**style)
                else:
                    print(button["order"])
    def re_create(self,imgeditor,buttons:dict=CANCEL_BUTTON_COFIGURATIONS):
        for widg in self.winfo_children():
            widg.destroy()
        self.create(self,imgeditor,buttons=buttons)
        self.update()
    def __init__(self,app,style:dict=STYLE_COFIGURATION,width=35,*args,**kawrgs):
        super().__init__(app,*args,**kawrgs)   
        self.images=[]
        self.width=width
        self.style=style
    def active_state(self,state):
        style=self.style.copy()
        grid=style.pop("grid")
        if state:
            for child in self.winfo_children():
                if not child in self.grid_slaves():
                    child.grid(row=self.grid_size()[1],**grid)
        else:
            for child in self.winfo_children():
                 child.grid_forget()


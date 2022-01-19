from pathlib import WindowsPath
from tkinter import *
from PIL import Image,ImageTk
import os
FILE_PATH=os.path.dirname(__file__)+"\\"
MENU_IMAGE=Image.open(FILE_PATH+"icons\\menu bar.png").resize((20,20))
SAVE_IMAGE=Image.open(FILE_PATH+"icons\\save.png").resize((20,20))
PLUS_IMAGE=Image.open(FILE_PATH+"icons\\plus.png").resize((20,20))
PLUS_IMAGE=Image.open(FILE_PATH+"icons\\plus.png").resize((20,20))
                                                             
                              
class title_bar(Frame):
    def __init__(self,app,*args,**kwars):
        super().__init__(app,*args,**kwars)
        self.menubar=ImageTk.PhotoImage(image=MENU_IMAGE)
        self.plusimage=ImageTk.PhotoImage(image=PLUS_IMAGE)
        self.save_image=ImageTk.PhotoImage(image=SAVE_IMAGE)
        
        self.btn_menu=Button(self,bd=0,image=self.menubar,bg=self["bg"],activebackground=self["bg"])
        self.lab_title=Label(self,text="title",bd=0,bg=self["bg"],foreground="black")
        self.btn_downloud=Button(self,bd=0,image=self.save_image,bg=self["bg"],activebackground=self["bg"])
        
        self.big_container=Frame(self,bg=self["bg"])
        self.controlling_frame=Frame(self.big_container,bg=self["bg"])
        self.controlling_frame.pack()
        
        self.lab_page=Label(self.controlling_frame,text="10/12",bd=0,bg=self["bg"],foreground="black",font="microsoft 15")
        self.btn_plus=Button(self.controlling_frame,bd=0,image=self.plusimage,bg=self["bg"],activebackground=self["bg"])
        self.lab_precent=Label(self.controlling_frame,text="80%",bd=0,bg=self["bg"],foreground="black",width=7,font="microsft 15")
        self.btn_minus=Button(self.controlling_frame,bd=0,image=self.plusimage,bg=self["bg"],activebackground=self["bg"])
        
        self.lab_page.grid(row=0,column=0)
        self.btn_plus.grid(row=0,column=1)
        self.lab_precent.grid(row=0,column=2)
        self.btn_minus.grid(row=0,column=3)
        
        #self.columnconfigure(0,weight=1)
        self.columnconfigure(2,weight=1)
        self.btn_menu.grid(row=0,column=0,sticky="nsw")
        self.lab_title.grid(row=0,column=1,sticky="nsw")
        self.big_container.grid(row=0,column=2,sticky=NSEW)
        self.btn_downloud.grid(row=0,column=3)
 
    def confing_dim(self):
        width=self.winfo_width()

if __name__=="__main__":
    root=Tk()

    root.geometry("100x100+200+400")
    tile_bar=title_bar(root,bg="white")
    tile_bar.pack(fill=X,expand=YES,side=TOP)


    
    root.mainloop()
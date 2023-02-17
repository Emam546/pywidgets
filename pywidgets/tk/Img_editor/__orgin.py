from tkinter import Frame,NSEW
from pycv2.img.utils import *
from pykeyboard import keyboard
from pykeyboard.keys import ENTER
from pywidgets._imgcv_objects.__origin import Img_cv,INR
from pywidgets.tk.Notebook import CusNotebook
import inspect
class CustomActive_Notebook(CusNotebook):
    def __init__(self, app, delet=True, extra=True, style={}, destyle={}, **kwargs):
        super().__init__(app, delet, extra, style, destyle, **kwargs)
        self.targets=[]
    def _active(self, title=None):
        super()._active(title)
        for target in self.targets:
            target()

class EMViewer(Frame,Img_cv):
    def __init__(self,app,imgcv,mask=None,points=None,**kwargs):
        
        if not hasattr(self,"mainNoteBook"):
            func_args = inspect.getfullargspec(Frame.__init__).args
            the_dic={}
            for arg in func_args:
                if arg in kwargs:
                    the_dic[arg]=kwargs[arg]
            super().__init__(app,**the_dic)
            Img_cv.__init__(self,imgcv,mask=mask,points=points,)
            self.zoomper=100
            self.rowconfigure(0, weight=1)
            self.columnconfigure(0, weight=1)
            self.mainNoteBook = CustomActive_Notebook(self)
            self.mainNoteBook.grid(row=0, column=0, sticky=NSEW)
        #for a cancel button

    def __getitem__(self, key: str) :
        if key in Frame.keys(self):
            Frame.__getitem__(self,key)
        else:
            Img_cv.__getitem__(self,key)   
    

    
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
        
    def show_viewers(self,state=True,colorImgState=True,**kwargs):
        for var in kwargs:
            #imgcv just for viewing
            if "imgcv"!=var:
                setattr(self,var,kwargs[var])
        #putting circles automatically
        the_dict=self.get_keys()
        #this is for coloring imgcv
        the_dict["colorimgstate"]=colorImgState
        if state and "points" not in the_dict:
            the_dict["points"]=self.points
            
        title=self.mainNoteBook.active_widget()
        if hasattr(title,"define_image"):
            INR(title.define_image,**the_dict)
    def remove_bind(self):
        self._remove_enter_key()
        for title in self.mainNoteBook:
            if hasattr(title.widget,"canvas"):
                bindings=list(title.widget.canvas.bind())
                for binding in bindings:
                    title.widget.canvas.unbind(binding)

        
    
    


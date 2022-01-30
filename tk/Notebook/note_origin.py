from tkinter import *
def clone(widget:Widget,parent:Widget,**kwrgs):
        clone = widget.__class__(parent,**kwrgs)
        for key in widget.keys():
            try:
                if key not in ["class","colormap","container","visual"]:
                    clone[key] = widget.cget(key)
            except Exception as e:print(str(e))
        return clone

class Swithcher_window(Frame,list):
    def __init__(self,app=None,*args,**kwargs):
        super().__init__(app,*args,**kwargs)
        list.__init__(self)
    def getitem(self,widget,parent):
        return clone(widget,parent)
    def add(self,widget:Widget):
        return self.append_item(self.getitem(widget,self))
    def append_item(self,widget: Widget):
        self.append(widget)
        return widget
    def _active(self,widget: Widget):
        for child in self:
            if child is widget:
                #child.widget.pack_forget()
                child.pack()
            else:
                child.pack_forget()
                #child.widget.pack()
                

    def __bool__(self):
        return True
from tkinter import *
SLIDER_STYLE={}
class Scale_reset(Scale):
    def __init__(self,app=None,defult_value=0,variable:IntVar=...,**kwargs):
        super().__init__(app,variable=variable,**kwargs)
        self.defult_value=defult_value
        self.variable=None if variable==... else variable
        def tracker_add(mode,funct):
            def track(*args,**kwargs):
                if self.variable.get()!=defult_value:
                    funct(*args,**kwargs)
            self.variable.__class__.trace_add(self.variable,mode,track)
        if self.variable!=None:
            self.variable.trace_add=tracker_add
        
        self.bind("<ButtonRelease-1>",lambda e:self.reset())
        self.reset()
    
    def reset(self):
        if self.variable is not None:
            self.set(self.defult_value) 
            #self.variable.set(self.defult_value)
        else:
            self.set(self.defult_value) 

    
class Side_bar(Frame):
    def __init__(self,app=None,**kwargs):
        super().__init__(app,**kwargs)

class Slider_1(Frame):
    def __init__(self,app=None,range:tuple=(0,100),orient=HORIZONTAL,**kwargs):
        super().__init__(app,**kwargs)
        self.range=range=dict(from_=range[0],to=range[1])
        self.var=IntVar()
        self.scale=Scale(self,variable=self.var,orient=orient,**range)
        self.scale.pack(fill=X,expand=YES)
class Slider_1_Reset(Frame):
    def __init__(self,app=None,defult_number=0,range:tuple=(0,100),orient=HORIZONTAL,**kwargs):
        super().__init__(app,**kwargs)
        self.range=range=dict(from_=range[0],to=range[1])
        self.var=IntVar()
        self.scale=Scale_reset(self,defult_number,variable=self.var,orient=orient,**range)
        self.scale.pack(fill=X,expand=YES)
class SLider_1_tracker(Slider_1):
    def __init__(self, app, target,range: tuple = (0, 100), orient=HORIZONTAL, **kwargs):
        super().__init__(app=app, range=range, orient=orient, **kwargs)
        self.var.trace_add("write",lambda *args:self._call_back())
        self.target=target
    def _call_back(self):
        self.target(self.var.get())

        
class Slider_2(Frame):
    def __init__(self,app=None,range: tuple=(0,100),orient=HORIZONTAL,**kwargs):
        super().__init__(app,**kwargs)
        self.range=range=dict(from_=range[0],to=range[1])
        self.var_1=IntVar()
        self.var_2=IntVar()
        self.scale_1=Scale(self,orient=orient,variable=self.var_1,**range)
        self.scale_2=Scale(self,orient=orient,variable=self.var_2,**range)
        if orient==HORIZONTAL:
            self.columnconfigure(0,weight=1)
            self.scale_1.grid(row=0,column=0,sticky=NSEW)
            self.scale_2.grid(row=1,column=0,sticky=NSEW)
        else:
            self.rowconfigure(0,weight=1)
            self.scale_1.grid(row=0,column=0,sticky=NSEW)
            self.scale_2.grid(row=0,column=1,sticky=NSEW)
        self.var_1.set(range["from_"])
        self.var_2.set(range["to"])
        self.var_1.trace_add("write",lambda f,s,t:self._minimer())
        self.var_2.trace_add("write",lambda f,s,t:self._minimer())
    def _minimer(self):
        min_num=self.var_1.get()
        max_num=self.var_2.get()
        num=max(self.range["from_"],min(min_num,max_num))
        if min_num>num:
            self.scale_1.set(num)
        self.var_1.set(num)
    def values(self):
        return self.var_1.get(),self.var_2.get()  
class Slider_2V(Frame):
    def __init__(self,app=None,range: tuple=(0,100),orient=HORIZONTAL,**kwargs):
        super().__init__(app,**kwargs)
        self.range=range=dict(from_=range[0],to=range[1])
        self.var_1=IntVar()
        self.var_2=IntVar()
        self.scale_1=Scale(self,orient=orient,variable=self.var_1,**range)
        self.scale_2=Scale(self,orient=orient,variable=self.var_2,**range)
        if orient==HORIZONTAL:
            self.columnconfigure(0,weight=1)
            self.columnconfigure(1,weight=1)
            self.scale_1.grid(row=0,column=0,sticky=NSEW)
            self.scale_2.grid(row=0,column=1,sticky=NSEW)
        else:
            self.rowconfigure(0,weight=1)
            self.rowconfigure(1,weight=1)
            self.scale_1.grid(row=0,column=0,sticky=NSEW)
            self.scale_2.grid(row=1,column=0,sticky=NSEW)
        self.var_1.set(range["from_"])
        self.var_2.set(range["to"])
        self.var_1.trace_add("write",lambda f,s,t:self._minimer())
        self.var_2.trace_add("write",lambda f,s,t:self._minimer())
    def _minimer(self):
        min_num=self.var_1.get()
        max_num=self.var_2.get()
        num=max(self.range["from_"],min(min_num,max_num))
        if min_num>num:
            self.scale_1.set(num)
        self.var_1.set(num)
    def values(self):
        return self.var_1.get(),self.var_2.get()  

class Slider_3x2(Frame):
    def __init__(self,app=None,orient=HORIZONTAL,range:tuple=(0,255),**kwargs):
        super().__init__(app,**kwargs)
        self.side_1=Slider_2V(self,range,orient)
        self.side_2=Slider_2V(self,range,orient)
        self.side_3=Slider_2V(self,range,orient)
        if orient==HORIZONTAL:
            self.columnconfigure(0,weight=1)
            self.side_1.grid(row=0,column=0,sticky=NSEW)
            self.side_2.grid(row=1,column=0,sticky=NSEW)
            self.side_3.grid(row=2,column=0,sticky=NSEW)
        else:
            self.rowconfigure(0,weight=1)
            self.side_1.grid(row=0,column=0,sticky=NSEW)
            self.side_2.grid(row=0,column=1,sticky=NSEW)
            self.side_3.grid(row=0,column=2,sticky=NSEW)
        self.range=range=dict(from_=range[0],to=range[1])
    def values(self):
        values=[]
        for var in [self.side_1,self.side_2,self.side_3]:
            values(var.values())
        return values
    
class SwithchBox(Frame):
    def __init__(self,app,target,defultstate=True,orient=VERTICAL,*args,**kwargs):
        super().__init__(app,*args,**kwargs)
        self.target=target
        self._laststate=defultstate
        self.button_1=Button(self,command=lambda:self._callbackstate(True))
        self.button_2=Button(self,command=lambda:self._callbackstate(False))
        if orient==HORIZONTAL:
            self.rowconfigure(0,weight=1)
            self.button_1.grid(row=0,column=0,sticky=NSEW)
            self.button_2.grid(row=0,column=1,sticky=NSEW)
        else:
            self.columnconfigure(0,weight=1)
            self.button_1.grid(row=0,column=0,sticky=NSEW)
            self.button_2.grid(row=1,column=0,sticky=NSEW)
        self._buttons_state(defultstate)
    def _callbackstate(self,state):
         self._buttons_state(state)
         self.target(state)
    def _buttons_state(self,state):
        self._laststate=state
        if state:
            self.button_1.config(relief=SUNKEN,state=ACTIVE)
            self.button_2.config(relief=RAISED,state=ACTIVE)
        else:
            self.button_1.config(relief=RAISED,state=ACTIVE)
            self.button_2.config(relief=SUNKEN,state=ACTIVE)


def main():
    root=Tk()
    slider=Slider_3x2(root,orient=HORIZONTAL,bg="red")
    slider.pack(fill=BOTH,expand=YES)
    root.mainloop()
def main2():
    root=Tk()
    var=IntVar()
    slider=Scale_reset(root,orient=HORIZONTAL,bg="red",variable=var)
    var.trace_add("write",lambda *args:print(var.get()))
  
    slider.pack(fill=BOTH,expand=YES)
    root.mainloop()
if __name__=="__main__":
    main2()
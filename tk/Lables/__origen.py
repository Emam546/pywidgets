from tkinter import *
class _EXPLORE(Frame,list):
    def __init__(self, app,  *args, **kw):
        super().__init__(app, *args, **kw)
        list.__init__(self)
        self.active_child=None
    def __setitem__(self, k, v):
        if k in Frame.keys(self):
            super().__setitem__(k,v)
        else:
            self.add_item(k,v)
    def _get_item(self,title,**kwargs):
        return Label(self,text=title,**kwargs)
    def _append_child(self,k,frame_container:Label):
        last_column = self.grid_size()[1]
        frame_container.grid(row=last_column,column=0,sticky=NSEW)
        #to insert the same number
        if k in range(len(self)):
            list.__setitem__(self,k,frame_container)
        else:
            list.append(self,frame_container)
        self.disabelall(frame_container)
        return frame_container
    def add_item(self,k:int,value,**kwargs):
        return self._append_child(k,self._get_item(value,**kwargs))

    def __getitem__(self, key: int):
        if key  in range(len(self)):
            return list.__getitem__(self,key)
        else:
            super().__getitem__(key)

    def disabelall(self,excepted=None):
        if excepted in range(len(self)) or excepted in range(-len(self),0):
            #the right number
            self.active_child=self.index(self[excepted])
            return self[excepted]
        elif excepted in self:
            self.active_child=self.index(excepted)
            return excepted
        self.active_child=None
        return 
    def delet_label(self,label:Label):
        self.remove(label)
        label.destroy()
    def __bool__(self):return True
    def __eq__(self, __o: object):
        return super().__eq__(__o)

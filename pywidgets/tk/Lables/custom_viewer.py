from tkinter import *
import os
import ntpath

from pywidgets.tk.func import bind_all_childes
from pywidgets.tk.Lables.__origen import _EXPLORE
from pywidgets.tk.Verticle_Frame import VerticalScrolledFrame
from PIL import ImageTk,Image

FILE_PATH=os.path.dirname(__file__)
RIGHTARROW=Image.open(os.path.join(FILE_PATH,"icons\\go_right.png"))
DOWNARROW=Image.open(os.path.join(FILE_PATH,"icons\\down-arrow2.png"))

class Explorer(_EXPLORE,VerticalScrolledFrame):
    def __init__(self, app, scrolling=False, *args, **kw):
        super().__init__(app, *args, **kw)
        VerticalScrolledFrame.__init__(self,app,scrolling=scrolling,*args,**kw)
        self.interior.columnconfigure(0,weight=1)
        self._lastactive=None
    def _get_item(self,title,**kwargs):
        return Title_Explorebar(self.interior,self,title,True,bd=0,**kwargs)
    def _append_child(self,k,frame_container:Label):
        last_column = self.interior.grid_size()[1]
        frame_container.grid(row=last_column,column=0,sticky=NSEW)
        #to insert the same number
        if k in range(len(self)):
            list.__setitem__(self,k,frame_container)
        else:
            list.append(self,frame_container)
        self.disabelall(frame_container)
        return frame_container
    def add_item(self,k,value,**kwargs):
        item=super().add_item(k,value,**kwargs)
        self.disabelall(item)
        return item
    def disabelall(self,excepted:str=None):
        bar=super().disabelall(excepted)
        _change=self._lastactive!=bar
        if False:
            for label in self:
                if not label is bar:
                    label.disabelall()
            self._lastactive=bar
        
        return bar,_change
        
"""
expanded Frame whcih present number or names of image
"""
class Title_Explorebar(_EXPLORE):
    def _create(self,the_title,rightarrow:Image=RIGHTARROW,downnarrow:Image=DOWNARROW):
        self.iconframe=Label(self.title_frame,compound=LEFT)
        self.text_title=Label(self.title_frame,text=the_title)
        
        self.resized=rightarrow.resize((20,20),Image.ANTIALIAS)
        self.rightarrow = ImageTk.PhotoImage(self.resized)
        
        self.downarrow=downnarrow.resize((20,20),Image.ANTIALIAS)
        self.downarrow = ImageTk.PhotoImage(self.downarrow)
        
        self.iconframe.grid(row=0,column=0,sticky=NE)
        self.text_title.grid(row=0,column=1,sticky=NSEW)

        bind_all_childes(self.iconframe,lambda e:self._hide(),"<Button-1>")
    def recreate(self):
        #getting the name of the path
        the_title=str(ntpath.basename(self.title)).split(".")[0]
        for child in self.title_frame.winfo_children():
            child.destroy()
        #creating the file:
        self._create(the_title)
    def __init__(self,app,parent_title:Explorer,title:str,defultstate=True,
        style_child_active:dict={},style_hover_active:dict={},
        style_child_disable:dict={},style_hover_disabled:dict={},
        *args,**kwargs):
        """title is full path or normal title
        defult state to the frist child added
        """
        super().__init__(app, *args, **kwargs)
        self.title=title
        self.number=0

        self._lastactive=None
        #parent title to disable other unselected images in the scene 
        self.parent=parent_title

        self.style_child_active=style_child_active
        self.style_child_disable=style_child_disable
        self.style_hover_active=style_hover_active
        self.style_hover_disabled=style_hover_disabled
        
        self.rowconfigure(1,weight=1)
        self.columnconfigure(0,weight=1)
        self.title_frame=Frame(self,*args,**kwargs)
        self.containerframe=Frame(self)
        #getting wedget swished out with frame
        self.title_frame.rowconfigure(1,weight=1)
        self.recreate()

        self.state=defultstate
        self.title_frame.grid(row=0,column=0,sticky=NSEW)
        #getting child container frame expand by clicking Frame
       
        self._hide()

    def _hide(self):
        self.state = not self.state
        if self.state:
            self.containerframe.grid(row=1,column=0,sticky=NSEW)
            self.iconframe.config(image=self.downarrow)
        else:
            self.iconframe.config(image=self.rightarrow)
            self.containerframe.grid_forget()

    def disabelall(self,excepted:int=None):
        bar=super().disabelall(excepted)
        _change=self._lastactive!=self.active_child
        if _change:
            for bar in self:
                if bar is bar:
                    bar.config(**self.style_child_active)
                    self.parent.disabelall(self)
                else:
                    bar.config(**self.style_child_disable)
            self._lastactive=self.active_child
        return bar,_change
    def add_item(self,title=None,**kwargs):
        frame=self._get_item(title=title,**kwargs)
        self._append_child(frame)
        self.disabelall(frame)
        #it will be used in installation
        return frame
    
    def _get_item(self,title=None,**kwargs):
        """get origion label to define
           you can change this in your subclass
            """
        title=title if not title is None else str(self.number)
        self.number+=1
        frame_container=Label(self.containerframe,text=str(title),**kwargs)
        return frame_container
    def _append_child(self,frame_container:Label):
        last_column = self.containerframe.grid_size()[1]
        frame_container.grid(row=last_column,column=0,sticky=NSEW)
        #to insert the same number

        list.append(self,frame_container)
        self.disabelall(frame_container)
  
        self._bind_child(frame_container)
        return frame_container
    def _bind_child(self,frame_container):
        def Hovering(enter):
            index=self.index(frame_container)
            if enter:
                frame_container.config(**self.style_hover_active)
            elif self.active_child!=index:
                frame_container.config(**self.style_hover_disabled)
        
        bind_all_childes(frame_container,lambda e:Hovering(True),"<Enter>")
        bind_all_childes(frame_container,lambda e:Hovering(False),"<Leave>")
        bind_all_childes(frame_container,lambda e:self._active_child(frame_container),"<Button-1>")
        return frame_container

    
def main():
    root =Tk()
    the_list=Explorer(root)
    root.columnconfigure(1,weight=1)
    the_list.interior["bg"]="blue"
    the_list["bg"]="blue"
    the_list[0]="Yes"
    the_list[0].add_item("1dfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdfs")
    the_list[0].add_item("2")
    the_list[0].add_item("3")
    the_list[1]="no"
    the_list[1].add_item("3")
    the_list[3]="okey"
    
    
    the_list.grid(row=0,column=0,sticky=NSEW)
    Frame(bg="red").grid(row=0,column=1,sticky=NSEW)
    root.mainloop()
if __name__=="__main__":
    main()
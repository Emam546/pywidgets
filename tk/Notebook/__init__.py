from tkinter import *
from functools import partial
from pywidgets.tk.Notebook.note_origin import Swithcher_window
from pywidgets.tk.Notebook.title_frame import Title,Title_Frame_container
from pywidgets.tk.Notebook.style import *
from pywidgets.tk.func import bind_all_childes
def clone(widget:Widget,parent:Widget,**kwrgs):
        clone = widget.__class__(parent,**kwrgs)
        for key in widget.keys():
            try:
                if key not in ["class","colormap","container","visual"]:
                    clone[key] = widget.cget(key)
            except Exception as e:print(str(e))
        return clone
def checktitle_exist(poped_menu:Menu,title:str):
    if poped_menu.index(END)!=None:
        for i in range(poped_menu.index(END)+1):
                if poped_menu.entrycget(i,'label') == title:
                    return True
    return False
class Title_Notebook(Title):
    def __init__(self, app, title: str,widget, delet_state=False, style={}, destyle={}, hover_style=..., def_hoversetyle=..., *args, **kwargs):
        super().__init__(app, title, delet_state, style=style, destyle=destyle, hover_style=hover_style, def_hoversetyle=def_hoversetyle, *args, **kwargs)
        self.widget=widget
class CusNotebook(Swithcher_window):
    def __init__(self,app,delet=True,extra=True,style={},destyle={}, **kwargs):
        super().__init__(app, **kwargs) 
        self.columnconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)

        self.active_child=True
        

        self.frame_title=Title_Frame_container(self,delet=delet,extra=extra,style=style,destyle=destyle)
        self.add_menu_pope=self.frame_title.add_menu_pope
        self.frame_container=Frame(self)
        
        self.frame_title.rowconfigure(0,weight=1)
        self.frame_title.grid(row=0,column=0,sticky=NSEW)
        self.frame_container.grid(row=1,column=0,sticky=NSEW)
        

        #to fill the frame after removing it all
        self.defult_window=Frame(self.frame_container,bg=self["bg"])
        
    def __bool__(self):
        return True

    
    def _get_title(self,title,widget,**kwargs):
        return Title_Notebook(self.frame_title,title,widget,
            self.frame_title.delet,self.frame_title.style,self.frame_title.destyle,**kwargs)
    def add(self,title:str,widget:Widget,again=False,**style):
        #to enusere the there is no repeate
        if not again:
            similers=[child.widget for child in self if child.title==title]
            if len(similers)>0:
                return similers[0]

        Nwidget=clone(widget,self.frame_container)
        title_frame=self.append_title(self._get_title(title,Nwidget,**style))
        self._active(title_frame)
        return Nwidget
    def append_title(self,title:Title_Notebook):
        self.frame_title.append_title(title,**STICKYNESS_TITLE)
        def remove():
            self._reactive(title)
            self._remove_title(title)
    
        title.button.config(command=remove)
        bind_all_childes(title,lambda e: self._active(title),"<Button-1>",add="")
        title.button.unbind("<Button-1>")
        self.frame_title.add_menu_pope.add_command(label=title.title,command=lambda:self._active(title))
        self.append(title)
        return title
    def _active(self,title=None):
        if self.active_child!=title:
            if title not in self.frame_title.grid_slaves() and title is not None:
                self._return_child(title)
            if title not in self:
                print("not in self")
            for child in self:
                if child is title:
                    child.widget.pack(expand=YES,fill=BOTH)
                else:
                    child.widget.pack_forget()
            self.frame_title._active(title)
        self.active_child=title

    def _return_child(self,title:Title_Notebook):
        self.frame_title._return_child(title)
    def __getitem__(self, key):
        if type(key)==int:
            return list.__getitem__(self,key)
        elif type(key)==str:
            return Frame.__getitem__(self,key)
    

    def set_defult_frame(self):
        self.defult_window.pack(fill=BOTH,expand=YES)
    
    def remove_all(self):
        for child in  self:
            child.remove()
    def _reactive(self,title:Title_Notebook):
        title=self.frame_title._reactive(title)
        
        self._active(title)
        if title is None:
            self.set_defult_frame()
    def _remove_title(self,title:Title_Notebook):
        self.frame_title._remove_title(title)
    def _remove_title_poped_menu(self,title:Title):
        self.frame_title._remove_title_poped_menu(title)

    def allowed(self,widgets:tuple,state=True,essential:tuple=()):
        def _checktitle_exist(title):
            return checktitle_exist(self.add_menu_pope,title)
        active_title=None
        for title in self.frame_title.grid_slaves():
            if title.active:
                active_title=title
        for title in self:  
            if (title.widget in widgets) ==state:
                if title not in self.frame_title.grid_slaves():
                    if not _checktitle_exist(title.title):
                        self.add_menu_pope.add_command(label=title.title,command=partial(self._active,title))
                    if title.widget in essential:
                        self._return_child(title)
            else:
                self._remove_title_poped_menu(title)
                self._remove_title(title)
        active_state=active_title in self.frame_title.grid_slaves()
        if active_state==True:
            self._active(active_title)
            return
        for title in self.frame_title.grid_slaves():
            if title.active:
                active_state=True;break
        if not active_state and len(self.frame_title.grid_slaves()):
            self._active(self.frame_title.grid_slaves()[0])
    
    def active_widget(self,widget:Widget):
        for title in self:
            if title.widget==widget:
                self._active(title)

    def actived_widget(self):
        for title in self:
            if title.active:
                return title.widget   
    def _set_defultwindow(self,widget: Widget):
        self.defult_window.destroy()
        self.defult_window=widget



def main2():
    from pywidgets.tk.Img_editor.__viewers import Viewer
    import numpy as np
    root=Tk()
    img=np.zeros((100,100,3),"uint8")
    img[:,:,0]=255
    frame=Viewer(root,img,bg="red")
    org=frame.mainnotebook._active
    def new_active(title):
        org(title)
        for target in frame.mainnotebook.targets:
            target()
    frame.mainnotebook.targets=[frame.show_viwers]
    frame.mainnotebook._active=new_active
    frame.show_viwers()
    #frame.mainnotebook.allowed((frame.viewer,),True)
    frame.pack(fill=BOTH,expand=YES)

    root.mainloop()
def main():
    root=Tk()
    custom_notebook=CusNotebook(root)
    custom_notebook.add("the title",Frame(bg="red"),)
    custom_notebook.add("the title 2",Frame(bg="green"),)
    custom_notebook.add("the title 3",Frame(bg="yellow"))
    custom_notebook.pack(fill=BOTH,expand=YES)

    root.mainloop()
if __name__=="__main__":
    main2()
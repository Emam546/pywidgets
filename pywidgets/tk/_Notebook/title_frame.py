from tkinter import *
import os,sys
from pathlib import Path
from style import STYLE_TITLE
_pathparent=os.path.dirname(Path(__file__).parent)
sys.path.append(_pathparent)
from func import bind_all_childes
class Title(Frame):
    def __init__(self,app,title:str,delet_state=False,
        style:dict=STYLE_TITLE,destyle:dict=STYLE_TITLE,hover_style={},def_hoversetyle={},
         **kwargs):
        super().__init__(app,  **kwargs)
        self.style=style
        self.destyle=destyle
        self.title=title
        self.last_state=False
        self.active=False
        self.rowconfigure(0,weight=1)
        self.label=Label(self,text=title)
        self.label.grid(row=0,column=0,sticky=NSEW)
        self.button=Button(self,text="X",relief=FLAT)
        if delet_state:
            self.button.grid(row=0,column=1,sticky=E) 
            self.button.bind("<Enter>",lambda e: self._hover_button(True))
            self.button.bind("<Leave>",lambda e: self._hover_button(False))
        self.button.bind("<Button-1>",lambda e: self.state(False),add="+")
        self.state(False)
    def _hover_button(self,enter):
        if  not self.active and  "fg" in self.destyle and "bg" in self.destyle:
            if enter:
                self.button["fg"]=self.destyle["fg"]
            else:
                self.button["fg"]=self.destyle["bg"] 
    def state(self,select):
        if self.active!=select:
            applied_style=self.style if select else self.destyle
        
            for child in self.winfo_children()+[self]:
                for key in applied_style:
                    if key in child.keys():
                        child[key]=applied_style[key]
            self.active=True
        self._hover_button(False)

class Title_Frame_container(Frame,list):
    def __init__(self,app,delet=True,extra=True,style:dict=STYLE_TITLE,destyle={},**kwargs):
        super().__init__(app,**kwargs)  
        list.__init__(self)
        self.style=style
        self.destyle=destyle
        #setting delet choice to the Title of the notebook
        self.delet=delet
        #pipong menu of adding after deleting the title frame
        self.extra=extra

        if extra:
            self.add_menu_pope=Menu(self.winfo_toplevel(),bd=0,activebackground="blue",bg=self["bg"],tearoff=False)
            self.bind("<Button-3>",lambda e:self.pop_menu())
    def pop_menu(self):
        if self.extra:
            self.add_menu_pope.tk_popup(self.winfo_pointerx(),self.winfo_pointery())
    def _get_item(self,title,**kwargs):
        
        return Title(self,title,self.delet,self.style,self.destyle,**kwargs)
    def _active(self,title:Title):
        for title_child in self:
            if title_child is title:
                title.state(True)
            else:
                title.state(False)
    def append_title(self,title_frame:Title,**kwargs):
        def remove():
            title_frame.active=False
            title_frame.grid_forget()
            self._reactive(title_frame)
        title_frame.button.config(command=remove)
        # title_frame.bind("<Button-1>",lambda e: self._active(title_frame),add="+")
        # title_frame.label.bind("<Button-1>",lambda e: self._active(title_frame),add="+")
        bind_all_childes(title_frame,lambda e: self._active(title_frame),"<Button-1>")
        bind_all_childes(title_frame,lambda e:self.pop_menu(),"<Button-3>",)
        

        last_column = len(self)
        title_frame.grid(column=last_column,row=0,**kwargs)
 
        self.append(title_frame)
        return title_frame
    def __getitem__(self, key: str):
        if key in self.keys():
            super().__getitem__(key)
        else:
            list.__getitem__(self,key)
    def _reactive(self,title:Title):
        cor=self.index(title)
        index=self.index(title)-1
        index=max(0,min(index,len(self)-1))
        if index==cor:
            index=self.index(title)+1
            index=max(0,min(index,len(self)-1))
        if self[index] in self.grid_slaves(row=0):
            self._active(self[index])
            return self[index]
        return None
    def _remove_title(self,title:Title):
        title.grid_forget()
        title.state(False)  
    def add_item(self,title:str,**kwargs):
        return self.append_title(self._get_item(title,**kwargs))
    def _remove_title_poped_menu(self,title:Title):
        if self.add_menu_pope.index(END)!=None:
            for i in range(self.add_menu_pope.index(END)+1):
                if self.add_menu_pope.entrycget(i,'label') == title.title:
                    self.add_menu_pope.delete(title.title) 
    def __bool__(self):return True

def main():
    root=Tk()
    title=Title_Frame_container(root,extra=True,delet=False)
    title.add_item("fish")
    title.add_item("the root 2")
    title.add_item("the root 3")
    title.add_item("the root 4")
    title.pack(fill=BOTH,expand=YES)
    root.mainloop()
if __name__=="__main__":
    main()  
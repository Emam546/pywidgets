from tkinter import *
import sys,os
sys.path.append(os.path.dirname(__file__))
from func import *

class VerticalScrolledFrame(Frame):
    def __init__(self, parent,scrolling=False, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)            
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        self._vscrollbar = Scrollbar(self, orient=VERTICAL,bg=self["bg"],bd=0
                            ,activebackground=self["bg"])
        self._vscrollbar.grid(row=0,column=1,sticky=NSEW)
        self.canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=self._vscrollbar.set,bg=self["bg"])
        
        self.canvas.grid(row=0,column=0,sticky=NSEW)
        self._vscrollbar.config(command=self.canvas.yview)

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the self.canvas which will be scrolled with it
        self.interior = interior = Frame(self.canvas,bg=self["bg"],)
        self._interior_id = self.canvas.create_window(0, 0, window=interior,
                                           anchor=NW)
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        if scrolling:
            self.winfo_toplevel().after(
                3000,lambda: bind_all_childes(self,_on_mousewheel,"<MouseWheel>")
            )
            self.winfo_toplevel().after(
                3000,lambda: bind_all_childes(self.interior,_on_mousewheel,"<MouseWheel>")
            )
            
            #self.canvas.bind_all(, _on_mousewheel)
        # track changes to the self.canvas and frame width and sync them,
        # also updating the scrollbar
        
        interior.bind('<Configure>',lambda e: self._configure_interior())

        self.canvas.bind('<Configure>',lambda e: self._configure_canvas())
    def _configure_canvas(self,event):
        if self._vscrollbar.winfo_exists()==FALSE:
            return
        h= self.interior.winfo_reqheight()
        ch=self.canvas.winfo_height()
        if h>ch:
            self._vscrollbar.grid(row=0,column=1, sticky=NSEW)
        else:
            self._vscrollbar.grid_forget()
            
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.itemconfigure(self._interior_id, width=self.canvas.winfo_width())
        
    def _configure_interior(self):
            if self._vscrollbar.winfo_exists()==FALSE:
                return

            h= self.interior.winfo_reqheight()
            ch=self.canvas.winfo_height()
            if h>ch:
                self._vscrollbar.grid(row=0,column=1, sticky=NSEW)
            else:
                self._vscrollbar.grid_forget()
            
            
            size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
            
            
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
                # update the self.canvas's width to fit the inner frame
                self.canvas.config(width=self.interior.winfo_reqwidth())
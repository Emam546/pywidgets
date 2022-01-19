from tkinter import *
import sys,os
sys.path.append(os.path.dirname(__file__))
from func import *

class VerticalScrolledFrame(Frame):
    def __init__(self, parent,scrolling=False, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)            
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        vscrollbar = Scrollbar(self, orient=VERTICAL,bg=self["bg"],bd=0
                            ,activebackground=self["bg"])
        vscrollbar.grid(row=0,column=1,sticky=NSEW)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set,bg=self["bg"])
        
        canvas.grid(row=0,column=0,sticky=NSEW)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas,bg=self["bg"],)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        if scrolling:
            self.winfo_toplevel().after(
                3000,lambda: bind_all_childes(self,_on_mousewheel,"<MouseWheel>")
            )
            self.winfo_toplevel().after(
                3000,lambda: bind_all_childes(self.interior,_on_mousewheel,"<MouseWheel>")
            )
            
            #canvas.bind_all(, _on_mousewheel)
        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            if vscrollbar.winfo_exists()==FALSE:
                return

            h= interior.winfo_reqheight()
            ch=canvas.winfo_height()
            if h>ch:
                vscrollbar.grid(row=0,column=1, sticky=NSEW)
            else:
                vscrollbar.grid_forget()
            
            
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            
            
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if vscrollbar.winfo_exists()==FALSE:
                return
            h= interior.winfo_reqheight()
            ch=canvas.winfo_height()
            if h>ch:
                vscrollbar.grid(row=0,column=1, sticky=NSEW)
            else:
                vscrollbar.grid_forget()
                
            if interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

    
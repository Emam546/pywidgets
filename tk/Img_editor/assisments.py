from pywidgets._functions import *
from tkinter import Canvas
class Select_box(Select_box):
    def bind(self,canvas:Canvas,pos=(0,0)):
        def correct(event):
            x,y = int(event.widget.canvasx(event.x))+pos[0],int(event.widget.canvasy(event.y))+pos[1]
            Select_box.motion(self,(x,y))
        canvas.bind("<Button-1>",correct)
        canvas.bind("<B1-Motion>",correct)
        canvas.bind("<ButtonRelease-1>",lambda e:self.release())

class Canvas_cut(Canvas_cut) :
    def bind(self,canvas:Canvas):
        def correct(event):
            x,y = int(event.widget.canvasx(event.x)),int(event.widget.canvasy(event.y))
            self.motion([x,y])
        canvas.bind("<B1-Motion>",correct)
        canvas.bind("<Button-1>",lambda e: self.release())   
        canvas.bind("<ButtonRelease-1>",correct)

class Control_Points(Control_Points):
    def bind(self,canvas:Canvas):
        def correct(event,state):
            x,y = int(event.widget.canvasx(event.x)),int(event.widget.canvasy(event.y))
            self.motion([x,y],state)
        canvas.bind("<Button-1>",lambda e:correct(e,True))
        canvas.bind("<ButtonRelease-1>",lambda e:self.release())
        canvas.bind("<B1-Motion>",lambda e:correct(e,True))
        canvas.bind("<Button-3>",lambda e:correct(e,False))
        
class multiy_selected_boxs(multiy_selected_boxs) :
    def bind(self,canvas:Canvas,pos=(0,0)):
        def correct(event):
            x,y = int(event.widget.canvasx(event.x))+pos[0],int(event.widget.canvasy(event.y))+pos[1]
            self.motion((x,y))
        canvas.bind("<Button-1>",correct)
        canvas.bind("<B1-Motion>",correct)
        canvas.bind("<ButtonRelease-1>",lambda e:self.release())
class Object_mover(Object_mover):
    def bind(self,canvas: Canvas):
        def correct(event):
            pos = int(event.widget.canvasx(event.x)),int(event.widget.canvasy(event.y))
            pos=clamp_point(pos,self.croped_objects[0].background)
            self.motion(pos)
        canvas.bind("<ButtonRelease-1>",lambda e:self.release())
        canvas.bind("<B1-Motion>",correct)
        canvas.bind("<Button-2>",correct)
        canvas.bind("<Double-Button-1>",lambda e: self.restore())
class Muilty_box_remover(Muilty_box_remover):
    def bind(self,canvas:Canvas):
        def correct(event,state=True):
            x,y = int(event.widget.canvasx(event.x)),int(event.widget.canvasy(event.y))
            self.motion(clamp_point([x,y],self.resultimg),state)
        canvas.bind("<ButtonRelease-1>",lambda e:self.release())
        canvas.bind("<B1-Motion>",correct)
        canvas.bind("<Button-1>",correct)
        canvas.bind("<Button-3>",lambda e: correct(e,False))
class Adding_edges_background(Adding_edges_background):
    def bind(self,canvas: Canvas):
        def correct(event):
            pos = int(event.widget.canvasx(event.x)),int(event.widget.canvasy(event.y))
            self.motion(pos)
        canvas.bind("<ButtonRelease-1>",lambda e:self.release())
        canvas.bind("<B1-Motion>",correct)
        canvas.bind("<Button-1>",correct)

class Brusher_Use(Brusher_Use):
    def bind(self,canvas:Canvas,pos):
        def correct(event,state):
            x,y = int(event.widget.canvasx(event.x))+pos[0],int(event.widget.canvasy(event.y))+pos[1]
            self.motion((x,y),state)
        canvas.bind("<Button-1>",lambda e:correct(e,True))
        canvas.bind("<B1-Motion>",lambda e:correct(e,True))
        canvas.bind("<Button-3>",lambda e:correct(e,False))
        canvas.bind("<B3-Motion>",lambda e:correct(e,False))
        canvas.bind("<ButtonRelease-1>",lambda e:self.release())
        canvas.bind("<ButtonRelease-3>",lambda e:self.release())
class Cut_Brushing_Reseizing(Cut_Brushing_Reseizing):
    def bind(self,canvas:Canvas,pos):
        def correct(event,state):
            x,y = int(event.widget.canvasx(event.x))+pos[0],int(event.widget.canvasy(event.y))+pos[1]
            self.motion((x,y),state)
        canvas.bind("<Button-1>",lambda e:correct(e,True))
        canvas.bind("<B1-Motion>",lambda e:correct(e,True))
        canvas.bind("<ButtonRelease-1>",lambda e:self.release())
        canvas.bind("<Button-3>",lambda e:correct(e,False))
        canvas.bind("<B3-Motion>",lambda e:correct(e,False))
        canvas.bind("<ButtonRelease-3>",lambda e:self.release())
class Filling_brush_Resizing(Filling_brush_Resizing):
    def bind(self,canvas: Canvas,pos):
        def correct(event,state):
            x,y = int(event.widget.canvasx(event.x))+pos[0],int(event.widget.canvasy(event.y))+pos[1]
            self.motion((x,y),state)
        canvas.bind("<Button-1>",lambda e:correct(e,True))
        canvas.bind("<B1-Motion>",lambda e:correct(e,True))
        canvas.bind("<ButtonRelease-1>",lambda e:self.release())
        canvas.bind("<Button-3>",lambda e:correct(e,False))
        canvas.bind("<B3-Motion>",lambda e:correct(e,False))
        canvas.bind("<ButtonRelease-3>",lambda e:self.release())
class Coloring_brsuh(Coloring_brsuh):
    def bind(self,canvas:Canvas):
        def correct(event,state):
            pos = int(event.widget.canvasx(event.x)),int(event.widget.canvasy(event.y))
            super(Coloring_brsuh,self).motion(pos,state)
        canvas.bind("<Button-1>",lambda e:correct(e,True))
        canvas.bind("<B1-Motion>",lambda e:correct(e,True))
        canvas.bind("<Button-3>",lambda e:correct(e,False))
        canvas.bind("<B3-Motion>",lambda e:correct(e,False))
        canvas.bind("<ButtonRelease-1>",lambda e:super(Coloring_brsuh,self).release())
        canvas.bind("<ButtonRelease-3>",lambda e:super(Coloring_brsuh,self).release())


    
     
    
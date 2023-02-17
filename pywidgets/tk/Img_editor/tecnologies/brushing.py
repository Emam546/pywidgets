from pywidgets.tk.Img_editor.assisments import Cut_Brushing_Reseizing,Filling_brush_Resizing
from pywidgets.tk.Img_editor.__viewers import Img
from pywidgets.tk.Img_editor.__orgin import EMViewer
from tkinter import Canvas
from typing import List,Tuple
class Brush_with_Mask(EMViewer,Cut_Brushing_Reseizing):
    def __init__(self, app, imgcv, mask=None, points=None,radius_brushing=10,radius_selcting=20, **kwargs):
        super().__init__(app=app, imgcv=imgcv, mask=mask, points=points, **kwargs)
        #keeping brush as self to update mask also in viewing
        Cut_Brushing_Reseizing.__init__(self,self.box,None,self.mask,radius_brushing=radius_brushing,radius_selcting=radius_selcting,centerstate=False)
        self.viewers_brushing:Tuple[Img,tuple]=[]
    def bind(self,*args,**kwargs):
        super().bind(*args,**kwargs)
    def define_mask(self):
        self.remove_bind()
        def show_viewer(mask,points):
            points=self.clamp_box(points)
            b=self.box
            self.mask[b[1]:b[1]+b[3],b[0]:b[0]+b[2]]=mask[b[1]:b[1]+b[3],b[0]:b[0]+b[2]]
            self.show_viewers(state=True,mask=self.mask,points=self.points)
        #target of calling back of binding
        self.target=show_viewer
        self.bind_brush()
    def bind_brush(self):
        for viewer,pos in self.viewers_brushing:
            Cut_Brushing_Reseizing.bind(self,viewer.canvas,pos)

class Filling_mask(EMViewer,Filling_brush_Resizing):
    def __init__(self, app, imgcv, mask=None, points=None, radius_selcting=20, **kwargs):
        super().__init__(app, imgcv, mask=mask, points=points,**kwargs)
        Filling_brush_Resizing.__init__(self,self.box,None,self.mask,radius_selcting=radius_selcting,centerstate=False)
        self.viewers_filler:List[Img]=[]
    def define_mask(self):
        self.remove_bind()
        def show_viewer(mask,_=None):
            b=self.box
            self.mask[b[1]:b[1]+b[3],b[0]:b[0]+b[2]]=mask[b[1]:b[1]+b[3],b[0]:b[0]+b[2]]
            self.show_viewers(state=True,mask=self.mask)
        #target of calling back of binding
        self.target=show_viewer
        self.bind_brush()
    def bind_brush(self):
        for viewer,pos in self.viewers_filler:
            Filling_brush_Resizing.bind(self,viewer.canvas,pos)
    def bind(self,*args,**kwargs):
        super().bind(*args,**kwargs)
class Switcher_mask(Brush_with_Mask,Filling_mask):
    def __init__(self, app, imgcv, mask=None, points=None, radius_brushing=10, radius_selcting=20,brushingstate=True, **kwargs):
        super().__init__(app, imgcv, mask=mask, points=points, radius_brushing=radius_brushing, radius_selcting=radius_selcting, **kwargs)
        Filling_mask.__init__(self,app, imgcv, mask=mask, points=points, radius_selcting=radius_selcting, **kwargs)
        self.brushingstate=brushingstate
    #defining mask in the super class
    def motion(self,pos,state):
        if state and not self.brushing:
            self.allow_clikcing=True
            x,y=pos
            index=self._get_grabbing_state(pos)
            if index!=None:
                self.target(self.mask,self.grab_box(pos,index))
            else:
                self.brushing=True
                self.grab=None
                self.target(self.fill_brush([x,y],state),self.box)
        else:
            self.brushing=True
            self.grab=None
            self.target(self.fill_brush(pos,state),self.box)
    def _organize_motion(self,canvas: Canvas,pos,state):
        if not self.brushingstate and canvas in [viewer.canvas for viewer,_ in self.viewers_filler]:
            Filling_mask.motion(self,pos,state)
        else:
            super().motion(pos,state)
    def _bind_child(self,canvas: Canvas,pos):
        def correct(event,state):
            x,y = int(event.widget.canvasx(event.x))+pos[0],int(event.widget.canvasy(event.y))+pos[1]
            self._organize_motion(canvas,(x,y),state)
        canvas.bind("<Button-1>",lambda e:correct(e,True))
        canvas.bind("<B1-Motion>",lambda e:correct(e,True))
        canvas.bind("<ButtonRelease-1>",lambda e:self.release())
        canvas.bind("<Button-3>",lambda e:correct(e,False))
        canvas.bind("<B3-Motion>",lambda e:correct(e,False))
        canvas.bind("<ButtonRelease-3>",lambda e:self.release())
    def bind_brush(self):
        for viewer,pos in self.viewers_filler+self.viewers_brushing:
            self._bind_child(viewer.canvas,pos)
    def release(self):
        Filling_mask.release(self)
        return super().release()
       
    
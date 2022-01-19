import sys,os
sys.path.append(os.path.dirname(__file__))
from brushing import *
from selecting import *
from moving import *
import cv2
class Cut_Brushing_Reseizing(Select_box_circels,Brusher_Use):
    def __init__(self,box,target,mask,radius_brushing=10,radius_selcting=10,centerstate=False):
        super().__init__(box,target,radius_selcting,centerstate)
        Brusher_Use.__init__(self,target,mask,radius_brushing)
        self.brushing=False
     

    def release(self):
        self.brushing=False
        self.grab=None
        self.start_point=None
        self.target(self.mask,self.box)
    def motion(self,pos,state):
        if state and not self.brushing:
            x,y=pos
            index=self._get_grabing_state(pos)
            if index!=None:
                self.target(self.mask,self.grab_box(pos,index))
            else:
                self.brushing=True
                self.grab=None
                self.target(self.brush([x,y],state),self.box)
        else:
            self.brushing=True
            self.grab=None
            self.target(self.brush(pos,state),self.box)

class Filling_brush_Resizing(Select_box_circels):
    def __init__(self, box, target,mask, radius_selcting=10, centerstate=True):
        super().__init__(box, target, radius_selcting=radius_selcting, centerstate=centerstate)
        self.mask=mask
        self.brushing=False
        self.allow_clikcing=True
    def release(self):
        self.brushing=False
        self.allow_clikcing=True
        self.grab=None
        self.target(self.mask,self.box)
    

    def motion(self,pos,state):
        if state and not self.brushing:
            self.allow_clikcing=True
            x,y=pos
            index=self._get_grabing_state(pos)
            if index!=None:
                self.target(self.mask,self.grab_box(pos,index))
            else:
                self.brushing=True
                self.grab=None
                self.target(self.fill_brush([x,y],state),self.box)
        else:
            self.brushing=True
            self.grab=None
            self.target(self.fill_brush(pos,state),self.circles)
    def fill_brush(self,pos,state):
        if self.allow_clikcing:
            new_value=255 if state else 0
            _,mask,_,_=cv2.floodFill(self.mask,None,pos,new_value)
            self.allow_clikcing=False
        else:
            mask=self.mask
        return mask

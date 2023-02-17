import cv2,numpy as np
class Brusher_Use:
    def __init__(self,target,mask,radius_brushing=10):
        self.radius_brushing=radius_brushing
        self.start_point=None
        if len(mask.shape)!=2:
            raise "this is not a mask"
        self.mask=mask
        self.target=target
    def brush(self,pos,state):
        new_value=255 if state else 0
        pt2=self.start_point if not self.start_point is None else pos
        mask=cv2.line(self.mask.copy(),pos,pt2 ,new_value,self.radius_brushing)
        self.start_point=pos
        return mask
    def motion(self,pos,state):
        self.target(*self.brush(pos,state))
    def release(self):
        self.start_point=None
class Coloring_brsuh(Brusher_Use):
    def __init__(self, target, mask,color=(255,255,255),coloerbackground=None, radius_brushing=10):
        super().__init__(target, mask, radius_brushing)
        self.color=color
        if coloerbackground is None:
            h,w=mask.shape[:2]
            coloerbackground=np.zeros((h,w,3),"uint8")
            coloerbackground[:]=self.color
        self.coloerbackground=coloerbackground
    def color_brush(self, pos, state):
        new_value=self.color if state else (0,0,0)
        pt2=self.start_point if not self.start_point is None else pos
        coloerbackground=cv2.line(self.coloerbackground.copy(),pos,pt2 ,new_value,self.radius_brushing)
        return super().brush(pos, state),coloerbackground
    def motion(self,pos,state):
        self.target(*self.color_brush(pos,state))

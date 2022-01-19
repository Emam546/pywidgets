import sys,os
sys.path.append(os.path.dirname(__file__))
from origin import *
class Select_box(Circles):
    def __init__(self, circles,target,radius_selcting=10,centerstate=True):
        super().__init__(circles,centerstate)           
        self.radius_selcting=radius_selcting
        self.grab=None
        self.target=target
    
    def motion(self,pos):
        index=self._get_grabing_state(pos)
        if index!=None:
            self.target(self.grab_box(pos,index))
    def _get_grabing_state(self,pos):
        if not self.grab is None:return self.grab
        return super()._get_grabing_state(pos,self.radius_selcting)
    
    def grab_box(self, pos, index):
        self.grab=index
        return super().grab_box(pos, index)
    def release(self):
        if self.centerstate:
            self.centerpoint()    
        self.grab=None   
        self.target(self.circles)

class Canvas_cut:
    def __init__(self,target,box=[0,0,0,0]):
        self.start_x=0
        self.start_y=0
        self.target=target
        self.box=box
    def release(self):
        self.start_x,self.start_y=(None,None)

    def motion(self,pos):
        if (self.start_x,self.start_y) != (None,None):
            x,y=pos
            pt1=(x,y)
            pt2=(self.start_x,self.start_y)
            x,y=min(pt1[0],pt2[0]),min(pt1[1],pt2[1])
            w,h=max(pt1[0],pt2[0])-x,max(pt1[1],pt2[1])-y
            self.box=(x,y,w,h)
            self.target((x,y,w,h))
        else:
            self.start_x,self.start_y=pos
    

class Select_box_circels(Box):
    def __init__(self, box,target,radius_selcting=10, centerstate=True):
        super().__init__(box, centerstate=centerstate)
        self.grab=None
        self.target=target
        self.radius_selcting=radius_selcting
    def grab_box(self, pos, index):
        self.grab=index
        return super().grab_box(pos, index)
    def release(self):
        self.grab=None
    def _get_grabing_state(self,pos):
        if not self.grab is None:return self.grab
        return super()._get_grabing_state(pos,self.radius_selcting)
    def inside_box(self,pos):
        x,y=pos
        return x in range(self.box[0],self.box[2]+self.box[0]) and y in range(self.box[1],self.box[3]+self.box[1])
    #NO NEDD FOR OTHER FUNCTONS

class Control_boxNp(Circles):
    def __init__(self, circles: list,target):
        super().__init__(circles)
        self.target=target
        self.grab=None

    def motion(self,pos,state):
        x,y=pos
        close=closest_node([x,y],self.circles,maxdistance=20)
        if self.grab!=None:
            close=self.circles[self.grab]
        if state:
            if close is None:
                if len(self.circles)<4:
                    self.circles.append([x,y])
                    self.grab=len(self.circles)-1
            else:
                n=self.circles.index(close)
                self.circles[n]=[x,y]
                self.grab=n   
        #deleting state
        elif not close is None:
            self.grab=None
            n=self.circles.index(close)
            self.circles.pop(n)
        self.target(self.circles)    
    def release(self):
        self.grab=None

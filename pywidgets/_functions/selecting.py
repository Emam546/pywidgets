
from .origin import *
class Select_box(Points):
    def __init__(self, points:list,target,radius_selecting=10,centerState=True):
        super().__init__(points,centerState)           
        self.radius_selecting=radius_selecting
        self.grab=None
        self.target=target
    
    def motion(self,pos):
        index=self._get_grabbing_state(pos)
        if index!=None:
            self.target(self.grab_box(pos,index))
    def _get_grabbing_state(self,pos):
        if not self.grab is None:return self.grab
        return super()._get_grabbing_state(pos,self.radius_selecting)
    
    def grab_box(self, pos, index):
        self.grab=index
        return super().grab_box(pos, index)
    def release(self):
        if self.centerState:
            self.centerpoint()    
        self.grab=None   
        self.target(self.points)

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
    

class Select_box_Points(Box):
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
    def _get_grabbing_state(self,pos):
        if not self.grab is None:return self.grab
        return super()._get_grabbing_state(pos,self.radius_selcting)
    def inside_box(self,pos):
        x,y=pos
        return x in range(self.box[0],self.box[2]+self.box[0]) and y in range(self.box[1],self.box[3]+self.box[1])
    #NO NEED FOR OTHER FUNCTIONS

class Control_boxNp(Points):
    def __init__(self, points: list,target):
        super().__init__(points)
        self.target=target
        self.grab=None

    def motion(self,pos,state):
        x,y=pos
        close=closest_node([x,y],self.points,maxdistance=20)
        if self.grab!=None:
            close=self.points[self.grab]
        if state:
            if close is None:
                if len(self.points)<4:
                    self.points.append([x,y])
                    self.grab=len(self.points)-1
            else:
                n=self.points.index(close)
                self.points[n]=[x,y]
                self.grab=n   
        #deleting state
        elif not close is None:
            self.grab=None
            n=self.points.index(close)
            self.points.pop(n)
        self.target(self.points)    
    def release(self):
        self.grab=None

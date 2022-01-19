from pycv2.img.utils import *
from pycv2.img.roate_img import *
xsame,ysame=[(0,3),(1,2)],[(0,1),(2,3)]
class Circles():
    def __init__(self,circles: list,centerstate=True):
        self.circles=convert_tupel_to_list(circles)
        self.centerstate=centerstate 
    def centerpoint(self):
        pt=center_pts(self.circles)
        if len(self.circles)==4:
            self.circles.append(pt)
        else:
            self.circles[4]=pt
    def _get_grabing_state(self,pos,selecting_area):
   
        if self.centerstate:
            self.centerpoint()
        close=closest_node(pos,self.circles,maxdistance=selecting_area)
        if close!=None:
            return self.circles.index(close)
        return None
    def grab_box(self,pos,index):
        x,y=pos
        if self.centerstate and index==4:
            cx,cy=self.circles[4]
            cenx,ceny=x,y
            #to get hte differenc distance
            dx,dy=cenx-cx,ceny-cy
            for id,pt in enumerate(self.circles):
                self.circles[id]=[pt[0]+dx,pt[1]+dy]
        else:
            for id,same in enumerate([xsame,ysame]):
                for groub in same:
                        if index in groub:
                            for cor in groub:
                                self.circles[cor][id]=[x,y][id]
            if self.centerstate:
                self.centerpoint()
        return self.circles

class Box():
    def __init__(self,box,centerstate=True):
        self.box=box
        self.centerstate=centerstate 
    def _get_grabing_state(self,pos,select_area=999999999):
        x,y=pos
        circles=xywh_2_pts(self.box)
        if self.centerstate:
            circles.append(center_pts(circles))
  
        close=closest_node([x,y],circles,maxdistance=select_area)
  
        if close!=None:
            return circles.index(close)
        
        return None
    
    def grab_box(self,pos,index):
        x,y=pos
        circles=xywh_2_pts(self.box)
        if self.centerstate and index==4:
            cx,cy=circles[4]
            cenx,ceny=x,y
            #to get hte differenc distance
            dx,dy=cenx-cx,ceny-cy
            for id,pt in enumerate(circles.copy()):
                circles[id]=[pt[0]+dx,pt[1]+dy]
        else:
            for id,same in enumerate([xsame,ysame]):
                for groub in same:
                        if index in groub:
                            for cor in groub:
                                circles[cor][id]=[x,y][id]
        self.box=pts_2_xywh(circles)
        return self.box

class Rotated_object:
    def __init__(self,croped_img,theshimg=None):
        self.cropedimg=croped_img
        self.thresh=theshimg if not theshimg is None else np.ones(croped_img.shape[:2],"uint8")
        
    def get_rotated_image(self,background,pos,angle,box=None):
        return rotate_object(pos,self.cropedimg,background,angle,self.thresh,box)

class object_moving(Rotated_object):
    def __init__(self,croped_img,background,theshimg=None):
        super().__init__(croped_img,theshimg)
        self.background=background.copy()
    def get_rotated_image(self,pos,angle,box=None):
        #the original postion not rotated postion
        return super().get_rotated_image(self.background,pos,angle,box=box)

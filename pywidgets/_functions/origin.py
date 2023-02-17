from typing import List
from pycv2.img.utils import *
from pycv2.img.roate_img import *
xsame,ysame=[(0,3),(1,2)],[(0,1),(2,3)]
def getSamePoint(pt: List[int],points: List[list]):
    for i,p in enumerate(points):
        if p[0]==pt[0] and p[1]==pt[1]:
            return i
    return 0
class Points():
    def __init__(self,points: list,centerState=True):
        self.points=points.copy()
        self.centerState=centerState 
    def centerpoint(self):
        pt=center_pts(self.points)
        if(len(self.points)>=5):
            self.points[4]=pt
        else:
            self.points.append(pt)
        return pt
    def _get_grabbing_state(self,pos,selecting_area):
        if self.centerState:
            self.centerpoint()  
        close=closest_node_index(pos,self.points,maxdistance=selecting_area)
        if close!=None:
            return close[0]
        return None
    def grab_box(self,pos,index):
        x,y=pos
        #get center of the box and move it
        if self.centerState and index==4:
            cx,cy=self.centerpoint()
            cenx,ceny=x,y
            #to get hte difference distance
            dx,dy=cenx-cx,ceny-cy
            for id,pt in enumerate(self.points):
                self.points[id]=[pt[0]+dx,pt[1]+dy]
        #not the center of the box so resize the box
        else:
            for id,same in enumerate([xsame,ysame]):
                for group in same:
                        if index in group:
                            for cor in group:
                                self.points[cor][id]=[x,y][id]
            if self.centerState:self.centerpoint()
        return self.points

class Box():
    def __init__(self,box,centerstate=True):
        self.box=box
        self.centerstate=centerstate 
    def _get_grabbing_state(self,pos,select_area=999999999):
        x,y=pos
        points=xywh_2_pts(self.box)
        if self.centerstate:
            points.append(center_pts(points))
        close=closest_node_index([x,y],points,maxdistance=select_area)
        if close!=None:
            return close[0]
        
        return None
    
    def grab_box(self,pos,index):
        x,y=pos
        points=xywh_2_pts(self.box)
        if self.centerstate and index==4:
            cx,cy=points[4]
            cenx,ceny=x,y
            #to get hte difference distance
            dx,dy=cenx-cx,ceny-cy
            for id,pt in enumerate(points.copy()):
                points[id]=[pt[0]+dx,pt[1]+dy]
        else:
            for id,same in enumerate([xsame,ysame]):
                for group in same:
                        if index in group:
                            for cor in group:
                                points[cor][id]=[x,y][id]
        self.box=pts_2_xywh(points)
        return self.box

class Rotated_object:
    def __init__(self,cropped_img,theshimg=None):
        self.cropedimg=cropped_img
        self.thresh=theshimg if not theshimg is None else np.ones(cropped_img.shape[:2],"uint8")
        
    def get_rotated_image(self,background,pos,angle,box=None):
        return rotate_object(pos,self.cropedimg,background,angle,self.thresh,box)

class object_moving(Rotated_object):
    def __init__(self,cropped_img,background,theshimg=None):
        super().__init__(cropped_img,theshimg)
        self.background=background.copy()
    def get_rotated_image(self,pos,angle,box=None):
        #the original position not rotated position
        return super().get_rotated_image(self.background,pos,angle,box=box)

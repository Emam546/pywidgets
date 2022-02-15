from pywidgets.tk.Img_editor.assisments import *
from pywidgets.tk.Img_editor.__viewers import *
from pywidgets.tk.Img_editor.__orgin import EMViwerer,INR
from pywidgets.tk.Img_editor.text_on_img import Text_putter as _Text_putter

from pycv2.img.drawing.box import draw_box_moving
from pycv2.img.textread import get_text_mask
import cv2
from pycv2.img.roate_img import *
from typing import List
from pywidgets.tk.Img_editor.tecnologies.croping import Wrapped_box,Control_box,MAKE_BOX
from pywidgets.tk.Img_editor.tecnologies.brushing import Swithcher_mask,Filling_mask,Brush_with_Mask
from pywidgets.tk.Img_editor.tecnologies.selecting_object import Adding_imgbackground_edges,Control_Select_region


class buttons_detectors(EMViwerer):    
    def detect_text_mask(self):
        b=self.box
        mask=get_text_mask(self.imgcv[b[1]:b[1]+b[3], b[0]:b[0]+b[2]])
        mask = cv2.bitwise_or(
            self.mask[b[1]:b[1]+b[3], b[0]:b[0]+b[2]],mask )
        self.mask[b[1]:b[1]+b[3], b[0]:b[0]+b[2]]=mask
        self.show_viwers()

class Add_background(Background_added):
    class Box(Points):
        def __init__(self, points: list,centerstate):
            super().__init__(points)
            self.center_state=centerstate
    def __init__(self, app=None, imgcv=None, mask=None, points=None,radius_selcting=10,centerstate=True, **kwargs):
        super().__init__(app=app, imgcv=imgcv, mask=mask, points=points, **kwargs)
        self.viewers_importbackground:List[Img]=[]
        self.con_back_box=Select_box(points,None,radius_selcting=radius_selcting,centerstate=centerstate)
    
    def resize_bakcground(self,index):
        current_obj,pos=self.imported_backgrounds[index]
        def define_img(points):
            finalimage,new_circles=self._background_for_object(points,self.imgcv.copy(),current_obj)
            self.con_back_box.points=list(new_circles)
            for viewer in self.viewers_importbackground:
                viewer.define_image(draw_box_moving(finalimage.copy(),new_circles))
            #define position of the background imgcv
            self.imported_backgrounds[index][0]=new_circles[0]
        self.con_back_box.target=define_img
        h,w=current_obj.imgcv.shape[:2]
        box=[pos[0],pos[1],w,h]
        self.con_back_box.points=xywh_2_pts(box)
        for viewer in self.viewers_importbackground:
            self.con_back_box.bind(viewer.canvas)
        define_img(xywh_2_pts(box))
    def mulity_resize_background(self):
        boxs=[]
        for obj,pos in self.imported_backgrounds:
            h,w=obj.background.shape[:2]
            points=xywh_2_pts([pos[0],pos[1],w,h])
            boxs.append(self.Box(points,centerstate=self.con_back_box.centerstate))
        def define_image(boxs=None):
            if boxs is None:
                boxs=current_box.boxs
            #ALL This for updating _imgcv
            if current_box.grab!=None:
                index=len(current_box.boxs)-1
                if current_box.grab[0]!=index:
                    #replaace the item in the end of the list to be grabed frist
                    current_box.boxs.insert(-1,current_box.boxs.pop(current_box.grab[0]))
                    #update imported image bacgroud too
                    self.imported_backgrounds.insert(index,self.imported_backgrounds.pop(current_box.grab[0]))
                    #defining knw graber and keep the box
                    current_box.grab=(index,current_box.grab[1])
                    boxs=current_box.boxs
            the_result_image=self.imgcv.copy()
            for id,box in enumerate(boxs):
                current_obj=self.imported_backgrounds[id][0]
                the_result_image,new_circles=self._background_for_object(the_result_image,box.points,current_obj)
                box.points=new_circles
                the_result_image=draw_rotated_box_img(the_result_image,new_circles)
                #setting new position point
                self.imported_backgrounds[id][1]=new_circles[0]
            for viewer in self.viewers_importbackground:
                viewer.define_image(the_result_image)
        current_box=multiy_selected_boxs(boxs,define_image,self.con_back_box.radius_selcting,)
        for viewer in self.viewers_importbackground:
            current_box.bind(viewer.canvas)

        define_image(boxs)
    
class COLORING_Brush(Viewer_coloredbackground,Coloring_brsuh):
    def __init__(self, app, imgcv, mask=None, points=None, coloerbackground=None, color=(255,255,255), **kwargs):
        super().__init__(app, imgcv, mask, points, coloerbackground, color, **kwargs)
        self.viewers_brushing_coloring:List[Img]=[self.viewer_colored]
    def bind_brush_coloring(self,):
        for viewer in self.viewers_brushing_coloring:
            Coloring_brsuh.bind(self,viewer.canvas)
    def coloring_mode(self):
        self.remove_bind()
        def show_viewer(mask,coloerbackground):
            self.show_viwers(False,mask=mask,coloerbackground=coloerbackground)
        self.target=show_viewer
        show_viewer(self.mask,self.coloerbackground)
        self.bind_brush_coloring()

class Text_putter(EMViwerer,_Text_putter):
    def __init__(self, app, imgcv, mask=None, points=None,radius_selcting=5, **kwargs):
        super().__init__(app, imgcv, mask, points, **kwargs)
        _Text_putter.__init__(self,self.winfo_toplevel(),self.imgcv,self.mask,box=self.box,target=None)
        self.radius_selcting=radius_selcting
        self.viewers_add_text:List[Img]=[]
    def text_mode(self,**kwargs):
        self.remove_bind()
        self.bind_text_viewers()
        
        def get_image(imgcv,mask):
            the_dict={"imgcv":imgcv,"mask":mask}
            for key,img in the_dict.items():
                the_dict[key]=self.draw_img_box(img.copy(),**kwargs)
            for viewer in self.viewers_add_text:
                INR(viewer.define_image,**the_dict)
        _Text_putter.__init__(self,self.winfo_toplevel(),self.imgcv,self.mask,box=self.box,target=get_image)
        def end():
            self.imgcv,self.mask=self._update_images()
        get_image(self.imgcv,self.mask)
        self.entered(end)
        
    def bind_text_viewers(self):
        for viewer in self.viewers_add_text:
            _Text_putter.bind(self,viewer.canvas)
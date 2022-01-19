import os,sys
sys.path.append(os.path.dirname(__file__))
from assisments import *
from __viewers import *
from __orgin import *
from pycv2.img.drawing.box import draw_box_moving
from pycv2.img.textread import get_text_mask,get_img_string
import numpy as np,cv2
THETA=[-90,180,90]

class _Crop_box(EMViwerer):
    def __init__(self, app=None, imgcv=None, mask=None, box=None, **kwargs):
        super().__init__(app=app, imgcv=imgcv, mask=mask, box=box, **kwargs)
        self.viewercropped=self.mainnotebook.add("Croped",Croped_Img(None,bg=self["bg"]))
        self.viewermaskcropped=self.mainnotebook.add("Croped Mask",Croped_mask(None,bg=self["bg"]))
    def _getsimg(self,viewers):
        final_arr=[]
        for obj in viewers:
            pos=[0,0]
            viewer,img=obj[:2]
            if len(obj)==3:
                pos=obj[2]
            if hasattr(self,img):
                final_arr.append(
                    (viewer,getattr(self,img),pos)
                )
            else:
                raise "there is no such a varaible in here"
        return final_arr
    def crop_image(self):
        b = self.box
        the_dict=[[x,z] for x,z in self.get_keys().items() if type(z)==np.ndarray]
        for name,img in the_dict:
            _img=img[b[1]:b[1]+b[3], b[0]:b[0]+b[2]]
            setattr(self,name,_img)
        h,w=self.imgcv.shape[:2]
        self.box=[0,0,w,h]
        return self.imgcv,self.mask
class Control_box(_Crop_box):
    def __init__(self, app=None, imgcv=None, mask=None, box=None,radius_selcting=10,centerstate=True, **kwargs):
        super().__init__(app=app, imgcv=imgcv, mask=mask, box=box, **kwargs)
        self.viewers_controling=[]
        self.control_npbox=Select_box(xywh_2_pts(self.box),None,radius_selcting=10,centerstate=True)
    def control_moving_box(self):
        self.remove_bind()
        viewers = (
            self._getsimg(self.viewers_controling),
            ((self.viewercropped, self.imgcv), (self.viewermaskcropped, self.mask)),
        )
        def define_image(circles=None):
            if circles is None:
                circles=self.control_npbox.circles.copy()
            circles[:4]=self.clamp_points(circles[:4])
            if len(circles)==5:
                circles[4]=self.clamp_point(circles[4])
            self.box=b =self.clamp_box(pts_2_xywh(circles[:4]))
            orgviewer=self.mainnotebook.actived_widget()
            for viewer, img,_ in viewers[0]:
                if orgviewer==viewer:
                    viewer.define_image(img.copy(), circles=circles)
            for viewer, img in viewers[1]:
                if orgviewer==viewer:
                    viewer.define_image(img,box=b)
        
        self.control_npbox.target=define_image
        circles=xywh_2_pts(self.box)
        circles.append(centerbox(self.box))
        self.control_npbox.circles=circles
        for viewer,_,_ in viewers[0]:
            self.control_npbox.bind(viewer.canvas)
        define_image()
    
class MAKE_BOX(_Crop_box):    
    def __init__(self, app=None, imgcv=None, mask=None, box=None,radius_selcting=10,centerstate=True, **kwargs):
        "viewer and img and box"
        super().__init__(app=app, imgcv=imgcv, mask=mask, box=box, **kwargs)
        
        self.viewers_making_box=[]
    def make_box(self):
        self.remove_bind()
        viwerers = (
            self._getsimg(self.viewers_making_box),
            ((self.viewercropped, self.imgcv), (self.viewermaskcropped, self.mask)),
        )
        def defineimg(b=None):
            b=self.canvas_cut.box if  b is None else b
            self.box=b=self.clamp_box(b)
            
            if (b[2]*b[3])==0:return
            self.box=b
            orgviewer=self.mainnotebook.actived_widget()
            pts=xywh_2_pts(b)
            for viewer, img2,_ in viwerers[0]:
                if viewer==orgviewer:
                    img2=img2.copy()
                    if len(img2.shape)==2:
                        img2=cv2.cvtColor(img2.copy(),cv2.COLOR_GRAY2BGR)
                    rectalbleimg=cv2.rectangle(img2.copy(),pts[0],pts[2],(0,0,255),1)
                    viewer.define_image(rectalbleimg)
            for viewer, img2 in viwerers[1]:
                if viewer==orgviewer:
                    viewer.define_image(img2.copy(),box=self.box)
        self.canvas_cut=Canvas_cut(defineimg)
        for viewer, img,_ in viwerers[0]:
            self.canvas_cut.bind(viewer.canvas)
            viewer.define_image(img.copy())

class Wrapped_box(_Crop_box):
    def __init__(self, app=None, imgcv=None, mask=None, box=None,radius_selcting=10,centerstate=True, **kwargs):
        "viewer and img and box"
        super().__init__(app=app, imgcv=imgcv, mask=mask, box=box, **kwargs)
        self.viewers_Wrepped_image=[]
    def make_wrapped_image(self):
        viewers=(
           self._getsimg(self.viewers_Wrepped_image), 
            (
                (self.viewercropped,self.imgcv.copy()),
                (self.viewermaskcropped,self.mask.copy()),
            ),
        )
        

        def update(circles=None):
            circles=self.wrapped_box.circles if circles is None else circles
            circles=self.wrapped_box.circles=self.clamp_points(circles)
            org_viewer=self.mainnotebook.actived_widget()
            circles=organise_pts(circles)
            for viwer,img,_ in viewers[0]:
                if org_viewer==viwer:
                    viwer.define_image(draw_box_moving(img.copy(),circles))
            if len(self.wrapped_box.circles)>=4:
                circles=order_points(np.array(circles))
                for viwer,img in viewers[1]:
                    if org_viewer is viwer:
                        wrapedimg=four_point_transform(img.copy(),circles)
                        viwer.define_image(wrapedimg) 
        circles=xywh_2_pts(self.box)
        self.wrapped_box=Control_boxNp(circles,update)
        for viwer,_,_ in viewers[0]:
            self.wrapped_box.bind(viwer.canvas)
        self.entered(self.define_image_wraped)
        update(circles)
    def define_image_wraped(self):
        if len(self.wrapped_box.circles)==4:
            circles=order_points(np.array(self.wrapped_box.circles))
            for att in self.get_keys():
                the_img=getattr(self,att)
                if type(the_img)==np.ndarray:
                    if len(the_img.shape)>=2:
                        new_value= four_point_transform(the_img, circles)
                        setattr(self,att,new_value)
            h,w=self.imgcv.shape[:2]
            self.box=[0,0,w,h]
            self.remove_bind()

            #for future purpuse
            return True
        return False

class buttons_detectors(EMViwerer):    
    def detect_text_mask(self):
        b=self.box
        mask=get_text_mask(self.imgcv[b[1]:b[1]+b[3], b[0]:b[0]+b[2]])
        mask = cv2.bitwise_or(
            self.mask[b[1]:b[1]+b[3], b[0]:b[0]+b[2]],mask )
        self.mask[b[1]:b[1]+b[3], b[0]:b[0]+b[2]]=mask
        self.show_viwers()

class Add_background(Background_added):
    class Box(Circles):
        def __init__(self, circles: list,centerstate):
            super().__init__(circles)
            self.radisu
            self.center_state=centerstate
    def __init__(self, app=None, imgcv=None, mask=None, box=None,radius_selcting=10,centerstate=True, **kwargs):
        super().__init__(app=app, imgcv=imgcv, mask=mask, box=box, **kwargs)
        self.viewers_importbackground=[]
        self.con_back_box=Select_box(xywh_2_pts(self.box),None,radius_selcting=radius_selcting,centerstate=centerstate)
    
    def resize_bakcground(self,index):
        current_obj,pos=self.imported_backgrounds[index]
        def define_img(circles):
            finalimage,new_circles=self._background_for_object(circles,self.imgcv.copy(),current_obj)
            self.con_back_box.circles=list(new_circles)
            for viewer in self.viewers_importbackground:
                viewer.define_image(draw_box_moving(finalimage.copy(),new_circles))
            #define position of the background imgcv
            self.imported_backgrounds[index][0]=new_circles[0]
        self.con_back_box.target=define_img
        h,w=current_obj.imgcv.shape[:2]
        box=[pos[0],pos[1],w,h]
        self.con_back_box.circles=xywh_2_pts(box)
        for viewer in self.viewers_importbackground:
            self.con_back_box.bind(viewer.canvas)
        define_img(xywh_2_pts(box))
    def mulity_resize_background(self):
        boxs=[]
        for obj,pos in self.imported_backgrounds:
            h,w=obj.background.shape[:2]
            circles=xywh_2_pts([pos[0],pos[1],w,h])
            boxs.append(self.Box(circles,centerstate=self.con_back_box.centerstate))
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
                the_result_image,new_circles=self._background_for_object(the_result_image,box.circles,current_obj)
                box.circles=new_circles
                the_result_image=draw_rotated_box_img(the_result_image,new_circles)
                #setting new position point
                self.imported_backgrounds[id][1]=new_circles[0]
            for viewer in self.viewers_importbackground:
                viewer.define_image(the_result_image)
        current_box=multiy_selected_boxs(boxs,define_image,self.con_back_box.radius_selcting,)
        for viewer in self.viewers_importbackground:
            current_box.bind(viewer.canvas)

        define_image(boxs)
    
class selectregion(Viewer_brushed):
    def __init__(self, app, imgcv, mask=None, box=None, radiusarea=2,radius_selecting=10, flags=..., **kwargs):
        super().__init__(app, imgcv, mask=mask, box=box, radiusarea=radiusarea, flags=flags, **kwargs)
        self.viewers_move=[]
        self.radius_selecting=radius_selecting
    def move_thresh_image(self,rotate_state=False,copy_state=False,**drawing_utilis):
        self.remove_bind()
        b=self.box
        #checking function
        if cv2.countNonZero(self.mask[b[1]:b[1]+b[3],b[0]:b[0]+b[2]])==0:return
        def end():
            self.imgcv,self.mask=mover.result()
            
        mask=self.mask.copy()
        def define_img(resultimg,resultmask):
            the_dict={"imgcv":resultimg,"mask":resultmask}
            for name,img in the_dict.items():
                the_dict[name]=mover.draw_image(img,**drawing_utilis)
            
            for viewer in self.viewers_move:
                INR(viewer.define_image,**the_dict)
        b=newbox(self.mask,self.box)
        mask=np.zeros_like(self.mask,"uint8")
        mask[b[1]:b[1]+b[3], b[0]:b[0]+b[2]] = self.mask[b[1]:b[1]+b[3], b[0]:b[0]+b[2]]
        
        mover=Object_mover(mask,self.imgcv,self.mask,target=define_img,rotate_state=rotate_state,copy_state=copy_state,radius_painting=self.radiusarea,radius_selcting=self.radius_selecting)
        for viewer in self.viewers_move:
            mover.bind(viewer.canvas)
        self.entered(end)
        define_img(*mover.result())
    
    def get_all_rotate_boxs(self,rotate_state=True,copy_state=False):  
        self.remove_bind()
        b=self.box
        mask=np.zeros(self.imgcv.shape[:2],"uint8")
        mask[b[1]:b[1]+b[3], b[0]:b[0]+b[2]]=\
            self.mask[b[1]:b[1]+b[3], b[0]:b[0]+b[2]]

        contours = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]
   
        if len(contours)!=0:
            all_points=[]
            for cnt in contours:
                box=cv2.boundingRect(cnt)
                if len(box)==4:
                    all_points.append(box)
        else:return
        def define_img(resultimg,resultmask):
            the_dict={"imgcv":resultimg,"mask":resultmask}
            for name,img in the_dict.items():
                the_dict[name]=mover.draw_img(img)
            for viewer in self.viewers_move:
                INR(viewer.define_image,**the_dict)
        mover=Muilty_box_remover(self.imgcv,self.mask,all_points,define_img,self.radiusarea,rotate_state,copy_state,self.radius_selecting)
        for viewer in self.viewers_move:
            mover.bind(viewer.canvas)
        define_img(self.imgcv.copy(),mask)
        
        def end():
            self.remove_bind()
            self.imgcv=mover.resultimg
            self.mask=mover.result_mask
        self.entered(end)

    def get_img_string(self):
        b=self.box
        return get_img_string(self.mask[b[1]:b[1]+b[3], b[0]:b[0]+b[2]])

    def makebox_withthresh(self):
        b=self.box
        mask=self.mask.copy()[b[1]:b[1]+b[3], b[0]:b[0]+b[2]]
        box=newbox([0,0,b[2],b[3]],mask)
        box[0]+=b[0];box[1]+=b[1]
        self.box=box
    @staticmethod
    def __getrotateobject(the_img:Img_cv,rotation_type=cv2.ROTATE_90_CLOCKWISE):
        
        h,w=the_img.imgcv.shape[:2]
        center=h//2,w//2
        for var in the_img.get_keys():
            img=getattr(the_img,var)
            if type(img)==np.ndarray:
                setattr(the_img,var,cv2.rotate(img.copy(),rotation_type))
            #getting imported images rotated
            elif var=="imported_backgrounds":
                for i,imgcvopject in enumerate(img):
                    imgcv,pt=imgcvopject
                    selectregion.__getrotateobject(imgcv,rotation_type)
                    img[i][0]=get_rotated_point(center,pt,THETA[rotation_type])
        
        the_img.box=get_rotated_box(the_img.box,THETA[rotation_type],center)
    def rotate_img(self,rotation_type=cv2.ROTATE_90_CLOCKWISE):
        self.__getrotateobject(self,rotation_type)
        


    def move_selected_area(self,rotate_state=True,copystate=False,**drawingutils):
        self.remove_bind()
        b=self.box
        #checking function
        if cv2.countNonZero(self.mask[b[1]:b[1]+b[3],b[0]:b[0]+b[2]])==0:return
        def end():
            self.remove_bind()
            self.imgcv=mover.result_img
            self.mask=mover.result_mask
        
        def define_img(resultimg,resultmask,circles,state):
            the_dict={"imgcv":resultimg,"mask":resultmask}
            
            for name,img in the_dict.items():
                the_dict[name]=mover.draw_image(img,circles,state,**drawingutils)
            for viewer in self.viewers_move:
                INR(viewer.define_image,**the_dict)

        b=self.box
        mask=np.zeros_like(self.mask,"uint8")
        mask[b[1]:b[1]+b[3], b[0]:b[0]+b[2]] = self.mask[b[1]:b[1]+b[3], b[0]:b[0]+b[2]]
       
        mover=Multi_mover_selector(mask,self.imgcv.copy(),define_img,rotate_state,copystate,self.radiusarea)
        the_dict={"imgcv":self.imgcv,"mask":mask,"colorimgstate":False}
        for viewer in self.viewers_move:
            mover.bind(viewer.canvas)
            INR(viewer.define_image,**the_dict)
        self.entered(end)

class Brush_with_Mask(EMViwerer,Cut_Brushing_Reseizing):
    def __init__(self, app, imgcv, mask=None, box=None,radius_brushing=10,radius_selcting=20, **kwargs):
        super().__init__(app=app, imgcv=imgcv, mask=mask, box=box, **kwargs)
        #keeping brush as self to update mask also in viewing
        Cut_Brushing_Reseizing.__init__(self,self.box,None,self.mask,radius_brushing=radius_brushing,radius_selcting=radius_selcting,centerstate=False)
        self.viewers_brushing=[]
    def bind(self,*args,**kwargs):
        super().bind(*args,**kwargs)
    def define_mask(self):
        self.remove_bind()
        def show_viewer(mask,box=None):
            self.box=b=self.clamp_box(box) if not box is None else self.box
            
            self.mask[b[1]:b[1]+b[3],b[0]:b[0]+b[2]]=mask[b[1]:b[1]+b[3],b[0]:b[0]+b[2]]
            self.show_viwers(state=True,mask=self.mask,circels=xywh_2_pts(self.box))
        self.target=show_viewer
        self.bind_brush()
    def bind_brush(self):
        for viewer,pos in self.viewers_brushing:
            Cut_Brushing_Reseizing.bind(self,viewer.canvas,pos)

class Filling_mask(EMViwerer,Filling_brush_Resizing):
    def __init__(self, app, imgcv, mask=None, box=None, radius_selcting=20, **kwargs):
        super().__init__(app, imgcv, mask=mask, box=box,**kwargs)
        Filling_brush_Resizing.__init__(self,self.box,None,self.mask,radius_selcting=radius_selcting,centerstate=False)
        self.viewers_filler=[]
    def define_mask(self):
        self.remove_bind()
        def show_viewer(mask,_=None):
            b=self.box
            self.mask[b[1]:b[1]+b[3],b[0]:b[0]+b[2]]=mask[b[1]:b[1]+b[3],b[0]:b[0]+b[2]]
            self.show_viwers(state=True,mask=self.mask)
        self.target=show_viewer
        self.bind_brush()
    def bind_brush(self):
        for viewer,pos in self.viewers_filler:
            Filling_brush_Resizing.bind(self,viewer.canvas,pos)
    def bind(self,*args,**kwargs):
        super().bind(*args,**kwargs)     
    
class Swithcher_mask(Brush_with_Mask,Filling_mask):
    def __init__(self, app, imgcv, mask=None, box=None, radius_brushing=10, radius_selcting=20,brushingstate=True, **kwargs):
        super().__init__(app, imgcv, mask=mask, box=box, radius_brushing=radius_brushing, radius_selcting=radius_selcting, **kwargs)
        Filling_mask.__init__(self,app, imgcv, mask=mask, box=box, radius_selcting=radius_selcting, **kwargs)
        self.brushingstate=brushingstate
    #defining mask in the super class
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
        
class Adding_imgbackground_edges(EMViwerer):
    def __init__(self, app, imgcv, mask=None, box=None,radius_selecting=10, **kwargs):
        super().__init__(app, imgcv, mask=mask, box=box, **kwargs)
        self.radius_selecting=radius_selecting
        self.viewers_adding_edges=[]
    def add_edges(self,blanck_background=False):
        self.remove_bind()
        def define_img(imgcv,mask):
            the_dict={"imgcv":imgcv,"mask":mask}
            h,w=resizer.result()[0].shape[:2]
            for key,img in the_dict.items():
                cv2.rectangle(img,(0,0),(w+2,h+2),(0,0,255),2)
                the_dict[key]=draw_box_moving(img.copy(),resizer.circle_positions,center_state=True)
                
            for viewer in self.viewers_adding_edges:
                INR(viewer.define_image,**the_dict)
        resizer=Adding_edges_background(self.imgcv,self.mask,target=define_img,blanck_background=blanck_background,radius_selcting=self.radius_selecting)
        def end():
            self.cancel()
            if blanck_background:
                self.imgcv=resizer.result()[0]
                #applying edge mask
                resized_mask=self.mask.copy()
                self.mask=np.zeros(self.imgcv.shape[:2],"uint8")
                self.box=b=pts_2_xywh(resizer.circle_positions[:4])
                resized_block=cv2.resize(resized_mask,(b[2],b[3]))
                self.mask[:]=255
                self.mask[b[1]:b[1]+b[3],b[0]:b[0]+b[2]]=resized_block
            else:
                self.imgcv,self.mask=resizer.result()
        for viewer in self.viewers_adding_edges:
            resizer.bind(viewer.canvas)
        self.entered(end)
        resizer._send()
    #for button gridder
    def add_edges_blankedges(self):
        self.add_edges(True) 

class COLORING_Brush(Viewer_coloredbackground,Coloring_brsuh):
    def __init__(self, app, imgcv, mask=None, box=None, coloerbackground=None, color=(255,255,255), **kwargs):
        super().__init__(app, imgcv, mask, box, coloerbackground, color, **kwargs)
        self.viewers_brushing_coloring=[self.viewer_colored]
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


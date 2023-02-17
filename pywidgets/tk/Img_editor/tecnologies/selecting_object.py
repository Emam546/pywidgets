from pywidgets.tk.Img_editor.__orgin import EMViewer,INR,Img_cv
from pywidgets.tk.Img_editor.assisments import *
from pywidgets.tk.Img import Img
from typing import List
from pywidgets.tk.Img_editor.__viewers import Viewer_brushed
THETA=[-90,180,90]
class Adding_imgbackground_edges(EMViewer):
    def __init__(self, app, imgcv, mask=None, box=None,radius_selecting=10, **kwargs):
        super().__init__(app, imgcv, mask=mask, box=box, **kwargs)
        self.radius_selecting=radius_selecting
        self.viewers_adding_edges:List[Img]=[]
    def add_edges(self,blank_background=False):
        self.remove_bind()
        def define_img(imgcv,mask):
            the_dict={"imgcv":imgcv,"mask":mask}
            h,w=resizer.result()[0].shape[:2]
            for key,img in the_dict.items():
                cv2.rectangle(img,(0,0),(w+2,h+2),(0,0,255),2)
                the_dict[key]=draw_box_moving(img.copy(),resizer.circle_positions,center_state=True)
                
            for viewer in self.viewers_adding_edges:
                INR(viewer.define_image,**the_dict)
        resizer=Adding_edges_background(self.imgcv,self.mask,target=define_img,blanck_background=blank_background,radius_selcting=self.radius_selecting)
        def end():
            self.cancel()
            if blank_background:
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
class Control_Select_region(Viewer_brushed):
    def __init__(self, app, imgcv, mask=None, points=None, radiusarea=2,radius_selecting=10, flags=..., **kwargs):
        super().__init__(app, imgcv, mask=mask, points=points, radiusarea=radiusarea, flags=flags, **kwargs)
        self.viewers_move:List[Img]=[]
        self.radius_selecting=radius_selecting
    def move_thresh_image(self,rotate_state=False,copy_state=False,**drawing_utilis):
        self.remove_bind()
        b=self.box
        #checking function
        if cv2.countNonZero(self.mask[b[1]:b[1]+b[3],b[0]:b[0]+b[2]])==0:return

        mask=self.mask.copy()
        def define_img(resultimg,resultmask):
            the_dict={"imgcv":resultimg,"mask":resultmask}
            for name,img in the_dict.items():
                the_dict[name]=mover.draw_image(img,**drawing_utilis)
            
            for viewer in self.viewers_move:
                INR(viewer.define_image,**the_dict)
        def end():
            self.imgcv,self.mask=mover.result()
            
        b=newbox(self.mask,self.box)
        mask=np.zeros_like(self.mask,"uint8")
        mask[b[1]:b[1]+b[3], b[0]:b[0]+b[2]] = self.mask[b[1]:b[1]+b[3], b[0]:b[0]+b[2]]
        
        mover=Object_mover(mask,self.imgcv,self.mask,target=define_img,rotate_state=rotate_state,copy_state=copy_state,radius_painting=self.radiusArea,radius_selcting=self.radius_selecting)
        for viewer in self.viewers_move:
            mover.bind(viewer.canvas)
        self.entered(end)
        define_img(*mover.result())
        return lambda:define_img(*mover.result())
    def get_all_rotate_boxes(self,rotate_state=True,copy_state=False):  
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
        mover=Muilty_box_remover(self.imgcv,self.mask,all_points,define_img,self.radiusArea,rotate_state,copy_state,self.radius_selecting)
        for viewer in self.viewers_move:
            mover.bind(viewer.canvas)
        define_img(self.imgcv.copy(),mask)
        
        def end():
            self.remove_bind()
            self.imgcv=mover.resultimg
            self.mask=mover.result_mask
        self.entered(end)

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
                    Control_Select_region.__getrotateobject(imgcv,rotation_type)
                    img[i][0]=get_rotated_point(center,pt,THETA[rotation_type])

        the_img.box=get_rotated_box(the_img.box,THETA[rotation_type],center)
    def rotate_img(self,rotation_type=cv2.ROTATE_90_CLOCKWISE):
        return self.__getrotateobject(self,rotation_type)

    def move_selected_area(self,rotate_state=True,copystate=False,**drawingutils):
        self.remove_bind()
        b=self.box
        #checking function
        if cv2.countNonZero(self.mask[b[1]:b[1]+b[3],b[0]:b[0]+b[2]])==0:return
        def end():
            self.remove_bind()
            self.imgcv=mover.result_img
            self.mask=mover.result_mask
        
        def define_img(resultimg,resultmask,points,state):
            the_dict={"imgcv":resultimg,"mask":resultmask}
            for name,img in the_dict.items():
                the_dict[name]=mover.draw_image(img,points,state,**drawingutils)
            for viewer in self.viewers_move:
                INR(viewer.define_image,**the_dict)

        b=self.box
        mask=np.zeros_like(self.mask,"uint8")
        mask[b[1]:b[1]+b[3], b[0]:b[0]+b[2]] = self.mask[b[1]:b[1]+b[3], b[0]:b[0]+b[2]]
       
        mover=Multi_mover_selector(mask,self.imgcv.copy(),define_img,rotate_state,copystate,self.radiusArea)
        the_dict={"imgcv":self.imgcv,"mask":mask,"colorimgstate":False}
        for viewer in self.viewers_move:
            mover.bind(viewer.canvas)
            INR(viewer.define_image,**the_dict)
        self.entered(end)


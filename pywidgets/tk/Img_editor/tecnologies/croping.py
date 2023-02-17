from pywidgets.tk.Img_editor.assisments import *
from pywidgets.tk.Img_editor.__viewers import Croped_Img,Croped_mask,DrawnImg
from pywidgets.tk.Img_editor.__orgin import EMViewer,INR
from typing import List,Tuple
class _Crop_box(EMViewer):
    def __init__(self, app=None, imgcv=None, mask=None, points=None, **kwargs):
        super().__init__(app=app, imgcv=imgcv, mask=mask, points=points, **kwargs)
        self.viewerCropped=self.mainNoteBook.add("Croped",Croped_Img(None,bg=self["bg"]))
        self.viewerMaskCropped=self.mainNoteBook.add("Croped Mask",Croped_mask(None,bg=self["bg"]))
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
    def __init__(self, app=None, imgcv=None, mask=None, points=None,radius_selecting=10, **kwargs):
        super().__init__(app=app, imgcv=imgcv, mask=mask, points=points, **kwargs)
        self.viewers_controlling:List[DrawnImg]=[]
        self.radius_selecting=radius_selecting
    def control_moving_box(self,**style_drawing):
        self.remove_bind()
        viewers:List[DrawnImg] = self.viewers_controlling+[self.viewerCropped ,self.viewerMaskCropped]
        def define_image(points):
            points=self.points if points is None else points
            self.points=points=self.clamp_points(points[:4])
            #cropped #images we need to define box
            the_dict={"imgcv":self.imgcv,"mask":self.mask, "points":points,"box":self.box}
            active_widget=self.mainNoteBook.active_widget()
            for viewer in viewers:
                if active_widget==viewer:
                    INR(viewer.define_image,**the_dict,**style_drawing)
                    return
        control_npBox=Select_box(self.points,define_image,radius_selecting=self.radius_selecting,centerState=True)
        for viewer in self.viewers_controlling:
            control_npBox.bind(viewer.canvas)
        define_image(self.points)
        return lambda:define_image(self.points)
        
class MAKE_BOX(_Crop_box):    
    def __init__(self, app=None, imgcv=None, mask=None, points=None,radius_selcting=10,centerstate=True, **kwargs):
        """viewer and img and thier points cutting"""
        super().__init__(app=app, imgcv=imgcv, mask=mask, points=points, **kwargs)
        
        self.viewers_making_box:Tuple[DrawnImg] =[]
    def make_box(self):
        self.remove_bind()
        viewers = (
            self.viewers_making_box,
            [self.viewerCropped,self.viewerMaskCropped],
        )
        def defineimg(b):
            b=self.clamp_box(b)
            if (b[2]*b[3])==0:return
            self.box=b
            orgViewer=self.mainNoteBook.active_widget()
            the_dict={
                "imgcv":cv2.rectangle(self.imgcv.copy(),self.points[0],self.points[2],(0,0,255),1),
                "mask":cv2.rectangle(cv2.cvtColor(self.mask,cv2.COLOR_GRAY2BGR),self.points[0],self.points[2],(0,0,255),1), 
            }
            for viewer in viewers[0]:
                if viewer==orgViewer:
                    INR(viewer.define_image,**the_dict)
                    return
            #define cutting box for the viewer cutters
            the_dict={"imgcv":self.imgcv,"mask":self.mask,"box":self.box}
            for viewer in viewers[1]:
                if viewer==orgViewer:
                    INR(viewer.define_image,**the_dict)
                    return
        canvas_cut=Canvas_cut(defineimg)
        the_dict={"imgcv":self.imgcv,"mask":self.mask}
        for viewer in self.viewers_making_box:
            canvas_cut.bind(viewer.canvas)
            INR(viewer.define_image,**the_dict)
        return lambda:defineimg(canvas_cut.box)
class Wrapped_box(_Crop_box):
    def __init__(self, app=None, imgcv=None, mask=None, points=None,radius_selcting=10,centerstate=True, **kwargs):
        "viewer and img and points"
        super().__init__(app=app, imgcv=imgcv, mask=mask, points=points, **kwargs)
        self.viewers_Wrapped_image:List[DrawnImg]=[]
    def make_wrapped_image(self):
        self.remove_bind()
        viewers_cropped:List[Tuple[DrawnImg,np.ndarray]]=[(self.viewerCropped,self.imgcv),(self.viewerMaskCropped,self.mask)] 
        def define_image(points):
            points=wrapped_box.points=self.clamp_points(points)
            points=order_points(np.array(points)).astype(np.int32).tolist()
            the_dict={"imgcv":self.imgcv,"mask":self.mask, "points":points,"box":self.box}
            activated_widget=self.mainNoteBook.active_widget()
            for viewer in self.viewers_Wrapped_image:
                if activated_widget==viewer:
                    INR(viewer.define_image,**the_dict)
                    return
            if len(wrapped_box.points)>=4:
                points=order_points(np.array(points))
                for viewer,img in viewers_cropped:
                    wrappedImg=four_point_transform(img,points)
                    viewer.define_image(wrappedImg) 
        wrapped_box=Control_Points(self.points,define_image)
        for viewer in self.viewers_Wrapped_image:
            wrapped_box.bind(viewer.canvas)
        def end():
            if len(wrapped_box.points)==4:
                self.remove_bind()
                points=order_points(np.array(wrapped_box.points))
                for att in self.get_keys():
                    the_img=getattr(self,att)
                    if isinstance(the_img,np.ndarray):
                        if len(the_img.shape)>=2:
                            new_value= four_point_transform(the_img, points)
                            setattr(self,att,new_value)
                h,w=self.imgcv.shape[:2]
                self.box=[0,0,w,h]
                
                #for future purpuse
                return True
            return False
        self.entered(end)
        define_image(self.points)
        return lambda:define_image(wrapped_box.points)

from tkinter import *
from pywidgets._imgcv_objects.Image_objects import *
from pywidgets.tk.Img_editor.tecnologies import *
from pywidgets.tk.Img_editor.__viewers import *
import inspect
import numpy as np,cv2
def combine(*args):
    the_dict={}
    for dic in args:
        for key in dic:
            the_dict[key]=dic[key]
    return the_dict
class Img_editor_simple(Switcher_mask,MAKE_BOX,Control_box,Viewer):
    def __init__(self, app, imgcv, mask=None, points=None, radius_brushing=10, radius_selecting=20, brushingstate=True, centerState=True, **kwargs):
        super().__init__(app, imgcv, mask, points, radius_brushing, radius_selecting, brushingstate, **kwargs)
        MAKE_BOX.__init__(self,app, imgcv, mask, points, radius_selecting,centerState, **kwargs)
        Control_box.__init__(self,app, imgcv, mask, points, radius_selecting, **kwargs)
        Viewer.__init__(self,app, imgcv, mask, points,**kwargs)

        self._masking_mode=False

        
        self.viewers_brushing=[
            [self.viewer,[0,0]],[self.viewermask,[0,0]],
        ]
        self.viewers_filler+=[[self.viewermask,[0,0]]]
        self.viewers_controlling+=[self.viewer,self.viewermask]
        self.viewers_making_box+=[self.viewer,self.viewermask]
        self.essential_viewers=[self.viewer]
    def simple_shower(self):
        self.remove_bind()
        self._simple_viewer()

    def _simple_viewer(self):
        self.mainNoteBook.allowed((self.viewer,self.viewermask),True,(self.viewer,self.viewermask))
        self.mainNoteBook.targets=[lambda:self.show_viewers(False,colorImgState=False)]
        self.show_viewers(False,colorImgState=False)
    def define_mask(self):
        self.mainNoteBook.allowed((None,),False,self.essential_viewers)
        super().define_mask()
        self.mainNoteBook.targets=[lambda:self.show_viewers(True)]
        self.show_viewers()
        self._masking_mode=True
    def remove_bind(self):
        self._masking_mode=False
        self.mainNoteBook.targets=[]
        return super().remove_bind()
    def get_keys(self):
        return super().get_keys()
    def cancel(self,active_simple_viewer=False):
        self.remove_bind()
        if active_simple_viewer:
            self._simple_viewer()
        
        super().cancel()
class Full_Editor(Img_editor_simple,COLORING_Brush,Control_Select_region,Add_background,buttons_detectors,Wrapped_box,Adding_imgbackground_edges,Text_putter,
            Viewer_Gray_image,Viewer_blurred,Viewer_brushed,Viewer_coloredbackground,Viewer_removedbackground,Viewer_clustering,Background_added,Brushed_Imgcv):
    def __init__(self,  **kwargs):
        #for enusere that the editbar do't edit on the image
        for value in Full_Editor.__bases__:
            func_args = inspect.getfullargspec(value.__init__).args
            the_dic={}
            for arg in func_args:
                if arg in kwargs:
                    the_dic[arg]=kwargs[arg]
            value.__init__(self,**the_dic)
        self.viewers_brushing+=[
            [self.viewer_blurred,[0,0]],[self.viewer_colored,[0,0]],
            [self.viewer_brushed,[0,0]],[self.viewer_removedbackground,[0,0]],
            [self.viewer_added_background,[0,0]],[self.viewer_clusteredimage,[0,0]],
            [self.viewer_gray_viewer,[0,0]]
        ]
        self.viewers_filler=[[self.viewermask,[0,0]]]
        self.viewers_Wrapped_image+=[self.viewer,self.viewermask]
        self.viewers_adding_edges+=[self.viewer,self.viewermask]
        self.viewers_importbackground+=[self.viewer]
        self.viewers_move+=[self.viewer,self.viewermask]
        self.viewers_brushing_coloring+=[self.viewer,self.viewermask]
        self.viewers_add_text+=[self.viewer,self.viewermask]
        
        def tracker(intvar:IntVar,__name):
            def track():
                setattr(self,__name,intvar.get())
                self.show_viewers()
            intvar.trace_add("write",lambda *args:track())
        #setting tracker to each variable
        blur_int_var=IntVar()
        blur_int_var.set(self.blurred)
        tracker(blur_int_var,"blurred")

        radiusArea_var=IntVar()
        radiusArea_var.set(self.radiusArea)
        tracker(radiusArea_var,"radiusArea")

        kmeans_var=IntVar()
        kmeans_var.set(self.kmeans)
        tracker(kmeans_var,"kmeans")


        #add tracker to img viewer
        self.viewer_blurred.add_tracker(blur_int_var,(0,30))
        self.viewer_brushed.add_tracker(radiusArea_var,(0,20))
        self.viewer_clusteredimage.add_tracker(kmeans_var,(2,40))
        #bind all canvases to be in the same slider
        def bind_viewers(canvases):
            commands=["xview_moveto","yview_moveto"]
            def argument(index,x0,x1):
                for id,g in enumerate(allCommands):
                    command=g[index]
                    getattr(Canvas,commands[index])(canvases[id],x0)
                    (lambda x0,x1:self.winfo_toplevel().tk.call(command,x0,x1))(x0,x1)
            allCommands=[]   
            for canvas in canvases:
                xscroll=canvas["xscrollcommand"]
                yscroll=canvas["yscrollcommand"]
                allCommands.append([xscroll,yscroll])
                canvas.config(
                    xscrollcommand=lambda *args:argument(0,*args),
                    yscrollcommand=lambda *args:argument(1,*args)
                )
        all_canvases=[]
        for title in self.mainNoteBook:
            if hasattr(title.widget,"canvas"):
                all_canvases.append(title.widget.canvas)
        bind_viewers(all_canvases)     
    def show_viewers(self,state=True,colorImgState=True,**kwargs):
        b=self.box
        self.colorBackground[b[1]:b[1]+b[3],b[0]:b[0]+b[2]]=self.color
        super().show_viewers(state,colorImgState,**kwargs)
    def control_moving_box(self):
        self.mainNoteBook.allowed(
            (self.viewer,self.viewermask,self.viewerCropped,self.viewerMaskCropped),True,
            self.essential_viewers
        )
        target=super().control_moving_box()
        self.mainNoteBook.targets=[target]
        return target
    def define_mask(self):
        self.mainNoteBook.allowed((None,),False,self.essential_viewers)
        super().define_mask()
        self.mainNoteBook.targets=[lambda:self.show_viewers(True)]
        self.show_viewers()
        self._masking_mode=True
    def update_imgcv(self,**kwargs):
        for key in kwargs:
            if key in self.__dict__:
                if type(kwargs[key])==np.ndarray:
                    kwargs[key]=kwargs[key].copy()
                if key =="box":
                    kwargs["box"]=self.clamp_box(kwargs["box"])
                elif type(kwargs[key])==list:
                    kwargs[key]=kwargs[key].copy()
                setattr(self,key,kwargs[key])


    def move_thresh_image(self, rotate_state=True, copy_state=False):
        self.mainNoteBook.allowed(self.viewers_move,True,self.essential_viewers)
        super().move_thresh_image(rotate_state,copy_state)
    def move_text(self):
        self.move_thresh_image()
    def move_text_copy(self):
        self.move_thresh_image(True,True)
    def rotate_img(self,*args,**kwargs):  
        super().rotate_img(*args,**kwargs)
        self.simple_shower()
    def get_all_rotate_boxes(self, rotate_state=True, copy_state=False):
        self.mainNoteBook.allowed(self.viewers_move,True,self.essential_viewers)
        super().get_all_rotate_boxes(rotate_state=rotate_state, copy_state=copy_state)
    def coloring_mode(self):
        self.mainNoteBook.allowed(self.viewers_brushing_coloring,True,self.essential_viewers)
        super().coloring_mode()
        self.mainNoteBook.targets=[lambda:self.show_viewers(False,mask=self.mask,coloerbackground=self.colorBackground)]
        self.show_viewers()
    def move_selected_area(self, rotatestate=False, copystate=False):
        self.mainNoteBook.allowed(self.viewers_move,True,self.essential_viewers)
        super().move_selected_area(rotatestate, copystate)
    def make_box(self):
        self.remove_bind()
        self.mainNoteBook.allowed(
            (self.viewer,self.viewermask,self.viewerCropped,self.viewerMaskCropped),True,
            self.essential_viewers
        )
        target=super().make_box()
        self.mainNoteBook.targets=[target]
    def make_wrapped_image(self):
        self.mainNoteBook.allowed(
            (self.viewer,self.viewermask,self.viewerCropped,self.viewerMaskCropped),True,
            self.essential_viewers
        )
        target=super().make_wrapped_image()
        self.mainNoteBook.targets=[target]
        return target
    def import_img_back_ground(self, imgcv_obj: Img_cv):
        return super().import_img_back_ground(imgcv_obj)
    def resize_background(self):
        self.mainNoteBook.allowed(self.viewers_importbackground,True,self.essential_viewers)
        return super().resize_background()
    def multi_resize_background(self):
        self.mainNoteBook.allowed(self.viewers_importbackground,True,self.essential_viewers)
        super().multi_resize_background()
        self.mainNoteBook.targets=[self.mulityboxselector.target]
    def add_edges(self,blank_background=False):
        self.mainNoteBook.allowed(self.viewers_adding_edges,True,self.essential_viewers)
        super().add_edges(blank_background=blank_background)
    def get_keys(self):
        return combine(
            Colored_Imgcv.get_keys(self),
            Blurred_imgcv.get_keys(self),
            Background_Img_cv.get_keys(self),
            Brushed_Imgcv.get_keys(self),
            Cluster_Imgcv.get_keys(self)
        )
    def text_mode(self,**kwargs):
        self.mainNoteBook.allowed(self.viewers_add_text,True,self.essential_viewers)
        super().text_mode(**kwargs)


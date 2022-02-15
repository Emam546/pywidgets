from tkinter import *
from pywidgets._imgcv_objects.Image_objects import *
from pywidgets.tk.Img_editor.tecnologies import *
from pywidgets.tk.Img_editor.__viewers import *
import inspect

def combine(*args):
    the_dict={}
    for dic in args:
        for key in dic:
            the_dict[key]=dic[key]
    return the_dict
class Img_editor_simple(Swithcher_mask,MAKE_BOX,Control_box,Viewer):
    def __init__(self, app, imgcv, mask=None, points=None, radius_brushing=10, radius_selcting=20, brushingstate=True, centerstate=True, **kwargs):
        super().__init__(app, imgcv, mask, points, radius_brushing, radius_selcting, brushingstate, **kwargs)
        MAKE_BOX.__init__(self,app, imgcv, mask, points, radius_selcting,centerstate, **kwargs)
        Control_box.__init__(self,app, imgcv, mask, points, radius_selcting,centerstate, **kwargs)
        Viewer.__init__(self,app, imgcv, mask, points,**kwargs)

        self._maksing_mode=False

        
        self.viewers_brushing=[
            [self.viewer,[0,0]],[self.viewermask,[0,0]],
        ]
        self.viewers_filler+=[[self.viewermask,[0,0]]]
        self.viewers_controling+=[self.viewer,self.viewermask]
        self.viewers_making_box+=[self.viewer,self.viewermask]
        self.essestial_viewers=[self.viewer]
    def simple_shower(self):
        self.remove_bind()
        self._simple_viewer()

    def _simple_viewer(self):
        self.mainnotebook.allowed((self.viewer,self.viewermask),True,(self.viewer,self.viewermask))
        self.mainnotebook.targets=[lambda:self.show_viwers(False,colorimgstate=False)]
        self.show_viwers(False,colorimgstate=False)
    def define_mask(self):
        self.mainnotebook.allowed((None,),False,self.essestial_viewers)
        super().define_mask()
        self.mainnotebook.targets=[lambda:self.show_viwers(True)]
        self.show_viwers()
        self._maksing_mode=True
    def remove_bind(self):
        self._maksing_mode=False
        self.mainnotebook.targets=[]
        return super().remove_bind()
    def get_keys(self):
        return super().get_keys()
    def cancel(self,active_simple_viwer=False):
        self.remove_bind()
        if active_simple_viwer:
            self._simple_viewer()
        
        super().cancel()
class Full_Editor(Img_editor_simple,COLORING_Brush,Control_Select_region,Add_background,buttons_detectors,Wrapped_box,Adding_imgbackground_edges,Text_putter,
            Viewer_Gray_iamge,Viewer_blured,Viewer_brushed,Viewer_coloredbackground,Viewer_removedbackground,Viewer_clustering,Background_added,Brueshed_Imgcv):
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
            [self.viewer_blured,[0,0]],[self.viewer_colored,[0,0]],
            [self.viewer_brushed,[0,0]],[self.viewer_removedbackground,[0,0]],
            [self.viewer_added_background,[0,0]],[self.viewer_clusteredimage,[0,0]],
            [self.viewer_gray_viewer,[0,0]]
        ]
        self.viewers_filler=[[self.viewermask,[0,0]]]
        self.viewers_Wrepped_image+=[self.viewer,self.viewermask]
        self.viewers_adding_edges+=[self.viewer,self.viewermask]
        self.viewers_importbackground+=[self.viewer]
        self.viewers_move+=[self.viewer,self.viewermask]
        self.viewers_brushing_coloring+=[self.viewer,self.viewermask]
        self.viewers_add_text+=[self.viewer,self.viewermask]
        
        def tracker(intvar:IntVar,__name):
            def track():
                setattr(self,__name,intvar.get())
                self.show_viwers()
            intvar.trace_add("write",lambda *args:track())
        #setting tracker to each varibale
        blur_int_var=IntVar()
        blur_int_var.set(self.blured)
        tracker(blur_int_var,"blured")

        radiusarea_var=IntVar()
        radiusarea_var.set(self.radiusarea)
        tracker(radiusarea_var,"radiusarea")

        kmeans_var=IntVar()
        kmeans_var.set(self.kmeans)
        tracker(kmeans_var,"kmeans")


        #add tracker to img viewer
        self.viewer_blured.add_tracker(blur_int_var,(0,30))
        self.viewer_brushed.add_tracker(radiusarea_var,(0,20))
        self.viewer_clusteredimage.add_tracker(kmeans_var,(2,40))
        #bind all canvases to be in the same slider
        def bind_viewers(canvases):
            commands=["xview_moveto","yview_moveto"]
            def argument(index,x0,x1):
                for id,g in enumerate(allcommands):
                    command=g[index]
                    getattr(Canvas,commands[index])(canvases[id],x0)
                    (lambda x0,x1:self.winfo_toplevel().tk.call(command,x0,x1))(x0,x1)
            allcommands=[]   
            for canvas in canvases:
                xscroll=canvas["xscrollcommand"]
                yscroll=canvas["yscrollcommand"]
                allcommands.append([xscroll,yscroll])
                canvas.config(
                    xscrollcommand=lambda *args:argument(0,*args),
                    yscrollcommand=lambda *args:argument(1,*args)
                )
        all_canvases=[]
        for title in self.mainnotebook:
            if hasattr(title.widget,"canvas"):
                all_canvases.append(title.widget.canvas)
        bind_viewers(all_canvases)     
    def show_viwers(self,state=True,colorimgstate=True,**kwargs):
        b=self.box
        self.coloerbackground[b[1]:b[1]+b[3],b[0]:b[0]+b[2]]=self.color
        super().show_viwers(state,colorimgstate,**kwargs)
    def control_moving_box(self):
        self.mainnotebook.allowed(
            (self.viewer,self.viewermask,self.viewercropped,self.viewermaskcropped),True,
            self.essestial_viewers
        )
        target=super().control_moving_box()
        self.mainnotebook.targets=[target]
        return target
    def define_mask(self):
        self.mainnotebook.allowed((None,),False,self.essestial_viewers)
        super().define_mask()
        self.mainnotebook.targets=[lambda:self.show_viwers(True)]
        self.show_viwers()
        self._maksing_mode=True
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
        self.mainnotebook.allowed(self.viewers_move,True,self.essestial_viewers)
        super().move_thresh_image(rotate_state,copy_state)
    def move_text(self):
        self.move_thresh_image()
    def move_text_copy(self):
        self.move_thresh_image(True,True)
    def rotate_img(self,*args,**kwargs):  
        super().rotate_img(*args,**kwargs)
        self.simple_shower()
    def get_all_rotate_boxs(self, rotate_state=True, copy_state=False):
        self.mainnotebook.allowed(self.viewers_move,True,self.essestial_viewers)
        super().get_all_rotate_boxs(rotate_state=rotate_state, copy_state=copy_state)
    def coloring_mode(self):
        self.mainnotebook.allowed(self.viewers_brushing_coloring,True,self.essestial_viewers)
        super().coloring_mode()
        self.mainnotebook.targets=[lambda:self.show_viwers(False,mask=self.mask,coloerbackground=self.coloerbackground)]
        self.show_viwers()
    def move_selected_area(self, rotatestate=False, copystate=False):
        self.mainnotebook.allowed(self.viewers_move,True,self.essestial_viewers)
        super().move_selected_area(rotatestate, copystate)
    def make_box(self):
        self.remove_bind()
        self.mainnotebook.allowed(
            (self.viewer,self.viewermask,self.viewercropped,self.viewermaskcropped),True,
            self.essestial_viewers
        )
        target=super().make_box()
        self.mainnotebook.targets=[target]
    def make_wrapped_image(self):
        self.mainnotebook.allowed(
            (self.viewer,self.viewermask,self.viewercropped,self.viewermaskcropped),True,
            self.essestial_viewers
        )
        target=super().make_wrapped_image()
        self.mainnotebook.targets=[target]
        return target
    def import_img_back_ground(self, imgcv_obj: Img_cv):
        return super().import_img_back_ground(imgcv_obj)
    def resize_background(self):
        self.mainnotebook.allowed(self.viewers_importbackground,True,self.essestial_viewers)
        return super().resize_background()
    def mulity_resize_background(self):
        self.mainnotebook.allowed(self.viewers_importbackground,True,self.essestial_viewers)
        super().mulity_resize_background()
        self.mainnotebook.targets=[self.mulityboxselector.target]
    def add_edges(self,blanck_background=False):
        self.mainnotebook.allowed(self.viewers_adding_edges,True,self.essestial_viewers)
        super().add_edges(blanck_background=blanck_background)
    def get_keys(self):
        return combine(
            Colored_Imgcv.get_keys(self),
            Blured_imgcv.get_keys(self),
            Background_Img_cv.get_keys(self),
            Brueshed_Imgcv.get_keys(self),
            Cluster_Imgcv.get_keys(self)
        )
    def text_mode(self,**kwargs):
        self.mainnotebook.allowed(self.viewers_add_text,True,self.essestial_viewers)
        super().text_mode(**kwargs)

def main(): 
    root=Tk()
    img=cv2.imread("D:\Projects\small projects\images\messi5.jpg") 
    if img is None:
        raise "the mask" 
    mask=np.zeros(img.shape[:2],"uint8")
    if mask is None:
        raise "error"
    #mask[:]=255
    img_editor=Full_Editor(app=root,imgcv=img,mask=mask)
    #img_editor.add_item("0",imgcv=img)
    #img_editor.mainnotebook.allowed((img_editor.viewer,),True)
    img_editor.pack(fill=X,expand=YES)
    img_editor.blured=10
    img_editor.color=(255,0,0)
    img_editor.coloerbackground[:]=(255,0,0)
    img_editor.pack(fill=BOTH,expand=YES)
    conatiner_frame=Frame(bg="red")
    button_Control=Button(conatiner_frame,text="control box",command=img_editor.control_moving_box)
    button_Control.pack()
    button_define_box=Button(conatiner_frame,text="define box",command=img_editor.define_mask)
    button_define_box.pack()
    button_define_box=Button(conatiner_frame,text="make box",command=img_editor.make_box)
    button_define_box.pack()

    button_define_box=Button(conatiner_frame,text="wrapped img",command=img_editor.make_wrapped_image)
    button_define_box.pack()

    button_define_box=Button(conatiner_frame,text="move text",command=lambda :img_editor.move_thresh_image(True))
    button_define_box.pack()

    button_define_box=Button(conatiner_frame,text="select object mask",command=lambda :img_editor.move_selected_area(True))
    button_define_box.pack()

    button_define_box=Button(conatiner_frame,text="move muilty object",command=lambda :img_editor.get_all_rotate_boxs(True))
    button_define_box.pack()

    button_define_box=Button(conatiner_frame,text="add edges",command=img_editor.add_edges)
    button_define_box.pack()

    button_define_box=Button(conatiner_frame,text="center state",command=img_editor.text_mode)
    button_define_box.pack()

    # backward_frame=Frame(conatiner_frame)
    # Button(backward_frame,text="undo",command=img_editor.undo).grid(row=0,column=0)
    # Button(backward_frame,text="forward",command=img_editor.forward).grid(row=0,column=1)
    # backward_frame.pack()


    conatiner_frame.pack(fill=BOTH,expand=YES)
    def import_image(path):
        imported_image=cv2.imread(path)
        mask=np.zeros(imported_image.shape[:2],"uint8");mask[:]=1
        img_editor.import_img_back_ground(Img_cv(imported_image,mask))
    #import_image("G:\python\opencv\\images\\Jellyfish.jpg")
    #import_image("G:\python\opencv\images\\aerial_image.jpg")
    
    #img_editor.text_mode()
  
    img_editor.simple_shower()
    root.mainloop()
if __name__=="__main__":
    import numpy as np,cv2
    main()
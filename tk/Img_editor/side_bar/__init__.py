import os
import sys
from pathlib import Path
from tkinter import *
from tkinter.constants import BOTH, X, YES
from PIL import Image,ImageTk
from pycv2.img.utils import rgb_to_hex
sys.path.append(os.path.dirname(Path(__file__).parent))
sys.path.append(os.path.dirname(Path(Path(__file__).parent).parent))
from widgets.color_picker import Colored_getting_box
from side_bar.bars import Adaptive_Tresh_Frame, Frame_Canny, Frame_Close, Frame_Open, Frame_dilite, Frame_erode, Thresholding_Frame, _donothing,cv2,SLider_1_tracker,SwithchBox
from side_bar.buttons_editor import Buttons_Frame,STYLE_COFIGURATION
from Verticle_Frame import VerticalScrolledFrame
from Notebook import Swithcher_window
IMAGES_BRUSH_PATHES=["icons\\paint_tool.png","icons\\fill_spaces_area.png",]
__FILEPATH=os.path.dirname(__file__)+"\\"
for i,path in enumerate(IMAGES_BRUSH_PATHES):
    IMAGES_BRUSH_PATHES[i]= __FILEPATH+path

class Brsuh_switcher(SwithchBox):
    def __init__(self, app, target, defultstate=True, orient=HORIZONTAL,images_pathes=IMAGES_BRUSH_PATHES,style=STYLE_COFIGURATION,width=35, *args, **kwargs):
        super().__init__(app, target, defultstate=defultstate, orient=orient, *args, **kwargs)
        self.width=width
        self._images=[]
        for path,button in zip(images_pathes,[self.button_1,self.button_2]):
            image=Image.open(path)
            w,h=image.size
            h=self.width
            image=image.resize((self.width,h))
            image=ImageTk.PhotoImage(image)
            self._images.append(image)
            button.config(image=image,**style["button_sidebar"])
    
     
class Editing_bar(VerticalScrolledFrame):
    """the editing bar return 3 items
        mask ,box and radius_brushing as radius of brush,brush_state,color
    """
    def __init__(self,app,imgcv,mask=None,target=None,radius_brush=10,**kwargs):
        super().__init__(app,scrolling=True,**kwargs)
        self.target=target=target if not target is None else _donothing 
        mask=mask if not mask is None else cv2.threshold(imgcv,0,255,cv2.THRESH_BINARY)[1]
        
        self.buttons=Buttons_Frame(self.interior,mask,target)
        
        self.brush_state_frame=Brsuh_switcher(self.interior,self._call_buttons_function)
        self.color_picker=Colored_getting_box(self.interior,self._call_color_function,)
        Label(self.interior,text="brush radius",justify=LEFT,)
        self.radius_slider=SLider_1_tracker(self.interior,self._call_radius_function,(0,70))
        self.radius_slider.var.set(radius_brush)

        Label(self.interior,text="thresh",justify=LEFT)
        self.frame_thresh=Thresholding_Frame(self.interior,imgcv,target)
        Label(self.interior,text="Adaptive threshold",justify=LEFT)
        self.adaptive_thresh=Adaptive_Tresh_Frame(self.interior,imgcv,target)
        Label(self.interior,text="canny edge detector",justify=LEFT)
        self.canny_edge=Frame_Canny(self.interior,imgcv,target)
        Label(self.interior,text="eroding dialtion",justify=LEFT)
        self.frame_erode=Frame_erode(self.interior,mask,target)
        self.frame_dialte=Frame_dilite(self.interior,mask,target)

        Label(self.interior,text="opening closing",justify=LEFT)
        self.frame_close=Frame_Close(self.interior,mask,target)
        self.frame_open=Frame_Open(self.interior,mask,target)

        #packing all
        for child in self.interior.winfo_children():
            child.pack(fill=X,expand=YES)
    def _update_brush_state_function(self,state):
        self.brush_state_frame._buttons_state(state)
    def _call_radius_function(self,radius_brushing):
        self.target(radius_brushing=radius_brushing)
    def _call_color_function(self,color):
        
        self.target(color=color)

    def _call_buttons_function(self,brush_state):
        self.target(brush_state=brush_state)
    def update_mask(self,mask):
        for viewer in [self.frame_erode,self.frame_dialte,self.frame_close,self.frame_open]:
            setattr(viewer,"mask",mask)   
        self.buttons.mask=mask
    def update_imgcv(self,imgcv):
        gray=imgcv if (imgcv.shape)==2 else cv2.cvtColor(imgcv,cv2.COLOR_BGR2GRAY)
        for viewer in [self.frame_thresh,self.adaptive_thresh,self.canny_edge,self.frame_erode]:
            setattr(viewer,"gray",gray)
    def update_box(self,box):
        self.buttons.box=box
    def update_radius_bar(self,radius):
        self.radius_slider.var.set(radius)
    def update_color_bar(self,color):
        #color as bgr value
        color=list(color)
        color.reverse()
        self.color_picker.change_color_box((None,rgb_to_hex(*color)))

class COLORING_BAR(VerticalScrolledFrame):
    def __init__(self, parent, scrolling=False, **kw):
        super().__init__(parent, scrolling, **kw)

class Swiching_bar(Swithcher_window):
    def __init__(self, app=None, *args, **kwargs):
        super().__init__(app, *args, **kwargs)  

def main():
    import numpy as np
    from threading import Thread
    root=Tk()
    imgcv=cv2.imread("D:\Projects\small projects\images\example_03.png")
    def show(imgcv):
        cv2.imshow("window",imgcv)
        cv2.waitKey(1)
    widget_img=Editing_bar(root,imgcv,target=show)
    widget_img.pack(fill=BOTH,expand=YES)
    root.mainloop()
    
if __name__=="__main__":
    main()


    
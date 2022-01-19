import os 
import sys
sys.path.append(os.path.dirname(__file__))
from pathlib import Path
sys.path.append(os.path.dirname(Path(__file__).parent))
from Img.__Img_viewers import *
from __orgin import *
from Image_objects import *
from tkinter import filedialog
class Viewer(EMViwerer):
    def __init__(self,app, imgcv, mask=None, box=None, **kwargs):
        super().__init__(app=app, imgcv=imgcv, mask=mask, box=box, **kwargs)
        self.viewer=self.mainnotebook.add("Image",Image_viewer(None,bg=self["bg"]))
        self.viewermask=self.mainnotebook.add("Mask",Mask(None,bg=self["bg"]))

class Viewer_blured(EMViwerer,Blured_imgcv):
    def __init__(self,app, imgcv, mask=None, box=None,blured=7 ,**kwargs):
        super().__init__(app=app, imgcv=imgcv, mask=mask, box=box, **kwargs)
        Blured_imgcv.__init__(self,imgcv, mask=mask, box=box,blured=blured)
        self.viewer_blured=self.mainnotebook.add("Blur",Bluerd_img(None,bg=self["bg"]))
           
class Viewer_removedbackground(EMViwerer):
    def __init__(self,app, imgcv, mask=None, box=None, **kwargs):
        super().__init__(app=app, imgcv=imgcv, mask=mask, box=box, **kwargs)
        self.viewer_removedbackground=self.mainnotebook.add("Removed Background",Removed_Background(None,bg=self["bg"]))
    def remove_img_back_ground(self):
        filename=filedialog.asksaveasfilename(filetypes=(("PNG","*.png"),),defaultextension=".png")
        if filename!="":
            image=get_trasperancy_image(
                self.imgcv,self.mask
            )
            cv2.imwrite(filename,image)

class Viewer_coloredbackground(EMViwerer,Colored_Imgcv):
    def __init__(self, app, imgcv, mask=None, box=None,coloerbackground=None,color=(255,255,255), **kwargs):
        super().__init__(app=app, imgcv=imgcv, mask=mask, box=box, **kwargs)
        Colored_Imgcv.__init__(self,imgcv=imgcv, mask=mask, box=box,coloerbackground=coloerbackground,color=color)
        self.viewer_colored=self.mainnotebook.add("Colored Image",Colored_Img(None,bg=self["bg"]))
        
class Viewer_brushed(EMViwerer,Brueshed_Imgcv):
    def __init__(self, app, imgcv, mask=None, box=None,radiusarea=2,flags=cv2.INPAINT_TELEA, **kwargs):
        super().__init__(app=app, imgcv=imgcv, mask=mask, box=box, **kwargs)
        Brueshed_Imgcv.__init__(self,imgcv=imgcv, mask=mask, box=box,radiusarea=radiusarea,flags=flags)
        self.viewer_brushed=self.mainnotebook.add("Brushed",Cutted_brush(bg=self["bg"]))
    
class Background_added(EMViwerer,Background_Img_cv):
    def __init__(self, app, imgcv, mask=None, box=None,imported_backgrounds:list=[], **kwargs):
        super().__init__(app=app, imgcv=imgcv, mask=mask, box=box, **kwargs)
        Background_Img_cv.__init__(self,imgcv=imgcv, mask=mask, box=box,imported_backgrounds=imported_backgrounds)
        self.viewer_added_background=self.mainnotebook.add("Background",Added_background_Img(bg=self["bg"]))

class Viewer_clustering(EMViwerer,Cluster_Imgcv):
    def __init__(self, app, imgcv, mask=None, box=None,kmeans=3, **kwargs):
        super().__init__(app, imgcv, mask=mask, box=box, **kwargs)
        Cluster_Imgcv.__init__(self,imgcv, mask=mask, box=box,kmeans=kmeans)
        self.viewer_clusteredimage=self.mainnotebook.add("Cluster",ClusteringtheImage(bg=self["bg"]))

class Viewer_Gray_iamge(EMViwerer):
    def __init__(self, app, imgcv, mask=None, box=None, **kwargs):
        super().__init__(app, imgcv, mask=mask, box=box, **kwargs)
        self.viewer_gray_viewer=self.mainnotebook.add("Gray",Gray_Image_viewer(bg=self["bg"]))
    def gray_image(self):
        grayimg=cv2.cvtColor(cv2.cvtcolor(self.imgcv,cv2.COLOR_BGR2GRAY),cv2.COLOR_GRAY2BGR)
        self.imgcv=add_back_ground(self.imgcv.copy(),self.mask,grayimg)
        

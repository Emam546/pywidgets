
from pywidgets.kivy.Img.__Img_viewers import *
from pywidgets.kivy.Img_editor.__origin import *
from pywidgets._imgcv_objects.Image_objects import *

class Viewer(EMViwerer):
    def __init__(self, imgcv, mask=None, points=None, **kwargs):
        super().__init__( imgcv=imgcv, mask=mask, points=points, **kwargs)
        self.viewer=self.add("Image",Image_viewer(None,bg=self["bg"]))
        self.viewermask=self.add("Mask",Mask(None,bg=self["bg"]))

class Viewer_blured(EMViwerer,Blurred_imgcv):
    def __init__(self, imgcv, mask=None, points=None,blured=7 ,**kwargs):
        super().__init__( imgcv=imgcv, mask=mask, points=points, **kwargs)
        Blurred_imgcv.__init__(self,imgcv, mask=mask, points=points,blured=blured)
        self.viewer_blured=self.add("Blur",Bluerd_img(None,bg=self["bg"]))
           
class Viewer_removedbackground(EMViwerer):
    def __init__(self, imgcv, mask=None, points=None, **kwargs):
        super().__init__(imgcv=imgcv, mask=mask, points=points, **kwargs)
        self.viewer_removedbackground=self.add("Removed Background",Removed_Background(None,bg=self["bg"]))
    # def remove_img_back_ground(self):
    #     filename=filedialog.asksaveasfilename(filetypes=(("PNG","*.png"),),defaultextension=".png")
    #     if filename!="":
    #         image=get_trasperancy_image(
    #             self.imgcv,self.mask
    #         )
    #         cv2.imwrite(filename,image)

class Viewer_coloredbackground(EMViwerer,Colored_Imgcv):
    def __init__(self,  imgcv, mask=None, points=None,coloerbackground=None,color=(255,255,255), **kwargs):
        super().__init__( imgcv=imgcv, mask=mask, points=points, **kwargs)
        Colored_Imgcv.__init__(self,imgcv=imgcv, mask=mask, points=points,coloerbackground=coloerbackground,color=color)
        self.viewer_colored=self.add("Colored Image",Colored_Img(None,bg=self["bg"]))
        
class Viewer_brushed(EMViwerer,Brushed_Imgcv):
    def __init__(self,  imgcv, mask=None, points=None,radiusarea=2,flags=cv2.INPAINT_TELEA, **kwargs):
        super().__init__( imgcv=imgcv, mask=mask, points=points, **kwargs)
        Brushed_Imgcv.__init__(self,imgcv=imgcv, mask=mask, points=points,radiusarea=radiusarea,flags=flags)
        self.viewer_brushed=self.add("Brushed",Cutted_brush(bg=self["bg"]))
    
class Background_added(EMViwerer,Background_Img_cv):
    def __init__(self,  imgcv, mask=None, points=None,imported_backgrounds:list=[], **kwargs):
        super().__init__( imgcv=imgcv, mask=mask, points=points, **kwargs)
        Background_Img_cv.__init__(self,imgcv=imgcv, mask=mask, points=points,imported_backgrounds=imported_backgrounds)
        self.viewer_added_background=self.add("Background",Added_background_Img(bg=self["bg"]))

class Viewer_clustering(EMViwerer,Cluster_Imgcv):
    def __init__(self,  imgcv, mask=None, points=None,kmeans=3, **kwargs):
        super().__init__( imgcv, mask=mask, points=points, **kwargs)
        Cluster_Imgcv.__init__(self,imgcv, mask=mask, points=points,kmeans=kmeans)
        self.viewer_clusteredimage=self.add("Cluster",ClusteringtheImage(bg=self["bg"]))

class Viewer_Gray_iamge(EMViwerer):
    def __init__(self,  imgcv, mask=None, points=None, **kwargs):
        super().__init__( imgcv, mask=mask, points=points, **kwargs)
        self.viewer_gray_viewer=self.add("Gray",Gray_Image_viewer(bg=self["bg"]))
    def gray_image(self):
        grayimg=cv2.cvtColor(cv2.cvtColor(self.imgcv,cv2.COLOR_BGR2GRAY),cv2.COLOR_GRAY2BGR)
        self.imgcv=add_back_ground(self.imgcv.copy(),self.mask,grayimg)
        

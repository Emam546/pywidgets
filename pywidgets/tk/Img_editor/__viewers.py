from tkinter import filedialog
from pywidgets.tk.Img.__Img_viewers import *
from pywidgets.tk.Img_editor.__orgin import EMViewer
from pywidgets.tk.Img.__Img_viewers import *
from pywidgets._imgcv_objects.Image_objects import *

class Viewer(EMViewer):
    def __init__(self,app, imgcv, mask=None, points=None, **kwargs):
        super().__init__(app=app, imgcv=imgcv, mask=mask, points=points, **kwargs)
        self.viewer=self.mainNoteBook.add("Image",Image_viewer(None,bg=self["bg"]))
        self.viewermask=self.mainNoteBook.add("Mask",Mask(None,bg=self["bg"]))

class Viewer_blurred(EMViewer,Blurred_imgcv):
    def __init__(self,app, imgcv, mask=None, points=None,blured=7 ,**kwargs):
        super().__init__(app=app, imgcv=imgcv, mask=mask, points=points, **kwargs)
        Blurred_imgcv.__init__(self,imgcv, mask=mask, points=points,blured=blured)
        self.viewer_blurred:Bluerd_img=self.mainNoteBook.add("Blur",Bluerd_img(None,bg=self["bg"]))
class Viewer_removedbackground(EMViewer):
    def __init__(self,app, imgcv, mask=None, points=None, **kwargs):
        super().__init__(app=app, imgcv=imgcv, mask=mask, points=points, **kwargs)
        self.viewer_removedbackground=self.mainNoteBook.add("Removed Background",Removed_Background(None,bg=self["bg"]))
    def remove_img_back_ground(self):
        filename=filedialog.asksaveasfilename(filetypes=(("PNG","*.png"),),defaultextension=".png")
        if filename!="":
            image=get_transparency_image(
                self.imgcv,self.mask
            )
            cv2.imwrite(filename,image)

class Viewer_coloredbackground(EMViewer,Colored_Imgcv):
    def __init__(self, app, imgcv, mask=None, points=None,coloerbackground=None,color=(255,255,255), **kwargs):
        super().__init__(app=app, imgcv=imgcv, mask=mask, points=points, **kwargs)
        Colored_Imgcv.__init__(self,imgcv=imgcv, mask=mask, points=points,coloerbackground=coloerbackground,color=color)
        self.viewer_colored=self.mainNoteBook.add("Colored Image",Colored_Img(None,bg=self["bg"]))
        
class Viewer_brushed(EMViewer,Brushed_Imgcv):
    def __init__(self, app, imgcv, mask=None, points=None,radiusarea=2,flags=cv2.INPAINT_TELEA, **kwargs):
        super().__init__(app=app, imgcv=imgcv, mask=mask, points=points, **kwargs)
        Brushed_Imgcv.__init__(self,imgcv=imgcv, mask=mask, points=points,radiusarea=radiusarea,flags=flags)
        self.viewer_brushed:Cutted_brush=self.mainNoteBook.add("Brushed",Cutted_brush(bg=self["bg"]))
    
class Background_added(EMViewer,Background_Img_cv):
    def __init__(self, app, imgcv, mask=None, points=None,imported_backgrounds:list=[], **kwargs):
        super().__init__(app=app, imgcv=imgcv, mask=mask, points=points, **kwargs)
        Background_Img_cv.__init__(self,imgcv=imgcv, mask=mask, points=points,imported_backgrounds=imported_backgrounds)
        self.viewer_added_background=self.mainNoteBook.add("Background",Added_background_Img(bg=self["bg"]))

class Viewer_clustering(EMViewer,Cluster_Imgcv):
    def __init__(self, app, imgcv, mask=None, points=None,kmeans=3, **kwargs):
        super().__init__(app, imgcv, mask=mask, points=points, **kwargs)
        Cluster_Imgcv.__init__(self,imgcv, mask=mask, points=points,kmeans=kmeans)
        self.viewer_clusteredimage:ClusteringtheImage=self.mainNoteBook.add("Cluster",ClusteringtheImage(bg=self["bg"]))

class Viewer_Gray_image(EMViewer):
    def __init__(self, app, imgcv, mask=None, points=None, **kwargs):
        super().__init__(app, imgcv, mask=mask, points=points, **kwargs)
        self.viewer_gray_viewer=self.mainNoteBook.add("Gray",Gray_Image_viewer(bg=self["bg"]))
    def gray_image(self):
        grayimg=cv2.cvtColor(cv2.cvtcolor(self.imgcv,cv2.COLOR_BGR2GRAY),cv2.COLOR_GRAY2BGR)
        self.imgcv=add_back_ground(self.imgcv.copy(),self.mask,grayimg)
        

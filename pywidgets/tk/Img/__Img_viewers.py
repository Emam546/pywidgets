import cv2,os
from pywidgets.tk.Img.__orign import *
from pycv2.img.utils import *
from pycv2.img.drawing.box import *
def donothing(*args,**kwrgs):pass
FILE_PATH=os.path.dirname(__file__)
CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
REMOVEDBACKGROUND=cv2.imread(os.path.join(FILE_PATH,"icons\\removedbackground.png"))
if REMOVEDBACKGROUND is None:
    raise "where is the image"
class __Croped_img(Img_with_scrollbar):
    def crop_Img(self,imgcv,b=None):
        if b is None:
            Img_with_scrollbar.define_image(self,imgcv)
        else:
            Img_with_scrollbar.define_image(self,imgcv[b[1]:b[1]+b[3], b[0]:b[0]+b[2]])
DEFAULT_DRAWING_POINTS=dict(
        color_line=(255,255,0),thickness=2,radius=2,
        colors=[(0,0,255)]*4,center_state=False,colorcenter=(0,0,255))
class DrawnImg(Img_with_scrollbar):
    def define_image(self,imgcv,points: list=None,**style_drawing_points):
        if points!=None:
            the_dict=DEFAULT_DRAWING_POINTS
            the_dict.update(style_drawing_points)
            super().define_image(draw_box_moving(imgcv.copy(),points,**the_dict))
        else:
            super().define_image(imgcv)
class Added_background_Img(Img_with_scrollbar):
    def define_image(self,imgcv,imported_backgrounds,mask=None):
        finalImg=imgcv.copy()
        for background,pos in imported_backgrounds:
            h,w=background["background"].shape[:2]
            _backMask=cv2.resize(background["mask"],(w,h)).astype(np.bool)
            finalImg[pos[1]:pos[1]+h,pos[0]:pos[0]+w][_backMask]=background["background"][_backMask]
        finalImg=add_back_ground(imgcv.copy(),mask,finalImg)
        super().define_image(finalImg)
class Colored_Img(DrawnImg):
    def define_image(self,imgcv,mask=None,coloerbackground=None,points=None,**style_drawing_points):
        if mask is None:mask=np.zeros(imgcv.shape[:2],"uint8")
        if coloerbackground is None:coloerbackground=np.zeros(imgcv.shape[:2],"uint8")
        super().define_image(add_back_ground(imgcv.copy(),mask, coloerbackground), points,**style_drawing_points)
class Bluerd_img(Image_with_slider,DrawnImg):
    def define_image(self,imgcv,mask=None,points=None,blured=0,**style_drawing_points):
        mask=mask if not mask is None else np.ones(imgcv.shape[:2],"uint8")*255
        if blured!=0:
            super().define_image(bluring(imgcv.copy(), mask, blured), points)
        else:
            super().define_image(imgcv, points,**style_drawing_points)
class Cutted_brush(Image_with_slider,DrawnImg):
    def define_image(self, imgcv,mask=None,radiusarea=2,points=None,**style_drawing_points):
        if mask is None:mask=np.zeros(self.shape[:2],"uint8")
        resultimg=cv2.inpaint(imgcv, mask, radiusarea, cv2.INPAINT_TELEA)
        super().define_image(resultimg,points,**style_drawing_points)
class Removed_Background(DrawnImg):
     def define_image(self, imgcv,mask=None,points=None,**style_drawing_points):
        if mask is None:mask=np.zeros(imgcv.shape[:2],"uint8")
        background=duplicate_image(REMOVEDBACKGROUND,imgcv.shape[:2])
        if points!=None:
            super().define_image(add_back_ground(imgcv.copy(),255-mask,background),points,**style_drawing_points)
    
class Croped_Img(__Croped_img):
    def define_image(self,imgcv,mask=None,box=None):
        if mask is None:
            coloredimg=imgcv
        else:
            coloredimg=color_back_ground(imgcv,mask,(255,255,255))
        self.crop_Img(coloredimg,box)
class Croped_mask(__Croped_img):
    def define_image(self,mask,box=None,):
        self.crop_Img(mask,box)
class Mask(DrawnImg):
    def define_image(self,mask,points=None,**style_drawing_points):
        super().define_image(mask,points,**style_drawing_points)
class Image_viewer(DrawnImg):
    def define_image(self,imgcv,colorimgstate=False,mask=None,points=None,**style_drawing_points):
        if mask is None or not colorimgstate:
            colored_imgcv=imgcv
        else:
            colored_imgcv=color_back_ground(imgcv.copy(),mask,(255,255,255))
        super().define_image(colored_imgcv,points,**style_drawing_points)
class ClusteringtheImage(Image_with_slider,DrawnImg):
    def __init__(self, app=None, *args, **kwargs):
        super().__init__(app=app, *args, **kwargs)
        #for saving processor effort
        self.last_kmeans=None
        self.last_img=None
        self.last_clusterd_img=None
    def define_image(self, imgcv,mask=None,kmeans=3,points=None,**style_drawing_points):
        mask=mask if not mask is None else np.zeros(imgcv.shape,"uint8")
        if kmeans!=self.last_kmeans or not ARE_EQUALE(self.last_img,imgcv):
            self.last_kmeans=kmeans
            self.last_img=imgcv.copy()
            Z = imgcv.reshape((-1,3))
            # convert to np.float32
            Z = np.float32(Z)
            # define criteria, number of clusters(K) and apply kmeans()
            _,label,center=cv2.kmeans(Z,kmeans,None,CRITERIA,10,cv2.KMEANS_RANDOM_CENTERS)
            # Now convert back into uint8, and make original image
            center = np.uint8(center)
            res = center[label.flatten()]
            self.last_clusterd_img=res.reshape((imgcv.shape))
        _background=add_back_ground(self.last_img.copy(),mask,self.last_clusterd_img)
        super().define_image(_background,points,**style_drawing_points)
class Gray_Image_viewer(DrawnImg):
    def define_image(self, imgcv,mask=None,points=None,**style_drawing_points):
        mask=mask if not mask is None else np.zeros(imgcv.shape,"uint8")
        #conver BGR 2 Gray and add 2 channels by cv2
        grayimg=cv2.cvtColor(cv2.cvtColor(imgcv,cv2.COLOR_BGR2GRAY),cv2.COLOR_GRAY2BGR)
        _background=add_back_ground(imgcv.copy(),mask,grayimg)
        super().define_image(_background,points,**style_drawing_points)
        
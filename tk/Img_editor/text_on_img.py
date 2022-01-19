from pathlib import Path
import cv2,numpy as np
import sys,os

__file=Path(Path(__file__).parent).parent
sys.path.append(os.path.dirname(__file))
from _functions.selecting import Select_box,Select_box_circels
from tkinter import *
from pycv2.img.utils import add_back_ground
from pycv2.PIL import TextDrawer
from pycv2.img.utils import xywh_2_pts 
from pycv2.img.drawing.box import draw_box_moving
from PIL import ImageFont,Image
from pycv2.PIL.utils import cv2pil,pil2cv2
from tkinter import Text,Widget,Tk
#, size=10, index=0, encoding='', layout_engine=Non
COLOR_CIRCELS=[(255,0,0),(255,0,0),(255,0,0),(255,0,0)]
class Text_putter(Select_box_circels):
    def __init__(self,root:Tk,*images, box, target, radius_selcting=10, centerstate=True,
        text:str="",text_color=(255,255,255),
        font:ImageFont=None,
        spacing=4,
        direction=None,
        features=None,
        language=None,
        stroke_width=0,break_=False):
        super().__init__(box, target, radius_selcting=radius_selcting, centerstate=centerstate,break_=False)
        self._textputter=_Text_getter(self,self.target)
        self.original_images=images
        self.text_color=text_color
        self.break_=break_


        self._last_text=text
        self._lastdiminsions=None

        
       
        self.break_=break_

        self.font=font
        self.spacing=spacing
        self.direction=direction
        self.features=features
        self._language=language
        self.stroke_width=stroke_width
        self._last_text=None

        


    def cursor_cor(self,pos):
        assert(self.inside_box(pos))
        c,r=self._textputter.cursor_cor(pos[0]-self.box[0],pos[1]-self.box[1])
        #set the row and column of the cursor in widget
        num=float(str(r)+"."+str(c))
        self._textputter.mark_set(num)

    def _track(self,text:str=None):
        if self._last_text==text:return
        self._last_text=text
        self.maskimg=self._textputter.get_text_mask(self.box,break_=self.break_)

        
    def motion(self, pos):
        index=self._get_grabing_state(pos)
        if index!=None:
            self.box=self.grab_box(pos,index)
        elif self.inside_box(pos):
            self.cursor_cor(pos)

    def draw_text(self,*images,color_line=(255,255,0),thickness=2,radius=2,
        colors=COLOR_CIRCELS,colorcenter=(0,0,255)):
        for img in images:
            draw_box_moving(img,xywh_2_pts(self.box),
            color_line=color_line,thickness=thickness,radius=radius,
            colors=colors,colorcenter=colorcenter )
            images
        pass
    def _focus(self,index=END):
        self._textputter
        
class _Text_getter(Text):
    def __init__(self,root:Tk,target,text:str="",
        font:ImageFont=None,
        spacing=4,
        direction=None,
        features=None,
        language=None,
        stroke_width=0,break_=False):
        self.text=text
        super().__init__(root.winfo_toplevel())
        root.winfo_toplevel().bind("<Key>",lambda *args:self.track())
        self.target=target
        self.place(relx=4)
        self.insert(0.0,text)
        
        self.font=font
        self.spacing=spacing
        self.direction=direction
        self.features=features
        self._language=language
        self.stroke_width=stroke_width
        
        self.break_=break_

        self.get_text_mask()
        self.winfo_toplevel().bind_all("<Key>",self.track)

    def track(self):
        self.focus_force()
        self.target(self.get(0.0,END))
    def get_cursor_index(self):
        h=self._drawer.multiline_textsize(self.text,self.font, self.spacing, self.direction, self.features, self._language, self.stroke_width)[1]
        x,y=self.box[1]
        lines=self.text.splitlines()
        index_line=min(lines[[h//x]*len(lines)],len(lines))
        total_width=0
        for i,letter in enumerate(lines[index_line]):
            width_charcter=self._drawer.textsize(letter,self.font, self.spacing, self.direction, self.features, self._language, self.stroke_width)[0]
            if total_width+width_charcter>=y:
                return i,index_line
        return i,index_line 
    
    
    def get_text_mask(self,box,break_=False,alining="left",anchor=None):
        #detect if there in change on the image

        self._last_text=self.text
        imgPIL=Image.new("GRAY",box[2:])
        self._drawer=TextDrawer.Draw(imgPIL)
        org=box[:2]
        
        text=self._drawer.text2lines(self.text,box[2],self.font,self.spacing,self.direction,self.features,self._language,self.stroke_width,break_)
        self._drawer.multiline_text(org,text,255,self.font,anchor,self.spacing,alining,self.direction,self._language,self.stroke_width,1)
        return pil2cv2(imgPIL)
        
    def mouse_pos(self):
        line_spacing = (
            self._drawer.textsize("A", font=self.font, stroke_width=self.stroke_width)[1] + self.spacing
        )
        row,columns=str(self.insert(INSERT)).split(".")
        total_height=int(row)*line_spacing+line_spacing
        lines=self.text.splitlines()
        total_width=0
        for i,letter in enumerate(lines[int(row)],0):
            total_width+=self._drawer.textsize(letter,self.font, self.spacing, self.direction, self.features, self._language, self.stroke_width)[0]
            if i==int(columns):
                return total_width,total_height
        
        return total_width,total_height
    def cursor_cor(self,pos):
        x,y=pos
        h=self._drawer.multiline_textsize(self.text,self.font, self.spacing, self.direction, self.features, self._language, self.stroke_width)[1]
        
        lines=self.text.splitlines()
        index_line=min(lines[[h//x]*len(lines)],len(lines))
        total_width=0
        for i,letter in enumerate(lines[index_line]):
            width_charcter=self._drawer.textsize(letter,self.font, self.spacing, self.direction, self.features, self._language, self.stroke_width)[0]
            if total_width+width_charcter>=y:
                return i,index_line
        return i,index_line

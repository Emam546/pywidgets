import cv2,numpy as np
from tkinter import *
from pycv2.PIL.TextDrawer import Draw
from pycv2.img.utils import xywh_2_pts,distance
from pycv2.img.drawing.box import draw_box_moving
from PIL import ImageFont,Image
#from pycv2.PIL.utils import pil2cv
from tkinter import Text,Widget,Tk

from pywidgets._functions.selecting import Select_box_Points
COLOR_POINTS=[(255,0,0),(255,0,0),(255,0,0),(255,0,0)]
class Text_putter:
    def __init__(self,root:Tk,*images, box, target, radius_selcting=10,
        text:str="",text_color=(255,255,255),font:ImageFont=None,spacing=4,direction=None,features=None,language=None,stroke_width=0,break_=False):
        #to avoid replacing in center state
        self.root=root
        self.selecting_box=Select_box_Points(box, None, radius_selcting=radius_selcting, centerstate=False)
        self._textputter=_Text_getter(root,self._track,text)
        self.target=target
        self.text_color=text_color
        self.break_=break_
        self.original_images=images
        self.drawn_images=list(images)
        self.box=box

        self.maskImg=self._textputter.get_text_mask(self.box,break_=self.break_)
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
        self.root.winfo_toplevel().bind("<Key>",lambda *args:self._textputter.track())

    def cursor_cor(self,pos):
        assert(self.selecting_box.inside_box(pos))
        index=self._textputter.cursor_cor([pos[0]-self.box[0],pos[1]-self.box[1]])
        print(index)
        self._textputter.mark_set("insert",index)
    def release(self):
        self.selecting_box.release()
    def _track(self,text:str=None):
        self._last_text=text
        self.maskImg=self._textputter.get_text_mask(self.box,break_=self.break_)
        self.target(*self._update_images())
    def _update_images(self):
        bool_img=self.maskImg.astype(np.bool)
        b=self.box
        for i,img in enumerate(self.original_images):
            drawn_img=img.copy()
            color=255 if len(img.shape)==2 else self.text_color
            drawn_img[b[1]:b[1]+b[3],b[0]:b[0]+b[2]][bool_img]=color
            self.drawn_images[i]=drawn_img
        return self.drawn_images
    def motion(self, pos):
        index=self.selecting_box._get_grabbing_state(pos)
        if index!=None:
            self.box=self.selecting_box.grab_box(pos,index)
            self._track()
            self._update_images()
        elif self.selecting_box.inside_box(pos):
            self.cursor_cor(pos)
        else:
            return
        
        self.target(*self.drawn_images)

    def draw_img_box(self,img,color_line=(255,255,0),thickness=2,radius=2,
        colors=COLOR_POINTS,colorcenter=(0,0,255)):
        img=draw_box_moving(img,xywh_2_pts(self.box),
            color_line=color_line,thickness=thickness,radius=radius,
            colors=colors,colorcenter=colorcenter)
        mousepos=self._textputter.mouse_pos()
        if not mousepos is None:
            pos,mouse_height=mousepos
            pos[0]+=self.box[0]
            pos[1]+=self.box[1]
            mouse_pos=pos.copy()
            mouse_pos[1]-=mouse_height
            cv2.line(img,pos,mouse_pos,color_line,2)
        
        return img
    def _focus(self):
        self._textputter.focus()

    def bind(self,canvas:Canvas):
        def correct(event):
            x,y = int(event.widget.canvasx(event.x)),int(event.widget.canvasy(event.y))
            self._focus()
            Text_putter.motion(self,[x,y])
        canvas.bind("<Button-1>",correct)
        canvas.bind("<B1-Motion>",correct)
        canvas.bind("<ButtonRelease-1>",lambda e:Text_putter.release(self))
        
class _Text_getter(Text):
    def __init__(self,root:Tk,target,text:str="",
        font:ImageFont=None,
        spacing=4,
        direction=None,
        features=None,
        language=None,
        stroke_width=0,break_=False):
        super().__init__(root.winfo_toplevel())
        self.text=text
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

    def track(self):
        self.focus()
        self.text=self.get(0.0,END)
        self.target(self.text)

    def get_text_mask(self,box,break_=False,alining="left",anchor=None):
        """detect if there in change on the image"""
        self._last_text=self.text
        imgPIL=Image.new("L",box[2:])
        self._drawer=Draw(imgPIL)
        #org=box[:2]
        self.text=self._drawer.text2lines(self.text,(box[2]),self.font,self.spacing,self.direction,self.features,self._language,self.stroke_width,break_)

        self._drawer.multiline_text((0,0),self.text,255,self.font,anchor,self.spacing,alining,self.direction,self._language,self.stroke_width,255)
        return np.array(imgPIL)

    def mouse_pos(self):
        """get mouse position according to size of the current font"""
        lines=self.text.splitlines()
        if len(lines)>0:
            line_spacing = (
            self._drawer.textsize("A", font=self.font, stroke_width=self.stroke_width)[1] + (self.spacing)
            )
            #this algorism is for ensure that we will get the right index
            #with the arrangement
            rows,columns=str(self.index(INSERT)).split(".")
            rows=int(rows)-1
            columns=max(0,int(columns))
            org_total_letters=0
            #if the cursor in the finished
            finished=False
            for r,line in enumerate(self.get(0.0,END).splitlines()):
                if r<=rows:
                    for c,letter in enumerate(line):
                        if c<columns or rows!=r:
                            org_total_letters+=1
                        else:
                            break
                    else:
                        #check if the cursor is in the end line or not
                        #if it is the same row
                        if r==rows:
                            finished=True
            #print(org_total_letters,rows,columns)
            total_height=0
            total_width=0
            if rows in range(len(lines)):
                total_letters=0
                for line in lines:
                    if total_letters<org_total_letters:
                        total_width=0
                        total_height+=line_spacing
                        for i,letter in enumerate(line):
                            total_width+=self._drawer.textsize(letter,self.font, self.spacing, self.direction, self.features, self._language, self.stroke_width)[0]
                            total_letters+=1
                            if total_letters>=org_total_letters and i!=len(line)-1:
                                return [total_width,total_height],line_spacing
                    elif not finished: 
                        total_width=0    
                return [total_width,total_height],line_spacing
            else:
                return [0,line_spacing*(rows+1)],line_spacing
    
    def cursor_cor(self,pos):
        """get the index of the cursor according to the givin position relative to the original text on the widget "(not resized one)" """
        line_spacing = (
            self._drawer.textsize("A", font=self.font, stroke_width=self.stroke_width)[1] + (self.spacing)
        )
        lines=self.text.splitlines()
        total_org_characters=0
        for r,line in enumerate(lines):
            height=line_spacing*(r+1)
            max_x_distance=distance([0,height],pos)
            count_all=False
            current_width=0
            for letter in line:
                #count all if it is not the same cursor row
                if not count_all:
                    current_width+=self._drawer.textsize(letter,self.font, self.spacing, self.direction, self.features, self._language, self.stroke_width)[0]
                    #getting the best 
                    char_distance=distance([current_width,height],pos)
                    if max_x_distance<=char_distance:
                        #check if it is the most perfect row or not by comaparse with next row height
                        #getting first row height
                        height2=line_spacing*(r+2)
                        current_distance=distance([0,height],pos)
                        next_distance=distance([0,height2],pos)
                        #if it is lower distance than next row break the inside loop
                        if next_distance>current_distance:
                            #it is the same distance
                            #finish the loop
                            #break  inside the loop
                            break
                        else:
                            #count all the letters because the cursor is not in the same row
                            count_all=True
                    else:
                        #continue searching
                        max_x_distance=char_distance
                        total_org_characters+=1
                else:
                    total_org_characters+=1
            #check if the loop ended by break or not
            else:
                #if not continue searching
                continue
            print("break")
            #if True break the loop and send the total number of letters
            break

        original_text= self.get(0.0,END)

        current_letters=0
        r,c=0,0
        for r,line in enumerate(original_text.splitlines()):
            if len(line)>=0:
                for c in range(len(line)):
                    if total_org_characters>current_letters:
                        current_letters+=1  
                    else:
                        break
                else:
                    continue
                break
            else:
                c=0
        return str(r)+"."+str(c)       

def main():
    root=Tk()
    img=np.zeros((700,800,3),"uint8")
    from pywidgets.tk.Img import Image_viewer
    def show(*images):
        for img in images:
            img=text_viewer.draw_img_box(img)
            imgShower.define_image(img,False)
    imgShower=Image_viewer(root)

    text_viewer=Text_putter(root,img,box=[0,0,100,700],target=show)
    imgShower.pack()
    text_viewer._textputter.pack(fill=BOTH,expand=YES)
    text_viewer.bind(imgShower.canvas)
    show(img.copy())
    root.mainloop()
    
if __name__=="__main__":
    main()
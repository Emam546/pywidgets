from tkinter import *
import cv2
import numpy as np
import sys,os
from pathlib import Path
sys.path.append(Path(os.path.dirname(__file__)).parent.__str__())
from pywidgets.tk.Img_editor.full_editor import Full_Editor
from pywidgets._imgcv_objects.__origin import *

def main(): 
    root=Tk()
    img=cv2.imread(os.path.join(os.path.dirname(__file__),"./Image.jpg"))

    if img is None:
        raise "the mask" 
    mask=np.zeros(img.shape[:2],"uint8")
    if mask is None:
        raise "error"
    img_editor=Full_Editor(app=root,imgcv=img,mask=mask)
    img_editor.pack(fill=X,expand=YES)
    img_editor.blurred=10
    img_editor.color=(255,0,0)
    img_editor.colorBackground[:]=(255,0,0)
    img_editor.pack(fill=BOTH,expand=YES)
    container_frame=Frame(bg="red")
    button_Control=Button(container_frame,text="control box",command=img_editor.control_moving_box)
    button_Control.pack()
    button_define_box=Button(container_frame,text="define mask",command=img_editor.define_mask)
    button_define_box.pack()
    button_define_box=Button(container_frame,text="make box",command=img_editor.make_box)
    button_define_box.pack()

    button_define_box=Button(container_frame,text="wrapped img",command=img_editor.make_wrapped_image)
    button_define_box.pack()

    button_define_box=Button(container_frame,text="move text",command=lambda :img_editor.move_thresh_image(True))
    button_define_box.pack()

    button_define_box=Button(container_frame,text="select object mask",command=lambda :img_editor.move_selected_area(True))
    button_define_box.pack()

    button_define_box=Button(container_frame,text="move multi object",command=lambda :img_editor.get_all_rotate_boxes(True))
    button_define_box.pack()

    button_define_box=Button(container_frame,text="add edges",command=img_editor.add_edges)
    button_define_box.pack()

    button_define_box=Button(container_frame,text="center state",command=img_editor.text_mode)
    button_define_box.pack()




    container_frame.pack(fill=BOTH,expand=YES)
    def import_image(path):
        imported_image=cv2.imread(path)
        mask=np.zeros(imported_image.shape[:2],"uint8");mask[:]=1
        img_editor.import_img_back_ground(Img_cv(imported_image,mask))

    
    #img_editor.text_mode()
    img_editor.simple_shower()
    root.mainloop()
if __name__=="__main__":
    main()
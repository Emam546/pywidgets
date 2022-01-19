import os
import sys
sys.path.append(os.path.dirname(__file__))
from  __orign import *
from __Img_viewers import *


def main():
    from tkinter import filedialog
    root=Tk()
    imgviewer=Img_with_scrollbar(root)
    imgviewer.pack(fill=BOTH,expand=YES)
    img=None
    def opedimage():
        filename=filedialog.askopenfilename(filetypes=(
            ("ALL","*.*"),
            ("PNG","*.png"),
            ("JPEG","*.jpg")
        ))
        if filename!="":
            global img
            img=cv2.imread(filename,cv2.IMREAD_UNCHANGED)
            imgviewer.define_image(img)
    def zoom(precent):
        currentprecent=imgviewer.zoom+precent
        the_precent.config(text=str(currentprecent)+" %")
        imgviewer.zoomprecent(currentprecent)
    def draw(event,state):
        if img is None:return
        canvas=event.widget
        x,y=int(canvas.canvasx(event.x)),int(canvas.canvasy(event.y))
        cv2.circle(img,(x,y),5,(255,255,255),cv2.FILLED)
        imgviewer.define_image(img)
    Button(text="root",command=opedimage).pack(fill=X)
    buttonframes=Frame()
    buttonframes.pack(fill=X,side=BOTTOM)
    the_precent=Label(buttonframes,text="100 %",width=20,font="microsoft 15",fg="red")
    buttonframes.columnconfigure(0,weight=1)
    buttonframes.columnconfigure(2,weight=1)
    Button(buttonframes,text="<<",command=lambda:zoom(-10)).grid(row=0,column=0,sticky=NSEW)
    Button(buttonframes,text=">>",command=lambda:zoom(10)).grid(row=0,column=2,sticky=NSEW)
    imgviewer.canvas.bind("<Button-1>",lambda e:draw(e,True))
    root.mainloop()  
if __name__=="__main__":
    main() 
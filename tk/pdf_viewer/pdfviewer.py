from tkinter import *
from typing import Dict,AnyStr,List
from pycv2.img.conv_pdf import convert_pdf_to_image
import PyPDF2,threading,numpy as np,cv2
from PIL import ImageTk,Image
from pycv2.img.utils import *
class PDF_Viewer(Frame):
    def __init__(self,app,dpi=200,padpagey=0,color=(255,255,255),radius=10,plusnumpage=4,*args, **kwargs):
        self.dpi=dpi
        self.zoomper=100
        self.padpagey=padpagey
        self.plusnumpage=plusnumpage
        self.num_pages=0
        self.canvas=Canvas(self,bg=self["bg"],scrollregion=(0,0,1000,1000),)
        vscroll=self.vscroll=Scrollbar(self,command=self.canvas.yview)
        hscroll=Scrollbar(self,orient=HORIZONTAL,command=self.canvas.xview)
        self.canvas.config(
            xscrollcommand=hscroll.set,
            yscrollcommand=self.scroll_bar_getter
            )
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.canvas.bind_all("<MouseWheel>",self. _on_mousewheel)
        self.canvas.grid(column=0,row=0,sticky=NSEW)
        vscroll.grid(column=1,row=0,sticky=NSEW)
        hscroll.grid(column=0,row=1,sticky=NSEW)
        self.imgtk:Dict[AnyStr,Image]={}
    def _on_mousewheel(self,event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    def scroll_bar_getter(self,x0,x1):
        if self.num_pages!=0:
            self.vscroll.set(x0,x1)
            self.geting_scrolled()
    def geting_scrolled(self,):
            page=int(self.vscroll.get()[1]*self.num_pages) 
            #height=float(self.canvas["scrollregion"].split(" ")[3])+self.plusnumpage
            #ridm=self.canvas.winfo_height()
            #num=int(((ridm*self.num_pages)/height)/2)+4
            minpage,maxpage=max(0,page-4),min(page+4,self.num_pages)
            the_numbers=list(range(minpage, maxpage))
            threading.Thread(
                target=lambda:self.define_image(the_numbers)
            ).start()
    def put_page(self,page):
        width=int((self.canvas.winfo_width()*self.zoomper)/100)
        if self.imgtk[str(page)][0]!=None \
                and  self.imgtk[str(page)][0].width()==width:return
        self._putpage(page)
    def _putpage(self,page):
        width=int((self.canvas.winfo_width()*self.zoomper)/100)
        img=self.imgtk[str(page)][1]
        w,h=img.size
        r = width / float(w)
        dim = [width, int(h * r)]
        resizedimg=img.resize(dim)
        self.imgtk[str(page)][0]=ImageTk.PhotoImage(image=resizedimg) 
        padding_width=int((self.canvas.winfo_width()-width)/2)
        padding_width=max(0,padding_width)
        #self.canvas.update()
        self.canvas.create_image(
            padding_width,((dim[1]*page)+self.padpagey),
            image=self.imgtk[str(page)][0],anchor=NW
        )
        self.canvas.update()
        
    def define_image(self,pages):
        if self.canvas.winfo_ismapped()!=1:return
        for page in pages:
            if not str(page) in self.imgtk:
                self.imgtk[str(page)]=None
                img=convert_pdf_to_image(self.filename,page,page+1,self.dpi)[0]
                img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                img=Image.fromarray(img.copy())
                self.imgtk[str(page)] = img
            if self.canvas.winfo_ismapped()!=1:break
            if self.imgtk[str(page)] !=None:
                self.put_page(page)
class ImgViewerPdf(Frame):         
    def __init__(self,app,dpi=200,padpagey=0,color=(255,255,255),radius=10,plusnumpage=4,*args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.dpi=dpi
        self.zoomper=100
        self.padpagey=padpagey
        self.plusnumpage=plusnumpage
        self.num_pages=0
        self.radius=radius
        self.color=color
        self.canvas=Canvas(self,bg=self["bg"],scrollregion=(0,0,1000,1000),)
        vscroll=self.vscroll=Scrollbar(self,command=self.canvas.yview)
        hscroll=Scrollbar(self,orient=HORIZONTAL,command=self.canvas.xview)
        self.canvas.config(
            xscrollcommand=hscroll.set,
            yscrollcommand=self.scroll_bar_getter
            )
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        self.canvas.grid(column=0,row=0,sticky=NSEW)
        vscroll.grid(column=1,row=0,sticky=NSEW)
        hscroll.grid(column=0,row=1,sticky=NSEW)

        self.canvas.bind("<Configure>",lambda e:self.config_canvas())
    
    def scroll_bar_getter(self,x0,x1):
        if self.num_pages!=0:
            self.vscroll.set(x0,x1)
            self.geting_scrolled()
    
    def geting_scrolled(self):
            page=int(self.vscroll.get()[1]*self.num_pages) 
            #height=float(self.canvas["scrollregion"].split(" ")[3])+self.plusnumpage
            #ridm=self.canvas.winfo_height()
            #num=int(((ridm*self.num_pages)/height)/2)+4
            minpage,maxpage=max(0,page-4),min(page+4,self.num_pages)
            the_numbers=list(range(minpage, maxpage))
            threading.Thread(
                target=lambda:self.define_image(the_numbers)
            ).start()
                     
    def define_pdf(self,filename):
        self.filename=filename
        pdf_reader = PyPDF2.PdfFileReader(filename)
        self.num_pages= int(pdf_reader.numPages)+1
        self.shape=pdf_reader.getPage(0).mediaBox[2:]
        self.imgtk={}
        self.config_canvas()
        
    def zoom(self,p):
        self.zoomper=p
        self.config_canvas()
        
    def define_image(self,pages):
        if self.canvas.winfo_ismapped()!=1:return
        for page in pages:
            if not str(page) in self.imgtk:
                self.imgtk[str(page)]=None
                img=convert_pdf_to_image(self.filename,page,page+1,self.dpi)[0]
                img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                mask=np.zeros((img.shape[:2]),np.uint8)
                img=Image.fromarray(img.copy())
                self.imgtk[str(page)] = [None,img,img,mask]
            if self.canvas.winfo_ismapped()!=1:break
            if self.imgtk[str(page)] !=None:
                self.put_page(page)
        #self.canvas.update()

    def put_page(self,page):
        width=int((self.canvas.winfo_width()*self.zoomper)/100)
        if self.imgtk[str(page)][0]!=None \
                and  self.imgtk[str(page)][0].width()==width:return
        self._putpage(page)
    
    def _putpage(self,page):
        width=int((self.canvas.winfo_width()*self.zoomper)/100)
        img=self.imgtk[str(page)][1]
        w,h=img.size
        r = width / float(w)
        dim = [width, int(h * r)]
        resizedimg=img.resize(dim)
        self.imgtk[str(page)][0]=ImageTk.PhotoImage(image=resizedimg) 
        padding_width=int((self.canvas.winfo_width()-width)/2)
        padding_width=max(0,padding_width)
        #self.canvas.update()
        self.canvas.create_image(
            padding_width,((dim[1]*page)+self.padpagey),
            image=self.imgtk[str(page)][0],anchor=NW
        )
        self.canvas.update()
        
    def config_canvas(self):
        if self.num_pages==0:return
        c_yview=self.canvas.yview()[0]
        c_xview=self.canvas.xview()[0]
        rdim=[self.canvas.winfo_width(),self.canvas.winfo_height()]
        dim=[0,0]
        w,h=self.shape[:2]
        r = rdim[0] / float(w)
        rdim[1] = int(h * r)
        dim[0]=(self.zoomper*rdim[0])/100
        dim[1]=(self.zoomper*rdim[1])/100
        height=(dim[1]*self.num_pages)+(self.padpagey*self.num_pages)
        self.canvas.config(scrollregion=(0,0,dim[0],height))
        self.canvas.yview_moveto(c_yview)
        
        self.canvas.xview_moveto(c_xview)
        page=int(self.vscroll.get()[1]*self.num_pages) 
        num=int(((rdim[1]*self.num_pages)/height)/2)+self.plusnumpage
        minpage,maxpage=max(0,page-num),min(page+num,self.num_pages)
        the_numbers=list(range(minpage, maxpage))
        for page in the_numbers:
            if str(page) in self.imgtk.copy():
                if self.imgtk[str(page)]!=None:
                    self.put_page(page)
            else:
                self.define_image([page])
        for page in self.imgtk:
            if int(page) not in the_numbers and self.imgtk[page]!=None:
                self.imgtk[page][0]=None
        
    def select_cursor(self,page):
        if self.num_pages!=0:
            self.canvas.yview_moveto(page/self.num_pages)
    
    def bind(self,key,target,add=None):
        def correct(event):
            def right_cor(val):
                return ((val*100)/self.zoomper)
            
                    
            width=(self.canvas.winfo_width()*self.zoomper)/100
            padding_width=int(right_cor((self.canvas.winfo_width()-width)/2))
            padding_width=max(0,padding_width)
            x=right_cor(int(self.canvas.canvasx(event.x)))-padding_width
            y=right_cor(int(self.canvas.canvasy(event.y)))
            target((x,y))

        self.canvas.bind(key,correct,add)
        
class drawingpdf(ImgViewerPdf):
    def __init__(self,app,*args,**kwargs):
        super().__init__(app,*args,**kwargs)
        self.circles={}
        self.circle=None
        self.cilicked=False
        self.bind("<B1-Motion>",lambda e: self.motion(e,True),add="+")
        self.bind("<Button-1>",lambda e: self.motion(e,True),add="+")
        
        self.bind("<Button-3>",lambda e: self.motion(e,False),add="+")
        self.bind("<B3-Motion>",lambda e: self.motion(e,False),add="+")
        
        self.bind("<ButtonRelease-1>",lambda e:self.release())
        self.bind("<ButtonRelease-3>",lambda e:self.release())
        
        self.canvas.bind("<Button>",self.circle_draw,add="+")
        self.canvas.bind("<Motion>",self.circle_draw,add="+")
        self.canvas.bind("<Button-3>",self.circle_draw,add="+")
        self.canvas.bind("<B3-Motion>",self.circle_draw,add="+")
        self.bind_all("<MouseWheel>", lambda e:self.removecircle(),add="+")

        self.canvas.bind("<Enter>",lambda e:self.remove_pointer(False))
        self.canvas.bind("<Leave>",lambda e:self.remove_pointer(True))
        self.__check_areas()
    def motion(self,point,state):
        point=list(point)
        self.cilicked=True
        height=int(
                (
                    int(
                        float(self.canvas["scrollregion"].split(" ")[3]))*100
                )/self.zoomper
            )
        page=str(
            int(
                (point[1]/height)*self.num_pages
                )
            )
        #print(page)
        
        if page not in self.imgtk or  self.imgtk[page]==None:
            return
        #self.draw(state,page,point)
        threading.Thread(
            target=lambda:self.draw(state,
                page,
                point
            )
            ).start()
    def release(self):
        self.cilicked=False
        self.circles={} 
    def draw(self,state,page:str,point):
        if page in self.circles:
            self.circles[page].append(
                (point,state)
            )
        else:
            self.circles[page]=[
                (point,state)
            ]
    
    def __check_areas(self):
        points=self.circles.copy()
        for page in points:
            if len(points[page])<=0:continue
            w,h=self.imgtk[page][2].size
            r=float(w)/self.canvas.winfo_width()
            drawingimg,orgimg,mask=self.imgtk[page][1:]
            drawingimg=np.array(drawingimg)
            drawingimg=cv2.cvtColor(drawingimg,cv2.COLOR_RGB2BGR)
            the_circles=points[page].copy()
            for id,circle in enumerate(the_circles):
                opoint,state=circle
                point=opoint.copy()
                point[0]=int(point[0]*r);point[1]=int(point[1]*r)
                point[1]-=int(h*int(page))
                if len(the_circles)==1 or id==0:
                    if state:
                        cv2.circle(drawingimg,point,self.radius,self.color,cv2.FILLED)
                        cv2.circle(mask,point,self.radius,(255,255,255),cv2.FILLED)
                    else:
                        cv2.circle(mask,point,self.radius,(0,0,0),cv2.FILLED)
                else:
                    pts=the_circles[id-1][0].copy()
                    pts[0]=int(pts[0]*r);pts[1]=int(pts[1]*r)
                    pts[1]-=int(h*int(page))
                    if state:
                        cv2.line(drawingimg,point,pts,self.color,self.radius*2)
                        cv2.line(mask,point,pts,(255,255,255),self.radius*2)
                    else:
                        cv2.line(mask,point,pts,(0,0,0),self.radius*2)
                    if the_circles[id-1] in points[page]:
                        points[page].pop(points[page].index(the_circles[id-1]))
                    if id!= len(the_circles)-1:
                        points[page].pop(points[page].index(circle))
                    
            #self.circles[page]=[]
            orgimg = np.array(orgimg)
            orgimg=cv2.cvtColor(orgimg,cv2.COLOR_RGB2BGR)
            add_image=add_back_ground(orgimg,mask,drawingimg)
            img=cv2.cvtColor(add_image,cv2.COLOR_BGR2RGB)
            img=Image.fromarray(img.copy())
            self.imgtk[page][1]=img
            self.imgtk[page][3]=mask
            self._putpage(int(page))
            if self.circle !=None:
                x_max, y_max, x_min, y_min=self.canvas.coords(self.circle)
                self.canvas.delete(self.circle)
                b,g,r=self.color
                color="#"+rgb_to_hex(r,g,b)
                self.circle = self.canvas.create_oval(x_max, y_max, x_min, y_min, outline=color,fill=color)
        if self.cilicked:
            self.circles=points
        self.winfo_toplevel().after(3,self.__check_areas)
    def remove_pointer(self,state):
        if state:
            self.canvas.config(cursor="arrow")
        else:
            self.canvas.config(cursor="none")
    def circle_draw(self,event):
        if self.num_pages==0:return
        self.remove_pointer(False)
        x=int(self.canvas.canvasx(event.x))
        y=int(self.canvas.canvasy(event.y))
        if self.circle !=None:
            self.canvas.delete(self.circle)
            self.circle=None
        radius=(self.canvas.winfo_width()*self.radius)/self.shape[0]
        radius = int(
            ((radius*self.zoomper)/100)
        )
        x_max = x + radius
        x_min = x - radius
        y_max = y + radius
        y_min = y - radius
        b,g,r=self.color
        color="#"+rgb_to_hex(r,g,b)
        self.circle = self.canvas.create_oval(x_max, y_max, x_min, y_min, outline=color,fill=color)
        
        #self.canvas.update()
    def removecircle(self):
        if self.circle !=None:
            self.canvas.delete(self.circle)
            self.remove_pointer(True)
    
class addingImg(drawingpdf):
    def __init__(self,app,*args,**kwargs):
        super().__init__(app,*args,**kwargs)  
        self.points=[0,0,0,0]
    
    def draw(self,state,page:str,point):
        x,y=point
        circles=self.points
        if self.grab!=None:
            close=circles[self.grab]
        else:close=closest_node([x,y],circles,maxdistance=self.radius_cursor)
        if close!=None:
            self.grab=self.points.index(close)
            pass        
        else:
            if page in self.circles:
                self.circles[page].append(
                    (point,state)
                )
            else:
                self.circles[page]=[
                    (point,state)
                ]
        
    def grab_box(self,point,state,pos):
        x,y = point
        x,y=(x+pos[0]),(y+pos[1])
        pos=x,y
        circles=self.points.copy()
        index=self.points.index(point)
        close=list(point)
        if close in circles[:4]:
            xsame,ysame=[(0,3),(1,2)],[(0,1),(2,3)]
            for id,same in enumerate([xsame,ysame]):
                for groub in same:
                    if close in circles[:4]:
                        if  circles[:4].index(close) in groub:
                            for cor in groub:
                                self.points[cor][id]=[x,y][id]

        self.grab=index
        self.target(self.mask,circles)

    def release(self):
        self.cilicked=False
        self.circles={} 
        self.grab=None
        self.brushing=False
    
    def check_mouse_box(self,page,point):
        pass


if __name__=="__main__":
    from tkinter import filedialog
    def openpdf(self:ImgViewerPdf):
        filename=filedialog.askopenfilename(filetypes=(
            ("PDF FILES","*.pdf"),
            ("PDF FILES","*.PDF")
        ))
        if filename!="":
            self.define_pdf(filename)
            self.winfo_toplevel().lift()
    root=Tk()
    pdfviwer=ImgViewerPdf(root,80,padpagey=0)
    pdfviwer.pack(fill=BOTH,expand=YES)
    def zoom(precent):
        currentprecent=pdfviwer.zoomper+precent
        the_precent.config(text=str(currentprecent)+" %")
        pdfviwer.zoom(currentprecent)
    
    Button(text="root",command=lambda:openpdf(pdfviwer)).pack(fill=X)
    buttonframes=Frame()
    buttonframes.pack(fill=X,side=BOTTOM)
    the_precent=Label(buttonframes,text="100 %",width=20,font="microsoft 15",fg="red")
    buttonframes.columnconfigure(0,weight=1)
    buttonframes.columnconfigure(2,weight=1)
    Button(buttonframes,text="<<",command=lambda:zoom(-10)).grid(row=0,column=0,sticky=NSEW)
    Button(buttonframes,text=">>",command=lambda:zoom(10)).grid(row=0,column=2,sticky=NSEW)
    the_precent.grid(row=0,column=1,sticky=NSEW)
    
    root.mainloop()
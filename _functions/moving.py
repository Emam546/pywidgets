import sys,os
sys.path.append(os.path.dirname(__file__))
from origin import *
from pycv2.img.drawing.box import draw_box_moving, drawbox
COLOR_CIRCLES=np.zeros((4,3),np.int)
COLOR_CIRCLES[:,2]=255
COLOR_CIRCLES=COLOR_CIRCLES.tolist()
class multiy_selected_boxs:
    def __init__(self,boxs,target,radius_selcting=10):           
        self.radius_selcting=radius_selcting
        self.boxs=boxs
        self.grab=None
        self.target=target

    def motion(self,pos):
        x,y=pos
        if self.grab==None:
            for id,bx in enumerate(self.boxs):
                bx.circles=convert_tupel_to_list(bx.circles)
                close=closest_node([x,y],bx.circles,maxdistance=self.radius_selcting)
                if close!=None and close in bx.circles:
                    index=bx.circles.index(close)
                    self.grab=(id,index)
                    break
        if self.grab !=None:
            close,index=self.grab
            self.boxs[close].grab_box(pos,index)
            self.target(self.boxs)
    def release(self):
        self.grab=None
        self.target(self.boxs)

class Object_mover():
    def __init__(self, mask,*srcs,target,
                 rotate_state=False,copy_state=False,radius_painting=2,radius_selcting):
        #mask of complet image is un complet image
        
        self.radius_selcting=radius_selcting
        self.target=target
        self.grab=None
        self.angel=0
        self.rotate=None
        self.rotate_state=rotate_state
        self.croped_objects=[]
        b=box=newbox(mask)
        for img in srcs:
            if copy_state:
                background_images=img.copy()
            else:
                background_images=cv2.inpaint(img, mask, radius_painting, cv2.INPAINT_TELEA)
            croped_img=img.copy()[b[1]:b[1]+b[3],b[0]:b[0]+b[2]]
            croped_mask=mask.copy()[b[1]:b[1]+b[3],b[0]:b[0]+b[2]]
            self.croped_objects.append(object_moving(croped_img,background_images,croped_mask))
        self.circles=xywh_2_pts(box)
        #appendingcenter point
        self.orginal_box=list(box).copy()
        self.pos=box[:2]


    def motion(self,pos):
        x,y=pos
        cx,cy=center_pts(self.circles)
        if self.rotate is None:
            circles=self.circles.copy()
            circles.append(center_pts(circles))
            #getting rotated points to idetificate it
            if self.rotate_state:
                for id,pt in enumerate(circles[:4]):
                    circles[id]=get_rotated_point((cx,cy),pt,math.radians(self.angel))
            #circles just for selecting
            close=closest_node(pos,circles,maxdistance=self.radius_selcting)
            close=circles[self.grab] if self.grab!=None else close
            if close!=None:
                #updating box
                index=circles.index(close)
                if index==4:
                    cenx,ceny=pos
                    dx,dy=cenx-cx,ceny-cy
                    for id,pt in enumerate(self.circles.copy()):
                        self.circles[id]=clamp_point([pt[0]+dx,pt[1]+dy],self.croped_objects[0].background)
                    self.pos=[self.pos[0]+dx,self.pos[1]+dy]
                    self.grab=index
                elif self.rotate_state:
                    self.rotate=self.dem=self.lastdem=list(pos)
                """elif not self.rotate_state:
                    w,h=self.orginal_box[2:4]
                    cx,cy=self.pos
                    x_r,y_r=clamp_point(
                        (max(cx, min(x, cx+w)),max(cy, min(y, cy+h))),self.resultimg
                        )

                    for id,same in enumerate([xsame,ysame]):
                        for groub in same:
                            if index in groub:
                                for cor in groub:
                                    self.d_box[cor][id]=[x_r,y_r][id]
                    #centering the object again
                    self.d_box[-1]=centerbox(pts_2_xywh(self.d_box[:4]))
                else:
                    pass
                    #rotated box
                    # x_r,y_r=clamppo()
                    # dx,dy=cenx-cx,ceny-cy
                    # for id,same in enumerate([xsame,ysame]):
                    #     for groub in same:
                    #         if index in groub:
                    #             for cor in groub:
                    #                 self.d_box[cor][id]=[x_r,y_r][id]
                """
            elif self.rotate_state:
                self.rotate=self.dem=self.lastdem=list(pos)
        else:
            self.dem=pos
            rx,ry=self.lastdem
            #setting the angle only
            self.angel-=math.degrees(math.atan2(ry-cy,rx-cx)-
                        math.atan2(y-cy,x-cx))
            if self.dem!=self.lastdem:self.lastdem=self.dem
        self.target(*self.result())
    def result(self):
        return[img_object.get_rotated_image(self.pos,self.angel,pts_2_xywh(self.circles[:4])) for img_object in self.croped_objects]
    
    def draw_image(self,img, color_line=(255,255,0),thickness=2,radius=2,
        colors=COLOR_CIRCLES,colorcenter=(0,0,255)):
        points=self.circles.copy()
        center=center_pts(self.circles)
        for id,pos in enumerate(self.circles[:4]):
            points[id]=get_rotated_point(center,pos,math.radians(self.angel))
        img=draw_box_moving(img,points,color_line,thickness,radius,colors,True,colorcenter)
        if not self.rotate is None:
            #draw the angel lines for inter face
            cv2.line(img,center,self.rotate,(0,0,255),thickness)
            cv2.line(img,center,self.dem,(0,0,255),thickness)
        cv2.circle(img,center,radius,colorcenter,cv2.FILLED)
        return img
    def restore(self):
        w,h=self.orginal_box[2:4]
        self.circles[:4]=xywh_2_pts([self.pos[0],self.pos[1],w,h])
        self.target(*self.result())   
    def release(self):
        self.grab=None
        self.rotate=None
        self.target(*self.result())

class Muilty_box_remover():
    class smallbox(Rotated_object):
        def __init__(self,box,cropedimg,threshimg):
            super().__init__(cropedimg,threshimg)
            self.d_box=xywh_2_pts(box)
            self.angel=0
            self.dem=[0,0]
            self.lastdem=[0,0]
        def motion(self,pos,maximum_center=10):
            #return rotate state
            center=center_pts(self.d_box)
            b=pts_2_xywh(self.d_box)
            #to enusre that the position is not insde the radius
            if distance(center,pos)<= maximum_center:
                self.move(pos)
                return False
            else:
                self.dem=pos
                self.lastdem=pos
                return True

        def rotate(self,pos):
            x,y=pos
            cx,cy=center_pts(self.d_box)
            self.dem=pos
            rx,ry=self.lastdem
            self.angel-=math.degrees(math.atan2(ry-cy,rx-cx)-
                        math.atan2(y-cy,x-cx))
        
            self.lastdem=self.dem if self.dem!=self.lastdem else self.lastdem
                
        def move(self,pos):
            x,y=pos
            cx,cy=center_pts(self.d_box)
            dx,dy=x-cx,y-cy
            for id,pt in enumerate(self.d_box):
                self.d_box[id]=[pt[0]+dx,pt[1]+dy]
        def put_img(self,resultimg,resultmask=None):
            resultmask=resultmask if not resultmask is None else np.zeros(resultimg.shape[:2],"uint8")

            box=self.d_box.copy()
            center=center_pts(self.d_box)
            angel=math.radians(self.angel)
            for id,pos in enumerate(self.d_box[:4]):
                box[id]=get_rotated_point(center,pos,angel)
            img=rotate_object(self.d_box[0],self.cropedimg,resultimg,self.angel,self.thresh)
            mask=rotate_object(self.d_box[0],self.thresh,resultmask,self.angel)
            return img,mask
        def draw(self,*images,colorline=(255,255,0),color_circles:tuple=COLOR_CIRCLES,thickness=2,radius=0):
            points=self.d_box.copy()
            images=list(images)
            center=center_pts(self.d_box)
            angel=math.radians(self.angel)
            for id,pos in enumerate(self.d_box[:4]):
                points[id]=get_rotated_point(center,pos,angel)
            for i,img in enumerate(images):
                
                images[i]=draw_box_moving(img,points,colorline,thickness,radius,color_circles,)
                cv2.circle(img,center,4,color_circles[0],cv2.FILLED)
            
            images=images[0] if len(images)==1 else images
            return images
        def draw_rotate(self,resultimg,pos,color_rotaate=(0,0,255),thickness=3):
            center=center_pts(self.d_box)
            cv2.line(resultimg,center,pos,color_rotaate,thickness)
            cv2.line(resultimg,center,self.dem,color_rotaate,thickness)
            return resultimg

    def __init__(self,completeimg,full_mask,all_boxs,target,radius_brushing=2,rotate_state=True,copy_state=False,radius_selecting=10):
        self.radius_selecting=radius_selecting
        self.target=target
        if copy_state:
            self._background_img=completeimg.copy()
        else:
            self._background_img=self.inpaintimg=cv2.inpaint(completeimg,full_mask, radius_brushing, cv2.INPAINT_TELEA)
        self.resultimg=completeimg.copy()
        self.all_boxs=[]
        for b in all_boxs:
            cropedimg=completeimg[b[1]:b[1]+b[3],b[0]:b[0]+b[2]]
            cropedthresh=full_mask[b[1]:b[1]+b[3],b[0]:b[0]+b[2]]
            self.all_boxs.append(
                self.smallbox(b,cropedimg,cropedthresh)
                )
        
        self.rotate=None
        self.rotate_state=rotate_state
        self.grab=None
        self.put_allboxs()
    def put_allboxs(self,*excetions,draw=True):
        self.putting_img=self._background_img.copy()
        self.putting_mask=np.zeros(self.putting_img.shape[:2],"uint8")
        for box in self.all_boxs:
            if box not in excetions:
                self.putting_img,self.putting_mask =box.put_img(self.putting_img,self.putting_mask)

        if draw:
            self._drawing_img=np.zeros_like(self.putting_mask,"uint8")
            for box in self.all_boxs:
                if box not in excetions:
                    self._drawing_img=box.draw(self._drawing_img)
            
    def motion(self,pos,state):
        if not state:
            return self.remove_box(pos)
        x,y=pos
        index=None
        change=False
        if self.rotate==None:
            nodes=[center_pts(box.d_box) for box in self.all_boxs]
            closest_index=nodes.index(closest_node(pos,nodes))
            if self.grab==None:
                if distance(nodes[closest_index],pos)<=self.radius_selecting:
                    index=closest_index
            else:
                index=self.grab
            if index !=None:
                rotateing_state=self.all_boxs[index].move(pos)

            else:
                rotateing_state=self.all_boxs[closest_index].motion(pos,self.radius_selecting)
                change=rotateing_state
                self.rotate=pos if rotateing_state else None
                self.grab=self.grab if not rotateing_state else None
        else:
            self.grab=None
            self.all_boxs[-1].rotate((x,y))
        if index!=None:
            if self.grab==None:
                self.all_boxs.append(self.all_boxs.pop(index))
                self.put_allboxs(self.all_boxs[-1])
            self.grab=-1
        elif change:
            self.all_boxs.append(self.all_boxs.pop(closest_index))
            self.put_allboxs(self.all_boxs[-1])
        self.update(self.all_boxs[-1])
        
       

    def update(self,smallbox: smallbox):
        self.resultimg,self.result_mask=smallbox.put_img(self.putting_img.copy(),self.putting_mask.copy())
        self.target(self.resultimg.copy(),self.result_mask.copy())
    def draw_img(self,image,defult_draw=True,colorline=(255,255,0),color_circles:tuple=COLOR_CIRCLES,thickness=2,radius=0):
        result_img=image.copy()
        result_img=cv2.cvtColor(result_img,cv2.COLOR_GRAY2BGR) if len(result_img.shape)==2 else result_img
        if defult_draw:
            drawed_img=self.all_boxs[-1].draw(self._drawing_img.copy(),colorline=colorline,color_circles=color_circles,thickness=thickness,radius=radius)
            drawed_mask=cv2.threshold(cv2.cvtColor(drawed_img,cv2.COLOR_BGR2GRAY),0,255,0)[1]
            img=add_back_ground(result_img,drawed_mask,drawed_img)
        else:
            for box in self.all_boxs:
                result_img=box.draw(result_img,colorline=colorline,color_circles=color_circles,thickness=thickness,radius=radius)
            img =result_img
        if self.rotate is None:
            return img
        else:
            return self.all_boxs[-1].draw_rotate(img,self.rotate,thickness)
    def release(self):
        self.grab=None
        self.rotate=None
        self.target(self.resultimg.copy(),self.result_mask.copy())
    def remove_box(self,pos):
        nodes=[center_pts(box.d_box) for box in self.all_boxs]
        close=closest_node(pos,nodes,self.radius_selecting)
        if close!=None:
            index=nodes.index(close)
            self._background_img=self.all_boxs[index].put_img(self._background_img.copy())[0]
            self.all_boxs.pop(index)
            self.put_allboxs()
            self.release()
            self.update(self.all_boxs[-1])


class Multi_mover_selector:
    #returning img,mask,circles of drawing and the, moving state
    def __init__(self,threshimg,completeimg,target
                 ,rotate_state=False,copy_state=False,radius_cutting=2,radius_selecting=10):
        
        self.result_img=completeimg.copy()
        self.result_mask=threshimg.copy()
        #taking colorfrom unmoved image
        self.unmoved_img=completeimg.copy()
        self.unmoved_thresh=threshimg.copy()
        self.target=target
        self.rotate_state=rotate_state
        if copy_state:
            self.backgroundImg=completeimg.copy()
        else:
            self.backgroundImg=cv2.inpaint(completeimg, threshimg, radius_cutting, cv2.INPAINT_TELEA)
        #the cutted image
        self._cutted_img=None
        self._cutted_thresh=None
        #the other uncroped image
        self._comp_other_img=None
        self._comp_other_thresh=None

        self.radius_selecting=radius_selecting
        self.start_pos=None

        self.angel=0
        self.rotate=None
        
        self.selected_object=None
        self.pos=None
        self._current_box=None
        self.grab=None  
    def bind(self,canvas):
        def correct(event,state=True):
            x,y = int(event.widget.canvasx(event.x)),int(event.widget.canvasy(event.y))
            self.motion(clamp_point([x,y],self.unmoved_img),state)
        canvas.bind("<ButtonRelease-1>",lambda e:self.release())
        canvas.bind("<ButtonRelease-3>",lambda e:self.release())
        canvas.bind("<B1-Motion>",correct)
        canvas.bind("<Button-1>",correct)
        canvas.bind("<Button-3>",lambda e: correct(e,False))
    def _grab_box(self,pos):
        x,y=pos
        circles=self.selected_object.copy()
        cx,cy=center_pts(circles)
        circles.append([cx,cy])
        if self.rotate_state:
            circles=get_rotated_pts(circles,math.radians(self.angel))
        if self.rotate is None:
            if self.grab==None:
                close=closest_node(pos,circles,self.radius_selecting)
                index=circles.index(close) if not close is None else None
            else:
                index=self.grab
            
            if not index is None:
                #circles just for selecting
                if index==4:
                    cenx,ceny=x,y
                    dx,dy=cenx-cx,ceny-cy
                    for id,pt in enumerate(self.selected_object.copy()):
                        self.selected_object[id]=clamp_point([pt[0]+dx,pt[1]+dy],self.unmoved_img)
                    self.pos=[self.pos[0]+dx,self.pos[1]+dy]
                # else:
                #     cx,cy=circles[index]
                #     cenx,ceny=x,y
                #     dx,dy=cenx-cx,ceny-cy
                #     for id,same in enumerate([xsame,ysame]):
                #             for groub in same:
                #                 if index in groub:
                #                     for cor in groub:
                #                         self.selected_object[cor][id]+=[dx,dy][id]
                    
                #     w,h=self.orginal_box[2:4]
                #     # _x,_y=self.pos[0]+(w//2),self.pos[1]+(h//2)
                #     # cx,cy=get_rotated_point((_x,_y),self.pos,math.radians(self.angel))
                #     def _clamp_box(pos):
                #         x,y=pos
                #         cx,cy=self.pos
                #         return clamp_point(
                #             (max(cx, min(x, cx+w)),max(cy, min(y, cy+h))),self.unmoved_img
                #         )
                #     for id,pt in enumerate(self.selected_object):
                #         self.selected_object[id]=_clamp_box(pt)
                
                self.grab=index
            elif self.rotate_state:
                #setting new diminsions for rotating object
                self.rotate=[x,y]
                self.dem=[x,y]
                self.lastdem=[x,y]
        else:
            self.dem=[x,y]
            rx,ry=self.lastdem
            #setting the angle only
            self.angel-=math.degrees(math.atan2(ry-cy,rx-cx)-
                        math.atan2(y-cy,x-cx))
            self.lastdem=self.dem if self.dem!=self.lastdem else self.lastdem
        self._put_imgs(self.angel)
    def _put_imgs(self,angle):

        self.result_img=rotate_object(self.pos,self._cutted_img,self.unmoved_img,angle,self._cutted_thresh)
        self.result_mask=rotate_object(self.pos,self._cutted_thresh,self.unmoved_thresh,angle,self._cutted_thresh)
        self.target(self.result_img.copy(),self.result_mask.copy(),get_rotated_pts(self.selected_object,math.radians(self.angel)),True)
    @staticmethod
    def draw_box_selectingarea(src,circles=None,state=True,colorline=(255,255,0),color_circles:tuple=COLOR_CIRCLES,thickness=2,radius=4):
        if circles is None :return src
        src=src if len(src.shape)>=2 else cv2.cvtcolor(src,cv2.COLOR_GRAY2BGR)  
        if state:
            return draw_box_moving(src.copy(),circles,colorline,thickness,radius,color_circles,True)
        else:
            return drawbox(src.copy(),pts_2_xywh(circles),colorline,thickness)
    def draw_image(self,src,circles=None,state=True,colorline=(255,255,0),color_circles:tuple=COLOR_CIRCLES,thickness=2,radius=0):
        img=self.draw_box_selectingarea(src,circles,state,colorline,color_circles,thickness,radius)
        if state and self.rotate!=None:
            cx,cy=center_pts(circles)
            #draw the angel lines for inter face
            cv2.line(img,(cx,cy),self.rotate,colorline,thickness)
            cv2.line(img,(cx,cy),self.dem,colorline,thickness)
        return img
        
    def _drag_box(self,pos):
        if not self.start_pos is None:
            pt1=pos
            pt2=self.start_pos
            x,y=min(pt1[0],pt2[0]),min(pt1[1],pt2[1])
            w,h=max(pt1[0],pt2[0])-x,max(pt1[1],pt2[1])-y
            self._current_box=box=[x,y,w,h]
            self.target(self.unmoved_img,self.unmoved_thresh,xywh_2_pts(box),False)
        else:
            self.start_pos=pos
    def motion(self,pos,state):
        if state:
            if self.selected_object is None:
                self._drag_box(pos)
            else:
                self._grab_box(pos)
        else:
            self._right_click(pos)

    def _make_thresh(self,b):
        cutted_thresh=self.unmoved_thresh[b[1]:b[1]+b[3],b[0]:b[0]+b[2]]
        if cv2.countNonZero(cutted_thresh)==0:return None
        b=newbox(cutted_thresh,b)
        self._cutted_img=self.unmoved_img.copy()[b[1]:b[1]+b[3],b[0]:b[0]+b[2]]
        self._cutted_thresh=self.unmoved_thresh.copy()[b[1]:b[1]+b[3],b[0]:b[0]+b[2]]
        self.unmoved_thresh[b[1]:b[1]+b[3],b[0]:b[0]+b[2]]=0
        self.unmoved_img[b[1]:b[1]+b[3],b[0]:b[0]+b[2]]=self.backgroundImg[b[1]:b[1]+b[3],b[0]:b[0]+b[2]]
        return b
    def _right_click(self,pos):
        if not self.selected_object is None:
            if self.radius_selecting>=distance(pos,center_pts(self.selected_object)):
                self.unmoved_img=self.result_img.copy()
                self.unmoved_thresh=self.result_mask.copy()
                self.selected_object=None
                self.target(self.unmoved_img,self.unmoved_thresh,None,False)
        self.release()
    def release(self):
        if self._current_box!=None:
            self._current_box=self._make_thresh(self._current_box)
            if not self._current_box is None:
                self.orginal_box=self._current_box
                self.selected_object=xywh_2_pts(self._current_box)
                self.pos=self._current_box[:2]
                self.motion(self.pos,True)
            self._current_box=None
        else:
            self.rotate=None
            self._put_imgs(self.angel)
            
        self.start_pos=None
        self.grab=None
        self.rotate=None

class Adding_edges_background():
    def __init__(self,*images,target,blanck_background=False,color_bakcground=(0,0,0),radius_selcting=10):
        """all the images with the same size
        target will return all_blank area *images to view it in viewer
        #get the result image from result method
        """
        self.radius_selcting=radius_selcting
        h,w=images[0].shape[:2]
        self._blackbackground=np.zeros((h*2,w*2,3),"uint8")
        self.circle_positions=xywh_2_pts([0,0,w,h])
        self.original_images=images
        self.border_images=[img.copy() for img in images]

        self.target=target
        self._border_type=cv2.BORDER_CONSTANT if blanck_background else cv2.BORDER_REPLICATE
        self.value=color_bakcground

        self.grab_expanded_edges=False
        self.grab_border_edges=False
        self.grab=None
    def motion(self,pos):
        h,w=self._blackbackground.shape[:2]
        expanded_eges=xywh_2_pts([0,0,w,h])
        #poping 0,0 corner
        expanded_eges.pop(0)
        close=True if self.grab_expanded_edges  else closest_node(pos,expanded_eges,self.radius_selcting)
        #to ensure the border don't stick with grab_border_edges
        if close is None or self.grab_border_edges or not self.grab is None:

            #corner of the background image
            circles=self.circle_positions.copy()
            circles.append(center_pts(circles))
            #getting the inside image positions
            close=circles[self.grab] if not self.grab is None else closest_node(pos,circles,self.radius_selcting)
            if close is None or self.grab_border_edges:
                h,w=self.border_images[0].shape[:2]
                border_expanded_edges=xywh_2_pts([0,0,w,h])
                #poping 0,0 corner

                border_expanded_edges.pop(0)
                #getting outside iamge border to modfie

                close=True if self.grab_border_edges else closest_node(pos,border_expanded_edges,self.radius_selcting)
                if not close is None:
                    self.grab_expanded_edges=False
                    self.grab_border_edges=True
                    self.garb=None
                    oh,ow=self.border_images[0].shape[:2]
                    #getting old diminshion to rationalization
                    old_dim=(ow,oh)
                    self.border_images=[self._drag_blankimage(img,pos,self._border_type,self.value) for img in self.border_images]        
                    #getting new diminshion to rationalization
                    nh,nw=self.border_images[0].shape[:2]
                    new_dim=(nw,nh)
                    #changeing the size of border image
                    for i,val in enumerate(self.circle_positions.copy()):
                        for g,corr in enumerate(val):
                            self.circle_positions[i][g]=int(corr*(new_dim[g]/old_dim[g]))
                    self._send()
            else:    
                #changeing position
                self._drag_pts(pos,circles.index(close))
                #drag the image
                self.drag_image()
                self._send()
 
        else:
            h,w=self.border_images[0].shape[:2]
            #to don't resize blank image over the view
            pos=max(w,pos[0]),max(h,pos[1])
            self.grab_expanded_edges=True
            self.grab_border_edges=False
            self.garb=None
            self._blackbackground=self._drag_blankimage(self._blackbackground,pos)
            self._send()
    @staticmethod
    def __merge_images(blankimages,src):
        src=cv2.cvtColor(src,cv2.COLOR_GRAY2BGR) if len(src.shape)==2 else src
        h,w=src.shape[:2]   
        blankimages[0:h,0:w]=src
        return blankimages
    
    def _send(self):
        self.target(*[self.__merge_images(self._blackbackground.copy(),img)for img in self.border_images])

    def result(self):
        return self.border_images
    def _drag_pts(self,pos,index=None):
        if index is None:
            circles=self.circle_positions.copy()
            circles.append(center_pts(circles))
            close=circles[self.grab] if not self.grab is None else closest_node(pos,circles,self.radius_selcting)
            index=circles.index(close)if not close is None else None
        cx,cy=center_pts(self.circle_positions)
        if index!=None:
            if index==4:
                cenx,ceny=pos
                dx,dy=cenx-cx,ceny-cy
                for id,pt in enumerate(self.circle_positions.copy()):
                    self.circle_positions[id]=clamp_point([pt[0]+dx,pt[1]+dy],self.border_images[0])
            else:
                x_r,y_r=clamp_point(pos,self.border_images[0])
                for id,same in enumerate([xsame,ysame]):
                    for groub in same:
                        if index in groub:
                            for cor in groub:
                                self.circle_positions[cor][id]=[x_r,y_r][id]
                    #centering the object again
                
            self.grab=index

         
    def drag_image(self):
        w,h=pts_2_xywh(self.circle_positions)[2:]
        oh,ow=self.border_images[0].shape[:2]
        self.border_images=[\
            self._border_image(cv2.resize(img,(w,h)),self.circle_positions,(ow,oh),self._border_type,self.value)\
            for img in self.original_images]
    @staticmethod
    def _border_image(src,pts,dim,border_type=cv2.BORDER_CONSTANT,value=(0,0,0)):
        b=pts_2_xywh(pts)
        left,top=b[:2]
        w,h=dim
        right,bottom=w-(left+b[2]),h-(top+b[3])
        return cv2.copyMakeBorder(src,top,bottom,left,right,border_type)


    @staticmethod
    def _drag_blankimage(src,pos,border_type=cv2.BORDER_CONSTANT,value=(0,0,0)):
  
        h,w=src.shape[:2]
        #left bottom
        right_pad,bottom_pad=[max(0,val-[w,h][i]) for i,val in enumerate(pos)]
        final_image=cv2.copyMakeBorder(src,0,bottom_pad,0,right_pad,border_type,value=value)
        
        x,y=[max(0,[w,h][i]-val) for i,val in enumerate(pos)]
        croped_image=final_image.copy()[0:h-y+bottom_pad,0:w-x+right_pad]
        #crop the image
        return croped_image

    def release(self):
        self.grab_expanded_edges=False
        self.grab_border_edges=False
        self.grab=None
    

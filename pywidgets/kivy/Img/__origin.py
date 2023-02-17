from kivy.uix.image import Image
import cv2
from kivy.graphics.texture import Texture
from kivy.uix.floatlayout import FloatLayout
from pywidgets.kivy.bind_widget import Bind_widget
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder


def generate_texture(imgcv,code="bgr"):
    imgcv = cv2.flip(imgcv, 0)
    data = imgcv.tobytes()
    
    # texture
    texture = Texture.create(size=(imgcv.shape[1], imgcv.shape[0]), colorfmt=code)
    texture.blit_buffer(data, bufferfmt="ubyte", colorfmt=code)
    
    return texture

class Binding_Image(Image,Bind_widget):
    def on_touch_down(self, touch):
        return Bind_widget.on_touch_down(self,touch)
    def on_touch_up(self, touch):
        return Bind_widget.on_touch_up(self,touch)
    def on_touch_move(self, touch):
        return Bind_widget.on_touch_move(self,touch)
class _Basic():
    def __init__(self,zoom=100):
        self.image_viewer=Binding_Image(size_hint=(None,None),pos_hint={"top": 1,})
        self.zoom=zoom
    def define_image(self,imgcv):
        self.imgcv=imgcv
        h,w=imgcv.shape[:2]
        h=int((self.zoom*h)/100)
        w=int((self.zoom*w)/100)
        resized_img=cv2.resize(imgcv,(w,h))
        self.image_viewer.texture=generate_texture(resized_img)
        self.image_viewer.size=self.image_viewer.texture_size

    def bind_touch(self,key,target,add=""):
        """Binding a whole image to get a corrected key

        Args:
            key ([str]): [key_word binding]
            target ([function]): [the reutrned target function]
        """
        def binding(event):
            event.x=int((event.x/self.zoom)*100)
            event.y=int((event.y/self.zoom)*100)
            target(event)
        self.image_viewer.bind_touch(key,binding,add)
    def hide_widget(self,wid, dohide=True):
        
        if dohide:
            wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True
        elif hasattr(wid,"saved_attrs"):
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
            
class Img(FloatLayout,_Basic):
    def __init__(self,zoom=100 ,**kwargs):
        super().__init__(**kwargs)
        _Basic.__init__(self,zoom=zoom)
        self.add_widget(self.image_viewer)
        

class Img_with_scrollbar(GridLayout,_Basic):
    def __init__(self,zoom=100 ,**kwargs):
        super().__init__(**kwargs)
        _Basic.__init__(self,zoom=zoom)
        
Builder.load_string("""
#:set cursor_radius dp(20)
<Img_with_scrollbar>
    rows:2
    columns:2
    on_size:
        self.hide_widget(horizinal_scroll,(self.width>self.image_viewer.texture_size[0]))
        self.hide_widget(vertical_scroll,(self.height>self.image_viewer.texture_size[1]))
    ScrollView:
        id:image_viewer
        scroll_y:vertical_scroll.value/100
        scroll_x:horizinal_scroll.value/100
        scroll_type:["bars"]
        on_parent:
            self.add_widget(self.parent.image_viewer)
    Slider:
        id:vertical_scroll
        value:image_viewer.scroll_y*100
        size_hint:(None,1)
        width:dp(20)
        orientation:'vertical'
        cursor_size:cursor_radius,cursor_radius
      
            

            
    Slider:
        id:horizinal_scroll
        value:image_viewer.scroll_x*100
        size_hint:(1,None)
        height:dp(20)
        orientation:"horizontal"
        cursor_size:cursor_radius,cursor_radius
    

""")






if __name__=="__main__":
    from kivy.app import App
    import numpy as np
    #image_viewer=Img()
    kv_file=Builder.load_string("""
#:import np numpy
BoxLayout:
    orientation:'vertical'
    Img_with_scrollbar:
        on_parent:
            self.bind_touch("<Button-1>",lambda x:print("widget 1"))
            self.define_image(np.random.randint(0,255,(1000,200,3),"uint8"))
    Img_with_scrollbar:
        on_parent:
            self.bind_touch("<Button-1>",lambda x:print("widget 2"))
            self.define_image(np.random.randint(0,255,(200,1000,3),"uint8"))
    """)
    
    class Programme(App):
        def build(self):
            return kv_file
      
            
           
    Programme().run()

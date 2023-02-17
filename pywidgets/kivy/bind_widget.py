from kivy.uix.widget import Widget
from pywidgets.kivy.binding import *

class Touch():
    def __init__(self,pos):
        self.x,self.y=pos
    @property
    def pos(self):
        return self.x,self.y
    @pos.setter
    def pos(self, value:tuple):
        self.x,self.y = value
  

class Bind_widget(Widget):
    def _detect_event(self,touch,event):
        if hasattr(self,"bindings") and self.collide_point(*touch.pos):
            if touch.button in self.bindings[event]:
                touch_in_modal = (int(touch.x - self.pos[0]),int(self.height-(touch.y- self.pos[1]))) 
                for target in self.bindings[event][touch.button]:
                    target(Touch(touch_in_modal))
    def on_touch_move(self, touch):
        self._detect_event(touch,MOTION)
    def on_touch_down(self, touch):
        if touch.is_double_tap:
            self._detect_event(touch,DOUBLE_PRESS)
        else:
            self._detect_event(touch,PRESS)
    def on_touch_up(self, touch):
        if not touch.is_double_tap:
            self._detect_event(touch,RELEASE)

    def remove_bind(self,key=None):
        if key==None:
            #clearing the binding dict
            for event in  self.bindings:
                self.bindings[event]={}
        elif key in self.bindings:
            if key in BINDING:
                event,mouse=BINDING[key]
                if mouse in self.bindings[event]:
                    self.bindings[event].pop(mouse)
            else:
                raise "The key is not in the list"
    def bind_touch(self,key,target,add=None):
        if not hasattr(self,"bindings"):
            self.bindings={
                MOTION:{},
                PRESS:{},
                DOUBLE_PRESS:{},
                RELEASE:{},
            }
        if key in BINDING:
            event,mouse=BINDING[key]
            #check if the key in add state or not
            if mouse in self.bindings[event]:
                if add=="+":
                    self.bindings[event][mouse]+=target
                else:
                    self.bindings[event][mouse]=[target]
            else:
                self.bindings[event][mouse]=[target]
        else:
            raise "The key is not in the list"

if __name__=="__main__":
    from kivy.app import App
    from kivy.lang import Builder
    kv_file=Builder.load_string("""
BoxLayout:
    orientation:'vertical'
    Bind_widget:
        on_parent:self.bind_touch("<Button-1>",lambda x:print("widget 1"))
        Button:
            size_hint:None,None
            size:self.parent.size
            
    Bind_widget:
        on_parent:self.bind_touch("<Button-1>",lambda x:print("widget 2"))
""")
    class Programme(App):
        def build(self,):
            return kv_file
    Programme().run() 


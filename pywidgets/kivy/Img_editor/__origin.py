import re
from kivy.uix.boxlayout import BoxLayout
from pywidgets._imgcv_objects.__origin import Img_cv,INR
from pywidgets.kivy.Notebook import CusNotebook
from kivy.core.window import Window
from pykeyboard.keys import ENTER
from pywidgets.kivy.Img import Img
class EMViwerer(CusNotebook,Img_cv):
    def __init__(self,imgcv,mask=None,points=None, **kwargs):
        super().__init__(**kwargs)
        Img_cv.__init__(self,imgcv,mask=mask,points=points,)
        Window.bind(on_key_down=self.on_key_down_enter)
        self.zoomper=100
        self._enter_state=False
    def on_key_down_enter(self,instance,keyboard,keycode,text,modifires):
        if self._enter_state and keycode==ENTER:
            self.endtarget()

    def unbind(self):
        self._enter_state=False
    def __getitem__(self, key: str):
        Img_cv.__getitem__(self,key)
    def entered(self, target):
        self.endtarget=target
        self.bind_enter_key()
    def _end_target(self):
        self.cancel()
        self.endtarget()
    def bind_enter_key(self):
        self._enter_state=True
    #for cnacle button inw widgets
    def cancel(self):
        self._remove_enter_key()
    def _remove_enter_key(self):
        self.unbind()
    def actived_widget(self)->Img:
        return self.get_current_tab().content

    def show_viwers(self,state=True,colorimgstate=True,**kwargs):
        for var in kwargs:
            setattr(self,var,kwargs[var])
        #putting circles automaticly
        the_dict=self.get_keys()
        #this is for coloring imgcv
        the_dict["colorimgstate"]=colorimgstate
        if state and "points" not in the_dict:
            the_dict["points"]=self.points
            
        title=self.actived_widget()
        if hasattr(title,"define_image"):
            INR(title.define_image,**the_dict)
    def remove_bind(self):
        self._remove_enter_key()
        for title in self.get_tab_list():
            if hasattr(title.content,"canvas"):
                title.content.image_viewer.remove_bind()

def main():
    pass
if __name__=="__main__":
    main()
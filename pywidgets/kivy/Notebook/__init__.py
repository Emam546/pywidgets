from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel,TabbedPanelHeader,TabbedPanel
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.lang import Builder
X_SIZE=dp(40)
class Poped_up_menu(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.titles=[]
        
        self._container=self.ids._container
        self._container.bind(height=self.setter("height"))
    def add(self,text:str,command=None,**kwargs):
        self.titles.append(text)
        def button_press(*args):
            self.dismiss()
            if command!=None:
                command()
        self._container.add_widget( Button(text=text,on_press=button_press,**kwargs))
    def title_in(self,text:str):
        return text in self.titles
    def clear_widgets(self, children=None):
        self.titles=[]
        return self._container.clear_widgets(children)
    def remove_title(self,title):
        for widget in self._container.children:
            if widget.text==title:
                self._container.remove_widget(widget)
class Custom_panel_view(TabbedPanelHeader):
    def delet(self):
        self.parent.tabbed_panel._delet_tab(self)
        
Builder.load_string("""

<Poped_up_menu>:
    size_hint:None,None
    auto_dismiss:True
    size:_container.size
    overlay_color:0,0,0,0
    BoxLayout:
        id:_container
<Custom_panel_view>:
    #:set pady dp(1)
    #:set widthbutton dp(7)
    halign:"left"
    size_hint:1,1
    valign:"middle"
    Button:
        text:"X"
        size_hint:None,None
        font_size: dp(20)
        height:self.parent.height-pady
        halign:"right"
        width:dp(8)
        x:(self.parent.pos[0]+self.parent.width)-self.width-dp(8)
        y:pady/2
        background_color:0.7,0,0,1
        on_release:self.parent.delet()

""")
class CusNotebook(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_default_tab=False
        self._dict_headers={}
        self.add_menu_pope=Poped_up_menu()
        self._tab_strip.size_hint_x=1
    
    def add(self,title,widget):
        if title not in self._dict_headers:
            self._dict_headers[title]=widget
            self._active(title)
    def _return_child(self):
        pass
    def _active(self,title:str):
        titles_text=[_min_tab.text for _min_tab in self.get_tab_list()]
        if not title in titles_text:
            header=Custom_panel_view(text=title,content=self._dict_headers[title])
            self.add_widget(header)
        else:
            header=[tab for tab in self.get_tab_list()if title==tab.text][0]
        if not self.add_menu_pope.title_in(title):
            self.add_menu_pope.add(title,command=lambda:self._active(title))
        self.switch_to(header)
    def _delet_tab(self,tab):
        index=self.get_tab_list().index(tab)
        self.remove_widget(tab)
        if self.get_current_tab()==tab and len(self.get_tab_list())>0:
            self.switch_to(self.get_tab_list()[index])
    def allowed(self,widgets:tuple,state=True,essential:tuple=()):
        active_title=self.get_current_tab().text
        titles_text=[_min_tab.text for _min_tab in self.get_tab_list()]
        for title,title_widgets in self._dict_headers.items():  
            if (title_widgets in widgets) ==state:
                if title not in titles_text:
                    if not self.add_menu_pope.title_in(title):
                        self.add_menu_pope.add(title,command=lambda:self._active(title))
                    if title_widgets in essential:
                        self._active(title)
            else:
                if title in titles_text:
                    tab=self.get_tab_list()[titles_text.index(title)]
                    self.remove_widget(tab)
                self.add_menu_pope.remove_title(title)
        active_state=active_title in [_min_tab.text for _min_tab in self.get_tab_list()]
        if active_state:
            self._active(active_title)
            return
        else:
            self.switch_to(self.get_tab_list()[0])
    
if __name__=="__main__":
    from kivy.app import App
    from kivy.uix.label import Label
    class Programme(App):
        def build(self):
            custom_view=CusNotebook()
            for _title in ["title 1","title 2","tuitle 3","title 4","title 5"]:
                container=BoxLayout()
                container.add_widget(Label(text=_title))
                custom_view.add(_title,container)
            custom_view.allowed((container,),True)
            custom_view._active("title 5")
            return custom_view
    Programme().run()
            
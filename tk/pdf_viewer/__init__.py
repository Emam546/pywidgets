from tkinter import *
import json

from pywidgets.tk.pdf_viewer.pdfviewer import *
from pywidgets.tk.pdf_viewer.title_bar import *

def change_label_properties(parent:Widget,Type,properties):                          
    for label in parent.winfo_children():
        if type(label)==Type:
            for por in properties:
                label[por]=properties[por]
        change_label_properties(label,Type,properties)
FILE_PATH=os.path.dirname(__file__)+"\\"
file = open(FILE_PATH+"style.json")
style = json.loads(file.read())
file.close()    

class full_Pdf_viewer(Tk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.columnconfigure(1,weight=1)
        frame_title=title_bar(self,**style["tiltebar"]["self"])
        change_label_properties(frame_title,Label,style["tiltebar"]["label"])
        frame_title.grid(row=0,column=1,sticky=EW)
def main():
    full_Pdf_viewer().mainloop()

if __name__=="__main__":
    main()
from tkinter import *
def bind_all_childes(parent:Widget,target,key,add="+"):
    parent.bind(key,target,add=add)
    for child in parent.winfo_children():
        child.bind(key,target,add=add)
        bind_all_childes(child,target,key,add)
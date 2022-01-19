from tkinter import *
import os,playsound
from tkinter import filedialog
from gtts import gTTS
from PIL import Image,ImageTk
from threading import Thread
import pyperclip as pc
from langdetect import detect
import os
import sys
from pathlib import Path
sys.path.append(os.path.dirname(__file__))
__FILEPATH=os.path.dirname(__file__)+"\\"
PHOTO = Image.open(__FILEPATH+"icons\\icon.png")
class Frame_text_area(Frame):
        def __init__(self,app,*args, **kwargs):
            super().__init__(app, *args, **kwargs)
            self.textarea=Text(self,bd=0)
            vscroll=Scrollbar(self,command=self.textarea.yview)
            hscroll=Scrollbar(self,orient=HORIZONTAL,command=self.textarea.xview)
            self.textarea.config(xscrollcommand=hscroll.set, yscrollcommand=vscroll.set)
            self.columnconfigure(0,weight=1)
            self.rowconfigure(0,weight=1)
            self.textarea.grid(column=0,row=0,sticky=NSEW)
            vscroll.grid(column=1,row=0,sticky=NSEW)
            hscroll.grid(column=0,row=1,sticky=NSEW)
        def insert(self,text):
            self.delet()
            if  type(text)==str:
                self.textarea.insert(END,text)
            else:
                for  (the_word, color) in text:
                    self.textarea.mark_set("begin", "insert")
                    self.textarea.insert("insert", the_word, the_word)
                    self.textarea.tag_configure(the_word, foreground=color)
        def delet(self):
            self.textarea.delete(1.0,END)
        def get(self):
            return str(self.textarea.get("1.0",END))

        # root – root window.
        # bg – background colour
        # fg – foreground colour
        # bd – border of widget.
        # height – height of the widget.
        # width – width of the widget.
        # font – Font type of the text.
        # cursor – The type of the cursor to be used.
        # insetofftime – The time in milliseconds for which the cursor blink is off.
        # insertontime – the time in milliseconds for which the cusrsor blink is on.
        # padx – horizontal padding.
        # pady – vertical padding.
        # state – defines if the widget will be responsive to mouse or keyboards movements.
        # highligththickness – defines the thickness of the focus highlight.
        # insertionwidth – defines the width of insertion character.
        # relief – type of the border which can be SUNKEN, RAISED, GROOVE and RIDGE.
        # yscrollcommand – to make the widget vertically scrollable.
        # xscrollcommand – to make the widget horizontally scrollable.

class TEXT_reader(Frame_text_area):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        frame_inputs = Frame(self)
        frame_inputs.grid(row=2, column=0, columnspan=2, sticky=NSEW)
        self.photo = PHOTO.resize((20, 20))
        self.photo = ImageTk.PhotoImage(self.photo)
        self.say_button = Button(frame_inputs, text="say", command=self.say)
        self.say_button.grid(row=0, column=0, sticky="e")
        self.number = 0
        Button(frame_inputs, text="save", command=self.save).grid(
            row=0, column=1, sticky="e")
        Button(frame_inputs, image=self.photo, compound=LEFT, bd=0,
               command=self.clip_hexcode).grid(row=0, column=2, sticky="e")

    def clip_hexcode(self):
        hexcolor = self.get()
        pc.copy(hexcolor)

    def say(self,):
        Thread(target=self.__say).start()

    def __say(self):
        self.number += 1
        lang = detect(self.get())
        tts = gTTS(lang=lang, text=self.get())
        filename = str(self.number)+".mp3"
        tts.save(filename)
        self.say_button.config(relief=SUNKEN)
        playsound.playsound(filename)
        self.say_button.config(relief=RAISED)
        os.remove(filename)

    def save(self):
        filename = filedialog.asksaveasfilename(filetypes=(("*.mp3", "MP3"),))
        if filename != "":
            lang = detect(self.get())
            tts = gTTS(lang=lang, text=self.get(),)
            tts.save(filename)
      
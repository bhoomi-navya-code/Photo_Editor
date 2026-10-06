import customtkinter as ctk 
from tkinter import filedialog, Canvas
from settings import *

class ImageImpoet(ctk.CTkFrame):
    def __init__(self, parent,import_func):
        super().__init__(master=parent)
        self.grid(row=0 ,column =0,columnspan =2,sticky ='news')
        self.import_func = import_func


        ctk.CTkButton(self,text='➕ Open Image', command= self.import_dialoge).pack(expand = True)

    def import_dialoge(self):
        path = filedialog.askopenfile().name
        self.import_func(path)

class ImageOutput(Canvas):
    def __init__(self,parent,resize_image):
        super().__init__(master= parent,background= BACKGROUND_COLOER, bd = 0,highlightthickness= 0 , relief= 'ridge')
        self.grid(row=0,column=1, sticky='news', pady =10,padx =10)
        self.bind('<Configure>',resize_image)

class CloseOutPut(ctk.CTkButton):
    def __init__(self, parent,close_func):
        super().__init__(master = parent ,  
                         command= close_func,
                         text = 'X', 
                         text_color= WHITE, 
                         fg_color='transparent',
                         width=40,
                         height= 40,
                         hover_color= CLOSE_RED,
                         corner_radius= 10
                         )
        self.place(relx = 0.99,rely = 0.01 , anchor = 'ne')


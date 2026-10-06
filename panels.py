import customtkinter as ctk
from tkinter import filedialog
from settings import *

class Panel(ctk. CTkFrame):
    def __init__(self,parents):
        super().__init__(master = parents, fg_color=DARK_GREY)
        self.pack(fill = 'x', pady =4, ipady = 8)


class SliderPanel(Panel):
    def __init__(self, parents,text,data_var,min_value,max_value):
        super().__init__(parents = parents)

        #layout
        self.rowconfigure((0,1),weight= 1)
        self.columnconfigure((0,1),weight= 1)

        self.data_var = data_var
        self.data_var.trace_add('write', self.update_text)

        ctk.CTkLabel(self, text= text).grid(column = 0, row =0, sticky = 'w',pady = 5,padx =10)

        self.num_lable =ctk.CTkLabel(self, text = data_var.get())

        self.num_lable.grid(column = 1, row =0,sticky = 'E', pady =5,padx =10)
        

        ctk.CTkSlider(
            self,
            variable=self.data_var,
            from_=min_value,
            to=max_value,
            
            ).grid(column = 0, row =1, columnspan =2 ,sticky = 'E', pady =10,padx =10)

    def update_text(self, *args):
        self.num_lable.configure(text =f'{round(self.data_var.get(),2)}')

class SegmentedPanel(Panel):
    def __init__(self, parents,text,data_var,options):
        super().__init__(parents = parents)

        ctk.CTkLabel(self,text= text).pack()
        ctk.CTkSegmentedButton(self,variable=data_var,values= options).pack(expand = True, fill = 'both',padx = 4, pady =4)

class SwitchPanel(Panel):
    def __init__(self, parent, *args):  
        super().__init__(parents = parent)

        for var, text in args:
            switch = ctk.CTkSwitch(
                self,
                text=text,
                variable=var,
                button_color=COLORS,
                fg_color=SLIDER_BG
            )
            switch.pack(side='left', expand=True, fill='both', padx=5, pady=5)

class DropDownPanel(ctk.CTkOptionMenu):


    def __init__(self, parent, data_var, options):
        super().__init__(
            master=parent,
            variable=data_var,
            values=options,
            fg_color= DARK_GREY,
            button_color= DROPDOWN_MAIN_COLOR,
            button_hover_color= DROPDOWN_HOVER_COLOR,
            dropdown_fg_color= DROPDOWN_MENU_COLOR,
        )
        self.pack(fill='x', pady=4)


class RevertButton(ctk.CTkButton):
    def __init__(self,parents,*args):
        super().__init__(master = parents, text='Revert',command= self.revert)
        self.pack(side = 'bottom', pady = 10)
        self.args = args

    def revert(self):
        for ver,value in self.args:
            ver.set(value)

class FileNamePanel(Panel):
    def __init__(self, parents,name_string, file_string):
        super().__init__(parents)

        #data
        self.name_string = name_string
        self.name_string.trace_add("write",self.update_text)
        self.file_string = file_string


        ctk.CTkEntry(self,textvariable= self.name_string).pack(fill = 'x',padx = 20,pady =5)

        frame = ctk.CTkFrame(self, fg_color= 'transparent')

        jpg_check = ctk.CTkCheckBox(frame, text='jpg',command= lambda: self.click('jpg'),variable= self.file_string,onvalue = 'jpg',offvalue ='png')
        jpg_check.pack(side='left', fill='x', expand=True)

        png_check = ctk.CTkCheckBox(frame, text='png',command= lambda: self.click('png'),variable= self.file_string,onvalue = 'png',offvalue = 'jpg')
        png_check.pack(side='left', fill='x', expand=True)

        frame.pack(expand = True,fill = 'x',padx = 20,pady = 10)


        self.output = ctk.CTkLabel(self,text= '')
        self.output.pack(pady = 10)


    def update_text(self,*args):
       if self.name_string.get():
           text = self.name_string.get().replace(' ','_') +'.'+ self.file_string.get()
           self.output.configure(text = text)


    def click(self, value):
        self.file_string.set(value)
        self.update_text()


class FilePathPanel(Panel):
    def __init__(self, parents, path_string):
        super().__init__(parents)
        self.path_string = path_string

        ctk.CTkButton(self, text='Open Explorer', command= self.open_file_dialog).pack(pady=5)
        ctk.CTkEntry(self,textvariable=self.path_string).pack(expand=True, fill='both', padx=5, pady=5)

    def open_file_dialog(self):
      self.path_string.set(filedialog.askdirectory())

class SaveButton(ctk.CTkButton):
    def __init__(self, parents,export_image,name_string,file_string,path_string):
        super().__init__(master= parents,text= 'save',command= self.save)
        self.pack(side = 'bottom', pady = 10)

        
        self.export_image = export_image
        self.name_string = name_string
        self.file_string = file_string
        self.path_string = path_string
      

     
    def save(self):
        self.export_image(
            self.name_string.get(),
            self.file_string.get(),
            self.path_string.get()
        )
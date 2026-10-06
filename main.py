import customtkinter as ctk
from image_widgets import *
from tkinter import messagebox
from PIL import Image, ImageTk, ImageOps,ImageEnhance,ImageFilter
from settings import *
from meanu import Menu



class Photo_Editor(ctk.CTk):
    def __init__(self):
        # setup
        super().__init__()

        ctk.set_appearance_mode('dark')
        self.geometry('1000x600')
        self.title('Photo Editor')
        self.minsize(800, 600)
        self.init_parameters()


        # layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2, uniform='a')
        self.columnconfigure(1, weight=6, uniform='a')

        
        # canvas data
        self.image_width = 0
        self.image_height =0
        self.canves_width = 0
        self.canves_height =0


        # widgets
        self.image_impoet = ImageImpoet(self, self.image_import)

        # run
        self.mainloop()

    # functions
    def init_parameters(self):
        self.pos_vars ={
            'rotate': ctk.DoubleVar(value =ROTATE_DEFAULT),
            'zoom' : ctk.DoubleVar(value = ZOOM_DEFAULT),
            'flip' : ctk.StringVar(value = FLIP_OPTIONS[0]),
        }

        self.color_var ={
            'brightness' :  ctk.DoubleVar(value = BRIGHTNESS_DEFAULT),
            'grayscale' : ctk.DoubleVar(value = GRAYSCALE_DEFAULT),
            'invert':  ctk.BooleanVar(value = INVERT_DEFAULT),
            'vairance' : ctk.DoubleVar(value = VIBRANCE_DEFAULT),
        }

        self.effect_var = {
            'blur' : ctk.DoubleVar(value = BLUR_DEFAULT),
            'comtrast' :  ctk.IntVar(value = CONTRAST_DEFAULT),
            'effect' : ctk.StringVar(value = EFFCT_OPTIONS[0]),
        }

        combined_var = list(self.pos_vars.values()) + list(self.effect_var.values()) + list(self.color_var.values())


        for var in combined_var:
            var.trace_add('write', self.manipulate_image)

    def manipulate_image(self, *args):
        self.image = self.orginal_img

        #rotate
        if self.pos_vars['rotate'].get() != ROTATE_DEFAULT:
         self.image = self.image.rotate(self.pos_vars['rotate'].get())

        #zoom
        if self.pos_vars['zoom'].get():
         self.image = ImageOps.crop(image= self.image, border= self.pos_vars['zoom'].get())
        
        #flip
        if self.pos_vars['flip'].get() != FLIP_OPTIONS[0]:
            if self.pos_vars['flip'].get() == 'X':
                self.image = ImageOps.mirror(self.image)
            if self.pos_vars['flip'].get() == 'Y':
                self.image = ImageOps.flip(self.image)
            if self.pos_vars['flip'].get() == 'Both':
                self.image = ImageOps.mirror(self.image)
                self.image = ImageOps.flip(self.image)

        #brightness & vibrance
        if self.color_var['brightness'].get() != BRIGHTNESS_DEFAULT:
            brightness_enhancer = ImageEnhance.Brightness(self.image)
            self.image = brightness_enhancer.enhance(self.color_var['brightness'].get())

        if self.color_var['vairance'].get() != VIBRANCE_DEFAULT:
            vibrance_enhancer = ImageEnhance.Color(self.image)
            self.image = vibrance_enhancer.enhance(self.color_var['vairance'].get())

        #coloer
        if self.color_var['grayscale'].get():
         self.image = ImageOps.grayscale(self.image)

        if self.color_var['invert'].get():
            self.image = ImageOps.invert(self.image)
         
        #blur 
        if self.effect_var['blur'].get() != BLUR_DEFAULT:
         self.image = self.image.filter(ImageFilter.GaussianBlur(self.effect_var['blur'].get()))

        #comtrast
        if self.effect_var['comtrast'].get() != CONTRAST_DEFAULT:
         self.image = self.image.filter(ImageFilter.UnsharpMask(self.effect_var['comtrast'].get()))

        #effect
        match self.effect_var['effect'].get():
            case 'Emboss' : self.image =self.image.filter(ImageFilter.EMBOSS)
            case 'Find edges' : self.image =self.image.filter(ImageFilter.FIND_EDGES)
            case 'Contour' : self.image =self.image.filter(ImageFilter.CONTOUR)
            case 'Edge enhance' : self.image =self.image.filter(ImageFilter.EDGE_ENHANCE_MORE)
            

        
        
        self.place_image()

    def image_import(self, path):
        self.orginal_img = Image.open(path)
        self.image = self.orginal_img

        # Get image dimensions
        self.image_ratio = self.image.size[0] / self.image.size[1]
        self.image_tk = ImageTk.PhotoImage(self.image)

        self.image_impoet.grid_forget()
        self.image_output = ImageOutput(self, self.resize_image)

        self.close_button = CloseOutPut(self,self.close_edit)

        self.menu = Menu(self,self.pos_vars,self.color_var,self.effect_var,self.export_image)

    def close_edit(self):
        self.image_output.grid_forget()
        self.close_button.place_forget()
        self.menu.grid_forget()

        self.image_impoet = ImageImpoet(self, self.image_import)

    def resize_image(self, event):

        # ratio
        canvas_ratio = event.width / event.height

        #update canvas

        self.canves_width = event.width
        self.canves_height = event.height

        # resize image with the window
        if canvas_ratio > self.image_ratio:
            # canvas is wider than the image
            self.image_height = event.height
            self.image_width = int(self.image_height * self.image_ratio)

        else:
            # canvas is taller than the image
            self.image_width = event.width
            self.image_height = int(self.image_width / self.image_ratio)

        self.place_image()

        
    def place_image(self):
        # resize image 
        self.image_output.delete('all')
        resized_image = self.image.resize((self.image_width, self.image_height))

        # create PhotoImage
        self.image_tk = ImageTk.PhotoImage(resized_image)

       

        self.image_output.create_image(
            self.canves_width / 2,
            self.canves_height / 2,
            image=self.image_tk
        )

    def export_image(self,name,file,path):
       export_string = f'{path}/{name}.{file}'
       print(export_string)
       messagebox.showinfo('Success', 'Your file was saved!')
       try:
          self.image.save(export_string)
          messagebox.showinfo('Success', f'Your file was saved!\n\n{export_string}')
       except Exception as e:
          messagebox.showerror('Error', f'Could not save the file:\n{e}')
       



if __name__ == "__main__":
    Photo_Editor()

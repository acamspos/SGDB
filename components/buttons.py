import tkinter as tk
from assets.globals import GUI_COLORS
import ttkbootstrap as ttb

class IconButton(tk.Button):
    def __init__(self, master=None, bg = GUI_COLORS['bg'], hover='#c7c7c7', *args, **kwargs):
        super().__init__(master, background=bg, *args,**kwargs)
        
        self.config(background=bg,activebackground=bg, foreground=GUI_COLORS['dark'], cursor='hand2')

        self.bind('<Enter>', lambda e: self.config(background=hover))
        self.bind('<Leave>', lambda e: self.config(background=bg))




class ButtonImage(ttb.Button):
    def __init__(self, master=None, image = None, img_h = None, img_p = None, img_d = None, *args, **kwargs):
        self.state_btn = ttb.StringVar()
        super().__init__(master, image=image, cursor='hand2', *args,**kwargs)
    

        self.__img = image
        self.__img_h = img_h
        self.__img_p = img_p
        self.__img_d = img_d

        self.state_btn.trace_add('write', lambda i,m,v: self.change_state())
        self.state_btn.set(value=self.cget('state'))

    def set_images(self,image = None, img_h = None, img_p = None, img_d = None,):
        self.__img = image
        self.__img_h = img_h
        self.__img_p = img_p
        self.__img_d = img_d
        self.config(image=self.__img)
      

    @staticmethod
    def trace_state(funcion_a):
        def funcion_c(self,*args, **kwargs):
            funcion_a(self,*args, **kwargs)
            if self.state_btn.get() != self.cget('state'):
                self.state_btn.set(self.cget('state'))

        return funcion_c

        
    
    @trace_state
    def configure(self, *args, **kwargs):
        super().configure(*args, **kwargs)
        
    config = configure
    
    def set_img(self, img):
        if self.state_btn.get() != self.cget('state'):
            self.state_btn.set(self.cget('state'))
        else:
            self.config(image=img)
        

    def change_state(self):
        
        if self.state_btn.get() == 'normal':
            self.config(image=self.__img)
            self.bind('<Enter>', lambda e: self.set_img(img=self.__img_h))
            self.bind('<Leave>', lambda e: self.set_img(img=self.__img))

            
            self.bind('<ButtonRelease>', lambda e: self.set_img(img=self.__img_h))

            # self.bind('<FocusIn>',lambda e: self.set_img(img=self.__img_h))
            # self.bind('<FocusOut>', lambda e: self.set_img(img=self.__img))
            
            self.bind('<Button-1>', lambda e: self.set_img(img=self.__img_p))
       
        else:
            self.config(image=self.__img_d)
            self.unbind('<Enter>')
            self.unbind('<Leave>')

            self.unbind('<Button-1>')
            self.unbind('<ButtonRelease>')
            # self.unbind('<FocusIn>')
            # self.unbind('<FocusOut>')




class ButtoLabel(ttb.Label):
    def __init__(self, master=None, image = None, img_h = None, img_p = None, img_d = None, command = None,background='#fff', *args, **kwargs):
        self.state_btn = ttb.StringVar()
        super().__init__(master, image=image, cursor='hand2', background=background, *args,**kwargs)
        self.command = command

        self.__img = image
        self.__img_h = img_h
        self.__img_p = img_p
        self.__img_d = img_d

        self.state_btn.trace_add('write', lambda i,m,v: self.change_state())
        self.state_btn.set(value=self.cget('state'))
      

    @staticmethod
    def trace_state(funcion_a):
        def funcion_c(self,*args, **kwargs):
            funcion_a(self,*args, **kwargs)
            if self.state_btn.get() != self.cget('state'):
                self.state_btn.set(self.cget('state'))

        return funcion_c

        
    
    @trace_state
    def configure(self, *args, **kwargs):
        super().configure(*args, **kwargs)
        
    config = configure
    
    def set_img(self, img):
        if self.state_btn.get() != self.cget('state'):
            self.state_btn.set(self.cget('state'))
        else:
            self.config(image=img)
        
    def press_btn(self):
        self.set_img(img=self.__img_h)
        if self.command:
            self.command()

    def change_state(self):
        
        if self.state_btn.get() == 'normal':
            self.config(image=self.__img)
            self.bind('<Enter>', lambda e: self.set_img(img=self.__img_h))
            self.bind('<Leave>', lambda e: self.set_img(img=self.__img))

            self.bind('<Button-1>', lambda e: self.set_img(img=self.__img_p))
            self.bind('<ButtonRelease>', lambda e: self.press_btn())
        else:
            self.config(image=self.__img_d)
            self.unbind('<Enter>')
            self.unbind('<Leave>')

            self.unbind('<Button-1>')
            self.unbind('<ButtonRelease>')
            

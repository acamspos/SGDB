from ttkbootstrap import Entry, Button
from assets.utils import resize_icon
from assets.globals import IMG_PATH
from PIL import Image
from components.buttons import ButtonImage


class PasswordEntry(Entry):
    def __init__(self, master = None, show='*', *args, **kwargs):
    
        super().__init__(master, show=show, *args, **kwargs)
        self.s_h_password = ButtonImage(self,  compound='center',
                            style='flatw.light.TButton', padding=0,
                            command=lambda: self.show_hide_password())
        self.s_h_password.grid(row=0, column=0, padx=(0,4), sticky='e',pady=2,)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid_propagate(0)

        

        self.s_h_password.bind('<Enter>', lambda e: self.s_h_password.config(image=self.PS_BT_IMG[1]) )
        self.s_h_password.bind('<Leave>', lambda e: self.s_h_password.config(image=self.PS_BT_IMG[0]))

        self.s_h_password.bind('<Button-1>', lambda e: self.s_h_password.config(image=self.PS_BT_IMG[0]))
        self.s_h_password.bind('<ButtonRelease>', lambda e: self.s_h_password.config(image=self.PS_BT_IMG[1])) 
        

        self.bind('<Configure>', lambda e: self.set_image())

    def set_image(self):
        self.create_images()
        self.s_h_password.set_images(image=self.PS_BT_IMG[0], img_h=self.PS_BT_IMG[1], img_p=self.PS_BT_IMG[0])

    def create_images(self):
        self.SHOW_PASS = Image.open(f"{IMG_PATH}/show.png")
        self.SHOW_PASS = resize_icon(self.SHOW_PASS, (self.winfo_height()-8,self.winfo_height()-8))

        self.HIDE_PASS = Image.open(f"{IMG_PATH}/hide.png")
        self.HIDE_PASS = resize_icon(self.HIDE_PASS, (self.winfo_height()-8,self.winfo_height()-8))

        self.SHOW_H_PASS = Image.open(f"{IMG_PATH}/show_h.png")
        self.SHOW_H_PASS = resize_icon(self.SHOW_H_PASS, (self.winfo_height()-8,self.winfo_height()-8))

        self.HIDE_H_PASS = Image.open(f"{IMG_PATH}/hide_h.png")
        self.HIDE_H_PASS = resize_icon(self.HIDE_H_PASS, (self.winfo_height()-8,self.winfo_height()-8))

        self.PS_BT_IMG = [self.SHOW_PASS, self.SHOW_H_PASS]

 
  
    def show_hide_password(self):
    
        if self['show'] == '*':
            self.PS_BT_IMG.clear()
            self.PS_BT_IMG.extend((self.HIDE_PASS, self.HIDE_H_PASS))
            self.config(show='')
            self.s_h_password.config(image=self.PS_BT_IMG[1])
        else:
            self.PS_BT_IMG.clear()
            self.PS_BT_IMG.extend((self.SHOW_PASS, self.SHOW_H_PASS))
            self.config(show='*')
            self.s_h_password.config(image=self.PS_BT_IMG[1])

        self.s_h_password.set_images(image=self.PS_BT_IMG[0], img_h=self.PS_BT_IMG[1], img_p=self.PS_BT_IMG[0])
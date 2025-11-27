import ttkbootstrap as ttb
from PIL import Image, ImageTk
from assets.utils import resize_image
from assets.globals import IMG_PATH

class Homepage(ttb.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid_propagate(0)

        self.logo = Image.open(f'{IMG_PATH}/logo.png')
        self.logo = ImageTk.PhotoImage(self.logo.resize(size=resize_image(45,self.logo.size)))

        self.log = ttb.Label(self,image=self.logo,anchor='center')
        self.log.grid(row=0, column=0, sticky='nsew',padx=2,pady=2)

        self.bind('<Map>', lambda e: self.update())
        self.bind('<Configure>', lambda e:  self.update())

        
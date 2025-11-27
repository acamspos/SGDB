import ttkbootstrap as ttb
from PIL import ImageTk
from assets.utils import resize_image

class DashboardCard(ttb.Frame):
    def __init__(self, master, card_background = None, background = '#fff', title = '', var:ttb.StringVar = None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.img = ImageTk.PhotoImage(card_background.resize(resize_image(60, card_background.size)))

        card_back = ttb.Label(self, image=self.img, borderwidth=0, relief='flat')
        card_back.pack()
        card_back.grid_propagate(0)
        card_back.anchor('w')


        ttb.Label(card_back, text=title, background=background, foreground='white', font=('segoi ui',11,'bold')).grid(row=0, column=0, sticky='w', padx=(95,0))
        ttb.Label(card_back, textvariable=var, background=background, foreground='white', font=('segoi ui',16,'bold')).grid(row=1, column=0, sticky='w', padx=(95,0))


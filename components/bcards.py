
import ttkbootstrap as ttb
from PIL import ImageTk
from assets.utils import resize_image, resize_icon
from assets.globals import IMG_PATH, GUI_COLORS
from customtkinter import CTkFrame

class BCards(ttb.Frame):
    def __init__(self, master = None,  card_background = None, icon = None, background_color = '#fff', title = 'Titulo', value= 'xx', sub_title='Sub titulo',bg_color = '#D9D9D9', size =  (308,188)):
        super().__init__(master)
       
        self.img = resize_icon(card_background, size)
        card_back = ttb.Label(self, image=self.img, background=bg_color, borderwidth=0, relief='flat')
        card_back.pack()
        card_back.grid_propagate(0)
        card_back.anchor('nw')
        card_back.columnconfigure(0,weight=1)
        card_back.rowconfigure(2, weight=1)
        
        self.icon = icon
        
        self.icon = resize_icon(icon,(45,45))


        ttb.Label(card_back, text=' '+title.upper(), background=background_color, foreground='white', font=('segoi ui',12,'bold'), anchor='w').grid(row=0, column=0, sticky='nsew', padx=(70,15), pady=(15,5))
        ttb.Separator(card_back, bootstyle='light').grid(row=1, column=0, sticky='nsew', padx=(20,20), )
        ttb.Label(card_back, background=background_color, image=self.icon).grid(row=0, column=0, sticky='w', padx=(20,0), pady=(15,5))
        
        block = CTkFrame(card_back, fg_color='white',width=100, height=50, corner_radius=5, bg_color=background_color)
        block.grid(row=2, column=0, pady=(10,5), sticky='nesw', padx=20,)
        block.grid_propagate(0)
        block.anchor('center')

        ttb.Label(block, textvariable=value, background='white', foreground=background_color, font=('segoi ui',12,'bold'), anchor='center').grid(row=0, column=0, sticky='nsew', padx=(10,10), pady=(5,5))

        ttb.Label(card_back, text=sub_title, background=background_color, foreground='white', font=('segoi ui',10), anchor='center').grid(row=3, column=0, sticky='nsew', padx=(20,20), pady=(0,15))



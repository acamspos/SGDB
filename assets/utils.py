import ttkbootstrap as ttb
from PIL import ImageTk
from assets.globals import DISPLAY_PAGE, SET_BUTTON
#############################################
############### DISPLAY PAGES ###############
#############################################

def set_homepage(homepage):
    global HOME
    HOME = homepage


        

   

def display_page(page:ttb.Frame=None, butt: ttb.Button= None, callback = None):
    global DISPLAY_PAGE, SET_BUTTON, HOME
    if DISPLAY_PAGE != page and page:    

        if DISPLAY_PAGE:
            DISPLAY_PAGE.grid_forget()
            if SET_BUTTON:
                SET_BUTTON.config(style='aside.TButton', state='normal')
        
        page.grid(row=0, column=0, sticky='nsew')
        DISPLAY_PAGE = page
        if butt:
            SET_BUTTON = butt
            SET_BUTTON.config(style='asideselected.TButton', state='normal')

    elif DISPLAY_PAGE == page or not page:
        if DISPLAY_PAGE:
         DISPLAY_PAGE.grid_forget()
        if SET_BUTTON:
            SET_BUTTON.config(style='aside.TButton', state='normal')
        HOME.grid(row=0, column=0, sticky='nsew')
        DISPLAY_PAGE = HOME
        

        
#     if callback:
#         callback()

#############################################
############### RESIZE IMAGES ###############
#############################################

def resize_icon(icon, icon_size = (35,35)):
    return ImageTk.PhotoImage(icon.resize(size=icon_size))

def resize_image(percentage, size):
    return (int(size[0]*percentage/100), int(size[1]*percentage/100))



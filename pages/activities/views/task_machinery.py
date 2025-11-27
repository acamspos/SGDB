import ttkbootstrap as ttb
from assets.globals import GUI_COLORS, IMG_PATH, GUI_FONT
from assets.utils import resize_image, resize_icon
from PIL import Image, ImageTk
from tkinter import messagebox
import tkinter as tk
from components.buttons import ButtoLabel, ButtonImage
from ttkbootstrap.scrolled import ScrolledFrame
from models.entitys.activity import Activity
from customtkinter import CTkFrame #767171
from assets.db.db_connection import DB
from assets.styles.styles import SGDB_Style
from tkinter import ttk
from datetime import datetime
from models.entitys.machinery import Machinery
FGCOLOR = 'white'
from models.entitys.activity import Activity

class MachineryActivityForm(ttb.Toplevel):
    def __init__(self, master=None, activity = None, callback = None, *args, **kwargs):
        super().__init__(master,background='red')
        SGDB_Style()

        self.minsize(width=650,height=507)
        self.title('Seleccion de Maquinaria')

        self.config(background='#D0CECE')
        self.withdraw()
        self.focus()

        self.transient()
        self.anchor('center')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)  
        self.grab_set()

        self.callback = callback
        self.__ACTIVITY: Activity = activity
      
        self.create_widgets()
        self.place_window_center()
        self.deiconify()

    def create_widgets(self):


        contentFrame = CTkFrame(self, fg_color='white',border_width=1,  border_color='#CFCFCF')
        contentFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=10, pady=10)
        contentFrame.columnconfigure(0, weight=1)
        contentFrame.rowconfigure(1, weight=1)        

        self.__services_icon = resize_icon(Image.open(f"{IMG_PATH}/task_icon.png"))


        titleFrame = CTkFrame(contentFrame, fg_color=GUI_COLORS['primary'])
        titleFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=8, pady=(8,0))
        ttb.Label(titleFrame, image=self.__services_icon, compound='left', text='  Gestor de Equipos', font=(GUI_FONT, 14, 'bold'), foreground='white', background=GUI_COLORS['primary']).grid(row=0,column=0, padx=10, pady=10, sticky='nsew')


        self.mainContent = tk.Frame(contentFrame)
        self.mainContent.config(background=FGCOLOR)
        self.mainContent.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        self.mainContent.columnconfigure(0, weight=1)
        self.mainContent.rowconfigure(0, weight=1)


            ########### Description Section ###########

        
        ttb.Separator(self.mainContent, bootstyle='light').grid(row=2, column=0, sticky='nsew', columnspan=2)


        buttonss_section_frame = tk.Frame(self.mainContent,)
        buttonss_section_frame.configure(background=FGCOLOR)
        buttonss_section_frame.grid(row=3, column=0, pady=(8,8), sticky='nsew', columnspan=2)
        buttonss_section_frame.anchor('e')



        closeimg = Image.open(f"{IMG_PATH}/closen.png")
        self.closeimg = ImageTk.PhotoImage(closeimg.resize(resize_image(20, closeimg.size)))
        closeimgh = Image.open(f"{IMG_PATH}/closeh.png")
        self.closeimgh = ImageTk.PhotoImage(closeimgh.resize(resize_image(20, closeimgh.size)))
        closeimgp = Image.open(f"{IMG_PATH}/closep.png")
        self.closeimgp = ImageTk.PhotoImage(closeimgp.resize(resize_image(20, closeimgp.size)))
        self.closeBTN = ButtonImage(buttonss_section_frame, image=self.closeimg, img_h=self.closeimgh, command=self.destroy, img_p=self.closeimgp, style='flatw.light.TButton', text='CERRAR', compound='center',padding=0)
        self.closeBTN.grid(row=0, column=0, sticky='nsew', pady=2, padx=(0,4))


        self.create_othersWidgets()
        self.__set_tasks()

    def create_othersWidgets(self):
            
        task_list_frame = tk.Frame(master=self.mainContent, width=800, height=600)
        task_list_frame.configure(background='#fff')
        task_list_frame.grid(row=0, column=0, padx=10, pady=(5,10), sticky='nsew')
        task_list_frame.columnconfigure(0, weight=1)
        task_list_frame.rowconfigure(0, weight=1)

       

        self.scroll_frame_content = ScrolledFrame(task_list_frame, style='white.TFrame', bootstyle='round dark')
        self.scroll_frame_content.grid(row=0, column=0, sticky='nsew', padx=4)
        self.scroll_frame_content.columnconfigure(0, weight=1)
        self.scroll_frame_content.columnconfigure(1, weight=3)
        

        ttb.Label(self.scroll_frame_content, background='#fff', justify='center', anchor='center', text=f'Codigo', font=('arial',11,'bold'),).grid(row=0, column=0, sticky='nsew')

        ttb.Label(self.scroll_frame_content, background='#fff', justify='center', text=f'Descripcion', font=('arial',11,'bold'),).grid(row=0, column=1, sticky='nsew',padx=(0,18))

        ttb.Separator(self.scroll_frame_content, bootstyle='dark').grid(row=1, column=0, columnspan=2, pady=(10,10), padx=(0,18),sticky='nsew')
 

        self.variables = []
        self.checkboxes = []

    def change_task_state(self,index, idT):
            DB.update_machinery_state(idT=idT,state=self.variables[index].get())
      
    

    def process_activity(self):
        ask = messagebox.askquestion(title='Confirmacion', message='Desea Procesar esta Actividad?', parent=self)
        if ask == 'yes':
            self.callback()
            self.destroy()

    def __set_tasks(self):
        tasks = self.__ACTIVITY.get_machinery()
        if tasks:
            for index, task in enumerate(tasks):
                newTask = Machinery(**task)
                #ttb.Label(self.cont, text=f'Task #{index+1}', font=('arial',11,'bold'), foreground=GUI_COLORS['danger'], padding=5, ).grid(row=index*2+2, column=0, sticky='nsew',padx=5,pady=5)
                ttb.Label(self.scroll_frame_content, background='#fff', anchor='center', text=f'{newTask.code}', font=('arial',11),).grid(row=index*2+2, column=0, sticky='nsew')
                ttb.Label(self.scroll_frame_content, background='#fff', justify='center', text=f'{newTask.description}', font=('arial',11),).grid(row=index*2+2, column=1, sticky='nsew')

                ttb.Separator(self.scroll_frame_content, bootstyle='light').grid(row=index*2+3, column=0, columnspan=4, padx=(0,18),pady=(10,15),sticky='nsew')

        

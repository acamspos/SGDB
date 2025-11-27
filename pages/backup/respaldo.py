import ttkbootstrap as ttb
from tkinter import ttk
from assets.globals import GUI_COLORS, GUI_FONT, IMG_PATH

from models.entitys.product import  Product
from pages.Extras.subtable import SubWindowsSelection
from pages.providers.providers import ProviderModule

from tkinter import messagebox
from tkinter import filedialog
from assets.styles.styles import SGDB_Style
from customtkinter import CTkFrame
from PIL import Image, ImageTk
from components.buttons import ButtonImage
from assets.utils import resize_icon, resize_image
import tkinter as tk
from assets.db.db_connection import DB
import os


class BackUp(ttb.Frame):
    def __init__(self, master=None, window_type = 'create', title = '', product = None):
        super().__init__(master, )
        self.valid_character = '012356789.-'
        self.focus()

        # SYSTEM_WIDTH = self.winfo_screenwidth()
        # SYSTEM_HEIGHT = self.winfo_screenheight()

        # pwidth = (SYSTEM_WIDTH-1158)//2
        # pheight = (SYSTEM_HEIGHT-794)//2

        # self.geometry(str(1158)+"x"+str(794)+"+"+str(pwidth)+"+"+str(pheight-60))
        # self.minsize(width=1158,height=794)

        
        self.window_title = title
        self.window_type = window_type

        ######### MODAL WINDOW CONFIG #########
   
 
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
       
        self.__createWidgets()
     

    


    
    def __createWidgets(self):
        


        FGCOLOR = 'white'

        contentFrame = CTkFrame(self, fg_color='white',border_width=1,  border_color='#CFCFCF')
        contentFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=10, pady=10)
        contentFrame.columnconfigure(0, weight=1)


        self.micon = resize_icon(Image.open(f"{IMG_PATH}/db.png"))


        subtitle = CTkFrame(contentFrame, fg_color=GUI_COLORS['primary'],)
        subtitle.grid(row = 0, column = 0, sticky = 'nsew', padx=8, pady=(8,0))
        
        ttb.Label(subtitle, image=self.micon, background=GUI_COLORS['primary'], ).grid(row=0, column=0, rowspan=2, sticky='nsew', padx=(8), pady=8)

        ttb.Label(subtitle, text='Respaldos de Informacion', background=GUI_COLORS['primary'], font=(GUI_FONT,13,'bold'), foreground='#fff', anchor='sw').grid(row=0, column=1, sticky='nsew', padx=(4,8), pady=(8,0))

        ttb.Label(subtitle, text='Inicio / Respaldos', background=GUI_COLORS['primary'], font=(GUI_FONT,9), foreground='#fff', anchor='nw').grid(row=1, column=1, sticky='nsew', padx=(4,8), pady=(0,8))



        ttb.Frame(contentFrame, bootstyle='dark').grid(row=1, column=0, sticky='nsew', padx=20, pady=5)

    
            ########### Description Section ###########

        mainInforFrame = tk.Frame(contentFrame)
        mainInforFrame.config(background=FGCOLOR)
        mainInforFrame.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)
 


        code_label = ttb.Label(mainInforFrame, 
                                      anchor='w', 
                                      text='Opciones de Respaldos de Información:', 
                                      bootstyle='info', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        code_label.grid(row=0, column=0, padx=(8,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew', columnspan=2)
       
        exportimg = Image.open(f"{IMG_PATH}/export.png")
        self.exportimg = ImageTk.PhotoImage(exportimg.resize(resize_image(16, exportimg.size)))
        exportimgh = Image.open(f"{IMG_PATH}/exporth.png")
        self.exportimgh = ImageTk.PhotoImage(exportimgh.resize(resize_image(16, exportimgh.size)))
        exportimgp = Image.open(f"{IMG_PATH}/exportp.png")
        self.exportimgp = ImageTk.PhotoImage(exportimgp.resize(resize_image(16, exportimgp.size)))

        self.exportBTN = ButtonImage(mainInforFrame, image=self.exportimg, img_h=self.exportimgh, img_p=self.exportimgp, style='flatw.light.TButton', text='     EXPORTAR DB', compound='center',padding=0, command=self.back_up)
        self.exportBTN.grid(row=2, column=0,  sticky='nse', pady=10, padx=(5,10),)


        importimg = Image.open(f"{IMG_PATH}/import.png")
        self.importimg = ImageTk.PhotoImage(importimg.resize(resize_image(16, importimg.size)))
        importimgh = Image.open(f"{IMG_PATH}/importh.png")
        self.importimgh = ImageTk.PhotoImage(importimgh.resize(resize_image(16, importimgh.size)))
        importimgp = Image.open(f"{IMG_PATH}/importp.png")
        self.importimgp = ImageTk.PhotoImage(importimgp.resize(resize_image(16, importimgp.size)))

        self.importBTN = ButtonImage(mainInforFrame, image=self.importimg, img_h=self.importimgh, img_p=self.importimgp, style='flatw.light.TButton', text='     IMPORTAR DB', compound='center',padding=0, command=self.__filefindwindow)


        self.importBTN.grid(row=2, column=1,  sticky='nsw', pady=10, padx=(10,5),)

        self.logo = Image.open(f'{IMG_PATH}/logo.png')
        self.logo = ImageTk.PhotoImage(self.logo.resize(size=resize_image(45,self.logo.size)))

        ttb.Label(self,image=self.logo,anchor='center').grid(row=1, column=0, sticky='nsew',padx=2,pady=2)


    def restore_db(self,backup_file):
        if backup_file and backup_file != 'Seleccionar Archivo':
            DB.restore_db(backup_file)
            messagebox.showinfo('Exito', 'Restauracion exitosa.')
            self.__window.destroy()
        else:
            messagebox.showinfo('Respaldo', 'No se ha seleccionado una copia de seguridad.', parent=self) 


    def set_path(self):
        filedialog.askdirectory(title='Selecionar Ruta para Almacenar el Respaldo', parent=self)

    
    def find_file(self):
        path = filedialog.askopenfilename(title='Selecionar Respaldo', parent= self.__window)
        if path:
            self.file.set(path)


    def __filefindwindow(self, ):
        self.__window = ttb.Toplevel(title=f'Seleccionar Archivo')
        self.__window.resizable(0,0)
        self.__window.focus()
        self.__window.grab_set()
       

        contentFrame = CTkFrame( self.__window, fg_color='white',border_width=1,  border_color='#CFCFCF')
        contentFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=10, pady=10)
        contentFrame.columnconfigure(0, weight=1)


        self.micon2 = resize_icon(Image.open(f"{IMG_PATH}/db.png"))


        subtitle = CTkFrame(contentFrame, fg_color=GUI_COLORS['primary'],)
        subtitle.grid(row = 0, column = 0, sticky = 'nsew', padx=8, pady=(8,0))
        
        ttb.Label(subtitle, image=self.micon2, background=GUI_COLORS['primary'], ).grid(row=0, column=0, rowspan=2, sticky='nsew', padx=(8), pady=8)

        ttb.Label(subtitle, text='Restauración', background=GUI_COLORS['primary'], font=(GUI_FONT,13,'bold'), foreground='#fff', anchor='sw').grid(row=0, column=1, sticky='nsew', padx=(4,8), pady=(8,0))

        ttb.Label(subtitle, text='Inicio / Respaldos / Seleccion de Archivo', background=GUI_COLORS['primary'], font=(GUI_FONT,9), foreground='#fff', anchor='nw').grid(row=1, column=1, sticky='nsew', padx=(4,8), pady=(0,8))



        ttb.Frame(contentFrame, bootstyle='dark').grid(row=1, column=0, sticky='nsew', padx=20, pady=5)

        self.file = ttb.StringVar(value='Seleccionar Archivo')
            ########### Description Section ###########

        mainInforFrame = tk.Frame(contentFrame)
        mainInforFrame.config(background='white')
        mainInforFrame.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)

        self.file_value = ttb.Label(mainInforFrame, textvariable=self.file, width=80, font=(GUI_FONT,11,), background='white')
        self.file_value.grid(row=0, column=0, padx=5, pady=5)
        self.file_value.bind('<Button-1>', lambda e: self.find_file())

        ttb.Separator(contentFrame, bootstyle='light').grid(row=3, column=0, pady=4, padx=10, sticky='nsew')


        buttonss_section_frame = tk.Frame(contentFrame,)
        buttonss_section_frame.configure(background='white')
        buttonss_section_frame.grid(row=4, column=0, pady=(2,6), padx=10, sticky='nsew', )
        buttonss_section_frame.anchor('e')
        buttonss_section_frame.columnconfigure(0, weight=1)


        self.pageNum = ttb.Label(buttonss_section_frame, text='Pagina: 1/3',font=(GUI_FONT,12,'bold'), background='#fff', bootstyle='dark')
        self.pageNum.grid(row=0, column=0, sticky='nsew', padx=(6,0))



        closeimg = Image.open(f"{IMG_PATH}/closen.png")
        self.closeimg = ImageTk.PhotoImage(closeimg.resize(resize_image(20, closeimg.size)))
        closeimgh = Image.open(f"{IMG_PATH}/closeh.png")
        self.closeimgh = ImageTk.PhotoImage(closeimgh.resize(resize_image(20, closeimgh.size)))
        closeimgp = Image.open(f"{IMG_PATH}/closep.png")
        self.closeimgp = ImageTk.PhotoImage(closeimgp.resize(resize_image(20, closeimgp.size)))
        self.closeBTN = ButtonImage(buttonss_section_frame, image=self.closeimg, img_h=self.closeimgh, command= self.__window.destroy, img_p=self.closeimgp, style='flatw.light.TButton', text='CERRAR', compound='center',padding=0)
        self.closeBTN.grid(row=0, column=1, sticky='nsew', pady=2, padx=(0,4))

        
      

        creatbtnimg = Image.open(f"{IMG_PATH}/registrar.png")
        self.creatbtnimg = ImageTk.PhotoImage(creatbtnimg.resize(resize_image(20, creatbtnimg.size)))
        creatbtnimgh = Image.open(f"{IMG_PATH}/registrarh.png")
        self.creatbtnimgh = ImageTk.PhotoImage(creatbtnimgh.resize(resize_image(20, creatbtnimgh.size)))
        creatbtnimgp = Image.open(f"{IMG_PATH}/registrarp.png")
        self.creatbtnimgp = ImageTk.PhotoImage(creatbtnimgp.resize(resize_image(20, creatbtnimgp.size)))

        self.createBTN = ButtonImage(buttonss_section_frame,   image=self.creatbtnimg, img_h=self.creatbtnimgh, img_p=self.creatbtnimgp, 
                                     style='flatw.light.TButton', text='RESTAURAR', compound='center',padding=0, command=lambda:self.restore_db(self.file.get()))
        self.createBTN.grid(row=0, column=3, sticky='nsew', pady=2, padx=(0,4))

    def back_up(self):
        path = filedialog.askdirectory(title='Selecionar Ubicacion', parent= self)
        if path:
            import subprocess
            import datetime

            # Configuración de la base de datos
            db_user = 'root'
            db_password = os.getenv('DB_PASSWORD')
            db_name = os.getenv('DB_NAME')

            # Configuración del archivo de respaldo

            timestamp = datetime.datetime.now().strftime("%d-%m-%Y")
            backup_file = f'"{path}//backup_{timestamp}.sql"'

            # Comando para generar el respaldo
            command = f'mysqldump -u {db_user} -p{db_password} {db_name} > {backup_file}'
            try:
                # Ejecutar el comando
                subprocess.run(command, shell=True, check=True)
                messagebox.showinfo('Copia de Seguridad',f'Copia de seguridad exitosa. Archivo guardado en: {backup_file}', parent=self)
            except subprocess.CalledProcessError as e:
                messagebox.showwarning('Error',f'Error al realizar la copia de seguridad: {e}', parent=self)

# app = ttb.Window(themename='new')
# SGDB_Style()
# ProductForm(app)

# app.mainloop()
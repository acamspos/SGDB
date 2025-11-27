import ttkbootstrap as ttb
from assets.globals import GUI_FONT, IMG_PATH
from assets.styles.styles import SGDB_Style
from customtkinter import CTkFrame
from PIL import Image, ImageTk
from components.buttons import ButtonImage
from assets.utils import resize_icon, resize_image
import tkinter as tk
from tkinter import messagebox
from assets.globals import validateFloat
from assets.db.db_connection import DB


class ExchangeForm(ttb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.withdraw()
        self.focus()

 

        ######### MODAL WINDOW CONFIG #########

        self.title('Tasa de Cambio del Sistema')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.transient()
        self.grab_set()
        self.config(background="#D9D9D9")
       

        ######### VARIABLES #########

        self.__exchange = ttb.StringVar(value=DB.select_currency())
       
        self.__createWidgets()

        self.place_window_center()
        self.iconbitmap('SIGAG.ico')
        self.deiconify()
    
    def __createWidgets(self):
        

        FGCOLOR = 'white'

        contentFrame = CTkFrame(self, fg_color='white',border_width=1,  border_color='#CFCFCF')
        contentFrame.grid(row = 1, column = 0, sticky = 'nsew', padx=10, pady=10)
        contentFrame.columnconfigure(0, weight=1)


        self.__products_icon = resize_icon(Image.open(f"{IMG_PATH}/exchange_icon.png"))


        titleFrame = CTkFrame(contentFrame, fg_color='#212946')
        titleFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=8, pady=(8,0))
        titleFrame.columnconfigure(0, weight=1)
        
        ttb.Label(titleFrame, image=self.__products_icon, compound='left', text=f' Tasa de Cambio', font=(GUI_FONT, 14, 'bold'), foreground='white', background='#212946').grid(row=0,column=0, padx=10, pady=10, sticky='nsew')

       
        product_info_content = tk.Frame(contentFrame)
        product_info_content.config(background=FGCOLOR)
        product_info_content.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        product_info_content.columnconfigure(1, weight=1)
        product_info_content.columnconfigure(2, weight=1)


            ########### name Section ###########

        mainInforFrame = tk.Frame(product_info_content)
        mainInforFrame.config(background=FGCOLOR)
        mainInforFrame.grid(row=0, column=0, sticky='nsew', columnspan=2)
        mainInforFrame.columnconfigure(1, weight=1)

        exchange_label = ttb.Label(mainInforFrame, 
                                      anchor='center', 
                                      text='USD $', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        exchange_label.grid(row=0, column=0, padx=(4,0), pady=(2,12), ipadx=8, ipady=8, sticky='nsew')

        self.exchangeEntry = ttb.Entry(mainInforFrame, textvariable=self.__exchange, font=('arial',11), justify='center', width=20,validate="key",validatecommand=(self.register(validateFloat), "%P"))
        self.exchangeEntry.grid(row=0, column=1, sticky='nsew',pady=(2,12),padx=(0,4), ipady=4, columnspan=1,)




        ttb.Separator(product_info_content, bootstyle='light').grid(row=9, column=0, sticky='nsew', columnspan=2)


        buttonss_section_frame = tk.Frame(product_info_content,)
        buttonss_section_frame.configure(background=FGCOLOR)
        buttonss_section_frame.grid(row=10, column=0, pady=(8,0), sticky='nsew', columnspan=2)
        buttonss_section_frame.anchor('e')



        closeimg = Image.open(f"{IMG_PATH}/closen.png")
        self.closeimg = ImageTk.PhotoImage(closeimg.resize(resize_image(20, closeimg.size)))
        closeimgh = Image.open(f"{IMG_PATH}/closeh.png")
        self.closeimgh = ImageTk.PhotoImage(closeimgh.resize(resize_image(20, closeimgh.size)))
        closeimgp = Image.open(f"{IMG_PATH}/closep.png")
        self.closeimgp = ImageTk.PhotoImage(closeimgp.resize(resize_image(20, closeimgp.size)))
        self.closeBTN = ButtonImage(buttonss_section_frame, image=self.closeimg, img_h=self.closeimgh, command=self.destroy, img_p=self.closeimgp, style='flatw.light.TButton', text='Cerrar', compound='center',padding=0)
        self.closeBTN.grid(row=0, column=0, sticky='nsew', pady=2, padx=(0,4))

     
                




        creatbtnimg = Image.open(f"{IMG_PATH}/registrar.png")
        self.creatbtnimg = ImageTk.PhotoImage(creatbtnimg.resize(resize_image(20, creatbtnimg.size)))
        creatbtnimgh = Image.open(f"{IMG_PATH}/registrarh.png")
        self.creatbtnimgh = ImageTk.PhotoImage(creatbtnimgh.resize(resize_image(20, creatbtnimgh.size)))
        creatbtnimgp = Image.open(f"{IMG_PATH}/registrarp.png")
        self.creatbtnimgp = ImageTk.PhotoImage(creatbtnimgp.resize(resize_image(20, creatbtnimgp.size)))

        self.createBTN = ButtonImage(buttonss_section_frame,  command=self.update_value_currency, image=self.creatbtnimg, img_h=self.creatbtnimgh, img_p=self.creatbtnimgp, style='flatw.light.TButton', text='Actualizar', compound='center',padding=0)
        self.createBTN.grid(row=0, column=1, sticky='nsew', pady=2, padx=(0,4))

            #self.__set_form_state()





    def update_value_currency(self):
        if self.__exchange.get() and float(self.__exchange.get()) > 0:
            ask = messagebox.askquestion('Actualizar','Actualizar la tasa de cambio del Sistema?', parent=self)
            if ask == 'yes':
                DB.update_exchange_value(self.__exchange.get())
                messagebox.showinfo('Aviso','Tasa de Cambio Actualizada.', parent=self)
              
        else:
            messagebox.showwarning('Aviso','La tasa de cambio debe ser mayor a 0.', parent=self)


 

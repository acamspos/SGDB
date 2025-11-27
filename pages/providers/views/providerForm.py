import ttkbootstrap as ttb
from assets.globals import GUI_FONT, IMG_PATH
from models.entitys.product import  Product
from customtkinter import CTkFrame
from PIL import Image, ImageTk
from components.buttons import ButtonImage
from assets.utils import resize_icon, resize_image
import tkinter as tk
from models.entitys.provider import Provider
from tkinter import messagebox


def on_validate(P, lenght = 20):
    # Verificar que la longitud del contenido no supere cierto límite
    return len(P) <= lenght  


class ProviderForm(ttb.Toplevel):
    def __init__(self, master=None, window_type = 'create', provider=None, title = ''):
        super().__init__(master, toolwindow=True)
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

        self.title(title)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.transient()
        self.grab_set()
        self.config(background="#D9D9D9")
       


        self.__PROVIDER: Provider = provider

        ######### VARIABLES #########
     
        self.__rif = ttb.StringVar()
        self.__name = ttb.StringVar()
        self.__address = ttb.StringVar()
        self.__email = ttb.StringVar()
        self.__phone = ttb.StringVar()
        self.__website = ttb.StringVar()

        self.__createWidgets()

        if self.__PROVIDER:
            self.__set_provider_info()
    
    def __createWidgets(self):
        

        FGCOLOR = 'white'

        contentFrame = CTkFrame(self, fg_color='white',border_width=1,  border_color='#CFCFCF')
        contentFrame.grid(row = 1, column = 0, sticky = 'nsew', padx=10, pady=10)
        contentFrame.columnconfigure(0, weight=1)


        self.__products_icon = resize_icon(Image.open(f"{IMG_PATH}/product.png"))


        titleFrame = CTkFrame(contentFrame, fg_color='#212946')
        titleFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=8, pady=(8,0))
        titleFrame.columnconfigure(0, weight=1)
        
        ttb.Label(titleFrame, image=self.__products_icon, compound='left', text=f' {self.window_title}', font=(GUI_FONT, 14, 'bold'), foreground='white', background='#212946').grid(row=0,column=0, padx=10, pady=10, sticky='nsew')

       
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

        rif_label = ttb.Label(mainInforFrame, 
                                      anchor='w', 
                                      text='RIF', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        rif_label.grid(row=0, column=0, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        self.rifEntry = ttb.Entry(mainInforFrame, textvariable=self.__rif, width=30,
                                  validate="key", validatecommand=(self.register(lambda e: on_validate(e,lenght=20)), '%P'))
        self.rifEntry.grid(row=1, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=4, columnspan=1)


        name_label = ttb.Label(mainInforFrame, 
                                      anchor='w', 
                                      text='Nombre', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        name_label.grid(row=0, column=1, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        self.nameEntry = ttb.Entry(mainInforFrame, width=80, textvariable=self.__name,
                                   validate="key", validatecommand=(self.register(lambda e: on_validate(e,lenght=100)), '%P'))
        self.nameEntry.grid(row=1, column=1, sticky='nsew',pady=(2,0),padx=4, ipady=4, columnspan=1)


        address_label = ttb.Label(mainInforFrame, 
                                      anchor='w', 
                                      text='Direccion', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        address_label.grid(row=2, column=0, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        self.addressEntry = ttb.Entry(mainInforFrame, textvariable=self.__address, width=50,
                                      validate="key", validatecommand=(self.register(lambda e: on_validate(e,lenght=300)), '%P'))
        self.addressEntry.grid(row=3, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=4, columnspan=2)


        moreInfoFrame = tk.Frame(product_info_content)
        moreInfoFrame.config(background=FGCOLOR)
        moreInfoFrame.grid(row=2, column=0, sticky='nsew', columnspan=2, pady=(0,12))
        moreInfoFrame.columnconfigure(0, weight=1)
        moreInfoFrame.columnconfigure(1, weight=1)
    

        email_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Correo', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=('arial',11,'bold'))
        email_label.grid(row=0, column=0, padx=(0,4), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        self.emailEntry = ttb.Entry(moreInfoFrame, textvariable=self.__email,
                                    validate="key", validatecommand=(self.register(lambda e: on_validate(e,lenght=100)), '%P'))
        self.emailEntry.grid(row=1, column=0, sticky='nsew',padx=(4,0), ipady=4,)


        phoneNumber_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Telefono', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=('arial',11,'bold'))
        phoneNumber_label.grid(row=0, column=1, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        self.phoneNumberEntry = ttb.Entry(moreInfoFrame, textvariable=self.__phone,
                                          validate="key", validatecommand=(self.register(lambda e: on_validate(e,lenght=12)), '%P'))
        self.phoneNumberEntry.grid(row=1, column=1, sticky='nsew',padx=(4,0), ipady=4)


        website_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Pagina Web', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=('arial',11,'bold'))
        website_label.grid(row=2, column=0, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew',)
        self.websiteEntry = ttb.Entry(moreInfoFrame, textvariable=self.__website,
                                      validate="key", validatecommand=(self.register(lambda e: on_validate(e,lenght=100)), '%P'))
        self.websiteEntry.grid(row=3, column=0, sticky='nsew',padx=(0,0), ipady=4,columnspan=2)


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
        self.closeBTN = ButtonImage(buttonss_section_frame, image=self.closeimg, img_h=self.closeimgh, command=self.destroy, img_p=self.closeimgp, style='flatw.light.TButton', text='CERRAR', compound='center',padding=0)
        self.closeBTN.grid(row=0, column=0, sticky='nsew', pady=2, padx=(0,4))

     
                


        if self.window_type == 'create':


            creatbtnimg = Image.open(f"{IMG_PATH}/registrar.png")
            self.creatbtnimg = ImageTk.PhotoImage(creatbtnimg.resize(resize_image(20, creatbtnimg.size)))
            creatbtnimgh = Image.open(f"{IMG_PATH}/registrarh.png")
            self.creatbtnimgh = ImageTk.PhotoImage(creatbtnimgh.resize(resize_image(20, creatbtnimgh.size)))
            creatbtnimgp = Image.open(f"{IMG_PATH}/registrarp.png")
            self.creatbtnimgp = ImageTk.PhotoImage(creatbtnimgp.resize(resize_image(20, creatbtnimgp.size)))

            self.createBTN = ButtonImage(buttonss_section_frame,  command=self.createProviderRecord, image=self.creatbtnimg, img_h=self.creatbtnimgh, img_p=self.creatbtnimgp, style='flatw.light.TButton', text='REGISTRAR', compound='center',padding=0)
            self.createBTN.grid(row=0, column=1, sticky='nsew', pady=2, padx=(0,4))

            #self.__set_form_state()

        elif self.window_type == 'edit':
            editbtn = Image.open(f"{IMG_PATH}/editn.png")
            self.editbtn = ImageTk.PhotoImage(editbtn.resize(resize_image(20, editbtn.size)))
            editbtnh = Image.open(f"{IMG_PATH}/edith.png")
            self.editbtnh = ImageTk.PhotoImage(editbtnh.resize(resize_image(20, editbtnh.size)))
            editbtnp = Image.open(f"{IMG_PATH}/editp.png")
            self.editbtnp = ImageTk.PhotoImage(editbtnp.resize(resize_image(20, editbtnp.size)))

            self.editBTN = ButtonImage(buttonss_section_frame, command=self.editProviderRecord, image=self.editbtn, img_h=self.editbtnh, img_p=self.editbtnp, style='flatw.light.TButton', text='MODIFICAR', compound='center',padding=0)
            self.editBTN.grid(row=0, column=2, sticky='nsew', pady=2, padx=(0,4))

            #self.__set_form_state()
            self.rifEntry.configure(state='readonly')
        
        self.FORM_FIELDS = [self.rifEntry, self.nameEntry, self.addressEntry, self.emailEntry, self.phoneNumberEntry, self.websiteEntry]
        self.FORM_DATA = [self.__rif, self.__name, self.__address, self.__email, self.__phone,self.__website]
        


    def __clean_fields(self):
        self.__PROVIDER = None

        for field in self.FORM_DATA:
            field.set('')


    def providerInstance(self):
        return Provider(
                        rif = self.__rif.get(),
                        name = self.__name.get(),
                        address = self.__address.get(),
                        email = self.__email.get(),
                        phone = self.__phone.get(),
                        website = self.__website.get())
    

    def __check_fields(self):
        return not '' in [value.get() for value in self.FORM_DATA]
    

    def createProviderRecord(self):
        if self.__check_fields():
            if Provider.validate_rif(self.__rif.get()):
                ask = messagebox.askquestion('Crear','Crear Registro de Proveedor?', parent=self)
                if ask == 'yes':
                    newProvider = self.providerInstance()
                    newProvider.create()
                    messagebox.showinfo('Aviso','Registro creado satisfactoriamente.', parent=self)
                    self.destroy()
            else:
                messagebox.showwarning('Aviso','El RIF ingresado ya se encuentra asociado a un registro.', parent=self)
        else:
            messagebox.showwarning('Aviso','Existen algunos campos invalidos.', parent=self)


    def editProviderRecord(self):
        if self.__check_fields():
            ask = messagebox.askquestion('Modificar','Modificar el Registro de Proveedor?', parent=self)
            if ask == 'yes':
                newProvider = self.providerInstance()
                newProvider.update()
                messagebox.showinfo('Aviso','Registro modificado satisfactoriamente.', parent=self)
                self.destroy()
        else:
            messagebox.showwarning('Aviso','Existen algunos campos invalidos.', parent=self)
        
    
    def __set_provider_info(self):

        self.__rif.set(self.__PROVIDER.rif)
        self.__name.set(self.__PROVIDER.name)
        self.__address.set(self.__PROVIDER.address)
        self.__email.set(self.__PROVIDER.email)
        self.__phone.set(self.__PROVIDER.phone)
        self.__website.set(self.__PROVIDER.website)

        



# app = ttb.Window(themename='new')
# SGDB_Style()
# ProductForm(window_type='edit', title='Modificar Producto')
# app.mainloop()
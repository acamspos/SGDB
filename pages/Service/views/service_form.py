import ttkbootstrap as ttb
from assets.globals import GUI_COLORS, GUI_FONT, IMG_PATH
from models.entitys.service import Service
# from models.entitys.service import  service
from assets.db.db_connection import DB
from datetime import datetime
from tkinter import messagebox

from customtkinter import CTkFrame
from PIL import Image, ImageTk
from components.buttons import ButtonImage
from assets.utils import resize_icon, resize_image
import tkinter as tk
from assets.globals import on_validate_length, on_combobox_change, validateFloat, limitar_longitud




class ServiceForm(ttb.Toplevel):
    def __init__(self, master=None, window_type = 'create', title = '', service = None):
        super().__init__(master)
        self.withdraw()
        self.window_title = title
        self.window_type = window_type

        ######### MODAL WINDOW CONFIG #########

        self.__SERVICE: Service = service

        ######### VARIABLES #########
        self.__code = ttb.StringVar()
        self.__name = ttb.StringVar()
        self.__description = ttb.StringVar()
        self.__description.trace_add('write', self.set_description_data)
        self.__warranty = ttb.StringVar()
        
        self.__currency = ttb.IntVar(value=2)
        self.__currencyName = ttb.StringVar()
        self.__currencyValue = ttb.DoubleVar()

        self.__price1 = ttb.StringVar()
        self.__price1.trace_add('write', lambda v,i,m: self.__calculate_exchange(price_var=self.__price1, exchange=self.__exchangePrice1, ))
       
        self.__price2 = ttb.StringVar()
        self.__price2.trace_add('write', lambda v,i,m: self.__calculate_exchange(price_var=self.__price2, exchange=self.__exchangePrice2,))

        self.__price3 = ttb.StringVar()
        self.__price3.trace_add('write', lambda v,i,m: self.__calculate_exchange(price_var=self.__price3, exchange=self.__exchangePrice3,))
  

        self.__exchangePrice1 = ttb.StringVar(value=0.00)
        self.__exchangePrice2 = ttb.StringVar(value=0.00)
        self.__exchangePrice3 = ttb.StringVar(value=0.00)

        self.__createWidgets()
        

        if self.__SERVICE:
            self.__set_service_data()
        
        self.title('Servicios')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.transient()
        self.grab_set()
        self.focus()
        self.config(background="#D9D9D9")
        self.place_window_center()
        self.iconbitmap('SIGAG.ico')
        self.deiconify()

    def set_description_data(self, var, index, mode):
        self.descriptionEntry.config(state='normal')
        self.descriptionEntry.delete('1.0', ttb.END)
        self.descriptionEntry.insert('1.0', self.__description.get())
        if self.window_type == 'view':
            self.descriptionEntry.config(state='disabled')

    def __calculate_exchange(self, price_var = None, exchange = None,):
        currency_value = float(self.__currencyValue.get())
        if currency_value == 0:
            currency_value = 1

        if price_var.get():
            exchange.set(float(price_var.get())*currency_value)
        else:
            exchange.set(0.00)
        
        
    
    def __createWidgets(self):

        FGCOLOR = 'white'

        contentFrame = CTkFrame(self, fg_color='white',border_width=1,  border_color='#CFCFCF')
        contentFrame.grid(row = 1, column = 0, sticky = 'nsew', padx=10, pady=10)

        self.__services_icon = resize_icon(Image.open(f"{IMG_PATH}/service.png"))


        titleFrame = CTkFrame(contentFrame, fg_color='#00B050')
        titleFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=8, pady=(8,0))
        ttb.Label(titleFrame, image=self.__services_icon, compound='left', text=f' {self.window_title}', font=(GUI_FONT, 14, 'bold'), foreground='white', background='#00B050').grid(row=0,column=0, padx=10, pady=10, sticky='nsew')


        service_info_content = tk.Frame(contentFrame)
        service_info_content.config(background=FGCOLOR)
        service_info_content.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)


            ########### Description Section ###########

        mainInforFrame = tk.Frame(service_info_content)
        mainInforFrame.config(background=FGCOLOR)
        mainInforFrame.grid(row=0, column=0, sticky='nsew')
        mainInforFrame.columnconfigure(1, weight=1)

        code_label = ttb.Label(mainInforFrame, 
                                      anchor='w', 
                                      text='Codigo', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        code_label.grid(row=0, column=0, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.codeEntry = ttb.Entry(mainInforFrame, width=30, textvariable=self.__code,validate='key',validatecommand=(self.register(lambda e: on_validate_length(e,lenght=20)), '%P'))
        self.codeEntry.grid(row=1, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=4, )


        name_label = ttb.Label(mainInforFrame, 
                                      anchor='w', 
                                      text='Nombre', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        name_label.grid(row=0, column=1, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.nameEntry = ttb.Entry(mainInforFrame,   width=50, textvariable=self.__name, validate='key',validatecommand=(self.register(lambda e: on_validate_length(e,lenght=200)), '%P'))
        self.nameEntry.grid(row=1, column=1, sticky='nsew',pady=(2,0),padx=4, ipady=4, )


        moreInfoFrame = tk.Frame(service_info_content)
        moreInfoFrame.config(background=FGCOLOR)
        moreInfoFrame.grid(row=1, column=0, sticky='nsew')
        moreInfoFrame.columnconfigure(0, weight=1)

        description_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Descripcion', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=('arial',11,'bold'))
        description_label.grid(row=0, column=0, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        self.descriptionEntry = ttb.Text(moreInfoFrame,height=3, cursor='xterm')
        self.descriptionEntry.grid(row=1, column=0, sticky='nsew',padx=(4,0), ipady=4,)
        self.descriptionEntry.bind('<KeyPress>', lambda e: limitar_longitud(self.descriptionEntry, 400))
        self.descriptionEntry.bind('<KeyRelease>', lambda e: limitar_longitud(self.descriptionEntry, 400))
        self.descriptionEntry.bind('Control-v', lambda e: limitar_longitud(self.descriptionEntry, 400))
        




        warranty_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Garantia', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=('arial',11,'bold'))
        warranty_label.grid(row=2, column=0, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
  

        self.warrantyEntry = ttb.Entry(moreInfoFrame, textvariable=self.__warranty,)
        self.warrantyEntry.grid(row=3, column=0, sticky='nsew',padx=(4,0), ipady=4,)
        
     
     
        
     

        sectionDelimiter = CTkFrame(service_info_content,fg_color=GUI_COLORS['dark'])
        sectionDelimiter.grid(row=2, column=0, pady=(10,4), ipadx=8, ipady=4, sticky='nsew')
        sectionDelimiter.anchor('center')

        ttb.Label(sectionDelimiter, text='Sección de Costos y Precios', font=(GUI_FONT,11,'bold'), bootstyle='dark inverse').grid(row=0, column=0, padx=4, pady=2)

        pricingSectionFrame = tk.Frame(service_info_content)
        pricingSectionFrame.config(background=FGCOLOR)
        pricingSectionFrame.grid(row=3, column=0, sticky='nsew')
        
        cost_section_frame = tk.Frame(pricingSectionFrame,)
        cost_section_frame.config(background=FGCOLOR)
        cost_section_frame.grid(row=3, column=0,  pady=(4,0), ipadx=8, ipady=8, sticky='nsew')

        


        CURRENCY =  DB.getCurrencyList()
        CURRENCY_DICT = {row[1]:row[0] for row in CURRENCY}
        CURRENCY_DICT_VALUE = {row[0]:row[2] for row in CURRENCY}
        del CURRENCY


            ###### Currency Section ######
        currency_label = ttb.Label(cost_section_frame, 
                                   anchor='w', 
                                   text='Moneda', 
                                   background=FGCOLOR,
                                   font=('arial',11,'bold'))
        currency_label.grid(row=0, column=0, padx=(4,0), pady=(2,0), ipadx=8, sticky='nsew')


        def set_exchange_rate(var,index,mode):
            value = CURRENCY_DICT_VALUE[self.__currency.get()]
            if value == 1:
                value = 0.0
            self.__currencyValue.set(value)
          
     
        
        self.currencyCombobox = ttb.Combobox(cost_section_frame, values=list(CURRENCY_DICT.keys()), state='readonly', style='selectionOnly.TCombobox', textvariable=self.__currencyName)
        self.currencyCombobox.grid(row=1, column=0, padx=(4,10), pady=(2,0), sticky='nsew')
        self.currencyCombobox.bind("<<ComboboxSelected>>", lambda e: on_combobox_change(e,self.__currency, CURRENCY_DICT, self.currencyCombobox))
        self.currencyCombobox.current(1)
        self.__currency.trace_add('write', set_exchange_rate)
        self.__currency.set(2)

        exchangeFrame = CTkFrame(cost_section_frame, fg_color=GUI_COLORS['info'], corner_radius=3)
        exchangeFrame.grid(row=2, column=0, padx=(4,10), pady=(8,0), sticky='nsew')
        exchangeFrame.anchor('center')


        ttb.Label(exchangeFrame, text='Tasa de Canbio', font=(GUI_FONT,11,'bold'), background=GUI_COLORS['info'], foreground='white').grid(row=0, column=0, padx=5,pady=5, sticky='nsew')
        ttb.Label(exchangeFrame, text='35.89', anchor='center', width=8, font=(GUI_FONT,11), background=GUI_COLORS['info'], foreground='white').grid(row=1, column=0, padx=5,pady=5, sticky='nsew')


       

        pricing_section_frame = tk.Frame(pricingSectionFrame,)
        pricing_section_frame.config(background=FGCOLOR)
        pricing_section_frame.grid(row=3, column=1, columnspan=1, pady=(4,0), ipadx=8, ipady=8, sticky='nsew')
        pricing_section_frame.columnconfigure(0, weight=1)

        price_section_title = ttb.Label(pricing_section_frame, 
                                text='Precios de Venta', 
                                bootstyle='dark', 
                                background=FGCOLOR,
                                anchor='w',
                                font=('arial',11,'bold'))
        price_section_title.grid(row=0, column=0, padx=4, pady=0, ipadx=2, ipady=2, sticky='nsew')

       
        ttb.Separator(pricing_section_frame, bootstyle='dark').grid(row=1, column=0, padx=4, pady=4, sticky='nsew',columnspan=2)

        priceFrame = tk.Frame(pricing_section_frame)
        priceFrame.config(background=FGCOLOR)
        priceFrame.grid(row=2, column=0, padx=4, sticky='nsew', columnspan=2)        
        priceFrame.columnconfigure(5, weight=1)

        ttb.Label(priceFrame, 
            anchor='w', 
            text='Precio 1 (PVP)', 
            background='white',
            font=('arial',11,'bold')
        ).grid(row=0, column=0, padx=0, pady=(0,4), ipadx=8, sticky='nsew')

        self.priceEntry1 = ttb.Entry(priceFrame,  width=14, validate="key",validatecommand=(self.register(validateFloat), "%P"), textvariable=self.__price1)
        self.priceEntry1.grid(row=0,column=1, sticky='nsew',pady=(0,4), ipady=4,)

        
        
        fp_currency = CTkFrame(priceFrame, fg_color='#767171', corner_radius=2)
        fp_currency.grid(row=0,column=2, padx=(4,0), sticky='nsew',pady=(0,3))
        fp_currency.anchor('center')

        ttb.Label(fp_currency,
                width=6, 
                textvariable=self.__currencyName,
                anchor='center',
                foreground='white',
                font=('arial',11,'bold'),
                background='#767171'
        ).grid(padx=2, pady=2)



        exchangeFirstPrice = CTkFrame(priceFrame, fg_color=GUI_COLORS['light'], corner_radius=2)
        exchangeFirstPrice.grid(row=0,column=3, padx=(4,0), sticky='nsew',pady=(0,3))
        exchangeFirstPrice.anchor('e')

        self.exchange_fp = ttb.Label(exchangeFirstPrice, 
                                width=16, 
                                anchor='e', 
                                textvariable=self.__exchangePrice1,
                                bootstyle='light inverse', 
                                font=('arial',11,'bold'))
        self.exchange_fp.grid(row=1, column=3, padx=(2,2), ipadx=8, sticky='nsew',pady=(2,2))

        exchange_fp_c = ttb.Label(exchangeFirstPrice,
                                  width=6, 
                                  text='Bs.',
                                  anchor='center', 
                                  bootstyle='light inverse',)
        exchange_fp_c.grid(row=1,column=4, sticky='nsew',pady=(2,2), padx=(0,2))

        ####################################

        ttb.Label(priceFrame, 
                                     anchor='w', 
                                     text='Precio 2 (PVP)', 
                                     background='white',
                                     font=('arial',11,'bold')
        ).grid(row=1, column=0, padx=(0,0), pady=(0,4), ipadx=8, sticky='nsew')


        self.priceEntry2 = ttb.Entry(priceFrame,  width=12, validate="key",validatecommand=(self.register(validateFloat), "%P"),textvariable=self.__price2, )
        self.priceEntry2.grid(row=1,column=1, sticky='nsew',pady=(0,4), ipady=4,)

        
        fp_currency = CTkFrame(priceFrame, fg_color='#767171', corner_radius=2)
        fp_currency.grid(row=1,column=2, padx=(4,0), sticky='nsew',pady=(0,3))
        fp_currency.anchor('center')

        ttb.Label(fp_currency,
                width=6, 
                textvariable=self.__currencyName,
                anchor='center',
                foreground='white',
                font=('arial',11,'bold'),
                background='#767171'
        ).grid(padx=2, pady=2)



        exchangeFirstPrice = CTkFrame(priceFrame, fg_color=GUI_COLORS['light'], corner_radius=2)
        exchangeFirstPrice.grid(row=1,column=3, padx=(4,0), sticky='nsew',pady=(0,3))
        exchangeFirstPrice.anchor('e')

        self.exchange_fp = ttb.Label(exchangeFirstPrice, 
                                width=16, 
                                anchor='e', 
                                textvariable=self.__exchangePrice2,
                                bootstyle='light inverse', 
                                font=('arial',11,'bold'))
        self.exchange_fp.grid(row=0, column=0, padx=(2,2), ipadx=8, sticky='nsew',pady=(2,2))

        exchange_fp_c = ttb.Label(exchangeFirstPrice,
                                  width=6, 
                                  text='Bs.',
                                  anchor='center', 
                                  bootstyle='light inverse',)
        exchange_fp_c.grid(row=0,column=1, sticky='nsew',pady=(2,2), padx=(0,2))




        ####################################

        ttb.Label(priceFrame, 
                                     anchor='w', 
                                     text='Precio 3 (PVP)', 
                                     background='white',
                                     font=('arial',11,'bold')
        ).grid(row=2, column=0, padx=(0,0), pady=(0,4), ipadx=8, sticky='nsew')


        self.priceEntry3 = ttb.Entry(priceFrame, width=14, textvariable=self.__price3,validate="key",validatecommand=(self.register(validateFloat), "%P"),)
        self.priceEntry3.grid(row=2,column=1, sticky='nsew',pady=(0,4), ipady=4,)

        
        fp_currency = CTkFrame(priceFrame, fg_color='#767171', corner_radius=2)
        fp_currency.grid(row=2,column=2, padx=(4,0), sticky='nsew',pady=(0,3))
        fp_currency.anchor('center')

        ttb.Label(fp_currency,
                width=6, 
                textvariable=self.__currencyName,
                anchor='center',
                foreground='white',
                font=('arial',11,'bold'),
                background='#767171'
        ).grid(padx=2, pady=2)



        exchangeFirstPrice = CTkFrame(priceFrame, fg_color=GUI_COLORS['light'], corner_radius=2)
        exchangeFirstPrice.grid(row=2,column=3, padx=(4,0), sticky='nsew',pady=(0,3))
        exchangeFirstPrice.anchor('e')

        self.exchange_fp = ttb.Label(exchangeFirstPrice, 
                                width=16, 
                                anchor='e', 
                                textvariable=self.__exchangePrice3,
                                bootstyle='light inverse', 
                                font=('arial',11,'bold'))
        self.exchange_fp.grid(row=0, column=0, padx=(2,2), ipadx=8, sticky='nsew',pady=(2,2))

        exchange_fp_c = ttb.Label(exchangeFirstPrice,
                                  width=6, 
                                  text='Bs.',
                                  anchor='center', 
                                  bootstyle='light inverse',)
        exchange_fp_c.grid(row=0,column=1, sticky='nsew',pady=(2,2), padx=(0,2))



        

        ttb.Separator(service_info_content, bootstyle='light').grid(row=9, column=0, sticky='nsew', columnspan=2)


        buttonss_section_frame = tk.Frame(service_info_content,)
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

        
        self.__FORM_ENTRIES =[self.codeEntry, self.descriptionEntry, self.nameEntry, self.warrantyEntry,  self.priceEntry1, self.priceEntry2, self.priceEntry3, ]
     
        self.__DATA_FORM = [self.__code, self.__description, self.__name, self.__warranty, self.__currency]
        self.__DATA_NUMBERS_FORM = [self.__price1, self.__price2, self.__price3,]

        if self.window_type == 'create':


            creatbtnimg = Image.open(f"{IMG_PATH}/registrar.png")
            self.creatbtnimg = ImageTk.PhotoImage(creatbtnimg.resize(resize_image(20, creatbtnimg.size)))
            creatbtnimgh = Image.open(f"{IMG_PATH}/registrarh.png")
            self.creatbtnimgh = ImageTk.PhotoImage(creatbtnimgh.resize(resize_image(20, creatbtnimgh.size)))
            creatbtnimgp = Image.open(f"{IMG_PATH}/registrarp.png")
            self.creatbtnimgp = ImageTk.PhotoImage(creatbtnimgp.resize(resize_image(20, creatbtnimgp.size)))

            self.createBTN = ButtonImage(buttonss_section_frame,  command=self.createServiceRecord, image=self.creatbtnimg, img_h=self.creatbtnimgh, img_p=self.creatbtnimgp, style='flatw.light.TButton', text='REGISTRAR', compound='center',padding=0)
            self.createBTN.grid(row=0, column=1, sticky='nsew', pady=2, padx=(0,4))

            self.__set_form_state()

        elif self.window_type == 'edit':
            editbtn = Image.open(f"{IMG_PATH}/editn.png")
            self.editbtn = ImageTk.PhotoImage(editbtn.resize(resize_image(20, editbtn.size)))
            editbtnh = Image.open(f"{IMG_PATH}/edith.png")
            self.editbtnh = ImageTk.PhotoImage(editbtnh.resize(resize_image(20, editbtnh.size)))
            editbtnp = Image.open(f"{IMG_PATH}/editp.png")
            self.editbtnp = ImageTk.PhotoImage(editbtnp.resize(resize_image(20, editbtnp.size)))

            self.editBTN = ButtonImage(buttonss_section_frame, command=self.editServiceRecord, image=self.editbtn, img_h=self.editbtnh, img_p=self.editbtnp, style='flatw.light.TButton', text='MODIFICAR', compound='center',padding=0)
            self.editBTN.grid(row=0, column=2, sticky='nsew', pady=2, padx=(0,4))

            self.__set_form_state()
            self.codeEntry.configure(state='readonly')
     
        
        else:
            self.__set_form_state('readonly')
            self.currencyCombobox.config(state='disabled')


        
        
        
    def __set_form_state(self, state = 'normal'):

        for field in self.__FORM_ENTRIES:
            if field.winfo_class() != 'TEntry' and state=='readonly':
                newstate='disabled'
                field.config(state=newstate,cursor='xterm')
                del newstate
                self.descriptionEntry.config(background='#D3D6DF', highlightcolor=GUI_COLORS['primary'], borderwidth=1)
            else:
                field.config(state=state,cursor='xterm')
          



    def serviceInstance(self):
        return Service(
            code=self.__code.get(),
            name=self.__name.get(),
            description=self.descriptionEntry.get('1.0', ttb.END).replace('\n',''),
            warranty=self.__warranty.get(),
            currency=self.__currency.get(),
            price1=self.__price1.get(),
            price2=self.__price2.get(),
            price3=self.__price3.get(),
        )
    

    def __check_fields(self):
        self.__description.set(self.descriptionEntry.get('1.0', ttb.END))
        return not '' in [value.get() for value in self.__DATA_FORM]
    

    def __field_num_entrys(self):
        for field in self.__DATA_NUMBERS_FORM:
            if not field.get():
                field.set(0)
    

    def createServiceRecord(self):

        if self.__check_fields():
            if not Service.validate_code(self.__code.get()):
                ask = messagebox.askquestion('Crear','Crear nuevo Servicio?', parent=self)
                if ask == 'yes':
                    self.__field_num_entrys()
                    newService = self.serviceInstance()
                    newService.create()
                    messagebox.showinfo('Aviso','Service creado satisfactoriamente.', parent=self)
                    self.destroy()
            else:
                messagebox.showwarning('Aviso','El codigo ingresado ya se encuentra asociado a un registro.', parent=self)
        else:
            messagebox.showwarning('Aviso','Existen algunos campos invalidos o faltan por rellenar.', parent=self)


    def editServiceRecord(self):
        if self.__check_fields():
            ask = messagebox.askquestion('Modificar','Modificar el Registro del Servicio?', parent=self)
            if ask == 'yes':
                self.__field_num_entrys()
                newService = self.serviceInstance()
                newService.update()
                messagebox.showinfo('Aviso','Registro modificado satisfactoriamente.', parent=self)
                self.destroy()
        else:
            messagebox.showwarning('Aviso','Existen algunos campos invalidos o faltan por rellenar.', parent=self)


    def __set_service_data(self):
        self.__code.set(self.__SERVICE.code)
        self.__description.set(self.__SERVICE.description)
        self.__name.set(self.__SERVICE.name)
        self.__warranty.set(self.__SERVICE.warranty)
        self.__currency.set(self.__SERVICE.currency)
        self.__currencyName.set(self.__SERVICE.get_currency())
        self.__price1.set(self.__SERVICE.price1)
        self.__price2.set(self.__SERVICE.price2)
        self.__price3.set(self.__SERVICE.price3)
 

# app = ttb.Window(themename='new')

# SGDB_Style()

# ServiceForm(window_type='edit', title='Modificar serviceo')

# app.mainloop()
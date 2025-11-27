import ttkbootstrap as ttb
from tkinter import ttk
from assets.globals import GUI_COLORS, GUI_FONT, IMG_PATH
from models.entitys.product import  Product
from pages.Extras.subtable import SubWindowsSelection
from pages.providers.providers import ProviderModule
from tkinter import messagebox
from customtkinter import CTkFrame
from PIL import Image, ImageTk
from components.buttons import ButtonImage
from assets.utils import resize_icon, resize_image
import tkinter as tk
from assets.db.db_connection import DB
from assets.globals import on_validate_length, validate_number, on_combobox_change, validateFloat





class ProductForm(ttb.Toplevel):
    def __init__(self, master=None, window_type = 'create', title = '', product = None, code = None):
        super().__init__(master)
        self.withdraw()

        self.window_title = title
        self.window_type = window_type

        self.prices_focus = ttb.BooleanVar(value=True)
        self.__PRODUCT: Product = product

        ######### VARIABLES #########
        self.__code = ttb.StringVar()
        self.__description = ttb.StringVar()
        self.__departmentId = ttb.IntVar()
        self.__departmentName = ttb.StringVar()
        self.__brandId = ttb.IntVar()
        self.__brandName = ttb.StringVar()
        self.__providerId = ttb.IntVar()
        self.__providerName = ttb.StringVar()
        self.__currency = ttb.IntVar(value=2)

        self.__currencyName = ttb.StringVar()
        self.__currencyValue = ttb.DoubleVar()
        self.__measurement = ttb.IntVar(value=1)
        self.__measurementName = ttb.StringVar()
        
        self.__cost = ttb.StringVar()
        
        self.__cost.trace_add('write', self.__cost_calculation)
        
        self.__cost_exchange = ttb.StringVar()
        self.__totalCost = ttb.StringVar()
        self.__totalExchangeCost = ttb.StringVar()
        self.__directCost = ttb.StringVar()
        self.__directCost.trace_add('write', self.__cost_calculation)

        self.__indirectCost = ttb.StringVar()
        self.__indirectCost.trace_add('write', self.__cost_calculation)
       
        self.__tax = ttb.IntVar(value=1)
        self.__taxName = ttb.StringVar()
        self.__taxValue = ttb.StringVar()

        self.__price1 = ttb.StringVar()
        self.__price1.trace_add('write', lambda v,i,m: self.calculate_exchange_price(price_var=self.__price1, exchange_var=self.__price1_exchange))
        self.__price1.trace_add('write', lambda v,i,m: self.__calculate_percentage(price_var=self.__price1, profit_var=self.__profit1, ))
 
        self.__price2 = ttb.StringVar()
        self.__price2.trace_add('write', lambda v,i,m: self.calculate_exchange_price(price_var=self.__price2, exchange_var=self.__price2_exchange))
        self.__price2.trace_add('write', lambda v,i,m: self.__calculate_percentage(price_var=self.__price2, profit_var=self.__profit2,))

        self.__price3 = ttb.StringVar()
        self.__price3.trace_add('write', lambda v,i,m: self.calculate_exchange_price(price_var=self.__price3, exchange_var=self.__price3_exchange))
        self.__price3.trace_add('write', lambda v,i,m: self.__calculate_percentage(price_var=self.__price3, profit_var=self.__profit3,))


        self.__price1_exchange = ttb.StringVar(value='0.00')
        self.__price2_exchange = ttb.StringVar(value='0.00')
        self.__price3_exchange = ttb.StringVar(value='0.00')

        self.__profit1 = ttb.StringVar()
        self.__profit1.trace_add('write', lambda v,i,m: self.__calculate_percentage(price_var=self.__price1, profit_var=self.__profit1, ))

        self.__profit2 = ttb.StringVar()
        self.__profit2.trace_add('write', lambda v,i,m: self.__calculate_percentage(price_var=self.__price2, profit_var=self.__profit2, ))

        self.__profit3 = ttb.StringVar()
        self.__profit3.trace_add('write', lambda v,i,m: self.__calculate_percentage(price_var=self.__price3, profit_var=self.__profit3, ))


        self.__mainStock = ttb.StringVar(value=0)
        self.__stock1 = ttb.StringVar(value=0)
        self.__stock2 = ttb.StringVar(value=0)
        self.__stock3 = ttb.StringVar(value=0)
        self.__stock4 = ttb.StringVar(value=0)

        self.bind('<F2>', self.__enabled_percentage_entry)
        self.__createWidgets()


        if self.__PRODUCT:
            self.__set_product_data()

        if code and self.window_type=='quickCreate':
            self.__code.set(code)
        
        self.place_window_center()
        self.focus()
        self.title(title)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.transient()
        self.grab_set()
        self.resizable(0,0)
        self.config(background="#D9D9D9")
        
        self.iconbitmap('SIGAG.ico')
        self.deiconify()
       
        
    
    def __cost_calculation(self, v=None, i=None, m=None):
        currency_value = float(self.__currencyValue.get())
        if currency_value == 0:
            currency_value = 1


        cost = self.__cost.get()
        if not cost:
            cost = 0
        else:
            cost = float(cost)
        self.__cost_exchange.set(cost*currency_value)


        tax = self.__taxValue.get()
        if not tax:
            tax = 0
        tax = cost * float(tax)/100


        percentage_directCost = self.__directCost.get()
        if not percentage_directCost:
            percentage_directCost = 0
        directCost = cost * float(percentage_directCost)/100

        percentage_indirectCost = self.__indirectCost.get()
        if not percentage_indirectCost:
            percentage_indirectCost = 0
        indirectCost = cost * float(percentage_indirectCost)/100

        totalCost = cost+tax+directCost+indirectCost
        self.__totalCost.set(totalCost)
        self.__totalExchangeCost.set(totalCost*currency_value)

        self.__calculate_percentage(price_var=self.__price1, profit_var=self.__profit1, )
        self.__calculate_percentage(price_var=self.__price2, profit_var=self.__profit2, )
        self.__calculate_percentage(price_var=self.__price3, profit_var=self.__profit3, )


    def __enabled_percentage_entry(self, e):
        if self.window_type == 'create':
            states = ['normal','readonly']
            if self.prices_focus.get() == True:
                states.reverse()
                self.prices_focus.set(False)
            else:
                self.prices_focus.set(True)
            self.priceEntry1.config(state=states[0])
            self.priceEntry2.config(state=states[0])
            self.priceEntry3.config(state=states[0])
            self.profitEntry1.config(state=states[1])
            self.profitEntry2.config(state=states[1])
            self.profitEntry3.config(state=states[1])


    def calculate_exchange_price(self, price_var = None, exchange_var = None):
        currency_value = float(self.__currencyValue.get())
        if currency_value == 0:
            currency_value = 1
        exchange_var.set(float(price_var.get())*currency_value)
        

    def __calculate_percentage(self, price_var = None, profit_var = None):
        cost = self.__totalCost.get()
        if self.prices_focus.get():
            price = price_var.get()
            if price and cost and float(cost) > 0 :
                profit_var.set(round((float(price) - float(cost)) / float(cost) * 100, 2))
            else:
                profit_var.set(0)
        else:
            profit = profit_var.get()
            if profit and cost and float(cost) > 0 :
                price_var.set( round(float(cost) * (1+float(profit)/100), 2) )
            else:
                price_var.set(0)

        

    
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

        if self.window_type == 'view':
            addroundimg = Image.open(f"{IMG_PATH}/addround.png")
            self.addroundimg = ImageTk.PhotoImage(addroundimg.resize(resize_image(12, addroundimg.size)))
            addroundimgh = Image.open(f"{IMG_PATH}/addroundh.png")
            self.addroundimgh = ImageTk.PhotoImage(addroundimgh.resize(resize_image(12, addroundimgh.size)))
            addroundimgp = Image.open(f"{IMG_PATH}/addroundp.png")
            self.addroundimgp = ImageTk.PhotoImage(addroundimgp.resize(resize_image(12, addroundimgp.size)))

            self.addBTN = ButtonImage(titleFrame,  command=lambda:self.__stock_manipulation('Agregar',self.__PRODUCT.return_existence), image=self.addroundimg, img_h=self.addroundimgh, img_p=self.addroundimgp, style='212946.TButton', padding=0)
            self.addBTN.grid(row=0, column=1, sticky='nsew', pady=2, padx=(0,4))


            removeroundimg = Image.open(f"{IMG_PATH}/removeround.png")
            self.removeroundimg = ImageTk.PhotoImage(removeroundimg.resize(resize_image(12, removeroundimg.size)))
            removeroundimgh = Image.open(f"{IMG_PATH}/removeroundh.png")
            self.removeroundimgh = ImageTk.PhotoImage(removeroundimgh.resize(resize_image(12, removeroundimgh.size)))
            removeroundimgp = Image.open(f"{IMG_PATH}/removeroundp.png")
            self.removeroundimgp = ImageTk.PhotoImage(removeroundimgp.resize(resize_image(12, removeroundimgp.size)))

            self.reduceBTN = ButtonImage(titleFrame,  command=lambda:self.__stock_manipulation('Reducir',self.__PRODUCT.reduce_existence), image=self.removeroundimg, img_h=self.removeroundimgh, img_p=self.removeroundimgp, style='212946.TButton', padding=0)
            self.reduceBTN.grid(row=0, column=2, sticky='nsew', pady=2, padx=(0,4))

        product_info_content = tk.Frame(contentFrame)
        product_info_content.config(background=FGCOLOR)
        product_info_content.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        product_info_content.columnconfigure(1, weight=1)
        product_info_content.columnconfigure(2, weight=1)


            ########### Description Section ###########

        mainInforFrame = tk.Frame(product_info_content)
        mainInforFrame.config(background=FGCOLOR)
        mainInforFrame.grid(row=0, column=0, sticky='nsew', columnspan=2)
        mainInforFrame.columnconfigure(1, weight=1)

        code_label = ttb.Label(mainInforFrame, 
                                      anchor='w', 
                                      text='Codigo', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        code_label.grid(row=0, column=0, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.codeEntry = ttb.Entry(mainInforFrame, textvariable=self.__code, width=30,validate='key',validatecommand=(self.register(lambda e: on_validate_length(e,lenght=20)), '%P'))
        self.codeEntry.grid(row=1, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=4, columnspan=1)


        description_label = ttb.Label(mainInforFrame, 
                                      anchor='w', 
                                      text='Descripcion', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        description_label.grid(row=0, column=1, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.descriptionEntry = ttb.Entry(mainInforFrame,  width=50,  textvariable=self.__description, validate='key',validatecommand=(self.register(lambda e: on_validate_length(e,lenght=200)), '%P'))
        self.descriptionEntry.grid(row=1, column=1, sticky='nsew',pady=(2,0),padx=4, ipady=4, columnspan=1)


        moreInfoFrame = tk.Frame(product_info_content)
        moreInfoFrame.config(background=FGCOLOR)
        moreInfoFrame.grid(row=2, column=0, sticky='nsew', columnspan=2)
        moreInfoFrame.columnconfigure(0, weight=1)
        moreInfoFrame.columnconfigure(1, weight=1)
        moreInfoFrame.columnconfigure(2, weight=1)

        department_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Departamento', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=('arial',11,'bold'))
        department_label.grid(row=0, column=0, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        
        department_frame = tk.Frame(moreInfoFrame)
        department_frame.config(background=FGCOLOR)
        department_frame.grid(row=1, column=0, sticky='nsew' ,pady=(4,0),padx=(4,10),)
        department_frame.columnconfigure(1,weight=1)

        department_frame.anchor('w')
        
        d_number_frame = CTkFrame(department_frame,  width=30,  height=30,  fg_color=GUI_COLORS['light'] )
        d_number_frame.grid(row=0, column=0, sticky='nsw')
        d_number_frame.anchor('center')
        d_number_frame.grid_propagate(0)

        ttb.Label(d_number_frame, textvariable=self.__departmentId, bootstyle='light inverse').grid(row=0, column=0, sticky='nsew')

        self.departmentEntry = ttb.Entry(department_frame, textvariable=self.__departmentName,state='readonly')
        self.departmentEntry.grid(row=0, column=1, sticky='nsew',padx=(4,0), ipady=4,)
        
        if not self.window_type == 'view':
            self.department_search_btn = ttb.Button(department_frame,  text='...', bootstyle='dark', command=lambda:self.__open_selection_modal('Departamentos','department',self.__set_dept_info))
            self.department_search_btn.grid(row=0, column=2, padx=(2), sticky='nsew', pady=1)




        brand_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Marca', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=('arial',11,'bold'))
        brand_label.grid(row=0, column=1, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        
        brand_frame = tk.Frame(moreInfoFrame)
        brand_frame.config(background=FGCOLOR)
        brand_frame.grid(row=1, column=1, sticky='nsew' ,pady=(4,0),padx=(4,10),)
        brand_frame.columnconfigure(1,weight=1)

        brand_frame.anchor('w')
    
        d_number_frame = CTkFrame(brand_frame,  width=30,  height=30,  fg_color=GUI_COLORS['light'],  )
        d_number_frame.grid(row=0, column=0, sticky='nsw')
        d_number_frame.anchor('center')
        d_number_frame.grid_propagate(0)

        ttb.Label(d_number_frame, textvariable=self.__brandId, bootstyle='light inverse').grid(row=0, column=0, sticky='nsew')


        self.brandEntry = ttb.Entry(brand_frame, textvariable=self.__brandName,state='readonly')
        self.brandEntry.grid(row=0, column=1, sticky='nsew',padx=(4,0), ipady=4,)
        
        if not self.window_type == 'view':
            self.brand_search_btn = ttb.Button(brand_frame, text='...', bootstyle='dark', command=lambda: self.__open_selection_modal('Marcas','brand',self.__set_brand_info))
            self.brand_search_btn.grid(row=0, column=2, padx=2, sticky='nsew', pady=1)


        provider_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Proveedor', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=('arial',11,'bold'))
        provider_label.grid(row=0, column=2, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        
        provider_frame = tk.Frame(moreInfoFrame)
        provider_frame.config(background=FGCOLOR)
        provider_frame.grid(row=1, column=2, sticky='nsew' ,pady=(4,0),padx=(4,4),)
        provider_frame.columnconfigure(1,weight=1)

        provider_frame.anchor('w')
        
        d_number_frame = CTkFrame(provider_frame,  width=30,  height=30,  fg_color=GUI_COLORS['light'])
        d_number_frame.grid(row=0, column=0, sticky='nsw')
        d_number_frame.anchor('center')
        d_number_frame.grid_propagate(0)

        ttb.Label(d_number_frame, textvariable=self.__providerId, bootstyle='light inverse', padding=0).grid(row=0, column=0, sticky='nsew')


        self.providerEntry = ttb.Entry(provider_frame, textvariable=self.__providerName,state='readonly' )
        self.providerEntry.grid(row=0, column=1, sticky='nsew',padx=(4,0), ipady=4,)
        
        if not self.window_type == 'view':
            self.provider_search_btn = ttb.Button(provider_frame, text='...', bootstyle='dark', command=self.__open_provider_selection)
            self.provider_search_btn.grid(row=0, column=2, padx=2, sticky='nsew', pady=1)

        
        characteristics_frame = tk.Frame(product_info_content,)
        characteristics_frame.config(background=FGCOLOR)
        characteristics_frame.grid(row=4, column=0, columnspan=2, pady=(4,0), ipadx=8, ipady=8, sticky='nsew')
        
        
        tax_label = ttb.Label(characteristics_frame, 
                              anchor='w', 
                              text='Impuesto', 
                              background=FGCOLOR,
                              font=('arial',11,'bold'))
        tax_label.grid(row=0, column=0, padx=(4,0), pady=(4,0), ipadx=8, ipady=8, sticky='nsew')


        TAX =  DB.getTaxList()
        TAX_DICT = {row[1]:row[0] for row in TAX}
        TAX_DICT_VALUE = {row[0]:row[2] for row in TAX}
        del TAX


        def set_tax_value(var,index,mode):
            value = TAX_DICT_VALUE[self.__tax.get()]
            self.__taxValue.set(value)
            self.__cost_calculation()

        self.taxCombobox = ttb.Combobox(characteristics_frame, values=list(TAX_DICT.keys()), state='readonly', style='selectionOnly.TCombobox', textvariable=self.__taxName)
                      
        self.taxCombobox.grid(row=1, column=0, padx=(4,10), pady=(2,0), sticky='nsew')
        self.taxCombobox.bind("<<ComboboxSelected>>", lambda e: on_combobox_change(e,self.__tax, TAX_DICT,self.taxCombobox))
        self.taxCombobox.current(0)
        self.__tax.trace_add('write', set_tax_value)
        self.__tax.set(1)
   
        MEASUREMENT =  DB.getMeasurementList()
        MEASUREMENT_DICT = {row[1]:row[0] for row in MEASUREMENT}
        del MEASUREMENT

            ########### Measurement Section ###########
        measurement_label = ttb.Label(characteristics_frame, 
                                      anchor='w', 
                                      text='Unidad Medida', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        measurement_label.grid(row=0, column=1, padx=(4,4), pady=(4,0), ipadx=8, ipady=8, sticky='nsew')

        self.measurementCombobox = ttk.Combobox(characteristics_frame, values=list(MEASUREMENT_DICT.keys()), state='readonly', style='selectionOnly.TCombobox', textvariable=self.__measurementName)
        self.measurementCombobox.grid(row=1, column=1, padx=(4,0), pady=(2,0), sticky='nsew')
        self.measurementCombobox.bind("<<ComboboxSelected>>", lambda e: on_combobox_change(e,self.__measurement, MEASUREMENT_DICT, self.measurementCombobox))
        self.measurementCombobox.current(0)

        sectionDelimiter = CTkFrame(product_info_content,fg_color=GUI_COLORS['dark'])
        sectionDelimiter.grid(row=5, column=0, columnspan=2, pady=(4,4), ipadx=8, ipady=4, sticky='nsew')
        sectionDelimiter.anchor('center')

        ttb.Label(sectionDelimiter, text='Sección de Costos y Precios', font=(GUI_FONT,11,'bold'), bootstyle='dark inverse').grid(row=0, column=0, padx=4, pady=2)


        
        cost_section_frame = tk.Frame(product_info_content,)
        cost_section_frame.config(background=FGCOLOR)
        cost_section_frame.grid(row=6, column=0, columnspan=1, pady=(4,0), ipadx=8, ipady=8, sticky='nsew')

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
            self.__cost_calculation()
     
        
        self.currencyCombobox = ttb.Combobox(cost_section_frame, values=list(CURRENCY_DICT.keys()), state='readonly', style='selectionOnly.TCombobox', textvariable=self.__currencyName)
        self.currencyCombobox.grid(row=1, column=0, padx=(4,10), pady=(2,0), sticky='nsew')
        self.currencyCombobox.bind("<<ComboboxSelected>>", lambda e: on_combobox_change(e,self.__currency, CURRENCY_DICT, self.currencyCombobox))
        self.currencyCombobox.current(1)
        self.__currency.trace_add('write', set_exchange_rate)
        self.__currency.set(2)


        exchangeFrame = CTkFrame(cost_section_frame, fg_color=GUI_COLORS['info'], corner_radius=3)
        exchangeFrame.grid(row=2, column=0, padx=(4,10), pady=(8,0), sticky='nsew')
        exchangeFrame.anchor('center')


        ttb.Label(exchangeFrame, text='Tasa de Canbio', font=(GUI_FONT,11,'bold'), background=GUI_COLORS['info'], foreground='white').grid(row=0, column=0, padx=5,pady=(5,0), sticky='nsew')
        ttb.Label(exchangeFrame, textvariable=self.__currencyValue, anchor='center', width=8, font=(GUI_FONT,11), background=GUI_COLORS['info'], foreground='white').grid(row=1, column=0, padx=5,pady=(2,5), sticky='nsew')


        cost_label = ttb.Label(cost_section_frame, 
                               anchor='w', 
                               text='Costo Factura', 
                               background=FGCOLOR, 
                               font=('arial',11,'bold'))
        cost_label.grid(row=0, column=1, padx=(4,0), pady=(2,0), ipadx=8, sticky='nsew')



        self.costEntry = ttb.Entry(cost_section_frame, width=12, textvariable=self.__cost,justify='center',
                                    validate="key",validatecommand=(self.register(validateFloat), "%P"))
        self.costEntry.grid(row=1,column=1, padx=(4,10), sticky='nsew', ipady=4,)

        costexchangeFrame = CTkFrame(cost_section_frame, fg_color=GUI_COLORS['light'], corner_radius=3)
        costexchangeFrame.grid(row=2, column=1, padx=(4,10), pady=(8,0), sticky='nsew')
        costexchangeFrame.anchor('center')


        ttb.Label(costexchangeFrame, text='Costo al Cambio', font=(GUI_FONT,11,'bold'), background=GUI_COLORS['light'], foreground=GUI_COLORS['dark']).grid(row=0, column=0, columnspan=2,padx=5,pady=(5,0))
        ttb.Label(costexchangeFrame, textvariable=self.__cost_exchange, anchor='center', width=12, font=(GUI_FONT,11), background=GUI_COLORS['light'], foreground=GUI_COLORS['dark']).grid(row=1, column=0, padx=(5,0),pady=(2,5))
        ttb.Label(costexchangeFrame, text='Bs.', anchor='center', font=(GUI_FONT,11,'bold'), background=GUI_COLORS['light'], foreground=GUI_COLORS['dark']).grid(row=1, column=1, padx=(0,5),pady=(2,5))

        directCost_label = ttb.Label(cost_section_frame, 
                                     anchor='w', 
                                     text='% Directos', 
                                     background=FGCOLOR,
                                     font=('arial',11,'bold'))
        directCost_label.grid(row=0, column=2, padx=(4,0), pady=(2,0), ipadx=8, sticky='nsew')

        self.directCostEntry = ttb.Entry(cost_section_frame, width=12,  textvariable=self.__directCost,validate="key",validatecommand=(self.register(validateFloat), "%P"), justify='center')
        self.directCostEntry.grid(row=1,column=2, padx=(4,10), ipady=4,sticky='nsew')


        indirectCost_label = ttb.Label(cost_section_frame, 
                                     anchor='w', 
                                     text='% Indirectos', 
                                     background=FGCOLOR,
                                     font=('arial',11,'bold'))
        indirectCost_label.grid(row=0, column=3, padx=(4,0), pady=(2,0), ipadx=8, sticky='nsew')

        self.indirectCostEntry = ttb.Entry(cost_section_frame, width=12, textvariable=self.__indirectCost,validate="key",validatecommand=(self.register(validateFloat), "%P"), justify='center')
        self.indirectCostEntry.grid(row=1,column=3,padx=(4,10), ipady=4, sticky='nsew')
        

        fullCost = CTkFrame(cost_section_frame, fg_color=GUI_COLORS['light'], corner_radius=3)
        fullCost.grid(row=2,column=2, columnspan=2, padx=(4,4), pady=(8,0),  sticky='nsew')
        fullCost.anchor('center')

        ttb.Label(fullCost, text='Precio De Costo Full', font=(GUI_FONT,11,'bold'), background=GUI_COLORS['light'], foreground=GUI_COLORS['dark']).grid(row=0, column=0, columnspan=2, padx=5,pady=5)
        ttb.Label(fullCost, textvariable=self.__totalExchangeCost, anchor='center', width=12, font=(GUI_FONT,11), background=GUI_COLORS['light'], foreground=GUI_COLORS['dark']).grid(row=1, column=0, padx=5,pady=5)
        ttb.Label(fullCost, text='Bs.', anchor='center', font=(GUI_FONT,11,'bold'), background=GUI_COLORS['light'], foreground=GUI_COLORS['dark']).grid(row=1, column=1, padx=5,pady=5)



        pricing_section_frame = tk.Frame(product_info_content,)
        pricing_section_frame.config(background=FGCOLOR)
        pricing_section_frame.grid(row=6, column=1, columnspan=1, pady=(4,0), ipadx=8, ipady=8, sticky='nsew')
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


        self.priceEntry1 = ttb.Entry(priceFrame, width=14, textvariable=self.__price1,validate="key",validatecommand=(self.register(validateFloat), "%P"), justify='center')
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
                                text='0,00', 
                                bootstyle='light inverse', 
                                font=('arial',11,'bold'))
        self.exchange_fp.grid(row=1, column=3, padx=(2,2), ipadx=8, sticky='nsew',pady=(2,2))

        exchange_fp_c = ttb.Label(exchangeFirstPrice,
                                  width=6, 
                                  text='Bs.',
                                  anchor='center', 
                                  bootstyle='light inverse',)
        exchange_fp_c.grid(row=1,column=4, sticky='nsew',pady=(2,2), padx=(0,2))

        self.profitEntry1 = ttb.Entry(priceFrame,  width=8,  textvariable=self.__profit1, validate="key",validatecommand=(self.register(validateFloat), "%P"), justify='center',state='readonly')
        self.profitEntry1.grid(row=0,column=5, sticky='nsew',pady=(0,4), ipady=4, padx=(4,0))


        ####################################

        ttb.Label(priceFrame, 
                                     anchor='w', 
                                     text='Precio 2 (PVP)', 
                                     background='white',
                                     font=('arial',11,'bold')
        ).grid(row=1, column=0, padx=(0,0), pady=(0,4), ipadx=8, sticky='nsew')


        self.priceEntry2 = ttb.Entry(priceFrame, width=12,validate="key",validatecommand=(self.register(validateFloat), "%P"), justify='center', textvariable=self.__price2,)
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
                                text='0,00', 
                                bootstyle='light inverse', 
                                font=('arial',11,'bold'))
        self.exchange_fp.grid(row=0, column=0, padx=(2,2), ipadx=8, sticky='nsew',pady=(2,2))

        exchange_fp_c = ttb.Label(exchangeFirstPrice,
                                  width=6, 
                                  text='Bs.',
                                  anchor='center', 
                                  bootstyle='light inverse',)
        exchange_fp_c.grid(row=0,column=1, sticky='nsew',pady=(2,2), padx=(0,2))

        self.profitEntry2 = ttb.Entry(priceFrame, width=8, textvariable=self.__profit2,validate="key",validatecommand=(self.register(validateFloat), "%P"), justify='center',state='readonly')
        self.profitEntry2.grid(row=1,column=5, sticky='nsew',pady=(0,4), ipady=4, padx=(4,0))



        ####################################

        ttb.Label(priceFrame, 
                                     anchor='w', 
                                     text='Precio 3 (PVP)', 
                                     background='white',
                                     font=('arial',11,'bold')
        ).grid(row=2, column=0, padx=(0,0), pady=(0,4), ipadx=8, sticky='nsew')


        self.priceEntry3 = ttb.Entry(priceFrame, width=14,validate="key",validatecommand=(self.register(validateFloat), "%P"), justify='center', textvariable=self.__price3)
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
                                text='0,00', 
                                bootstyle='light inverse', 
                                font=('arial',11,'bold'))
        self.exchange_fp.grid(row=0, column=0, padx=(2,2), ipadx=8, sticky='nsew',pady=(2,2))

        exchange_fp_c = ttb.Label(exchangeFirstPrice,
                                  width=6, 
                                  text='Bs.',
                                  anchor='center', 
                                  bootstyle='light inverse',)
        exchange_fp_c.grid(row=0,column=1, sticky='nsew',pady=(2,2), padx=(0,2))

        self.profitEntry3 = ttb.Entry(priceFrame, width=8, textvariable=self.__profit3, validate="key",validatecommand=(self.register(validateFloat), "%P"), justify='center',state='readonly')
        self.profitEntry3.grid(row=2,column=5, sticky='nsew',pady=(0,4), ipady=4, padx=(4,0))



        
        sectionDelimiter = CTkFrame(product_info_content,fg_color=GUI_COLORS['dark'])
        sectionDelimiter.grid(row=7, column=0, columnspan=2, pady=(4,0), ipadx=8, ipady=4, sticky='nsew')
        sectionDelimiter.anchor('center')

        ttb.Label(sectionDelimiter, text='Sección de Inventario', font=(GUI_FONT,11,'bold'), bootstyle='dark inverse').grid(row=0, column=0, padx=4, pady=2)


        
        inventory_section_frame = tk.Frame(product_info_content,)
        inventory_section_frame.config(background=FGCOLOR)
        inventory_section_frame.grid(row=8, column=0, columnspan=2, pady=(4,0), ipadx=8, ipady=8, sticky='nsew')



        stocklabel = CTkFrame(inventory_section_frame, fg_color='#212946', corner_radius=3)
        stocklabel.grid(row=0, column=0, padx=19,pady=(4,2), sticky='nsew')

        ttb.Label(stocklabel, 
            anchor='center', 
            text='Inventario Principal', 
            background='#212946',
            foreground='white',                       
            font=('arial',11,'bold')
        ).grid(row=0, column=0, padx=6, pady=8, ipadx=8, sticky='nsew')



        self.mainStockEntry = ttb.Entry(inventory_section_frame,   width=12, justify='center', textvariable=self.__mainStock,validate="key",state='readonly',
                                    validatecommand=(self.register(validate_number), "%S"))
        self.mainStockEntry.grid(row=1, column=0, sticky='nsew',pady=(0,4),padx=20, ipady=6)

        depositFrame = tk.Frame(inventory_section_frame)
        depositFrame.config(background=FGCOLOR)
        depositFrame.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=4, pady=4)
        depositFrame.rowconfigure(2, weight=1)


        deposit_section_title = ttb.Label(depositFrame, 
                                text='Depositos', 
                                bootstyle='dark', 
                                background=FGCOLOR,
                                anchor='w',
                                font=('arial',11,'bold'))
        deposit_section_title.grid(row=0, column=0, padx=4, pady=0, ipadx=2, ipady=2, sticky='nsew')

        ttb.Separator(depositFrame, bootstyle='dark').grid(row=1, column=0, padx=6, pady=4, sticky='nsew',)

        depositEntryFrame = tk.Frame(depositFrame)
        depositEntryFrame.config(background=FGCOLOR)
        depositEntryFrame.grid(row=2, column=0, sticky='sew',padx=4)

    
        ttb.Label(depositEntryFrame, 
                  anchor='center', 
                  text='D1', 
                  background=FGCOLOR,
                  font=('arial',11,'bold')
        ).grid(row=0, column=0, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        
        self.depositEntry1 = ttb.Entry(depositEntryFrame,  width=12, justify='center', textvariable=self.__stock1, validate="key",state='readonly',
                                    validatecommand=(self.register(validate_number), "%S"))
        self.depositEntry1.grid(row=0, column=1, sticky='nsew',pady=(2,0),padx=(2,6))

        ttb.Label(depositEntryFrame, 
                  anchor='center', 
                  text='D2', 
                  background=FGCOLOR,
                  font=('arial',11,'bold')
        ).grid(row=0, column=2, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        
        self.depositEntry2 = ttb.Entry(depositEntryFrame, width=12, justify='center', textvariable=self.__stock2,validate="key",state='readonly',
                                    validatecommand=(self.register(validate_number), "%S"))
        self.depositEntry2.grid(row=0, column=3, sticky='nsew',pady=(2,0),padx=(2,6))

        ttb.Label(depositEntryFrame, 
                  anchor='center', 
                  text='D3', 
                  background=FGCOLOR,
                  font=('arial',11,'bold')
        ).grid(row=0, column=4, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.depositEntry3 = ttb.Entry(depositEntryFrame,   width=12, justify='center', textvariable=self.__stock3, validate="key",state='readonly',
                                    validatecommand=(self.register(validate_number), "%S"))
        self.depositEntry3.grid(row=0, column=5, sticky='nsew',pady=(2,0),padx=(2,6))

        ttb.Label(depositEntryFrame, 
                  anchor='center',
                  text='D4', 
                  background=FGCOLOR,
                  font=('arial',11,'bold')
        ).grid(row=0, column=6, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.depositEntry4 = ttb.Entry(depositEntryFrame,  width=12, justify='center', textvariable=self.__stock4,validate="key",state='readonly',
                                    validatecommand=(self.register(validate_number), "%S"))
        self.depositEntry4.grid(row=0, column=7, sticky='nsew',pady=(2,0),padx=(2,6))


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

        
        self.__form_fields =[self.codeEntry, self.descriptionEntry, self.costEntry, self.directCostEntry, self.indirectCostEntry, self.priceEntry1, self.priceEntry2, self.priceEntry3,]


        self.__STOCK_FIELDS = [ self.mainStockEntry, self.depositEntry1, self.depositEntry2, self.depositEntry3, self.depositEntry4]
        self.__NUM_FIELDS = [self.costEntry, self.directCostEntry, self.indirectCostEntry,self.priceEntry1,self.priceEntry2,self.priceEntry3, self.mainStockEntry, self.depositEntry1, self.depositEntry2, self.depositEntry3, self.depositEntry4]
        self.__DATA_FORM = [self.__code, self.__description, self.__brandId, self.__departmentId, self.__providerId, self.__tax, self.__currency, self.__measurement, ]
        self.__DATA_NUMBERS_FORMVAR = [self.__cost, self.__directCost, self.__indirectCost, self.__price1, self.__price2, self.__price3, self.__profit1, self.__profit2, 
                                    self.__profit3, self.__mainStock, self.__stock1, self.__stock2, self.__stock3, self.__stock4]

        if self.window_type == 'create' or self.window_type == 'quickCreate':


            creatbtnimg = Image.open(f"{IMG_PATH}/registrar.png")
            self.creatbtnimg = ImageTk.PhotoImage(creatbtnimg.resize(resize_image(20, creatbtnimg.size)))
            creatbtnimgh = Image.open(f"{IMG_PATH}/registrarh.png")
            self.creatbtnimgh = ImageTk.PhotoImage(creatbtnimgh.resize(resize_image(20, creatbtnimgh.size)))
            creatbtnimgp = Image.open(f"{IMG_PATH}/registrarp.png")
            self.creatbtnimgp = ImageTk.PhotoImage(creatbtnimgp.resize(resize_image(20, creatbtnimgp.size)))

            self.createBTN = ButtonImage(buttonss_section_frame,  command=self.createProductRecord, image=self.creatbtnimg, img_h=self.creatbtnimgh, img_p=self.creatbtnimgp, style='flatw.light.TButton', text='REGISTRAR', compound='center',padding=0)
            self.createBTN.grid(row=0, column=1, sticky='nsew', pady=2, padx=(0,4))

            self.__set_form_state()
            if self.window_type == 'quickCreate':
                self.codeEntry.config(state='readonly')
                for field in self.__NUM_FIELDS:
                    field.config(state='readonly')
            else:
                for field in self.__STOCK_FIELDS:
                    field.config(state='normal') 

        elif self.window_type == 'edit':
            editbtn = Image.open(f"{IMG_PATH}/editn.png")
            self.editbtn = ImageTk.PhotoImage(editbtn.resize(resize_image(20, editbtn.size)))
            editbtnh = Image.open(f"{IMG_PATH}/edith.png")
            self.editbtnh = ImageTk.PhotoImage(editbtnh.resize(resize_image(20, editbtnh.size)))
            editbtnp = Image.open(f"{IMG_PATH}/editp.png")
            self.editbtnp = ImageTk.PhotoImage(editbtnp.resize(resize_image(20, editbtnp.size)))

            self.editBTN = ButtonImage(buttonss_section_frame, command=self.editProductRecord, image=self.editbtn, img_h=self.editbtnh, img_p=self.editbtnp, style='flatw.light.TButton', text='MODIFICAR', compound='center',padding=0)
            self.editBTN.grid(row=0, column=2, sticky='nsew', pady=2, padx=(0,4))

            self.__set_form_state()
            self.codeEntry.configure(state='readonly')
        
        
        else:
            self.__set_form_state('readonly')


        
        
        
    def __set_form_state(self, state = 'normal'):
        for field in self.__form_fields:
            if field.winfo_class() == 'TEntry':
                field.config(state=state, cursor='xterm')
            elif field.winfo_class() in ['TCombobox','TButton']:
                newstate = state
                if state == 'readonly':
                    newstate='disabled'
                field.config(state=newstate, cursor='xterm')
            elif field.winfo_class() == 'TFrame':
                self.__set_form_state(field, state)
            



    def __open_selection_modal(self, title, table, callback = None):
        select_window = SubWindowsSelection(window_title=title, database_table=table, callback = callback)
        self.wait_window(select_window)
        self.grab_set()
        self.transient()
        self.focus()
    
    def __open_provider_selection(self):
        select_window = ProviderModule( callback = self.__set_provider_info, selectionMode=True)
        self.wait_window(select_window)
        self.grab_set()
        self.transient()

    def __set_dept_info(self, id, description):
        self.__departmentId.set(id)
        self.__departmentName.set(description)

    def __set_brand_info(self, id, description):
        self.__brandId.set(id)
        self.__brandName.set(description)

    def __set_provider_info(self, provider):
        self.__providerId.set(provider.id)
        self.__providerName.set(provider.name)






    def productInstance(self):
        return Product(
            code=self.__code.get(),
            description=self.__description.get(),
            department=self.__departmentId.get(),
            brand=self.__brandId.get(),
            provider=self.__providerId.get(),
            currency=self.__currency.get(),
            measurement=self.__measurement.get(),
            tax=self.__tax.get(),
            cost=self.__cost.get(),
            indirectcost=self.__directCost.get(),
            directcost=self.__directCost.get(),
            price_1=self.__price1.get(),
            price_2=self.__price2.get(),
            price_3=self.__price3.get(),
            profit_1=self.__profit1.get(),
            profit_2=self.__profit2.get(),
            profit_3=self.__profit3.get(),
            stock=self.__mainStock.get(),
            stock_1=self.__stock1.get(),
            stock_2=self.__stock2.get(),
            stock_3=self.__stock3.get(),
            stock_4=self.__stock4.get(),
        )
    

    def __check_fields(self):
        return not '' in [value.get() for value in self.__DATA_FORM] and not 0 in [value.get() for value in self.__DATA_FORM] 
    

    def __field_num_entrys(self):
        for field in self.__DATA_NUMBERS_FORMVAR:
            if not field.get():
                field.set(0)
    

    def createProductRecord(self):
        if self.__check_fields():
            if not Product.validate_code(self.__code.get()):
                ask = messagebox.askquestion('Crear','Crear nuevo producto?', parent=self)
                if ask == 'yes':
                    self.__field_num_entrys()
                    newProduct = self.productInstance()
                    newProduct.create()
                    messagebox.showinfo('Aviso','Producto creado satisfactoriamente.', parent=self)
                    self.destroy()
            else:
                messagebox.showwarning('Aviso','El codigo ingresado ya se encuentra asociado a un registro.', parent=self)
        else:
            messagebox.showwarning('Aviso','Existen algunos campos invalidos o faltan por rellenar.', parent=self)


    def editProductRecord(self):
        if self.__check_fields():
            ask = messagebox.askquestion('Modificar','Modificar el Registro de Producto?', parent=self)
            if ask == 'yes':
                self.__field_num_entrys()
                newProdcut = self.productInstance()
                newProdcut.update()
                messagebox.showinfo('Aviso','Registro modificado satisfactoriamente.', parent=self)
                self.destroy()
        else:
            messagebox.showwarning('Aviso','Existen algunos campos invalidos o faltan por rellenar.', parent=self)

    def __stock_manipulation(self, title, callback):
        def set_days():
            if self.stockAmount.get():
                ask = messagebox.askquestion('Confirmacion', 'Esta accion generará cambios en el stock del producto. Desea ejecutar la acción?', parent=window)
                if ask == 'yes':
                    check = callback(int(self.stockAmount.get()))
                    if check:
                        window.destroy()
                        messagebox.showinfo('Aviso', 'Stock Actualizado con exito!', parent=self)
                    else:
                        messagebox.showwarning('Cantidad','Accion invalida. No esta permitido reducir una cantidad mayor a la disponible en el stock.', parent=window)
                    window.destroy()
                
            

        window = ttb.Toplevel(title=f'{title} Stock', toolwindow=True)
        window.resizable(0,0)
        window.focus()
        window.grab_set()
        auxFrame = CTkFrame(window, fg_color='white')
        auxFrame.grid(row=0, column=0, padx=10, pady=10)


        code_label = ttb.Label(auxFrame, 
                                      anchor='w', 
                                      text=f'Cantidad a {title}', 
                                      bootstyle='primary', 
                                      background='#fff',
                                      font=('arial',11,'bold'))
        code_label.grid(row=0, column=0, padx=(4,4), pady=(4,0), ipadx=8,  ipady=4, sticky='nsew')

        self.stockAmount = ttb.Entry(auxFrame,   width=30, justify='center',)
        self.stockAmount.grid(row=1, column=0, sticky='nsew',pady=(2,8),padx=10, ipady=4, columnspan=1)
        self.stockAmount.focus()

        if title.lower() == 'agregar':
            button = 'green'
        else:
            button = 'red'

        addimg = Image.open(f"{IMG_PATH}/{button}Button.png")
        self.addimg = ImageTk.PhotoImage(addimg.resize(resize_image(19, addimg.size)))
        addimgh = Image.open(f"{IMG_PATH}/{button}Buttonh.png")
        self.addimgh = ImageTk.PhotoImage(addimgh.resize(resize_image(19, addimgh.size)))
        addimgp = Image.open(f"{IMG_PATH}/{button}Buttonp.png")
        self.addimgp = ImageTk.PhotoImage(addimgp.resize(resize_image(19, addimgp.size)))

        self.acceptBTN = ButtonImage(auxFrame,  command=set_days, compound='center', text=title.upper(),image=self.addimg, img_h=self.addimgh, img_p=self.addimgp, style='flatw.light.TButton', padding=0)
        self.acceptBTN.grid(row=2, column=0, sticky='', pady=(0,8), padx=(4))

        self.wait_window(window)
        self.grab_set()
        self.transient()
        self.focus()
        self.__set_product_data()
        

    def __set_product_data(self):
        self.__code.set(self.__PRODUCT.code)
        self.__description.set(self.__PRODUCT.description)
        self.__brandId.set(self.__PRODUCT.brand)
        self.__brandName.set(self.__PRODUCT.get_brand())
        self.__departmentId.set(self.__PRODUCT.department)
        self.__departmentName.set(self.__PRODUCT.get_department())
        self.__providerId.set(self.__PRODUCT.provider)
        self.__providerName.set(self.__PRODUCT.get_provider())
        self.__currency.set(self.__PRODUCT.currency)
        self.__currencyName.set(self.__PRODUCT.get_currency())
        self.__tax.set(self.__PRODUCT.tax)
        self.__taxName.set(self.__PRODUCT.get_tax())
        self.__measurement.set(self.__PRODUCT.measurement)
        self.__measurementName.set(self.__PRODUCT.get_measurement())
        self.__cost.set(self.__PRODUCT.cost)
        self.__directCost.set(self.__PRODUCT.directcost)
        self.__indirectCost.set(self.__PRODUCT.indirectcost)
        self.__price1.set(self.__PRODUCT.price_1)
        self.__price2.set(self.__PRODUCT.price_2)
        self.__price3.set(self.__PRODUCT.price_3)
        self.__profit1.set(self.__PRODUCT.profit_1)
        self.__profit2.set(self.__PRODUCT.profit_2)
        self.__profit3.set(self.__PRODUCT.profit_3)
        self.__mainStock.set(self.__PRODUCT.stock)
        self.__stock1.set(self.__PRODUCT.stock_1)
        self.__stock2.set(self.__PRODUCT.stock_2)
        self.__stock3.set(self.__PRODUCT.stock_3)
        self.__stock4.set(self.__PRODUCT.stock_4)
        

# app = ttb.Window(themename='new')
# SGDB_Style()
# ProductForm(window_type='create', title='Registrar Producto')
# app.mainloop()
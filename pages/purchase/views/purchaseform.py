import ttkbootstrap as ttb
from tkinter import ttk
from assets.globals import GUI_COLORS, GUI_FONT, IMG_PATH
from models.entitys.product import  Product
from pages.Products.views.product_search import ProductSelection
from pages.providers.providers import ProviderModule
from datetime import datetime
from tkinter import messagebox
from customtkinter import CTkFrame
from PIL import Image, ImageTk
from components.buttons import ButtonImage
from assets.utils import resize_icon, resize_image
import tkinter as tk
from assets.db.db_connection import DB
from models.entitys.purchase import PurchaseDocument
from pages.Products.views.product_form import ProductForm
from assets.globals import on_validate_length, limitar_longitud, checkDATE, on_combobox_change, validate_number, validateFloat
from pages.Extras.payments import PaymentForm
FGCOLOR = 'white'




class PurchaseForm(ttb.Toplevel):
    def __init__(self, master=None, window_type = 'create', title = '', purchase:PurchaseDocument=None):
        super().__init__(master)
        self.withdraw()

        self.window_title = title
        self.window_type = window_type

        ######### MODAL WINDOW CONFIG #########

        self.BUDGET = None
       
        ########### VARIABLES ############
        self.BCODE = ttb.StringVar()
        self.BCONTROL = ttb.StringVar()
        self.BPROVIDER_ID = ttb.IntVar()
        self.BPROVIDER_RIF = ttb.StringVar()
        self.BPROVIDER_NAME = ttb.StringVar()
        self.BDOCUMENTSTATE = ttb.IntVar()
        self.BDOCUMENTO_CONDITION = ttb.StringVar()
        self.BDOCUMENTO_CONDITION.trace_add('write', lambda v,i,m: self.checkDocumentCondition())
        self.BCURRENCY = ttb.IntVar()
        self.BCURRENCY.trace_add('write', lambda v,i,m: self.check_exchangerate())
        self.BCURRENCYNAME = ttb.StringVar()
        
        self.BDATEOFISSUE = ttb.StringVar(value=datetime.today().strftime('%d/%m/%Y'))
        self.BDATEOFISSUE.trace_add('write', lambda v,i,m: self.sameDateCallback())
        self.BEXPIRATIONDATE = ttb.StringVar(value=datetime.today().strftime('%d/%m/%Y'))
        self.BREGISTERDATE = ttb.StringVar(value=datetime.today().strftime('%d/%m/%Y'))
        self.BDOCUMENT_TYPE = ttb.IntVar(value=1)
        self.BDOCUMENT_TYPE.trace_add('write', lambda v,i,m: self.enabled_fields_by_documentType())
        self.BDOCUMENT_TYPENAME = ttb.StringVar()
        
        self.BEXCHANGERATE = ttb.StringVar(value=0)
        self.BEXCHANGERATE.trace_add('write', lambda v,i,m: self.set_debt_amount())
  

        self.BAMOUNT = ttb.StringVar(value=0)
        self.BAMOUNT.trace_add('write', lambda v,i,m: self.set_debt_amount())
        self.BAMOUNT.trace_add('write', lambda v,i,m: self.calculate_usd_amount())

        self.BAMOUNTUSD = ttb.StringVar(value=0)
        self.BDEBT = ttb.DoubleVar(value=0)
        self.BTOTALPAID = ttb.DoubleVar(value=0)

        if self.window_type == 'view':
            self.BAMOUNT_DEBT = ttb.StringVar(value=0)
            self.BAMOUNT_PAID = ttb.StringVar(value=0)
            self.BSTATUS = ttb.StringVar()
            self.BSTATE = ttb.StringVar()

        
        self.prices_focus = ttb.BooleanVar(value=True)
        self.__PRODUCT: Product = None
        ######### VARIABLES #########
        self.__code = ttb.StringVar()
        self.__description = ttb.StringVar()

        self.__currency = ttb.IntVar(value=2)

        self.oldmeasurementName = ttb.StringVar()
        self.oldcost = ttb.StringVar(value='0.00')
        self.oldtax = ttb.StringVar()
        self.oldstock = ttb.StringVar()
        self.oldcostexchange = ttb.StringVar(value='0.00')
       
        self.__currency = ttb.IntVar(value=2)

        self.__currencyName = ttb.StringVar(value='USD $')
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


        self.stock_var = ttb.StringVar(value=0)

        self.stocka_var = ttb.StringVar(value=0)
        self.stock_1_var = ttb.StringVar(value=0)
        self.stock_2_var = ttb.StringVar(value=0)
        self.stock_3_var = ttb.StringVar(value=0)
        self.stock_4_var = ttb.StringVar(value=0)

        self.expiration_date_var = ttb.StringVar()
        self.observation_var = ttb.StringVar()

        self.__createWidgets()

        if purchase:
            self.__DOCUMENT = purchase
            self.set_purchase_info()

            colorstate = {1:'secondary',2:'danger', 3:'success'}
            colorpayment = {1:'danger', 2:'success'}
            self.documentStatEntry.config(bootstyle=colorstate[self.__DOCUMENT.documentState])
            self.documentStatusEntry.config(bootstyle=colorpayment[self.__DOCUMENT.payment_status])

        self.title(title)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.transient()
        self.grab_set()
        self.focus()
        self.config(background="#fff")
        self.place_window_center()
        self.iconbitmap('SIGAG.ico')
        self.deiconify()

    def enabled_fields_by_documentType(self):
        if self.window_type != 'view':
            if self.BDOCUMENT_TYPE.get() == 1:
                self.amountLabelMain.grid_forget()
                self.amountEntry.grid_forget()
              
            else:
                self.amountLabelMain.grid(row=0, column=3, padx=5, pady=(4,0), ipadx=8, ipady=4, sticky='nsew')
                self.amountEntry.grid(row=1, column=3, sticky='nsew',pady=(2,0),padx=4, ipady=10)
                
        if self.BDOCUMENT_TYPE.get() == 1:
            self.maxpage = 3
        else:
            self.maxpage = 1 
        self.__set_page()


    def SET_ITEMS_MAIN_CURRRENCY(self):
        self.itemsGridview.heading('totalUSD', text=f'Total {self.BCURRENCYNAME.get()}')


    def __delete_record(self, selected = None):
        if selected == None:
            selected = self.itemsGridview.focus()
        if selected:    
            self.itemsGridview.delete(selected)
            self.__update_balance()
            


    def __delete_all_record(self):
        ask = messagebox.askquestion('Retornar','Retornar todos los elementos al inentario?', parent=self)
        if ask == 'yes':
            for record in self.itemsGridview.get_children():
                self.__delete_record(record)

    def calculate_exchange_price(self, price_var = None, exchange_var = None):
        currency_value = float(self.__currencyValue.get())
        if currency_value == 0:
            currency_value = 1
        if price_var.get():
            exchange_var.set(float(price_var.get())*currency_value)

    def __check_fields(self):
        return not ('') in [value.get() for value in list(self.PURCHASE_FIELDS.values())]
    
    def __createWidgets(self):
        
        contentFrame = CTkFrame(self, fg_color='white',border_width=1,  border_color='#CFCFCF')
        contentFrame.grid(row = 1, column = 0, sticky = 'nsew', padx=10, pady=10)
        contentFrame.columnconfigure(0, weight=1)


        self.__products_icon = resize_icon(Image.open(f"{IMG_PATH}/invoice.png"))


        titleFrame = CTkFrame(contentFrame, fg_color='#212946')
        titleFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=8, pady=(8,0))
        titleFrame.columnconfigure(0, weight=1)
        
        ttb.Label(titleFrame, image=self.__products_icon, compound='left', text=f' {self.window_title}', font=(GUI_FONT, 14, 'bold'), foreground='white', background='#212946').grid(row=0,column=0, padx=10, pady=10, sticky='nsew')

        
    
       

        self.product_info_content = tk.Frame(contentFrame)
        self.product_info_content.config(background=FGCOLOR)
        self.product_info_content.grid(row=1, column=0, sticky='nsew', padx=10, pady=(0,5))
        self.product_info_content.columnconfigure(1, weight=1)
        self.product_info_content.columnconfigure(2, weight=1)


            ########### Description Section ###########

        

        ttb.Separator(self.product_info_content, bootstyle='light').grid(row=9, column=0, pady=(8,0), sticky='nsew', columnspan=2)


        buttonss_section_frame = tk.Frame(self.product_info_content,)
        buttonss_section_frame.configure(background=FGCOLOR)
        buttonss_section_frame.grid(row=10, column=0, pady=(8,0), sticky='nsew', columnspan=2)
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
        self.closeBTN = ButtonImage(buttonss_section_frame, image=self.closeimg, img_h=self.closeimgh, command=self.destroy, img_p=self.closeimgp, style='flatw.light.TButton', text='CERRAR', compound='center',padding=0)
        self.closeBTN.grid(row=0, column=1, sticky='nsew', pady=2, padx=(0,4))

        
        #self.__form_fields =[self.codeEntry, self.descriptionEntry, self.departmentEntry, self.brandEntry, self.providerEntry, self.taxCombobox, self.measurementCombobox, self.currencyCombobox, self.costEntry, self.directCostEntry, self.indirectCostEntry,
        #                     self.priceEntry1, self.priceEntry2, self.priceEntry3, self.profitEntry1, self.profitEntry2, self.profitEntry3, self.mainStockEntry, self.depositEntry1, self.depositEntry2, self.depositEntry3, self.depositEntry4]
        
        #self.__form_variables = [self.code_var, self.description_var, self.department_var, self.brand_var, self.provider_var, self.tax_var, self.measurement_var, self.currency_var, self.cost_var, self.indirect_cost_var, self.direct_cost_var,
            #                     self.price_1_var, self.price_2_var, self.price_3_var, self.profit_1_var, self.profit_2_var, self.profit_3_var, self.stock_var, self.stock_1_var, self.stock_2_var, self.stock_3_var, self.stock_4_var]
        backbtnimg = Image.open(f"{IMG_PATH}/back.png")
        self.backbtnimg = ImageTk.PhotoImage(backbtnimg.resize(resize_image(15.5, backbtnimg.size)))
        backbtnimgh = Image.open(f"{IMG_PATH}/backh.png")
        self.backbtnimgh = ImageTk.PhotoImage(backbtnimgh.resize(resize_image(15.5, backbtnimgh.size)))
        backbtnimgp = Image.open(f"{IMG_PATH}/backp.png")
        self.backbtnimgp = ImageTk.PhotoImage(backbtnimgp.resize(resize_image(15.5, backbtnimgp.size)))

        self.backBTN = ButtonImage(buttonss_section_frame,  command=self.__back_page, image=self.backbtnimg, img_h=self.backbtnimgh, img_p=self.backbtnimgp, style='flatw.light.TButton',padding=0)


        creatbtnimg = Image.open(f"{IMG_PATH}/registrar.png")
        self.creatbtnimg = ImageTk.PhotoImage(creatbtnimg.resize(resize_image(20, creatbtnimg.size)))
        creatbtnimgh = Image.open(f"{IMG_PATH}/registrarh.png")
        self.creatbtnimgh = ImageTk.PhotoImage(creatbtnimgh.resize(resize_image(20, creatbtnimgh.size)))
        creatbtnimgp = Image.open(f"{IMG_PATH}/registrarp.png")
        self.creatbtnimgp = ImageTk.PhotoImage(creatbtnimgp.resize(resize_image(20, creatbtnimgp.size)))

        self.createBTN = ButtonImage(buttonss_section_frame,  command=self.check_data_compra, image=self.creatbtnimg, img_h=self.creatbtnimgh, img_p=self.creatbtnimgp, style='flatw.light.TButton', text='CONTINUAR', compound='center',padding=0)
        self.createBTN.grid(row=0, column=3, sticky='nsew', pady=2, padx=(0,4))

        self.__all_pages = []
        

        self.__page = ttb.StringVar(value=1)
        self.__page.trace_add('write', lambda i,m,v: self.__set_page())
        self.__firstPage()
        self.__all_pages.append(self.firtsPageFrame)
        
        if self.window_type != 'view':
            self.__secondPage()
            self.__all_pages.append(self.second_page)
            self.maxpage = 3
        else: self.maxpage = 2

        self.__thirthdPage()
        self.BCURRENCYNAME.trace_add('write', lambda v,i,m: self.SET_ITEMS_MAIN_CURRRENCY())
        self.SET_ITEMS_MAIN_CURRRENCY()
      
        self.__all_pages.append(self.thirth_page)
        self.__set_page()

        if self.window_type == 'view':
            self.__set_form_state(self.moreInfoFrame,'readonly')
            # self.searchProviderBTN.config(state='disabled')
            # self.provider_search_btn.config(state='disabled')
        else:
            self.bind('<F2>', self.__enabled_percentage_entry)
    
    def __enabled_percentage_entry(self, e):
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

    def __next_page(self):
       
        self.__page.set(int(self.__page.get())+1)

    def __back_page(self):
        self.__page.set(int(self.__page.get())-1)

    def __set_page(self):
        page = int(self.__page.get())
  
        if page == self.maxpage:
            if self.window_type == 'create':
                if self.maxpage > 1:
                    self.createBTN.configure(text='REGISTRAR', command=lambda:self.create_purchases())
                else:
                    self.createBTN.config(text='REGISTRAR',command=self.check_data_compra)
            else:
                self.createBTN.grid_forget()
            if self.maxpage > 1:
                self.backBTN.grid(row=0, column=2, sticky='nsew', pady=2, padx=(0,4))
        else:
        
            if self.window_type != 'create' and not self.createBTN.winfo_ismapped():
                self.createBTN.grid(row=0, column=3, sticky='nsew', pady=2, padx=(0,4))

            self.createBTN.configure(text='CONTINUAR',command=self.__next_page)
            if page == 1:
                self.createBTN.config(command=self.check_data_compra)
                self.backBTN.grid_forget()
            else:
                self.backBTN.grid(row=0, column=2, sticky='nsew', pady=2, padx=(0,4))
        
        self.__all_pages[page-1].tkraise()
            
        self.pageNum.config(text=f'Pagina: {page}/{self.maxpage}')


        
        
   

    def __thirthdPage(self):
        self.thirth_page = tk.Frame(self.product_info_content)
        self.thirth_page.config(background=FGCOLOR)
        self.thirth_page.grid(row=0, column=0, sticky='nsew', columnspan=2)
        self.thirth_page.columnconfigure(0, weight=1)
        self.thirth_page.grid_propagate(0)
        self.thirth_page.rowconfigure(1,weight=1)

            #### Gridview Button options ####
        buttons_menu_frame = ttb.Frame(self.thirth_page, style='white.TFrame')
        buttons_menu_frame.grid(row=0, column=0, sticky='nsew', columnspan=2)

        ttb.Label(buttons_menu_frame, text='Listado de Items', font=(GUI_FONT,12,'bold'), background='#fff').grid(row=0, column=0, sticky='nsew', padx=(0,4))
        ttb.Separator(buttons_menu_frame,
                      orient='vertical'
        ).grid(row=0, column=1, sticky='ns', pady=12,)

        if self.window_type == 'create':

            deleteimg = Image.open(f"{IMG_PATH}/deleten.png")
            self.deleteimg = ImageTk.PhotoImage(deleteimg.resize(resize_image(18, deleteimg.size)))
            deleteimgh = Image.open(f"{IMG_PATH}/deleteh.png")
            self.deleteimgh = ImageTk.PhotoImage(deleteimgh.resize(resize_image(18, deleteimgh.size)))
            deleteimgp = Image.open(f"{IMG_PATH}/deletep.png")
            self.deleteimgp = ImageTk.PhotoImage(deleteimgp.resize(resize_image(18, deleteimgp.size)))

            self.deleteBTN = ButtonImage(buttons_menu_frame,  command=self.__delete_all_record, image=self.deleteimg, img_h=self.deleteimgh, img_p=self.deleteimgp, style='white.TButton', padding=0)
            self.deleteBTN.grid(row=0, column=2, sticky='nsew', pady=2, padx=(10,5))


            deleteoneimg = Image.open(f"{IMG_PATH}/deleteone.png")
            self.deleteoneimg = ImageTk.PhotoImage(deleteoneimg.resize(resize_image(18, deleteoneimg.size)))
            deleteoneimgh = Image.open(f"{IMG_PATH}/deleteoneh.png")
            self.deleteoneimgh = ImageTk.PhotoImage(deleteoneimgh.resize(resize_image(18, deleteoneimgh.size)))
            deleteoneimgp = Image.open(f"{IMG_PATH}/deleteonep.png")
            self.deleteoneimgp = ImageTk.PhotoImage(deleteoneimgp.resize(resize_image(18, deleteoneimgp.size)))

            self.deleteoneBTN = ButtonImage(buttons_menu_frame,  command=self.__delete_record, image=self.deleteoneimg, img_h=self.deleteoneimgh, img_p=self.deleteoneimgp, style='white.TButton', padding=0)
            self.deleteoneBTN.grid(row=0, column=3, sticky='nsew', pady=2, padx=(5,10))


        ttb.Separator(buttons_menu_frame,
                      orient='vertical'
        ).grid(row=0, column=4, sticky='ns', pady=12)

    

            ##### SCROLLBARS #####

        

        yscroll = ttb.Scrollbar(self.thirth_page, orient='vertical',bootstyle="dark-round")
        yscroll.grid(row=1, column=1, padx=2, pady=2,sticky='ns', rowspan=2)

        xscroll = ttb.Scrollbar(self.thirth_page, orient='horizontal',bootstyle="dark-round")
        xscroll.grid(row=2, column=0, padx=2, pady=2,sticky='ew')

            ##### GRIDVIEW #####
        columns = ('code',
                   'description',
                   'impuesto',
                   'moneda',
                   'unit',
                   'cost',
                   'price',
                   'price2',
                   'price3',
                   'profit',
                   'profit2',
                   'profit3',
                   'stock',
                   'stock1',
                   'stock2',
                   'stock3',
                   'stock4',
                   'totalstock',
                   'totalcost',
                   'totalUSD')




        self.itemsGridview = ttb.Treeview(self.thirth_page,
                                columns=columns,
                                show='headings',
                                bootstyle='dark',
                                height=7,
                                padding=2,
                                yscrollcommand=yscroll.set,
                                xscrollcommand=xscroll.set)
        self.itemsGridview.grid(row=1,column=0,padx=2,pady=(2,2),sticky='nsew')




        yscroll.config(command=self.itemsGridview.yview)
        xscroll.config(command=self.itemsGridview.xview)

        self.itemsGridview.heading(columns[0],text='Codigo')
        self.itemsGridview.heading(columns[1], text='Descripción')
        self.itemsGridview.heading(columns[2],text='Impuesto')
        self.itemsGridview.heading(columns[3],text='Moneda')
        self.itemsGridview.heading(columns[4], text='Unid.')
        self.itemsGridview.heading(columns[5], text='Costo')
        self.itemsGridview.heading(columns[6],text='Precio 1')
        self.itemsGridview.heading(columns[7], text='Precio 2')
        self.itemsGridview.heading(columns[8],text='Precio 3')
        self.itemsGridview.heading(columns[9], text='% Ganancia 1')
        self.itemsGridview.heading(columns[10], text='% Ganancia 2')
        self.itemsGridview.heading(columns[11], text='% Ganancia 3')
        self.itemsGridview.heading(columns[12], text='Stock')
        self.itemsGridview.heading(columns[13], text='Deposito 1')
        self.itemsGridview.heading(columns[14], text='Deposito 2')
        self.itemsGridview.heading(columns[15], text='Deposito 3')
        self.itemsGridview.heading(columns[16], text='Deposito 4')
        self.itemsGridview.heading(columns[17], text='Stock Total')
        self.itemsGridview.heading(columns[18], text='Costo Total')
        self.itemsGridview.heading('totalUSD', text='Total USD')


        self.itemsGridview.column(columns[0],width=120,stretch=False,anchor='center')
        self.itemsGridview.column(columns[1],width=300,stretch=False,anchor='w')
        self.itemsGridview.column(columns[2],width=120,stretch=False,anchor='center')
        self.itemsGridview.column(columns[3],width=120,stretch=False,anchor='center')
        self.itemsGridview.column(columns[4],width=120,stretch=False,anchor='center')
        self.itemsGridview.column(columns[5],width=120,stretch=False,anchor='center')
        self.itemsGridview.column(columns[6],width=120,stretch=False,anchor='center')
        self.itemsGridview.column(columns[7],width=120,stretch=False,anchor='center')
        self.itemsGridview.column(columns[8],width=120,stretch=False,anchor='center')
        self.itemsGridview.column(columns[9],width=120,stretch=False,anchor='center')
        self.itemsGridview.column(columns[10],width=120,stretch=False,anchor='center')
        self.itemsGridview.column(columns[11],width=120,stretch=False,anchor='center')
        self.itemsGridview.column(columns[12],width=120,stretch=False,anchor='center')
        self.itemsGridview.column(columns[13],width=120,stretch=False,anchor='center')
        self.itemsGridview.column(columns[14],width=120,stretch=False,anchor='center')
        self.itemsGridview.column(columns[15],width=120,stretch=False,anchor='center')
        self.itemsGridview.column(columns[16],width=120,stretch=False,anchor='center')
        self.itemsGridview.column(columns[17],width=120,stretch=False,anchor='center')
        self.itemsGridview.column(columns[18],width=120,stretch=False,anchor='center')
        self.itemsGridview.column(columns[19],width=120,stretch=False,anchor='center')

        tags_frames = ttb.Frame(self.thirth_page, style='white.TFrame')
        tags_frames.grid(row=5, column=0, sticky='nsew',padx=2,pady=(6,2), columnspan=2)
        tags_frames.anchor('e')
       

        ttb.Label(tags_frames, text='Total', font=(GUI_FONT,11,'bold'), bootstyle='inverse primary', anchor='center', width=16, padding='10 5').grid(row=0, column=4, sticky='nsew', pady=2)


        self.totalEntry = ttb.Entry(tags_frames,
                                     textvariable=self.BAMOUNT, font=(GUI_FONT,10,'bold'), foreground=GUI_COLORS['danger'],
                                     width=30, state='readonly', justify='center'
                                     )
        self.totalEntry.grid(row=0, column=5, sticky='nsew',padx=(2,0), ipady=4, pady=2)
        ttb.Label(tags_frames, textvariable=self.BCURRENCYNAME, font=(GUI_FONT,11,'bold'), bootstyle='danger', anchor='center', width=8, padding='10 5').grid(row=0, column=6, sticky='nsew', pady=2)





    def __secondPage(self):
        self.second_page = tk.Frame(self.product_info_content)
        self.second_page.config(background=FGCOLOR)
        self.second_page.grid(row=0, column=0, sticky='nsew', columnspan=2)
        self.second_page.columnconfigure(0, weight=1)



        titleSection = CTkFrame(self.second_page, fg_color=GUI_COLORS['dark'], corner_radius=4)
        titleSection.grid(row=0, column=0, sticky='nsew',padx=10, pady=(10,5))
        titleSection.columnconfigure(0, weight=1)
        ttb.Label(titleSection, text='Seleccion de Producto', font=(GUI_FONT,12,'bold'),anchor='center', background=GUI_COLORS['dark'], foreground='#fff').grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        product_static_data = ttb.Frame(self.second_page, style='white.TFrame')
        product_static_data.grid(row=1, column=0, sticky='nsew', padx=10, pady=(0,4))
        product_static_data.columnconfigure(4, weight=1)


       
        ttb.Label(product_static_data, text='CODIGO', background='#fff',
                  font=(GUI_FONT,11,'bold'), padding='3 3', anchor='e').grid(row=0, column=0, pady=(0,2), padx=(0,2), sticky='nsew')

        self.code_entry = ttb.Entry(product_static_data, width=25, textvariable=self.__code,validate="key", validatecommand=(self.register(lambda e: on_validate_length(e,lenght=20)), '%P'))
        self.code_entry.grid(row=0, column=1, pady=(0,2), sticky='nsew',padx=(0,2),ipady=4)
        self.code_entry.bind('<Return>', lambda e: self.__check_product_code())


        self.searchProduct = ttb.Button(product_static_data, text='...', bootstyle='dark', command=self.__open_product_selection)
        self.searchProduct.grid(row=0, column=2, pady=(0,2), sticky='nsew',padx=(0,2),ipadx=5)

    

        ttb.Label(product_static_data, text='Descripcion',  background='#fff',
                  font=(GUI_FONT,11,'bold'), padding='3 3', anchor='e').grid(row=0, column=3, pady=2, padx=(8,2), sticky='nsew')
        
        ttb.Entry(product_static_data, textvariable=self.__description,
                 width=60,state='readonly').grid(row=0, column=4, pady=2, padx=2, sticky='nsew',ipady=4)
        
    
        extrainfoFrame = ttb.Frame(product_static_data, style='white.TFrame')
        extrainfoFrame.grid(row=1, column=0, columnspan=5, sticky='nsew', pady=(4,0))

        ttb.Label(extrainfoFrame, text='Medida',  background='#fff',
                  font=(GUI_FONT,11,'bold'), padding='3 3', anchor='w').grid(row=0, column=0, pady=2, padx=(8,2), sticky='nsew')
        
        ttb.Entry(extrainfoFrame, textvariable=self.oldmeasurementName,
                 width=20,state='readonly').grid(row=1, column=0, pady=2, padx=2, sticky='nsew',ipady=4)
        

        ttb.Label(extrainfoFrame, text='Cant.',  background='#fff', 
                  font=(GUI_FONT,11,'bold'), padding='3 3', anchor='w').grid(row=0, column=1, pady=2, padx=(8,2), sticky='nsew')
        
        ttb.Entry(extrainfoFrame, textvariable=self.oldstock,
                 width=20,state='readonly').grid(row=1, column=1, pady=2, padx=2, sticky='nsew',ipady=4)
        
        ttb.Label(extrainfoFrame, text='Iva para Venta',  background='#fff', 
                  font=(GUI_FONT,11,'bold'), padding='3 3', anchor='w').grid(row=0, column=2, pady=2, padx=(8,2), sticky='nsew')
        
        ttb.Entry(extrainfoFrame, textvariable=self.oldtax,
                 width=20,state='readonly').grid(row=1, column=2, pady=2, padx=2, sticky='nsew',ipady=4)
        


        titleSection = CTkFrame(self.second_page, fg_color=GUI_COLORS['dark'], corner_radius=4)
        titleSection.grid(row=2, column=0, sticky='nsew',padx=10, pady=(10,5))
        titleSection.columnconfigure(0, weight=1)
        ttb.Label(titleSection, text='Calculo de Costos', font=(GUI_FONT,12,'bold'),anchor='center', background=GUI_COLORS['dark'], foreground='#fff').grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        costDataFrame = ttb.Frame(self.second_page, style='white.TFrame')
        costDataFrame.grid(row=3, column=0, sticky='nsew', padx=10, pady=(0,4))


        cost_frame = tk.Frame(costDataFrame,)
        cost_frame.config(background=FGCOLOR)
        cost_frame.grid(row=0, column=0,  pady=(4,0), sticky='nsew')


        cost_label = ttb.Label(cost_frame, 
                               anchor='w', 
                               text='Costo Factura', 
                               background=FGCOLOR, 
                               font=('arial',11,'bold'))
        cost_label.grid(row=0, column=0, padx=(4,0), pady=(2,0), ipadx=8, sticky='nsew')

        self.costEntry = ttb.Entry(cost_frame,
                                    width=20,
                                    validate="key",validatecommand=(self.register(validateFloat), "%P"),
                                    textvariable=self.__cost,)
        self.costEntry.grid(row=1,column=0, padx=(4,0), sticky='nsew', ipady=4,)

        costexchangeFrame = CTkFrame(cost_frame, fg_color=GUI_COLORS['light'], corner_radius=3)
        costexchangeFrame.grid(row=2, column=0, padx=(4,0), pady=(2,0), sticky='nsew')
        costexchangeFrame.anchor('e')


        ttb.Label(costexchangeFrame, text='Costo Anterior', font=(GUI_FONT,8,'bold'), background=GUI_COLORS['light'], foreground=GUI_COLORS['dark'], anchor='e').grid(row=0, column=0, padx=6,pady=(2,0), sticky='e')
        ttb.Label(costexchangeFrame, textvariable=self.oldcost, anchor='e', width=12, font=(GUI_FONT,8), background=GUI_COLORS['light'], foreground=GUI_COLORS['dark']).grid(row=1, column=0, padx=6,pady=(0,2),sticky='e')
       

        costexchangeFrame = CTkFrame(cost_frame, fg_color=GUI_COLORS['light'], corner_radius=3)
        costexchangeFrame.grid(row=1, column=1, rowspan=2, padx=(4,0), pady=(0,0), sticky='nsew')
        costexchangeFrame.anchor('center')

        ttb.Label(costexchangeFrame,textvariable=self.__currencyName, width=6, font=(GUI_FONT,11,'bold'), background=GUI_COLORS['light'], foreground=GUI_COLORS['dark'], anchor='center').grid(row=0, column=0, padx=2,pady=2, sticky='nsew')

        
        cost_label = ttb.Label(cost_frame, 
                               anchor='w', 
                               text='Costo en Factura al Cambio', 
                               background=FGCOLOR, 
                               font=('arial',11,'bold'))
        cost_label.grid(row=0, column=2, padx=(12,0), pady=(2,0), ipadx=8, sticky='nsew')

        self.costexchangeEntry = ttb.Entry(cost_frame,
                                    width=20, textvariable=self.__cost_exchange
                                    )
        self.costexchangeEntry.grid(row=1,column=2, padx=(12,0),pady=(2,0), sticky='nsew', ipady=4,)
        self.costexchangeEntry.config(state='readonly')

        self.costBeforeEntry = ttb.Entry(cost_frame,
                                    width=20,textvariable=self.oldcostexchange
                                    )
        self.costBeforeEntry.grid(row=2,column=2, padx=(12,0),pady=(2,0), sticky='nsew', ipady=4,)
      
        self.costBeforeEntry.config(state='readonly')

        costexchangeFrame = CTkFrame(cost_frame, fg_color=GUI_COLORS['light'], corner_radius=3)
        costexchangeFrame.grid(row=1, column=3, rowspan=2, padx=(4,0), pady=(0,0), sticky='nsew')
        costexchangeFrame.anchor('center')

        ttb.Label(costexchangeFrame, text='Bs.', width=6, font=(GUI_FONT,11,'bold'), background=GUI_COLORS['light'], foreground=GUI_COLORS['dark'], anchor='center').grid(row=0, column=0, padx=2,pady=2, sticky='nsew')




        TAX =  DB.getTaxList()
        self.TAX_DICT = {row[1]:row[0] for row in TAX}
        TAX_DICT_VALUE = {row[0]:row[2] for row in TAX}
        del TAX


        def set_tax_value(var,index,mode):
            value = TAX_DICT_VALUE[self.__tax.get()]
            self.__taxValue.set(value)
            self.__cost_calculation()

        self.taxCombobox = ttb.Combobox(cost_frame, values=list(self.TAX_DICT.keys()), state='readonly', style='selectionOnly.TCombobox', textvariable=self.__taxName)
                      
        self.taxCombobox.grid(row=1, column=5, padx=(2,0), sticky='nsew')
        self.taxCombobox.bind("<<ComboboxSelected>>", lambda e: on_combobox_change(e,self.__tax, self.TAX_DICT,self.taxCombobox))
        self.taxCombobox.current(0)
        self.__tax.trace_add('write', set_tax_value)
        self.__tax.set(1)

        
        self.CURRENCY_DICT = {row[1]:row[0] for row in DB.getCurrencyList()}


            ########### Measurement Section ###########
        MEASUREMENT =  DB.getMeasurementList()
        self.MEASUREMENT_DICT = {row[1]:row[0] for row in MEASUREMENT}
        del MEASUREMENT

            ########### Measurement Section ###########
        measurement_label = ttb.Label(cost_frame, 
                                      anchor='w', 
                                      text='Unidad Medida', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        measurement_label.grid(row=2, column=4, padx=(12,0), pady=(2,0), ipadx=8, ipady=4,  sticky='nsew')

        self.measurementCombobox = ttk.Combobox(cost_frame, values=list(self.MEASUREMENT_DICT.keys()), state='readonly', style='selectionOnly.TCombobox', textvariable=self.__measurementName)
        self.measurementCombobox.grid(row=2, column=5, padx=(2,0), pady=(2,0), sticky='nsew')
        self.measurementCombobox.bind("<<ComboboxSelected>>", lambda e: on_combobox_change(e,self.__measurement, self.MEASUREMENT_DICT, self.measurementCombobox))
        self.measurementCombobox.current(0)







        titleSection = CTkFrame(self.second_page, fg_color=GUI_COLORS['dark'], corner_radius=4)
        titleSection.grid(row=4, column=0, sticky='nsew',padx=10, pady=(10,5))
        titleSection.columnconfigure(0, weight=1)
        ttb.Label(titleSection, text='Calculos de Precio', font=(GUI_FONT,12,'bold'),anchor='center', background=GUI_COLORS['dark'], foreground='#fff').grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        pricing_section_frame = tk.Frame(self.second_page,)
        pricing_section_frame.config(background=FGCOLOR)
        pricing_section_frame.grid(row=5, column=0, sticky='nsw', padx=10, pady=(0,4))
        pricing_section_frame.columnconfigure(0, weight=1)

        price_section_title = ttb.Label(pricing_section_frame, 
                                text='Precios de Venta', 
                                bootstyle='dark', 
                                background=FGCOLOR,
                                anchor='w',
                                font=('arial',11,'bold'))
        price_section_title.grid(row=0, column=0, padx=4, pady=0, ipadx=2, ipady=2, sticky='nsew')

        price_section_title = ttb.Label(pricing_section_frame, 
                                text='% Ganancia', 
                                bootstyle='dark', 
                                background=FGCOLOR,
                                anchor='w',
                                font=('arial',11,'bold'))
        price_section_title.grid(row=0, column=1, padx=(4,4), pady=0, ipadx=2, ipady=2, sticky='nsew')
        ttb.Separator(pricing_section_frame, bootstyle='dark').grid(row=1, column=0, padx=4, pady=4, sticky='nsew',columnspan=2)

        priceFrame = tk.Frame(pricing_section_frame)
        priceFrame.config(background=FGCOLOR)
        priceFrame.grid(row=2, column=0, padx=4, sticky='nsew', columnspan=2)        

        ttb.Label(priceFrame, 
            anchor='w', 
            text='Precio 1 (PVP)', 
            background='white',
            font=('arial',11,'bold')
        ).grid(row=0, column=0, padx=0, pady=(0,4), ipadx=8, sticky='nsew')


        self.priceEntry1 = ttb.Entry(priceFrame,
                                validate="key",validatecommand=(self.register(validateFloat), "%P"), width=14, 
                                textvariable=self.__price1)
        self.priceEntry1.grid(row=0,column=1, sticky='nsew',pady=(0,4), ipady=4,)

        
        
        fp_currency = CTkFrame(priceFrame, fg_color='#767171', corner_radius=2)
        fp_currency.grid(row=0,column=2, padx=(4,0), sticky='nsew',pady=(0,3))
        fp_currency.rowconfigure(0, weight=1)
        fp_currency.columnconfigure(0, weight=1)

        ttb.Label(fp_currency,
                width=6, 
                textvariable=self.__currencyName,
                anchor='center',
                foreground='white',
                font=('arial',11,'bold'),
                background='#767171'
        ).grid(padx=2, pady=2, sticky='nsew')



        exchangeFirstPrice = CTkFrame(priceFrame, fg_color=GUI_COLORS['light'], corner_radius=2)
        exchangeFirstPrice.grid(row=0,column=3, padx=(4,0), sticky='nsew',pady=(0,3))
        exchangeFirstPrice.anchor('e')

        self.exchange_fp = ttb.Label(exchangeFirstPrice, 
                                width=16, 
                                anchor='e', 
                                textvariable=self.__price1_exchange,
                                bootstyle='light inverse', 
                                font=('arial',11,'bold'))
        self.exchange_fp.grid(row=1, column=3, padx=(2,2), ipadx=8, sticky='nsew',pady=(2,2))

        exchange_fp_c = ttb.Label(exchangeFirstPrice,
                                  width=6, 
                                  text='Bs.',
                                  anchor='center', 
                                  bootstyle='light inverse',)
        exchange_fp_c.grid(row=1,column=4, sticky='nsew',pady=(2,2), padx=(0,2))

        self.profitEntry1 = ttb.Entry(priceFrame,
                              width=12, state='readonly',validate="key",validatecommand=(self.register(validateFloat), "%P"),
                              textvariable=self.__profit1,
                             )
        self.profitEntry1.grid(row=0,column=5, sticky='nsew',pady=(0,4), ipady=4, padx=(4,0))


        ####################################

        ttb.Label(priceFrame, 
                                     anchor='w', 
                                     text='Precio 2 (PVP)', 
                                     background='white',
                                     font=('arial',11,'bold')
        ).grid(row=1, column=0, padx=(0,0), pady=(0,4), ipadx=8, sticky='nsew')


        self.priceEntry2 = ttb.Entry(priceFrame,
                                      width=12,
                                    validate="key",validatecommand=(self.register(validateFloat), "%P"),
                                      textvariable=self.__price2,
                                 )
        self.priceEntry2.grid(row=1,column=1, sticky='nsew',pady=(0,4), ipady=4,)

        
        sp_currency = CTkFrame(priceFrame, fg_color='#767171', corner_radius=2)
        sp_currency.grid(row=1,column=2, padx=(4,0), sticky='nsew',pady=(0,3))
        sp_currency.rowconfigure(0, weight=1)
        sp_currency.columnconfigure(0, weight=1)

        ttb.Label(sp_currency,
                width=6, 
                textvariable=self.__currencyName,
                anchor='center',
                foreground='white',
                font=('arial',11,'bold'),
                background='#767171'
        ).grid(padx=2, pady=2, sticky='nsew')



        exchangeSecondPriceFrame = CTkFrame(priceFrame, fg_color=GUI_COLORS['light'], corner_radius=2)
        exchangeSecondPriceFrame.grid(row=1,column=3, padx=(4,0), sticky='nsew',pady=(0,3))
        exchangeSecondPriceFrame.anchor('e')

        self.exchange_sp = ttb.Label(exchangeSecondPriceFrame, 
                                width=16, 
                                anchor='e', 
                                textvariable=self.__price2_exchange,
                                bootstyle='light inverse', 
                                font=('arial',11,'bold'))
        self.exchange_sp.grid(row=0, column=0, padx=(2,2), ipadx=8, sticky='nsew',pady=(2,2))

        exchange_sp_c = ttb.Label(exchangeSecondPriceFrame,
                                  width=6, 
                                  text='Bs.',
                                  anchor='center', 
                                  bootstyle='light inverse',)
        exchange_sp_c.grid(row=0,column=1, sticky='nsew',pady=(2,2), padx=(0,2))

        self.profitEntry2 = ttb.Entry(priceFrame,
                              width=12, state='readonly',validate="key",validatecommand=(self.register(validateFloat), "%P"),
                              textvariable=self.__profit2
                             )
        self.profitEntry2.grid(row=1,column=5, sticky='nsew',pady=(0,4), ipady=4, padx=(4,0))



        ####################################

        ttb.Label(priceFrame, 
                                     anchor='w', 
                                     text='Precio 3 (PVP)', 
                                     background='white',
                                     font=('arial',11,'bold')
        ).grid(row=2, column=0, padx=(0,0), pady=(0,4), ipadx=8, sticky='nsew')


        self.priceEntry3 = ttb.Entry(priceFrame,
                                      width=14, 
                                    validate="key",validatecommand=(self.register(validateFloat), "%P"),
                                      textvariable=self.__price3,
                                 )
        self.priceEntry3.grid(row=2,column=1, sticky='nsew',pady=(0,4), ipady=4,)

        
        tp_currency = CTkFrame(priceFrame, fg_color='#767171', corner_radius=2)
        tp_currency.grid(row=2,column=2, padx=(4,0), sticky='nsew',pady=(0,3))
        tp_currency.rowconfigure(0, weight=1)
        tp_currency.columnconfigure(0, weight=1)

        ttb.Label(tp_currency,
                width=6, 
                textvariable=self.__currencyName,
                anchor='center',
                foreground='white',
                font=('arial',11,'bold'),
                background='#767171'
        ).grid(padx=2, pady=2, sticky='nsew')



        exchangeThirthPriceFrame = CTkFrame(priceFrame, fg_color=GUI_COLORS['light'], corner_radius=2)
        exchangeThirthPriceFrame.grid(row=2,column=3, padx=(4,0), sticky='nsew',pady=(0,3))
        exchangeThirthPriceFrame.anchor('e')

        self.exchange_tp = ttb.Label(exchangeThirthPriceFrame, 
                                width=16, 
                                anchor='e', 
                                textvariable=self.__price3_exchange,
                                bootstyle='light inverse', 
                                font=('arial',11,'bold'))
        self.exchange_tp.grid(row=0, column=0, padx=(2,2), ipadx=8, sticky='nsew',pady=(2,2))

        exchange_tp_c = ttb.Label(exchangeThirthPriceFrame,
                                  width=6, 
                                  text='Bs.',
                                  anchor='center', 
                                  bootstyle='light inverse',)
        exchange_tp_c.grid(row=0,column=1, sticky='nsew',pady=(2,2), padx=(0,2))

        self.profitEntry3 = ttb.Entry(priceFrame,
                              width=12, state='readonly',  validate="key",validatecommand=(self.register(validateFloat), "%P"),
                              textvariable=self.__profit3,
                             )
        self.profitEntry3.grid(row=2,column=5, sticky='nsew',pady=(0,4), ipady=4, padx=(4,0))



        
        titleSection = CTkFrame(self.second_page, fg_color=GUI_COLORS['dark'], corner_radius=4)
        titleSection.grid(row=6, column=0, sticky='nsew',padx=10, pady=(5,5))
        titleSection.columnconfigure(0, weight=1)
        ttb.Label(titleSection, text='Inventario', font=(GUI_FONT,12,'bold'),anchor='center', background=GUI_COLORS['dark'], foreground='#fff').grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        ttb.Label(titleSection, text='Sección de Inventario', font=(GUI_FONT,11,'bold'), bootstyle='dark inverse').grid(row=0, column=0, padx=4, pady=2)


        
        inventory_section_frame = tk.Frame(self.second_page,)
        inventory_section_frame.config(background=FGCOLOR)
        inventory_section_frame.grid(row=7, column=0, columnspan=2, pady=(0,0), ipadx=8,  sticky='nsew')
        inventory_section_frame.columnconfigure(1, weight=1)


  
        ttb.Label(inventory_section_frame, 
                                     anchor='center', 
                                     text='Inventario Principal', 
                           
                                     background='#fff',
                                    
                                     font=('arial',11,'bold')
        ).grid(row=0, column=0, padx=(14,4), pady=4, ipadx=4, sticky='nsew')



        self.mainStockEntry = ttb.Entry(inventory_section_frame, 
                                         validatecommand=(self.register(validate_number), "%S"),validate='key',
                                         width=12,
                                         justify='center',
                                         textvariable=self.stock_var,)
        self.mainStockEntry.grid(row=1, column=0, sticky='nsew',pady=(0,4),padx=(14,4), ipady=6)

        depositFrame = tk.Frame(inventory_section_frame)
        depositFrame.config(background=FGCOLOR)
        depositFrame.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=4, pady=4)
        depositFrame.rowconfigure(2, weight=1)
        depositFrame.columnconfigure(1, weight=1)


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
        
        self.depositEntry1 = ttb.Entry(depositEntryFrame, 
                              width=12,
                              justify='center',
                              textvariable=self.stock_1_var,
                              validatecommand=(self.register(validate_number), "%S"),validate='key',
                              )
        self.depositEntry1.grid(row=0, column=1, sticky='nsew',pady=(2,0),padx=(2,6))

        ttb.Label(depositEntryFrame, 
                  anchor='center', 
                  text='D2', 
                  background=FGCOLOR,
                  font=('arial',11,'bold')
        ).grid(row=0, column=2, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        
        self.depositEntry2 = ttb.Entry(depositEntryFrame,  
                              width=12,
                              justify='center',
                              textvariable=self.stock_2_var,
                              validatecommand=(self.register(validate_number), "%S"),validate='key'
                          )
        self.depositEntry2.grid(row=0, column=3, sticky='nsew',pady=(2,0),padx=(2,6))

        ttb.Label(depositEntryFrame, 
                  anchor='center', 
                  text='D3', 
                  background=FGCOLOR,
                  font=('arial',11,'bold')
        ).grid(row=0, column=4, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.depositEntry3 = ttb.Entry(depositEntryFrame,  
                              width=12,
                              justify='center',
                              textvariable=self.stock_3_var,
                              validatecommand=(self.register(validate_number), "%S"),validate='key'
                              )
        self.depositEntry3.grid(row=0, column=5, sticky='nsew',pady=(2,0),padx=(2,6))

        ttb.Label(depositEntryFrame, 
                  anchor='center',
                  text='D4', 
                  background=FGCOLOR,
                  font=('arial',11,'bold')
        ).grid(row=0, column=6, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.depositEntry4 = ttb.Entry(depositEntryFrame,  
                              width=12,
                              justify='center',
                              textvariable=self.stock_4_var,
                              validatecommand=(self.register(validate_number), "%S"),validate='key'
                         )
        self.depositEntry4.grid(row=0, column=7, sticky='nsew',pady=(2,0),padx=(2,6))


        
        if self.window_type == 'create':
            additrmimg = Image.open(f"{IMG_PATH}/add_item.png")
            self.additrmimg = ImageTk.PhotoImage(additrmimg.resize(resize_image(18, additrmimg.size)))
            additrmimgh = Image.open(f"{IMG_PATH}/add_item_h.png")
            self.additrmimgh = ImageTk.PhotoImage(additrmimgh.resize(resize_image(18, additrmimgh.size)))
            additrmimgp = Image.open(f"{IMG_PATH}/add_item_p.png")
            self.additrmimgp = ImageTk.PhotoImage(additrmimgp.resize(resize_image(18, additrmimgp.size)))

            self.ADDBTN = ButtonImage(depositFrame,  command=lambda:self.add_product(), image=self.additrmimg, img_h=self.additrmimgh, img_p=self.additrmimgp, style='flatw.light.TButton', text='     AGREGAR', compound='center',padding=0)
            self.ADDBTN.grid(row=0, column=1, rowspan=3, sticky='nse', pady=3, padx=8,)

        self.ITEMS_FIELDS = [self.code_entry, self.costEntry, self.taxCombobox, self.measurementCombobox, self.priceEntry1,self.priceEntry2, self.priceEntry3, self.profitEntry1, self.profitEntry2, self.profitEntry3,
                             self.mainStockEntry, self.depositEntry1, self.depositEntry2, self.depositEntry3, self.depositEntry4]

    def __firstPage(self):
 
        self.firtsPageFrame = tk.Frame(self.product_info_content)
        self.firtsPageFrame.config(background=FGCOLOR)
        self.firtsPageFrame.grid(row=0, column=0, sticky='nsew', columnspan=2, )
        self.firtsPageFrame.columnconfigure(1, weight=1)


        provider_label = ttb.Label(self.firtsPageFrame, 
                                     anchor='w', 
                                     text='Proveedor', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=(GUI_FONT,11,'bold'))
        provider_label.grid(row=0, column=0, padx=5, pady=(2,0), ipadx=8, ipady=4, sticky='nsew')
        
        provider_frame = tk.Frame(self.firtsPageFrame)
        provider_frame.config(background=FGCOLOR)
        provider_frame.grid(row=1, column=0, sticky='nsew' ,pady=5,padx=(10,10),columnspan=2)
        provider_frame.columnconfigure(3,weight=1)

        provider_frame.anchor('w')
         
        ttb.Label(provider_frame, text='RIF', font=(GUI_FONT,10,'bold'), background='#fff').grid(row=0, column=0)
        

        self.rifProviderEntry = ttb.Entry(provider_frame, 
                                     textvariable=self.BPROVIDER_RIF,
                                     width=20, state='readonly'
                                     )
        self.rifProviderEntry.grid(row=0, column=1, sticky='nsew',padx=5, ipady=4,)

        if self.window_type != 'view':

            self.provider_search_btn = ttb.Button(provider_frame, 
                                        command=self.__open_provider_selection,
                                        text='...',
                                        bootstyle='dark')
            self.provider_search_btn.grid(row=0, column=2, padx=(2), sticky='nsew', pady=1)

        self.nameProviderEntry = ttb.Entry(provider_frame, width=80,state='readonly',
                                        textvariable=self.BPROVIDER_NAME
                                     )
        self.nameProviderEntry.grid(row=0, column=3, sticky='nsew',padx=5, ipady=4,)



        self.moreInfoFrame = tk.Frame(self.firtsPageFrame)
        self.moreInfoFrame.config(background=FGCOLOR)
        self.moreInfoFrame.grid(row=2, column=0, sticky='nsew', columnspan=2)
        self.moreInfoFrame.columnconfigure(0, weight=1)
        self.moreInfoFrame.columnconfigure(1, weight=1)

        vcmd = (self.register(lambda e: on_validate_length(e,lenght=10)), '%P')

        conditionPurchase_label = ttb.Label(self.moreInfoFrame, 
                                     anchor='w', 
                                     text='Condicion', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=(GUI_FONT,11,'bold'))
        conditionPurchase_label.grid(row=0, column=0, padx=5, pady=(4,0), ipadx=8, ipady=4, sticky='nsew')
        
        self.conditionPurchaseEntry = ttb.Combobox(self.moreInfoFrame, state='readonly', style='selectionOnly.TCombobox',
                                                   textvariable=self.BDOCUMENTO_CONDITION, values=['CREDITO', 'CONTADO'])
        self.conditionPurchaseEntry.grid(row=1, column=0, sticky='nsew',pady=(2,0),padx=4, columnspan=1)
      
        

        purchaseCode_label = ttb.Label(self.moreInfoFrame, 
                                     anchor='w', 
                                     text='Factura', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=(GUI_FONT,11,'bold'))
        purchaseCode_label.grid(row=2, column=1, padx=5, pady=(4,0), ipadx=8, ipady=4, sticky='nsew')
        
        self.purchaseCodeEntry = ttb.Entry(self.moreInfoFrame,textvariable=self.BCODE, justify='center', validate="key", validatecommand=vcmd)
        self.purchaseCodeEntry.grid(row=3, column=1, sticky='nsew',pady=(2,0),padx=4, ipady=6,)


        controlCode_label = ttb.Label(self.moreInfoFrame, 
                                     anchor='w', 
                                     text='Control', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=(GUI_FONT,11,'bold'))
        controlCode_label.grid(row=2, column=0, padx=5, pady=(4,0), ipadx=8, ipady=4, sticky='nsew')
        

        self.controlCodeEntry = ttb.Entry(self.moreInfoFrame,textvariable=self.BCONTROL, justify='center', validate="key", validatecommand=vcmd)
        self.controlCodeEntry.grid(row=3, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=6,)

        CURRENCY =  DB.getCurrencyList()
        CURRENCY_DICT = {row[1]:row[0] for row in CURRENCY}

        del CURRENCY

        currency_label = ttb.Label(self.moreInfoFrame, 
                                   anchor='w', 
                                   text='Moneda', 
                                   background=FGCOLOR,
                                   font=(GUI_FONT,11,'bold'))
        currency_label.grid(row=0, column=1, padx=5, pady=(4,0), ipadx=8, sticky='nsew')
     
        

        self.currencyCombobox = ttb.Combobox(self.moreInfoFrame, values=list(CURRENCY_DICT.keys()), state='readonly', style='selectionOnly.TCombobox', textvariable=self.BCURRENCYNAME)
        self.currencyCombobox.grid(row=1, column=1, padx=(4,10), pady=(2,0), sticky='nsew')
        self.currencyCombobox.bind("<<ComboboxSelected>>", lambda e: on_combobox_change(e,self.BCURRENCY, CURRENCY_DICT, self.currencyCombobox))
        self.currencyCombobox.current(1)
        
        self.BCURRENCY.set(2)

    


        ########### SECOND ROW

        creationDate_label = ttb.Label(self.moreInfoFrame, 
                                     anchor='w', 
                                     text='Fecha de Emision', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=(GUI_FONT,11,'bold'))
        creationDate_label.grid(row=4, column=0, padx=5, pady=(4,0), ipadx=8, ipady=4, sticky='nsew')
        
        self.creationDateEntry = ttb.DateEntry(self.moreInfoFrame, startdate=datetime.today(), dateformat='%d/%m/%Y')
        self.creationDateEntry.grid(row=5, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=6,columnspan=1)
        self.creationDateEntry.entry.config(textvariable=self.BDATEOFISSUE)
        self.creationDateEntry.entry.bind('<FocusOut>', lambda e: checkDATE(self.BDATEOFISSUE))

        expirationDate_label = ttb.Label(self.moreInfoFrame, 
                                     anchor='w', 
                                     text='Fecha de Vencimiento', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=(GUI_FONT,11,'bold'))
        expirationDate_label.grid(row=4, column=1, padx=5, pady=(4,0), ipadx=8, ipady=4, sticky='nsew')


        
        
        self.expirationDateEntry = ttb.DateEntry(self.moreInfoFrame, startdate=datetime.today(), dateformat='%d/%m/%Y')
        self.expirationDateEntry.grid(row=5, column=1, sticky='nsew',pady=(2,0),padx=4, ipady=6,)
        self.expirationDateEntry.entry.config(textvariable=self.BEXPIRATIONDATE)
        self.expirationDateEntry.entry.bind('<FocusOut>', lambda e: checkDATE(self.BEXPIRATIONDATE))

        registerDate_label = ttb.Label(self.moreInfoFrame, 
                                     anchor='w', 
                                     text='Fecha de Registro', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=(GUI_FONT,11,'bold'))
        registerDate_label.grid(row=6, column=0, padx=5, pady=(4,0), ipadx=8, ipady=4, sticky='nsew')
        
        self.registerDateEntry = ttb.DateEntry(self.moreInfoFrame,  startdate=datetime.today(), dateformat='%d/%m/%Y')
        self.registerDateEntry.grid(row=7, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=6,)
        self.registerDateEntry.entry.config(textvariable=self.BREGISTERDATE)
        self.registerDateEntry.entry.bind('<FocusOut>', lambda e: checkDATE(self.BREGISTERDATE))

        documentType_label = ttb.Label(self.moreInfoFrame, 
                                      anchor='w', 
                                      text='Tipo de Factura', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=(GUI_FONT,11,'bold'))
        documentType_label.grid(row=6, column=1, padx=5, pady=(4,0), ipadx=8, ipady=4, sticky='nsew')



        BillsType =  DB.getBillTypeList()
        BillsType_DICT = {row[1]:row[0] for row in BillsType}

        del BillsType

        self.documentTypeCombobox = ttb.Combobox(self.moreInfoFrame, state='readonly',textvariable=self.BDOCUMENT_TYPENAME,
                                    style='selectionOnly.TCombobox', values=list(BillsType_DICT.keys()))
        self.documentTypeCombobox.grid(row=7, column=1, sticky='nsew',pady=(2,0),padx=4)
        self.documentTypeCombobox.bind("<<ComboboxSelected>>", lambda e: on_combobox_change(e,self.BDOCUMENT_TYPE, BillsType_DICT, self.documentTypeCombobox))
        self.documentTypeCombobox.current(0)


        if self.window_type != 'create':

            documentStateLabel = ttb.Label(self.moreInfoFrame, 
                                        anchor='w', 
                                        text='Estado', 
                                        bootstyle='primary',
                                        background=FGCOLOR ,
                                        font=(GUI_FONT,11,'bold'))
            documentStateLabel.grid(row=8, column=0, padx=5, pady=(4,0), ipadx=8, ipady=4, sticky='nsew')
            
            self.documentStatEntry = ttb.Entry(self.moreInfoFrame, state='readonly', justify='center', textvariable=self.BSTATE)
            self.documentStatEntry.grid(row=9, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=6,)
           
        

            paymentStatusLabel = ttb.Label(self.moreInfoFrame, 
                                        anchor='w', 
                                        text='Status', 
                                        bootstyle='primary', 
                                        background=FGCOLOR,
                                        font=(GUI_FONT,11,'bold'))
            paymentStatusLabel.grid(row=8, column=1, padx=5, pady=(4,0), ipadx=8, ipady=4, sticky='nsew')



            self.documentStatusEntry = ttb.Entry(self.moreInfoFrame, state='readonly', justify='center',textvariable=self.BSTATUS)
            self.documentStatusEntry.grid(row=9, column=1, sticky='nsew',pady=(2,0),padx=4)

            


        descriptiom_Label = ttb.Label(self.moreInfoFrame, 
                                     anchor='w', 
                                     text='Descripcion (Opcional)', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=(GUI_FONT,11,'bold'))
        descriptiom_Label.grid(row=10, column=0, padx=5, pady=(4,0), ipadx=8, ipady=4, sticky='nsew')
        
        self.descriptionText = ttb.Text(self.moreInfoFrame, height=2, highlightbackground=GUI_COLORS['info'], width=10)
        self.descriptionText.grid(row=11, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=6,columnspan=2)
        self.descriptionText.bind('<KeyPress>', lambda e: limitar_longitud(self.descriptionText, 400))
        self.descriptionText.bind('<KeyRelease>', lambda e: limitar_longitud(self.descriptionText, 400))
        self.descriptionText.bind('Control-v', lambda e: limitar_longitud(self.descriptionText, 400))
        #--------------------------------------------------------------------------------------------
    

        currencyDetailsFrame = ttb.Frame(self.moreInfoFrame, style='white.TFrame')
        currencyDetailsFrame.grid(row=12, column=0, columnspan=2, padx=4, sticky='nsew', pady=(6,0))


        


        if self.window_type != 'create':
            self.amountLabelMain = ttb.Label(currencyDetailsFrame, 
                                        anchor='w', 
                                        text='Monto Factura', 
                                        bootstyle='primary',
                                        background=FGCOLOR ,
                                        font=(GUI_FONT,11,'bold'))
            self.amountLabelMain.grid(row=0, column=0, padx=5, pady=(4,0), ipadx=8, ipady=4, sticky='nsew')
                
            self.amountEntry = ttb.Entry(currencyDetailsFrame,width=20, bootstyle='primary', justify='center', textvariable=self.BAMOUNT,
                                            validate="key",validatecommand=(self.register(validateFloat), "%P"))
            self.amountEntry.grid(row=1, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=10)
            self.amountEntry.bind('<FocusOut>', lambda e: self.__check_amounts_value(self.BAMOUNT))

            amountPaidLabel = ttb.Label(currencyDetailsFrame, 
                                        anchor='w', 
                                        text='Monto Pagado USD $', 
                                        bootstyle='primary',
                                        background=FGCOLOR ,
                                        font=(GUI_FONT,11,'bold'))
            amountPaidLabel.grid(row=0, column=3, padx=5, pady=(4,0), ipadx=8, ipady=4, sticky='nsew')
            self.amountPaidEntry = ttb.Entry(currencyDetailsFrame, justify='center',width=20, textvariable=self.BAMOUNT_PAID)
            self.amountPaidEntry.grid(row=1, column=3, sticky='nsew',pady=(2,0),padx=4, ipady=10)


            debtLabel = ttb.Label(currencyDetailsFrame, 
                                        anchor='w', 
                                        text='Deuda $', 
                                        bootstyle='primary',
                                        background=FGCOLOR ,
                                        font=(GUI_FONT,11,'bold'))
            debtLabel.grid(row=0, column=4, padx=5, pady=(4,0), ipadx=8, ipady=4, sticky='nsew')
            self.debtEntry = ttb.Entry(currencyDetailsFrame, justify='center',width=20,textvariable=self.BAMOUNT_DEBT)
            self.debtEntry.grid(row=1, column=4, sticky='nsew',pady=(2,0),padx=4, ipady=10)


            amountUSDLabel = ttb.Label(currencyDetailsFrame, 
                                     anchor='w', 
                                     text='Total USD $', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=(GUI_FONT,11,'bold'))
            amountUSDLabel.grid(row=0, column=2, padx=5, pady=(4,0), ipadx=8, ipady=4, sticky='nsew')
            self.amountUSDEntry = ttb.Entry(currencyDetailsFrame, justify='center',width=20,textvariable=self.BAMOUNTUSD)
            self.amountUSDEntry.grid(row=1, column=2, sticky='nsew',pady=(2,0),padx=4, ipady=10)


        self.exchangerate_label = ttb.Label(currencyDetailsFrame, 
                                     anchor='w', 
                                     text='Tasa de Cambio', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=(GUI_FONT,11,'bold'))
        self.exchangerate_label.grid(row=0, column=1, padx=5, pady=(4,0), ipadx=8, ipady=4, sticky='nsew')
        
        self.exchangerateEntry = ttb.Entry(currencyDetailsFrame,width=15, justify='center', textvariable=self.BEXCHANGERATE,
                                           validate="key",validatecommand=(self.register(validateFloat), "%P"))
        self.exchangerateEntry.grid(row=1, column=1, sticky='nsew',pady=(2,0),padx=(4,30), ipady=10,)
        self.exchangerateEntry.bind('<FocusOut>', lambda e: self.__check_amounts_value(self.BEXCHANGERATE))


        self.amountLabelMain = ttb.Label(currencyDetailsFrame, 
                                        anchor='w', 
                                        text='Monto Factura', 
                                        bootstyle='primary',
                                        background=FGCOLOR ,
                                        font=(GUI_FONT,11,'bold'))
        
            
        self.amountEntry = ttb.Entry(currencyDetailsFrame,width=20, bootstyle='primary', justify='center', textvariable=self.BAMOUNT,
                                        validate="key",validatecommand=(self.register(validateFloat), "%P"))

        self.amountEntry.bind('<FocusOut>', lambda e: self.__check_amounts_value(self.BAMOUNT))



        
        
        self.conditionPurchaseEntry.current(1)
        #self.BDOCUMENTO_CONDITION.set(self.conditionPurchaseEntry.get())
        
        self.PURCHASE_FIELDS = {
            'code': self.BCODE,
            'provider': self.BPROVIDER_RIF,
            'control': self.BCONTROL,
            'documentCondition': self.BDOCUMENTO_CONDITION,
            'currency': self.BCURRENCY,
            'dateOfIssue': self.BDATEOFISSUE,
            'expirationDate': self.BEXPIRATIONDATE,
            'registrationDate': self.BREGISTERDATE,
            'total': self.BAMOUNT,
            'totalUSD': self.BAMOUNTUSD,
            'debtUSD':self.BDEBT,
            'totalPaidUSD': self.BTOTALPAID,
            'exchangeRate': self.BEXCHANGERATE,
            'purchaseType': self.BDOCUMENT_TYPE,
            'documentState': self.BDOCUMENTSTATE
        }
        
        if self.window_type == 'view':
            self.creationDateEntry.button.config(state='disabled')
            self.expirationDateEntry.button.config(state='disabled')
            self.registerDateEntry.button.config(state='disabled')

    
    def __open_provider_selection(self):
        select_window = ProviderModule( callback = self.__set_provider_info, selectionMode=True)
        self.wait_window(select_window)
        self.grab_set()
        self.transient()


    def __open_product_selection(self):
        select_window = ProductSelection(callback = self.set_product, selectionMode=True)
        self.wait_window(select_window)
        self.grab_set()
        self.transient()


    def __set_provider_info(self, provider):
        self.BPROVIDER_RIF.set(provider.rif)
        self.BPROVIDER_NAME.set(provider.name)
        self.BPROVIDER_ID.set(provider.id)
        del provider

    
    def sameDateCallback(self):
        if self.BDOCUMENTO_CONDITION.get() == 'CONTADO':
            self.BEXPIRATIONDATE.set(self.BDATEOFISSUE.get())


    def checkDocumentCondition(self):
        if self.window_type == 'create':
            STATE = 'disabled'
            self.BDOCUMENTSTATE.set(3)
            if self.BDOCUMENTO_CONDITION.get() == 'CREDITO':
                STATE = 'normal'
                self.BDOCUMENTSTATE.set(1)

            self.expirationDateEntry.entry.config(state=STATE)
            self.expirationDateEntry.button.config(state=STATE)
            


    def formatData(self):
        DATA = {key:value.get() for key, value in self.PURCHASE_FIELDS.items()}
        DATA['exchangeRate'] = float(DATA['exchangeRate'])
        DATA['total'] = float(DATA['total'])
        DATA['dateOfIssue'] = datetime.strptime(DATA['dateOfIssue'], '%d/%m/%Y')
        DATA['expirationDate'] = datetime.strptime(DATA['expirationDate'], '%d/%m/%Y')
        DATA['registrationDate'] = datetime.strptime(DATA['registrationDate'], '%d/%m/%Y')
        DATA['description'] = self.descriptionText.get('1.0', ttb.END).replace('\n','')
        return DATA

    def check_data_compra(self):
        if self.window_type != 'view':
            if not self.__check_fields():
                messagebox.showwarning('Aviso','Existen algunos campos invalidos.', parent=self)
            elif int(self.BCURRENCY.get())!=1 and float(self.BEXCHANGERATE.get()) == 0:
                messagebox.showwarning('Aviso','La tasa de cambio debe ser mayor a 0.', parent=self)

            elif self.__check_fields() and float(self.BAMOUNT.get())>=0:
                ask = messagebox.askquestion('Compra',f"""Datos de la Factura Correctos?\n
    Codigo: {self.BCODE.get()}
    Moneda: {self.BCURRENCYNAME.get()}
    Tasa de Cambio: {self.BEXCHANGERATE.get()}
    Proveedor: {self.BPROVIDER_NAME.get()}
    Condición: {self.BDOCUMENTO_CONDITION.get()}""", parent=self)
                if ask =='yes':
                    if self.maxpage > 1:
                        self.__next_page()
                        self.createBTN.config(command=self.__next_page)
                    else:
                        self.create_purchases()
                    
        else:
            if self.maxpage > 1:
                self.__next_page()
            else:
                self.create_purchases()
                    
   


    def calculate_usd_amount(self):
        if self.BAMOUNT.get() and self.BEXCHANGERATE.get():
            if self.BCURRENCY.get() == 2:
                self.BAMOUNTUSD.set(self.BAMOUNT.get())
            elif self.BCURRENCY.get() == 1:
                self.BAMOUNTUSD.set(round(float(self.BAMOUNT.get())*(1/float(self.BEXCHANGERATE.get()))/(1/DB.getCurrencyValues(1)),2))
               
            # elif self.BCURRENCY.get() == 3:
            #     self.BAMOUNTUSD.set(round(float(self.BAMOUNT.get())*(1/DB.getCurrencyValues(2))/(1/float(self.BEXCHANGERATE.get())),2))

            

    def check_exchangerate(self):
        if int(self.BCURRENCY.get()) in [1,2]:
            self.BEXCHANGERATE.set(DB.getCurrencyValues(2))
        else:
            self.BEXCHANGERATE.set(DB.getCurrencyValues(3))

    def clean_data(self):
        self.__code.set('')
        self.__description.set('')
        
        self.__currency.set(2)
        self.__currencyName.set('USD $')

        
        self.__currencyValue.set(self.BEXCHANGERATE.get())
        self.__measurement.set(1)
        self.measurementCombobox.current(0)
        self.oldmeasurementName.set('')

        self.__cost.set('0.00')
        self.__cost_exchange.set('0.00')
        self.oldcost.set('0.00')
        self.oldcostexchange.set('0.00')
       
        self.__directCost.set(0)
        self.__indirectCost.set(0)
        self.__tax.set(1)
        self.taxCombobox.current(0)
        self.oldtax.set('')


   
        self.__price1.set(0)
        self.__price2.set(0)
        self.__price3.set(0)
        self.__profit1.set(0)
        self.__profit2.set(0)
        self.__profit3.set(0)
        self.stock_var.set(0)
        self.oldstock.set('')
        self.stock_1_var.set(0)
        self.stock_2_var.set(0)
        self.stock_3_var.set(0)
        self.stock_4_var.set(0)

    def set_product(self, product: Product):
        self.__PRODUCT = product

        self.__code.set(product.code)
        self.__description.set(product.description)
       
        self.__currency.set(product.currency)
        self.__currencyName.set(product.get_currency())

        
        self.__currencyValue.set(float(self.BEXCHANGERATE.get()) if product.currency == 2 else 0)
        self.__measurement.set(product.measurement)
        self.__measurementName.set(product.get_measurement())
        self.oldmeasurementName.set(product.get_measurement())

        self.__cost.set(0)
        self.__cost_exchange.set(0)
        self.oldcost.set(product.cost)
        exchange = float(self.__currencyValue.get())
        self.oldcostexchange.set(product.cost * (exchange if exchange>0 else 1))
       
        self.__directCost.set(product.directcost)
        self.__indirectCost.set(product.indirectcost)
        self.__tax.set(product.tax)
        self.__taxName.set(product.get_tax())
        self.oldtax.set(product.get_tax())
       
      
        self.__price1.set(product.price_1)
        self.__price2.set(product.price_2)
        self.__price3.set(product.price_3)

        self.__profit1.set(product.profit_1)
        self.__profit2.set(product.profit_2)
        self.__profit3.set(product.profit_3)

        self.stock_var.set(0)
        self.oldstock.set(product.stock)

        self.stocka_var.set(0)
        self.stock_1_var.set(0)
        self.stock_2_var.set(0)
        self.stock_3_var.set(0)
        self.stock_4_var.set(0)

    def get_item_list(self):
        items = []
        all_items = self.itemsGridview.get_children()

        for item_id in all_items:
            values = list(self.itemsGridview.item(item_id, 'values'))
            values[2] = self.TAX_DICT[values[2]]
            values[3] = self.CURRENCY_DICT[values[3]]
            values[4] = self.MEASUREMENT_DICT[values[4]]
            values.insert(0,self.BCODE.get())
  
            items.append(values)
        return items
    def __check_amounts_value(self, var):
        if not var.get():
            var.set(0)
    
    def create_purchases(self):
        ask = messagebox.askquestion('Crear','Crear nuevo registro de Compra?', parent=self)
        if ask == 'yes':
            DATA = self.formatData()
            newPurchase = PurchaseDocument(**DATA)
            items = self.get_item_list()
    
            newPurchase.create(items)
            self.result = False

            if self.BDOCUMENTO_CONDITION.get() == 'CONTADO':
                def set_result():
                    self.result = True
                messagebox.showinfo('Aviso','Registrar Pago para culminar con el proceso.', parent=self)
                window = PaymentForm(self,doc=newPurchase, callback=set_result, full_payment_required=True)
                self.wait_window(window)
                self.grab_set()
            else: 
                self.result = True
         
            if self.result == True:
                messagebox.showinfo('Aviso','Registro creado satisfactoriamente.', parent=self)
                self.destroy()
            else:
                newPurchase.delete()

    def add_product(self):
        if self.__code.get():
            total_stock = int(self.stock_var.get()) + int(self.stock_1_var.get()) + int(self.stock_2_var.get()) + int(self.stock_3_var.get()) + int(self.stock_4_var.get())

            total_cost = total_stock*float(self.__cost.get())
            if self.__currency.get() == 1:
                exp = -1
            else:
                exp = 1

            total_cost_main = total_cost if self.__currency.get() == self.BCURRENCY.get() else round(total_cost*(float(self.BEXCHANGERATE.get()))**(exp),2)


            if total_stock<=0:
                messagebox.showinfo('Stock','No se ha especificado las cantidades a agregar del producto.',parent=self)
            else:
                if not self.__PRODUCT.code in self.itemsGridview.get_children():
                    ask = messagebox.askquestion('Registrar',' Desea agregar el producto al listado?', parent=self)
                    if ask =='yes':
                
                        self.itemsGridview.insert("",
                                ttb.END,
                                id=self.__PRODUCT.code,
                                values=(
                                self.__PRODUCT.code,#0
                                self.__description.get(),#1
                                self.__taxName.get(),#2
                                self.__currencyName.get(),#3
                                self.__measurementName.get(),#4
                                self.__cost.get(),
                                self.__price1.get(),
                                self.__price2.get(),
                                self.__price3.get(),
                                self.__profit1.get(),
                                self.__profit2.get(),
                                self.__profit3.get(),
                                self.stock_var.get(),#12
                                self.stock_1_var.get(),
                                self.stock_2_var.get(),
                                self.stock_3_var.get(),
                                self.stock_4_var.get(),#16
                                total_stock,
                                total_cost,
                                total_cost_main
                                ))
                else:
                        ask = messagebox.askquestion('Registro','El producto seleccionado ya se encuentra en el listado.\nDesea actualizar las caracteristicas y adicionar las cantidades del producto?',parent=self)
                        if ask == 'yes':
                            item = self.itemsGridview.item(self.__PRODUCT.code,'values')
                            self.itemsGridview.item(self.__PRODUCT.code, values=(
                                    self.__PRODUCT.code,#0
                                    self.__description.get(),#1
                                    self.__taxName.get(),#2
                                    self.__currencyName.get(),#3
                                    self.__measurementName.get(),#4
                                    self.__cost.get(),
                                    self.__price1.get(),
                                    self.__price2.get(),
                                    self.__price3.get(),
                                    self.__profit1.get(),
                                    self.__profit2.get(),
                                    self.__profit3.get(),
                                    int(self.stock_var.get())+int(item[12]),#12
                                    int(self.stock_1_var.get())+int(item[13]),#
                                    int(self.stock_2_var.get())+int(item[14]),#
                                    int(self.stock_3_var.get())+int(item[15]),#
                                    int(self.stock_4_var.get())+int(item[16]),#
                                    int(total_stock)+int(item[17]),
                                    float(total_cost)+float(item[18]),
                                    float(total_cost_main)+float(item[19])
                                    ))
                self.clean_data()
                self.__update_balance()
            
    def set_purchase_info(self):
        
        self.BPROVIDER_RIF.set(self.__DOCUMENT.provider)
        self.BPROVIDER_NAME.set(self.__DOCUMENT.get_company())
        self.BCODE.set(self.__DOCUMENT.code)
        self.BCONTROL.set(self.__DOCUMENT.control)
        self.BDOCUMENTO_CONDITION.set(self.__DOCUMENT.documentCondition)
        self.BCURRENCY.set(self.__DOCUMENT.currency)

        self.BCURRENCYNAME.set(self.__DOCUMENT.get_currency())

        self.BDATEOFISSUE.set(self.__DOCUMENT.dateOfIssue.strftime('%d/%m/%Y'))
        self.BEXPIRATIONDATE.set(self.__DOCUMENT.expirationDate.strftime('%d/%m/%Y'))
        self.BREGISTERDATE.set(self.__DOCUMENT.registrationDate.strftime('%d/%m/%Y'))
        self.BDOCUMENT_TYPE.set(self.__DOCUMENT.purchaseType)
        self.BDOCUMENT_TYPENAME.set(self.__DOCUMENT.get_purchaseType())
        self.BSTATE.set(self.__DOCUMENT.get_documentState())
        self.BSTATUS.set(self.__DOCUMENT.get_documentStatus())
        self.BAMOUNT.set(float(self.__DOCUMENT.total))
        self.BAMOUNT_PAID.set(float(self.__DOCUMENT.totalPaidUSD))
        self.BAMOUNT_DEBT.set(float(self.__DOCUMENT.debtUSD))
        self.BEXCHANGERATE.set(float(self.__DOCUMENT.exchangeRate))
        self.BAMOUNTUSD.set(float(self.__DOCUMENT.totalUSD))

        self.descriptionText.insert('1.0', self.__DOCUMENT.description)
        self.descriptionText.config(state='disabled')

        self.set_items()


    def set_items(self):
        for item in self.__DOCUMENT.findItems():
            self.itemsGridview.insert("",
                            ttb.END,
                            values=(
                            item[1],#0
                            item[2],#1
                            item[3],#2
                            item[4],#3
                            item[5],#4
                            item[6],
                            item[7],
                            item[8],
                            item[9],
                            item[10],
                            item[11],
                            item[12],
                            item[13],
                            item[14],
                            item[15],
                            item[16],
                            item[17],
                            item[18],
                            item[19],
                            item[20]
                            ))
            
            self.__update_balance()


    def set_debt_amount(self):
        if self.BDOCUMENTO_CONDITION.get() == 'CREDITO':
            self.BDEBT.set(self.BAMOUNTUSD.get())
            self.BTOTALPAID.set(0)
        else:
            self.BDEBT.set(0)
            self.BTOTALPAID.set(self.BAMOUNTUSD.get())
     
        
    def __set_form_state(self, content, state = 'normal'):
       
        for field in content.winfo_children():
            if field.winfo_class() == 'TEntry':
                field.config(state=state, cursor='xterm')
            elif field.winfo_class() in ['TCombobox','TButton']:
                newstate = state
                if state == 'readonly':
                    newstate='disabled'
                field.config(state=newstate, cursor='xterm')
            elif field.winfo_class() == 'TFrame':
                self.__set_form_state(field, state)


    
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

        self.__calculate_percentage(price_var=self.__price1, profit_var=self.__profit1)
        self.__calculate_percentage(price_var=self.__price2, profit_var=self.__profit2)
        self.__calculate_percentage(price_var=self.__price3, profit_var=self.__profit3)


    def __calculate_percentage(self, price_var = None, profit_var = None,):
        cost = self.__totalCost.get()
      
        if self.prices_focus.get():
            price = price_var.get()
            if price and cost and float(cost) > 0 :
                profit_var.set(round((float(price) - float(cost)) / float(cost) * 100, 2))
            else:
                profit_var.set('')
        else:
            profit = profit_var.get()
            if profit and cost and float(cost) > 0 :
                price_var.set( round(float(cost) * (1+float(profit)/100), 2) )
            else:
                
                price_var.set(0)


    def __check_product_code(self):
        result = Product.validate_code(self.__code.get())

        if result:
            producto = Product.findOneProduct(self.__code.get())
            self.set_product(producto)
        else:
            messagebox.showinfo('Producto','El codigo registrado no se encuentra vinculado a ningun producto.',parent=self)
            ask = messagebox.askquestion('Registrar','Desea crear un nuevo registro de producto?',parent=self)
            if ask =='yes':
                window = ProductForm(self, window_type='quickCreate', title='Registrar Producto',code=self.__code.get())
                self.wait_window(window)
                self.grab_set()

    def __update_balance(self):
        total_price = 0
        for item in self.itemsGridview.get_children():
            data = self.itemsGridview.item(item, 'values')
            total_price += float(data[-1])

        self.BAMOUNT.set(round(total_price, 2))

# app = ttb.Window(themename='new')
# SGDB_Style()
# PurchaseForm(window_type='create', title='Registrar Factura')
# app.mainloop()
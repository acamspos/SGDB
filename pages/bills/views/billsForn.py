import ttkbootstrap as ttb
from tkinter import ttk
from pages.bills.views.itemscode import ItemsCodePosition
from assets.globals import GUI_COLORS, GUI_FONT, IMG_PATH
from models.entitys.bills import  Bill
from pages.clients.clients import ClientModule
from pages.representative.representative import RepresentativeModule
from pages.Products.views.product_search import ProductSelection
from pages.Service.views.service_search import ServiceSelection
from datetime import datetime
from tkinter import messagebox
from customtkinter import CTkFrame
from PIL import Image, ImageTk
from components.buttons import ButtonImage
from assets.utils import resize_icon, resize_image
import tkinter as tk
from assets.db.db_connection import DB
from models.entitys.bills import Bill, Item
from models.entitys.payment import Payment
from models.entitys.product import Product
from pages.bills.views.bill_selection import BillSelection
import assets.globals as constGlobal
from assets.globals import limitar_longitud, validate_number, on_combobox_change, on_validate_length, validateFloat, checkDATE
from tkinter.filedialog import askdirectory
from models.entitys.service import Service
FGCOLOR = 'white'


class BillForm(ttb.Toplevel):
    def __init__(self, master=None, window_type = 'create', title = '', bill = None):
        super().__init__(master)
        self.withdraw()
        self.protocol("WM_DELETE_WINDOW", self.close_confirmation)
        self.window_title = title
        self.window_type = window_type

        ######### MODAL WINDOW CONFIG #########
       


        self.__BILL: Bill = bill
        self.__REJECTBILL:Bill = None
        code = str(Bill.getNextBillcode())
        if not code.isdigit():
            code = '1'
       
        self.B_CODE = ttb.StringVar(value=f"{'0'*(6-len(code))+code}")
        self.B_DESCRIPTION = ttb.StringVar()
        self.B_DESCRIPTION.trace_add('write', lambda v,i,m: self.set_info_textarea(variable=self.B_DESCRIPTION, textarea=self.descriptionEntry))
        self.B_NOTES = ttb.StringVar()
        self.B_NOTES.trace_add('write', lambda v,i,m: self.set_info_textarea(variable=self.B_NOTES, textarea=self.notesEntry))
        self.B_COMPANY = ttb.StringVar()
        self.B_RIF = ttb.StringVar()
        self.B_ORDER = ttb.StringVar()
        self.B_CURRENCY = ttb.IntVar()
        self.B_CURRENCY_NAME = ttb.IntVar()
        self.B_DST = ttb.StringVar(value=datetime.today().strftime('%d/%m/%Y'))
        self.B_EST = ttb.StringVar(value=datetime.today().strftime('%d/%m/%Y'))
        self.BEXCHANGERATE = ttb.StringVar()
        self.B_BUDGET_CODE = ttb.StringVar()

        self.ITEM_MODE = ttb.IntVar(value=0)
        
        self.BAMOUNT = ttb.StringVar(value=0)
        #self.BAMOUNT.trace_add('write',self.calculate_usdexchange)
        self.BAMOUNTUSD = ttb.StringVar(value=0)
        self.BDEBT = ttb.DoubleVar(value=0)
        self.BTOTALPAID = ttb.DoubleVar(value=0)

        
        self.BAMOUNT_DEBT = ttb.StringVar(value=0)
        self.BAMOUNT_PAID = ttb.StringVar(value=0)
        self.BSTATUS = ttb.StringVar()
        self.BSTATE = ttb.StringVar()

        self.__FORM_DATA = [self.B_CODE, self.B_DESCRIPTION, self.B_NOTES, self.B_COMPANY, self.B_RIF,self.B_ORDER,
                             self.B_CURRENCY,self.B_DST, self.B_EST, self.BEXCHANGERATE]
      
        self.__itemDescription = ttb.StringVar()
        self.__itemDepartment = ttb.StringVar()
        self.__itemBrand = ttb.StringVar()
        self.__itemExistence = ttb.StringVar()
        self.__itemTax = ttb.StringVar()


        self.__subTotal = ttb.DoubleVar()
        self.__iva = ttb.DoubleVar()
        self.__total = ttb.DoubleVar()
        

        self.__page = ttb.StringVar(value=1)
        self.__page.trace_add('write', lambda i,m,v: self.__set_page())


        self.__createWidgets()
        self.set_info(self.__BILL)

        self.config(background="#D9D9D9")
        self.focus()
        self.grab_set()
        self.transient()
        self.title(title)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.place_window_center()
        self.iconbitmap('SIGAG.ico')
        self.deiconify()
    
    def use_reject_bill_callback(self, bill):
        self.__REJECTBILL: Bill = bill
        self.set_info(self.__REJECTBILL)
        #self.__BILL = None


    def create_pdf(self):
        ask = messagebox.askquestion('PDF','Crear pdf de la factura?', parent=self)
        if ask == 'yes':
          
            path = askdirectory(parent=self)
            if path:
                document = self.__BILL.create_pdf(path,parent=self)
                       
            else:
                messagebox.showinfo('Aviso','Proceso Cancelado. No se genero el PDF del documento.', parent=self)
           

    def set_info(self, bill:Bill):
        if bill:
            self.B_CODE.set(f"{'0'*(6-len(str(bill.code)))+str(bill.code)}")
            self.B_DESCRIPTION.set(bill.description)
            self.B_RIF.set(bill.client)
            self.B_COMPANY.set(bill.get_company())    
            self.B_NOTES.set(bill.notes)
            self.B_ORDER.set(bill.purchaseOrder)
            self.B_DST.set(bill.creationDate.strftime('%d/%m/%Y'))
            self.B_EST.set(bill.expirationDate.strftime('%d/%m/%Y'))
            self.B_CURRENCY.set(bill.currency)
            self.BAMOUNT.set(bill.total_amount)
            self.BEXCHANGERATE.set(bill.exchange_rate)
            self.BAMOUNTUSD.set(bill.totalUSD)
            self.BDEBT.set(bill.debtUSD)
            self.BTOTALPAID.set(bill.totalPaidUSD)
            self.BSTATUS.set(bill.get_documentStatus())
            self.BSTATE.set(bill.get_documentState())
            self.B_BUDGET_CODE.set(bill.budget_code)
            self.B_CURRENCY_NAME.set(bill.get_currency())

            items = bill.findItems()
            self.__set_items(items)
   
    def __createWidgets(self):

        contentFrame = CTkFrame(self, fg_color='white',border_width=1,  border_color='#CFCFCF')
        contentFrame.grid(row = 1, column = 0, sticky = 'nsew', padx=10, pady=10)
        contentFrame.columnconfigure(0, weight=1)

        self.__products_icon = resize_icon(Image.open(f"{IMG_PATH}/invoice.png"))

        titleFrame = CTkFrame(contentFrame, fg_color='#212946')
        titleFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=8, pady=(8,0))
        titleFrame.columnconfigure(0, weight=1)
        
        ttb.Label(titleFrame, image=self.__products_icon, compound='left', text=f' {self.window_title}', font=(GUI_FONT, 14, 'bold'), foreground='white', background='#212946').grid(row=0,column=0, padx=10, pady=10, sticky='nsew')

        if self.window_type != 'view':
            billsfileimg = Image.open(f"{IMG_PATH}/billsfile.png")
            self.billsfileimg = ImageTk.PhotoImage(billsfileimg.resize(resize_image(18, billsfileimg.size)))
            billsfileimgh = Image.open(f"{IMG_PATH}/billsfileh.png")
            self.billsfileimgh = ImageTk.PhotoImage(billsfileimgh.resize(resize_image(18, billsfileimgh.size)))
            billsfileimgp = Image.open(f"{IMG_PATH}/billsfilep.png")
            self.billsfileimgp = ImageTk.PhotoImage(billsfileimgp.resize(resize_image(18, billsfileimgp.size)))

            self.billsfileBTN = ButtonImage(titleFrame,  command=lambda:BillSelection(self, self.use_reject_bill_callback, selectionMode=True), image=self.billsfileimg, img_h=self.billsfileimgh, img_p=self.billsfileimgp, style='212946.TButton', padding=0)
            self.billsfileBTN.grid(row=0, column=1, sticky='nsew', pady=2, padx=(0,4))

        elif self.window_type == 'view':
            pdfBTN = Image.open(f"{IMG_PATH}/pdf.png")
            self.pdfBTN = ImageTk.PhotoImage(pdfBTN.resize(resize_image(11, pdfBTN.size)))
            pdfBTNh = Image.open(f"{IMG_PATH}/pdfh.png")
            self.pdfBTNh = ImageTk.PhotoImage(pdfBTNh.resize(resize_image(11, pdfBTNh.size)))
            pdfBTNp = Image.open(f"{IMG_PATH}/pdfp.png")
            self.pdfBTNp = ImageTk.PhotoImage(pdfBTNp.resize(resize_image(11, pdfBTNp.size)))

            self.pdfBTN = ButtonImage(titleFrame, image=self.pdfBTN, img_h=self.pdfBTNh, img_p=self.pdfBTNp, command=self.create_pdf, style='212946.TButton', padding=0)
            self.pdfBTN.grid(row=0, column=3, sticky='nsew', pady=2, padx=(0,4))
       

       

        self.product_info_content = tk.Frame(contentFrame)
        self.product_info_content.config(background=FGCOLOR)
        self.product_info_content.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        self.product_info_content.columnconfigure(1, weight=1)
        self.product_info_content.columnconfigure(2, weight=1)


            ########### Description Section ###########

        

        ttb.Separator(self.product_info_content, bootstyle='light').grid(row=9, column=0, pady=(8,0), sticky='nsew', columnspan=2)


        buttonss_section_frame = tk.Frame(self.product_info_content,)
        buttonss_section_frame.configure(background=FGCOLOR)
        buttonss_section_frame.grid(row=10, column=0, pady=(8,0), sticky='nsew', columnspan=2)
        buttonss_section_frame.anchor('e')
        buttonss_section_frame.columnconfigure(0, weight=1)


        self.pageNum = ttb.Label(buttonss_section_frame, text='Pagina: 1/2',font=(GUI_FONT,12,'bold'), background='#fff', bootstyle='dark')
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

        self.backBTN = ButtonImage(buttonss_section_frame,  command=lambda:self.__back_page(), image=self.backbtnimg, img_h=self.backbtnimgh, img_p=self.backbtnimgp, style='flatw.light.TButton',padding=0)
        

       


        creatbtnimg = Image.open(f"{IMG_PATH}/registrar.png")
        self.creatbtnimg = ImageTk.PhotoImage(creatbtnimg.resize(resize_image(20, creatbtnimg.size)))
        creatbtnimgh = Image.open(f"{IMG_PATH}/registrarh.png")
        self.creatbtnimgh = ImageTk.PhotoImage(creatbtnimgh.resize(resize_image(20, creatbtnimgh.size)))
        creatbtnimgp = Image.open(f"{IMG_PATH}/registrarp.png")
        self.creatbtnimgp = ImageTk.PhotoImage(creatbtnimgp.resize(resize_image(20, creatbtnimgp.size)))

        self.createBTN = ButtonImage(buttonss_section_frame,  command=lambda:self.__next_page(), image=self.creatbtnimg, img_h=self.creatbtnimgh, img_p=self.creatbtnimgp, style='flatw.light.TButton', text='CONTINUAR', compound='center',padding=0)
        self.createBTN.grid(row=0, column=3, sticky='nsew', pady=2, padx=(0,4))

    
        self.__secondPage()
        self.__firstPage()
        self.maxpage = 2 
        self.__all_pages = [self.firtsPageFrame, self.second_page]
        if self.window_type == 'view':
            self.maxpage = 3
            self.__thirthPage()
            self.__all_pages.append(self.thirth_page)
        self.__set_page()


    def __set_page(self):
        page = int(self.__page.get())
        if page == self.maxpage:
            if self.window_type == 'create':
                self.createBTN.configure(text='REGISTRAR', command=lambda:self.__createBill())
            else:
                self.createBTN.grid_forget()
            self.backBTN.grid(row=0, column=2, sticky='nsew', pady=2, padx=(0,4))
        else:
            if self.window_type != 'create' and not self.createBTN.winfo_ismapped():
                self.createBTN.grid(row=0, column=3, sticky='nsew', pady=2, padx=(0,4))

            self.createBTN.configure(text='CONTINUAR',command=self.__next_page)
            if page == 1:
                self.backBTN.grid_forget()
            else:
                self.backBTN.grid(row=0, column=2, sticky='nsew', pady=2, padx=(0,4))
        self.__all_pages[page-1].tkraise()
        self.pageNum.config(text=f'Pagina: {page}/{self.maxpage}')



    def __back_page(self):
        self.__page.set(int(self.__page.get())-1)
        if len(self.itemsGridview.get_children())>0:
            self.currencyCombobox.config(state='disabled')
        else:
            self.currencyCombobox.config(state='readonly')

        
    def __set_form_state(self, state = 'normal'):
        for field in self.__form_fields:
            field.config(state=state)
            if field.winfo_class() == 'TEntry':
                field.config(cursor='xterm')
            else:
                field.config(cursor='hand2')
    
    def set_info_textarea(self, var=None, index=None, mode=None, variable=None, textarea=None):
        textarea.config(state='normal')
        textarea.delete('1.0', ttb.END)
        textarea.insert('1.0', variable.get())
        if self.window_type == 'view':
            textarea.config(state='disabled')


    def __thirthPage(self):
        self.thirth_page = tk.Frame(self.product_info_content)
        self.thirth_page.config(background=FGCOLOR)
        self.thirth_page.grid(row=0, column=0, sticky='nsew', columnspan=2)
        self.thirth_page.columnconfigure(0, weight=1)
        self.thirth_page.rowconfigure(0, weight=1)


        payments_made_frame = ttb.Frame(self.thirth_page,  style='white.TFrame')
        payments_made_frame.grid(row=0, column=0, sticky='nsew',padx=8,  ipady=4,pady=6)
        payments_made_frame.grid_propagate(0)
        payments_made_frame.columnconfigure(0, weight=1)
        payments_made_frame.rowconfigure(1, weight=1)


        PMDF_menu_bar = ttb.Frame(payments_made_frame, 
                                  style='white.TFrame',
                                  padding='2 2')
        PMDF_menu_bar.grid(row=0, column=0, sticky='nsew', padx=4, pady=4)

    
        
        ttb.Label(PMDF_menu_bar, text='Pagos Asociados al Documento (Factura)', font=(GUI_FONT,10,'bold'), background='#fff').grid(row=0, column=0, sticky='nsew')


    


        ################ TREEVIEW ELEMENTS ################
        yscroll = ttb.Scrollbar(payments_made_frame, 
                                orient='vertical',
                                bootstyle="dark-round")
        yscroll.grid(row=1, column=1, padx=(0,1), pady=1,sticky='ns', rowspan=2)
        
        xscroll = ttb.Scrollbar(payments_made_frame, 
                                orient='horizontal',
                                bootstyle="dark-round")
        xscroll.grid(row=2, column=0, padx=1, pady=1,sticky='ew')

        columns = ('date', 'document', 'reference', 'payment_method','currency','amount','amountUSD','exchange','details')

        self.__documents_paid_gridview = ttb.Treeview(payments_made_frame,
                                columns=columns,
                                bootstyle='dark', 
                                height=10,
                                selectmode='extended', 
                                yscrollcommand=yscroll.set,
                                xscrollcommand=xscroll.set)
        self.__documents_paid_gridview.grid(row=1,column=0,padx=4,pady=4,sticky='nsew')

        yscroll.configure(command=self.__documents_paid_gridview.yview)
        xscroll.configure(command=self.__documents_paid_gridview.xview)

        self.__documents_paid_gridview.heading("#0")
        self.__documents_paid_gridview.heading(columns[0], anchor='center', text='Fecha')
        self.__documents_paid_gridview.heading(columns[1], anchor='center', text='Documento')
        self.__documents_paid_gridview.heading(columns[2], anchor='center', text='Referencia')
        self.__documents_paid_gridview.heading(columns[3], anchor='center', text='Forma de Pago')
        self.__documents_paid_gridview.heading(columns[4], anchor='center', text='Moneda')
        self.__documents_paid_gridview.heading(columns[5], anchor='center', text='Monto')
        self.__documents_paid_gridview.heading(columns[6], anchor='center', text='Monto USD')
        self.__documents_paid_gridview.heading(columns[7], anchor='center', text='Tasa de Cambio')
        self.__documents_paid_gridview.heading(columns[8], anchor='center', text='Detalles')

        self.__documents_paid_gridview.column('#0', width=0, stretch=False, anchor='center')
        self.__documents_paid_gridview.column(columns[0], width=140, stretch=False, anchor='center')
        self.__documents_paid_gridview.column(columns[1], width=140, stretch=False, anchor='center')
        self.__documents_paid_gridview.column(columns[2], width=140, stretch=False, anchor='center')
        self.__documents_paid_gridview.column(columns[3], width=230, stretch=False, anchor='center')
        self.__documents_paid_gridview.column(columns[4], width=140, stretch=False, anchor='center')
        self.__documents_paid_gridview.column(columns[5], width=140, stretch=False, anchor='center')
        self.__documents_paid_gridview.column(columns[6], width=140, stretch=False, anchor='center')
        self.__documents_paid_gridview.column(columns[7], width=140, stretch=False, anchor='center')
        self.__documents_paid_gridview.column(columns[8], width=300, stretch=False, anchor='center')
        
        self.set_payments()


    def __secondPage(self):
        self.second_page = tk.Frame(self.product_info_content)
        self.second_page.config(background=FGCOLOR)
        self.second_page.grid(row=0, column=0, sticky='nsew', columnspan=2)
        self.second_page.columnconfigure(0, weight=1)
        self.second_page.rowconfigure(0, weight=1)


         ###### CONTENT TITLE ######
        itemsGridview_frame =  ttb.Frame(self.second_page, style='white.TFrame')
        itemsGridview_frame.grid(row=0,column=0,sticky='nsew', padx=8,  ipady=4,pady=6)
        itemsGridview_frame.columnconfigure(0, weight=1)
        itemsGridview_frame.rowconfigure(3,weight=1)

            #### Gridview Button options ####

        if self.window_type != 'view':
            buttons_menu_frame = ttb.Frame(itemsGridview_frame, style='white.TFrame')
            buttons_menu_frame.grid(row=0, column=0, sticky='nsew', columnspan=2)


            self.item_type_label = ttb.Label(buttons_menu_frame,
                    bootstyle='primary',
                    text='Productos'.upper(),
                    font=(GUI_FONT,12,'bold'),
                    background='#fff',
                    anchor='w',
                    )
            self.item_type_label.grid(row=0, column=0, padx=8,  ipady=4,pady=4, sticky='nsw')

            ttb.Separator(buttons_menu_frame,
                        orient='vertical'
            ).grid(row=0, column=1, sticky='ns', pady=12)

            findimg = Image.open(f"{IMG_PATH}/find.png")
            self.findimg = ImageTk.PhotoImage(findimg.resize(resize_image(18, findimg.size)))
            findimgh = Image.open(f"{IMG_PATH}/findh.png")
            self.findimgh = ImageTk.PhotoImage(findimgh.resize(resize_image(18, findimgh.size)))
            findimgp = Image.open(f"{IMG_PATH}/findp.png")
            self.findimgp = ImageTk.PhotoImage(findimgp.resize(resize_image(18, findimgp.size)))

            self.findBTN = ButtonImage(buttons_menu_frame, text='F3',compound='left', image=self.findimg, img_h=self.findimgh, img_p=self.findimgp, style='white.TButton', padding=0)
            self.findBTN.grid(row=0, column=2, sticky='nsew', pady=2, padx=(10,5))

          
            self.findBTN.config(command=self.__open_selection_items_modals)
        

            ttb.Separator(buttons_menu_frame,
                        orient='vertical'
            ).grid(row=0, column=4, sticky='ns', pady=12)


            createimg = Image.open(f"{IMG_PATH}/create.png")
            self.createimg = ImageTk.PhotoImage(createimg.resize(resize_image(18, createimg.size)))
            createimgh = Image.open(f"{IMG_PATH}/createh.png")
            self.createimgh = ImageTk.PhotoImage(createimgh.resize(resize_image(18, createimgh.size)))
            createimgp = Image.open(f"{IMG_PATH}/createp.png")
            self.createimgp = ImageTk.PhotoImage(createimgp.resize(resize_image(18, createimgp.size)))

            self.createNewItemBTN = ButtonImage(buttons_menu_frame,  command=lambda:print(self.winfo_width(),self.winfo_height()),text='F4',compound='left', image=self.createimg, img_h=self.createimgh, img_p=self.createimgp, style='white.TButton', padding=0)
            self.createNewItemBTN.grid(row=0, column=3, sticky='nsew', pady=2, padx=(5,10))



            deleteimg = Image.open(f"{IMG_PATH}/deleten.png")
            self.deleteimg = ImageTk.PhotoImage(deleteimg.resize(resize_image(18, deleteimg.size)))
            deleteimgh = Image.open(f"{IMG_PATH}/deleteh.png")
            self.deleteimgh = ImageTk.PhotoImage(deleteimgh.resize(resize_image(18, deleteimgh.size)))
            deleteimgp = Image.open(f"{IMG_PATH}/deletep.png")
            self.deleteimgp = ImageTk.PhotoImage(deleteimgp.resize(resize_image(18, deleteimgp.size)))

            self.deleteBTN = ButtonImage(buttons_menu_frame,  command=self.__delete_all_record, image=self.deleteimg, img_h=self.deleteimgh, img_p=self.deleteimgp, style='white.TButton', padding=0)
            self.deleteBTN.grid(row=0, column=5, sticky='nsew', pady=2, padx=(10,5))


            deleteoneimg = Image.open(f"{IMG_PATH}/deleteone.png")
            self.deleteoneimg = ImageTk.PhotoImage(deleteoneimg.resize(resize_image(18, deleteoneimg.size)))
            deleteoneimgh = Image.open(f"{IMG_PATH}/deleteoneh.png")
            self.deleteoneimgh = ImageTk.PhotoImage(deleteoneimgh.resize(resize_image(18, deleteoneimgh.size)))
            deleteoneimgp = Image.open(f"{IMG_PATH}/deleteonep.png")
            self.deleteoneimgp = ImageTk.PhotoImage(deleteoneimgp.resize(resize_image(18, deleteoneimgp.size)))

            self.deleteoneBTN = ButtonImage(buttons_menu_frame, state='disabled', command=self.__delete_record, image=self.deleteoneimg, img_h=self.deleteoneimgh, img_p=self.deleteoneimgp, style='white.TButton', padding=0)
            self.deleteoneBTN.grid(row=0, column=6, sticky='nsew', pady=2, padx=(5,10))


            ttb.Separator(buttons_menu_frame,
                        orient='vertical'
            ).grid(row=0, column=7, sticky='ns', pady=12)

          
            changeimg = Image.open(f"{IMG_PATH}/change.png")
            self.changeimg = ImageTk.PhotoImage(changeimg.resize(resize_image(18, changeimg.size)))
            changeimgh = Image.open(f"{IMG_PATH}/changeh.png")
            self.changeimgh = ImageTk.PhotoImage(changeimgh.resize(resize_image(18, changeimgh.size)))
            changeimgp = Image.open(f"{IMG_PATH}/changep.png")
            self.changeimgp = ImageTk.PhotoImage(changeimgp.resize(resize_image(18, changeimgp.size)))

            self.changeBTN = ButtonImage(buttons_menu_frame,  command=lambda:self.__change_item_mode(),text='F7',compound='left', image=self.changeimg, img_h=self.changeimgh, img_p=self.changeimgp, style='white.TButton', padding=0)
            self.changeBTN.grid(row=0, column=8, sticky='nsew', pady=2, padx=10)

                ##### SCROLLBARS #####

            ttb.Separator(itemsGridview_frame,
                        orient='horizontal', bootstyle='dark'
            ).grid(row=1, column=0, sticky='nsew', padx=2, columnspan=2)

            specifications_frame = ttb.Frame(itemsGridview_frame, style='white.TFrame')
            specifications_frame.grid(row=2,column=0,padx=6,pady=8,sticky='nsew')

            specifications_frame.columnconfigure(4, weight=1)
            specifications_frame.columnconfigure(6, weight=1)

            ttb.Label(specifications_frame,
                    text='Codigo',
                
                    padding='5 0',
                    anchor='w',
                    
                    font=(GUI_FONT, 12, 'bold'),
                    bootstyle='primary inverse'
            ).grid(row=0, column=0, sticky='nsew', padx=2, pady=(0,2), ipady=6, ipadx=4)

            self.code_entry = ttb.Entry(specifications_frame,
                                font=(GUI_FONT,12),
                                )
            self.code_entry.grid(row=0, column=1, sticky='nsew',pady=(0,2), columnspan=2)
            self.code_entry.bind('<Return>', lambda e: self.findItem_by_entry())
        
            ttb.Label(specifications_frame,
                    text='Precio',
                    padding='5 0',
                    anchor='w',
                    
                    font=(GUI_FONT, 12, 'bold'),
                    bootstyle='primary inverse'
            ).grid(row=1, column=0, sticky='nsew', padx=2, pady=(0,2),)

            self.price_combobox = ttk.Combobox(specifications_frame,
                                width=10,
                                font=(GUI_FONT,12),
                                state='readonly')
            self.price_combobox.grid(row=1, column=1, sticky='nsew', pady=(0,2), )

        
            
            ttb.Label(specifications_frame,
                    text='Cantidad',
                    
                    font=(GUI_FONT, 12, 'bold'),
                    bootstyle='primary inverse',
                    padding='5 0',
                    anchor='e',
            ).grid(row=2, column=0, sticky='nsew', ipadx=2, padx=2, pady=(0,2),)

            self.amount_entry = ttk.Entry(specifications_frame,
                                    width=10,
                                    font=(GUI_FONT,12),
                                    justify='center',validate="key",
                                    validatecommand=(self.register(validate_number), "%S")
            )
            self.amount_entry.grid(row=2, column=1, sticky='nsew', pady=(0,2), ipady=3)
            self.amount_entry.bind('<Return>', lambda e: self.__add_item())


            additemimg = Image.open(f"{IMG_PATH}/additem.png")
            self.additemimg = ImageTk.PhotoImage(additemimg.resize(resize_image(30, additemimg.size)))
            additemimgh = Image.open(f"{IMG_PATH}/additemh.png")
            self.additemimgh = ImageTk.PhotoImage(additemimgh.resize(resize_image(30, additemimgh.size)))
            additemimgp = Image.open(f"{IMG_PATH}/additemp.png")
            self.additemimgp = ImageTk.PhotoImage(additemimgp.resize(resize_image(30, additemimgp.size)))

            self.additemBTN = ButtonImage(specifications_frame, compound='center',command=self.__add_item,  image=self.additemimg, img_h=self.additemimgh, img_p=self.additemimgp, style='white.TButton', padding=0)
            self.additemBTN.grid(row=1, column=2, rowspan=2, sticky='nsew',padx=(2,0))




        

            self.description_label = ttb.Label(specifications_frame,
                                        textvariable=self.__itemDescription,
                                        background='#fff',
                                        bootstyle='danger',
                                        padding='5 5',
                                        font=(GUI_FONT,12, 'bold'))
            self.description_label.grid(row=0, column=3, padx=8,  ipady=4,columnspan=4, sticky='nsew')

            


            

            ttb.Label(specifications_frame,
                        text='Departamento:',
                        anchor='w',
                        background='#fff',
                        font=(GUI_FONT,11, 'bold')
            ).grid(row=1, column=3, padx=8,  ipady=4,sticky='nsew')

            self.department_label = ttb.Label(specifications_frame,
                                        textvariable=self.__itemDepartment,
                                        background='#fff',
                                        width=20,
                                        font=(GUI_FONT,12))
            self.department_label.grid(row=1, column=4, sticky='nsew')


            ttb.Label(specifications_frame,
                        text='Marca:',background='#fff',
                        anchor='w',
                        font=(GUI_FONT,11, 'bold')
            ).grid(row=2, column=3, padx=8,  ipady=4,sticky='nsew')

            self.brand = ttb.Label(specifications_frame,
                                        textvariable=self.__itemBrand,
                                        background='#fff',
                                        width=20,
                                        font=(GUI_FONT,12))
            self.brand.grid(row=2, column=4, sticky='nsew')


            ttb.Label(specifications_frame,
                        text='Iva:',background='#fff',
                        anchor='w',
                        font=(GUI_FONT,11, 'bold')
            ).grid(row=1, column=5, padx=8,  ipady=4,sticky='nsew')

            self.iva_label = ttb.Label(specifications_frame,
                                        textvariable=self.__itemTax,
                                        background='#fff',
                                        width=20,
                                        font=(GUI_FONT,12))
            self.iva_label.grid(row=1, column=6, sticky='nsew')


            ttb.Label(specifications_frame,
                        text=' Existencia:',background='#fff',
                        anchor='w',
                        font=(GUI_FONT,11, 'bold')
            ).grid(row=2, column=5, padx=8,  ipady=4,sticky='nsew')

            

            self.existence_label = ttb.Label(specifications_frame,
                                        textvariable=self.__itemExistence,
                                        background='#fff',
                                        width=20,
                                        font=(GUI_FONT,12))
            self.existence_label.grid(row=2, column=6, sticky='nsew')

        yscroll = ttb.Scrollbar(itemsGridview_frame, orient='vertical',bootstyle="dark-round")
        yscroll.grid(row=3, column=1, padx=2, pady=2,sticky='ns', rowspan=2)

        xscroll = ttb.Scrollbar(itemsGridview_frame, orient='horizontal',bootstyle="dark-round")
        xscroll.grid(row=4, column=0, padx=2, pady=2,sticky='ew')

            ##### GRIDVIEW #####
        columns = ('Codigo',
                   'description',
                   'type',
                   'cost',
                   'amount',
                   'P.U',
                   'total',
                   'totalUSD')

        #Create menu
        


        self.itemsGridview = ttb.Treeview(itemsGridview_frame,
                                columns=columns,
                                show='headings',
                                bootstyle='dark',
                                height=7,
                                padding=2,
                                yscrollcommand=yscroll.set,
                                xscrollcommand=xscroll.set)
        self.itemsGridview.grid(row=3,column=0,padx=2,pady=(2,2),sticky='nsew')




        yscroll.config(command=self.itemsGridview.yview)
        xscroll.config(command=self.itemsGridview.xview)

        self.itemsGridview.heading(columns[0],text='Codigo')
        self.itemsGridview.heading(columns[1], text='Descripción')
        self.itemsGridview.heading(columns[2], text='Tipo')
        self.itemsGridview.heading(columns[3], text='Costo USD $')
        self.itemsGridview.heading(columns[4],text='Cant.')
        self.itemsGridview.heading(columns[5],text='P.U')
        self.itemsGridview.heading(columns[6], text='Total')
        self.itemsGridview.heading(columns[7], text='Total USD $')

        self.itemsGridview.column(columns[0],width=150,stretch=True,anchor='center')
        self.itemsGridview.column(columns[1],width=300,stretch=True,anchor='w')
        self.itemsGridview.column(columns[2],width=150,stretch=True,anchor='center')
        self.itemsGridview.column(columns[3],width=150,stretch=True,anchor='center')
        self.itemsGridview.column(columns[4],width=150,stretch=True,anchor='center')
        self.itemsGridview.column(columns[5],width=150,stretch=True,anchor='center')
        self.itemsGridview.column(columns[6],width=150,stretch=True,anchor='center')
        self.itemsGridview.column(columns[7],width=150,stretch=True,anchor='center')

        if self.window_type == 'create':
            self.itemsGridview.bind('<<TreeviewSelect>>', lambda e:self.__selection_options())



        tags_frames = ttb.Frame(itemsGridview_frame, style='white.TFrame')
        tags_frames.grid(row=5, column=0, sticky='nsew',padx=2,pady=(6,2), columnspan=2)
        tags_frames.anchor('e')
        for x in range(6):
            tags_frames.columnconfigure(x, weight=1)

        

        ttb.Label(tags_frames, text='Sub-total', font=(GUI_FONT,11,'bold'), bootstyle='inverse primary', width=16,anchor='center', padding='10 5').grid(row=0, column=0, sticky='nsew', pady=2)


        self.subtotalEntry = ttb.Entry(tags_frames, 
                                     textvariable=self.__subTotal,
                                     width=20, state='readonly', justify='center'
                                     )
        self.subtotalEntry.grid(row=0, column=1, sticky='nsew',padx=(2,2), ipady=4, pady=2)


     
        ttb.Label(tags_frames, text='IVA', font=(GUI_FONT,11,'bold'), bootstyle='inverse primary', width=16,anchor='center', padding='10 5').grid(row=0, column=2, sticky='nsew', pady=2)


        self.ivaEntry = ttb.Entry(tags_frames, 
                                     textvariable=self.__iva,
                                     width=20, state='readonly', justify='center'
                                     )
        self.ivaEntry.grid(row=0, column=3, sticky='nsew',padx=(2,2), ipady=4, pady=2)


       
        ttb.Label(tags_frames, text='Total', font=(GUI_FONT,11,'bold'), bootstyle='inverse primary', anchor='center', width=16, padding='10 5').grid(row=0, column=4, sticky='nsew', pady=2)


        self.totalEntry = ttb.Entry(tags_frames, 
                                     textvariable=self.__total, font=(GUI_FONT,10,'bold'), foreground=GUI_COLORS['danger'],
                                     width=20, state='readonly', justify='center'
                                     )
        self.totalEntry.grid(row=0, column=5, sticky='nsew',padx=(2,0), ipady=4, pady=2)
        ttb.Label(tags_frames, textvariable=self.B_CURRENCY_NAME, font=(GUI_FONT,11,'bold'), bootstyle='danger', anchor='center', width=8, padding='10 5').grid(row=0, column=6, sticky='nsew', pady=2)




    def __firstPage(self):
        self.firtsPageFrame = tk.Frame(self.product_info_content)
        self.firtsPageFrame.config(background=FGCOLOR)
        self.firtsPageFrame.grid(row=0, column=0, sticky='nsew', columnspan=2, padx=6)
        self.firtsPageFrame.columnconfigure(1, weight=1)

        code_label = ttb.Label(self.firtsPageFrame, 
                                      anchor='w', 
                                      text='Factura Nº', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=(GUI_FONT,11,'bold'))
        code_label.grid(row=0, column=0, padx=5, pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.codeEntry = ttb.Entry(self.firtsPageFrame, justify='center',
                                       width=30, textvariable=self.B_CODE, state='readonly'
                                      )
        self.codeEntry.grid(row=1, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=4, columnspan=1)

        client_label = ttb.Label(self.firtsPageFrame, 
                                     anchor='w', 
                                     text='Cliente', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=(GUI_FONT,11,'bold'))
        client_label.grid(row=0, column=1, padx=5, pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        
        client_frame = tk.Frame(self.firtsPageFrame)
        client_frame.config(background=FGCOLOR)
        client_frame.grid(row=1, column=1, sticky='nsew' ,pady=(2,0),padx=(4,10),)
        client_frame.columnconfigure(2,weight=1)
        client_frame.rowconfigure(0, weight=1)

        client_frame.anchor('w')
        
        if self.window_type != 'view':
            self.client_search_btn = ttb.Button(client_frame, 
                                            command=self.__open_client_selection,
                                            text='...',
                                            bootstyle='dark')
            self.client_search_btn.grid(row=0, column=0, padx=(2), sticky='nsew', pady=1)

        self.clientIdEntry = ttb.Entry(client_frame, 
                                     textvariable=self.B_RIF,
                                     width=20, state='readonly'
                                     )
        self.clientIdEntry.grid(row=0, column=1, sticky='nsew',padx=5, ipady=4,)

        self.clientEntry = ttb.Entry(client_frame, width=80,
                                     textvariable=self.B_COMPANY, state='readonly'
                                     )
        self.clientEntry.grid(row=0, column=2, sticky='nsew',padx=5, ipady=4,)


        description_label = ttb.Label(self.firtsPageFrame, 
                                      anchor='w', 
                                      text='Descripcion', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=(GUI_FONT,11,'bold'))
        description_label.grid(row=2, column=0, padx=5, pady=(2,0), ipadx=8, ipady=8, sticky='nsew', columnspan=2)

        self.descriptionEntry = ttb.Text(self.firtsPageFrame, height=3)
        self.descriptionEntry.grid(row=3, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=4, columnspan=2)
        self.descriptionEntry.bind('<KeyPress>', lambda e: limitar_longitud(self.descriptionEntry, 400))
        self.descriptionEntry.bind('<KeyRelease>', lambda e: limitar_longitud(self.descriptionEntry, 400))
        self.descriptionEntry.bind('Control-v', lambda e: limitar_longitud(self.descriptionEntry, 400))




        notes_label = ttb.Label(self.firtsPageFrame, 
                                      anchor='w', 
                                      text='Notas', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=(GUI_FONT,11,'bold'))
        notes_label.grid(row=4, column=0, padx=5, pady=(2,0), ipadx=8, ipady=8, sticky='nsew', columnspan=2)

        self.notesEntry = ttb.Text(self.firtsPageFrame, height=2)
        self.notesEntry.grid(row=5, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=4, columnspan=2)
        self.notesEntry.bind('<KeyPress>', lambda e: limitar_longitud(self.notesEntry, 400))
        self.notesEntry.bind('<KeyRelease>', lambda e: limitar_longitud(self.notesEntry, 400))
        self.notesEntry.bind('Control-v', lambda e: limitar_longitud(self.notesEntry, 400))


        moreInfoFrame = tk.Frame(self.firtsPageFrame)
        moreInfoFrame.config(background=FGCOLOR)
        moreInfoFrame.grid(row=6, column=0, sticky='nsew', columnspan=2)
        moreInfoFrame.columnconfigure(0, weight=1)
        moreInfoFrame.columnconfigure(1, weight=1)
        moreInfoFrame.columnconfigure(2, weight=1)

        orderPurchase_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Orden de Compra', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=(GUI_FONT,11,'bold'))
        orderPurchase_label.grid(row=0, column=0, padx=5, pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        
        self.orderPurchaseEntry = ttb.Entry(moreInfoFrame, justify='center', textvariable=self.B_ORDER,validate="key", validatecommand=(self.register(lambda e: on_validate_length(e,lenght=20)), '%P'))
        self.orderPurchaseEntry.grid(row=1, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=4, columnspan=1)


        startDate_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Fecha de Creacion', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=(GUI_FONT,11,'bold'))
        startDate_label.grid(row=0, column=1, padx=5, pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        
        self.startDateEntry = ttb.DateEntry(moreInfoFrame, dateformat='%d/%m/%Y', startdate=datetime.today())
        self.startDateEntry.grid(row=1, column=1, sticky='nsew',pady=(2,0),padx=4, ipady=0,)
        self.startDateEntry.entry.config(justify='center',textvariable=self.B_DST)
        self.startDateEntry.entry.bind('<FocusOut>', lambda e: checkDATE(self.B_DST))


        endDate_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Fecha de Vencimiento', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=(GUI_FONT,11,'bold'))
        endDate_label.grid(row=0, column=2, padx=5, pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        
        self.endDateEntry = ttb.DateEntry(moreInfoFrame, dateformat='%d/%m/%Y', startdate=datetime.today())
        self.endDateEntry.grid(row=1, column=2, sticky='nsew',pady=(2,0),padx=4, ipady=0,)
        self.endDateEntry.entry.config(justify='center',textvariable=self.B_EST)
        self.endDateEntry.entry.bind('<FocusOut>', lambda e: checkDATE(self.B_EST))
        


        currency_label = ttb.Label(moreInfoFrame, 
                                   anchor='w', 
                                   text='Moneda', 
                                   background=FGCOLOR,
                                   font=(GUI_FONT,11,'bold'))
        currency_label.grid(row=2, column=0, padx=5, pady=(2,0), ipadx=8, sticky='nsew')
     
        
        CURRENCY =  DB.getCurrencyList()
        self.CURRENCY_DICT = {row[1]:row[0] for row in CURRENCY}
        self.CURRENCY_DICT_VALUE = {row[0]:row[2] for row in CURRENCY}
        del CURRENCY



        def set_exchange_rate(var,index,mode):
            value = self.CURRENCY_DICT_VALUE[int(self.B_CURRENCY.get())]
            if value == 1:
                value = 0.0
            self.BEXCHANGERATE.set(value)

     
        
        self.currencyCombobox = ttb.Combobox(moreInfoFrame, values=list(self.CURRENCY_DICT.keys()), state='readonly', style='selectionOnly.TCombobox', textvariable=self.B_CURRENCY_NAME, font=(GUI_FONT,10,'bold'))
        self.currencyCombobox.grid(row=3, column=0, padx=(4,10), pady=(4,0), sticky='nsew')
        self.currencyCombobox.bind("<<ComboboxSelected>>", lambda e: on_combobox_change(e,self.B_CURRENCY, self.CURRENCY_DICT, self.currencyCombobox))
        self.currencyCombobox.current(0)
        self.B_CURRENCY.trace_add('write', set_exchange_rate)
        self.B_CURRENCY.set(1)

        if self.window_type  == 'view':
            self.currencyCombobox.config(state='disabled')


        if self.window_type != 'create':

            documentStateLabel = ttb.Label(moreInfoFrame, 
                                        anchor='w', 
                                        text='Estado', 
                                        bootstyle='primary',
                                        background=FGCOLOR ,
                                        font=(GUI_FONT,11,'bold'))
            documentStateLabel.grid(row=2, column=1, padx=5, pady=(4,0), ipadx=8, ipady=4, sticky='nsew')
            
            self.documentStatEntry = ttb.Entry(moreInfoFrame, state='readonly', justify='center', textvariable=self.BSTATE)
            self.documentStatEntry.grid(row=3, column=1, sticky='nsew',pady=(2,0),padx=4, ipady=6,)
           
        

            paymentStatusLabel = ttb.Label(moreInfoFrame, 
                                        anchor='w', 
                                        text='Status', 
                                        bootstyle='primary', 
                                        background=FGCOLOR,
                                        font=(GUI_FONT,11,'bold'))
            paymentStatusLabel.grid(row=2, column=2, padx=5, pady=(4,0), ipadx=8, ipady=4, sticky='nsew')



            self.documentStatusEntry = ttb.Entry(moreInfoFrame, state='readonly', justify='center',textvariable=self.BSTATUS)
            self.documentStatusEntry.grid(row=3, column=2, sticky='nsew',pady=(2,0),padx=4)


            colorstate = {1:'secondary',2:'danger', 3:'success',4:'danger',}
            colorpayment = {1:'danger', 2:'success'}
            self.documentStatEntry.config(bootstyle=colorstate[self.__BILL.documentState])
            self.documentStatusEntry.config(bootstyle=colorpayment[self.__BILL.payment_status])

      

        currencyDetailsFrame = ttb.Frame(moreInfoFrame, style='white.TFrame')
        currencyDetailsFrame.grid(row=4, column=0, columnspan=3, padx=4, sticky='nsew', pady=(6,0))
        
        self.exchangerate_label = ttb.Label(currencyDetailsFrame, 
                                     anchor='w', 
                                     text='Tasa de Cambio', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=(GUI_FONT,11,'bold'))
        self.exchangerate_label.grid(row=0, column=1, padx=5, pady=(4,0), ipadx=8, ipady=4, sticky='nsew')
        
        self.exchangerateEntry = ttb.Entry(currencyDetailsFrame,width=20, justify='center', textvariable=self.BEXCHANGERATE,
                                           validate="key",validatecommand=(self.register(validateFloat), "%P"))
        self.exchangerateEntry.grid(row=1, column=1, sticky='nsew',pady=(2,0),padx=(4,90), ipady=10,)
      


        self.FIELDS = [
            self.codeEntry, self.exchangerateEntry, self.notesEntry, self.descriptionEntry, self.startDateEntry.entry, self.endDateEntry.entry, self.startDateEntry.button, 
            self.endDateEntry.button, self.orderPurchaseEntry
        ]


        if self.window_type != 'create':
            amountLabelMain = ttb.Label(currencyDetailsFrame, 
                                        anchor='w', 
                                        text='Monto Factura', 
                                        bootstyle='primary',
                                        background=FGCOLOR ,
                                        font=(GUI_FONT,11,'bold'))
            amountLabelMain.grid(row=0, column=0, padx=5, pady=(4,0), ipadx=8, ipady=4, sticky='nsew')
                
            self.amountEntry = ttb.Entry(currencyDetailsFrame,width=30, bootstyle='primary', justify='center', textvariable=self.BAMOUNT,
                                            validate="key",validatecommand=(self.register(validateFloat), "%P"))
            self.amountEntry.grid(row=1, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=10)
    

            amountPaidLabel = ttb.Label(currencyDetailsFrame, 
                                        anchor='w', 
                                        text='Monto Pagado $', 
                                        bootstyle='primary',
                                        background=FGCOLOR ,
                                        font=(GUI_FONT,11,'bold'))
            amountPaidLabel.grid(row=0, column=3, padx=5, pady=(4,0), ipadx=8, ipady=4, sticky='nsew')
            self.amountPaidEntry = ttb.Entry(currencyDetailsFrame, justify='center',width=30, textvariable=self.BTOTALPAID)
            self.amountPaidEntry.grid(row=1, column=3, sticky='nsew',pady=(2,0),padx=4, ipady=10)


            debtLabel = ttb.Label(currencyDetailsFrame, 
                                        anchor='w', 
                                        text='Deuda $', 
                                        bootstyle='primary',
                                        background=FGCOLOR ,
                                        font=(GUI_FONT,11,'bold'))
            debtLabel.grid(row=0, column=4, padx=5, pady=(4,0), ipadx=8, ipady=4, sticky='nsew')
            self.debtEntry = ttb.Entry(currencyDetailsFrame, justify='center',width=30,textvariable=self.BDEBT)
            self.debtEntry.grid(row=1, column=4, sticky='nsew',pady=(2,0),padx=4, ipady=10)


            amountUSDLabel = ttb.Label(currencyDetailsFrame, 
                                     anchor='w', 
                                     text='Total USD $', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=(GUI_FONT,11,'bold'))
            amountUSDLabel.grid(row=0, column=2, padx=5, pady=(4,0), ipadx=8, ipady=4, sticky='nsew')
            self.amountUSDEntry = ttb.Entry(currencyDetailsFrame, justify='center',width=30,textvariable=self.BAMOUNTUSD)
            self.amountUSDEntry.grid(row=1, column=2, sticky='nsew',pady=(2,0),padx=4, ipady=10)

            self.FIELDS.extend([self.amountUSDEntry, self.debtEntry, self.amountPaidEntry, self.amountEntry])
        
        if self.window_type == 'view':
            self.__set_form_state('readonly')

    def __set_form_state(self, state = 'normal'):
      
        for field in self.FIELDS:
            if field.winfo_class() != 'TEntry' and state=='readonly':
                newstate='disabled'
                field.config(state=newstate)
                del newstate

                self.descriptionEntry.config(background='#D3D6DF', highlightcolor=GUI_COLORS['primary'], borderwidth=1)
                self.notesEntry.config(background='#D3D6DF', highlightcolor=GUI_COLORS['primary'], borderwidth=1)
            else:
                field.config(state=state)

     

    
    def __selection_options(self):
        if self.itemsGridview.selection()!= ():
            self.deleteoneBTN.config(state='normal')
        else:
            self.deleteoneBTN.config(state='disabled')


   


    def set_info_textarea(self, var=None, index=None, mode=None, variable=None, textarea=None):
        textarea.config(state='normal')
        textarea.delete('1.0', ttb.END)
        textarea.insert('1.0', variable.get())
        if self.window_type == 'view':
            textarea.config(state='disabled')


    def __open_client_selection(self):
        select_window = ClientModule( callback = self.__set_client_info, selectionMode=True)
        self.wait_window(select_window)
        self.grab_set()
        self.transient()

 

    def __set_client_info(self, client):
        self.B_RIF.set(client.rif)
        self.B_COMPANY.set(client.name)





    def __check_fields(self):
 
        self.B_DESCRIPTION.set(self.descriptionEntry.get('1.0', ttb.END).replace('\n',''))
        self.B_NOTES.set(self.notesEntry.get('1.0', ttb.END).replace('\n',''))

        return not '' in [value.get() for value in self.__FORM_DATA]
    

    def __open_selection_items_modals(self):
        if self.ITEM_MODE.get() == 0:
            window = ProductSelection(self, callback=self.__set_product, selectionMode=True)
        else:
            window = ServiceSelection(self, callback=self.__set_service, selectionMode=True)

    
    def __set_product(self, product):
        self.__clean()
        self.code_entry.insert(0, product.code)

        currency = self.B_CURRENCY.get()

        product_rate = 1
        document_rate = float(self.BEXCHANGERATE.get())

        if currency == 2:
            product_rate, document_rate = document_rate, product_rate
        

        set_price = lambda x: round(float(x),2) if currency == product.currency else round(float(x) * document_rate/product_rate, 2)
     
        price_1 = set_price(product.price_1)
        price_2 = set_price(product.price_2)
        price_3 = set_price(product.price_3)
        prices = list(set([price_1, price_2, price_3]))
        prices.sort(reverse=True)
        if float(0) in prices:
            prices.remove(float(0))
        self.price_combobox.config(values=prices)
        self.price_combobox.current(0)
 
        self.__itemDescription.set(product.description)
        self.__itemDepartment.set(product.get_department())
        self.__itemExistence.set(product.stock)
        self.__itemTax.set(product.get_tax())
        self.__itemBrand.set(product.get_brand())
        self.ITEM_SELECTED = product
        self.amount_entry.focus()


    def __set_service(self, service):
        self.__clean()
        self.code_entry.insert(0, service.code)
       
        currency = self.B_CURRENCY.get()

        service_rate = 1
        document_rate = float(self.BEXCHANGERATE.get())

        if currency == 2:
            service_rate, document_rate = document_rate, service_rate
        

        set_price = lambda x: round(float(x),2) if currency == service.currency else round(float(x) * document_rate/service_rate, 2)
                              
        price_1 = set_price(service.price1)
        price_2 = set_price(service.price2)
        price_3 = set_price(service.price3)
        prices = list(set([price_1, price_2, price_3]))
        prices.remove(float(0))

        self.price_combobox.config(values=prices)
        self.price_combobox.current(0)
 
        self.__itemDescription.set(service.description)
        self.__itemDepartment.set('Servicio')

        self.ITEM_SELECTED = service
        self.amount_entry.focus()

    
    def __change_item_mode(self, set_manual = 0):
        if self.ITEM_MODE.get() == 0 or set_manual == 1:
             self.item_type_label.config(text='SERVICIOS')
             self.ITEM_MODE.set(1)
        else:
             self.item_type_label.config(text='PRODUCTOS')
             self.ITEM_MODE.set(0)

    

    def billInstance(self):
        self.calculate_usdexchange()
        return Bill(
            description=self.B_DESCRIPTION.get(),
            client=self.B_RIF.get(),
            creationDate=datetime.strptime(self.B_DST.get(),'%d/%m/%Y'),
            expirationDate=datetime.strptime(self.B_EST.get(),'%d/%m/%Y'),
            currency=self.B_CURRENCY.get(),
            purchaseOrder=self.B_ORDER.get(),
            paymentStatus=1,
            sub_total=self.__subTotal.get(),
            iva=self.__iva.get(),
            total_amount=self.__total.get(),
            exchange_rate=self.BEXCHANGERATE.get(),
            notes=self.B_NOTES.get(),
            totalUSD=self.BAMOUNTUSD.get(),
            totalPaidUSD=self.BTOTALPAID.get(),
            debtUSD=self.BDEBT.get(),
            budget_code=self.B_BUDGET_CODE.get() if self.B_BUDGET_CODE.get() else None,
            creationUser=constGlobal.loggued_user.id
        )
    

    def getItemsList(self):
        items = []
        all_items = self.itemsGridview.get_children()

        for item_id in all_items:
            typeI = self.itemsGridview.item(item_id, 'text')

            values = self.itemsGridview.item(item_id, 'values')
  
            items.append({'itemType':int(typeI), 'itemId':values[0],'itemDescription':values[1],'cost':values[3],'quantity':values[4],
                          'price':values[-2], 'total_price':values[-2], 'totalUSD':values[-1],'currency':self.B_CURRENCY.get(),'date':datetime.strptime(self.B_DST.get(),'%d/%m/%Y')})
        return items
    


    def __createBill(self):
        if self.__check_item_list():
            ask = messagebox.askquestion('Procesar','Procesar Factura?', parent=self)
            if ask == 'yes':
                if self.__BILL == None:
                    self.__BILL = self.billInstance()
                    self.__BILL.create(self.getItemsList())
                    messagebox.showinfo('Aviso','Factura creada satisfactoriamente.', parent=self)
                    if self.__REJECTBILL:
                        self.__REJECTBILL.update_reject_status()
                        self.__REJECTBILL = None
                ask = messagebox.askquestion('Documento de Aceptacion','Los items asociados disponen de documentos de aceptacion?', parent=self)
                if ask=='yes':
                    window = ItemsCodePosition(self, bill=self.__BILL, )
                    self.wait_window(window)
                    if not window.success_code:
                        messagebox.showwarning('Error','No se logro completar el proceso. Los documentos no fueron asignados.', parent=self)
                        return False
                ask = messagebox.askquestion('Generar Factura en PDF', 'Desea generar un pdf de la factura?', parent=self)
                if ask == 'yes':
                    path = askdirectory(parent=self)
                    if path:
                        document = self.__BILL.create_pdf(path, parent=self)
                    else:
                        messagebox.showinfo('Aviso','Proceso Cancelado. No se genero el PDF del documento.', parent=self)
                self.destroy()
        else:
            messagebox.showwarning('Aviso','Debe selecionar los items que estaran vinculados a esta cotizacion!', parent=self)

                
    def __check_item_list(self):
        return len(self.itemsGridview.get_children()) > 0


    
    def __update_balance(self):
        total_price = 0
        for item in self.itemsGridview.get_children():
            data = self.itemsGridview.item(item, 'values')
            total_price += float(data[-2])
        self.__subTotal.set(round(total_price, 2))
        self.__iva.set(round(self.__subTotal.get()*0.16, 2))
        self.__total.set(round(self.__subTotal.get()+self.__iva.get(), 2))


    def checkItemExistInGrid(self, code, itemtype, amount,price):
        
        data = self.itemsGridview.item(f"{itemtype}-{code}",'values')
        newAmount = int(data[4])+int(amount)
        total = round(newAmount*float(price),2)
        self.itemsGridview.item(f"{itemtype}-{code}", values=(data[0],data[1],data[2],data[3],newAmount,price, total,total if self.B_CURRENCY.get() == 2 else round(float(total)/float(self.BEXCHANGERATE.get()),2),))


    def __add_product(self, amount, price):
        if amount <= self.ITEM_SELECTED.stock:
            if not f'2-{self.ITEM_SELECTED.code}' in self.itemsGridview.get_children():
                total = price*amount
                self.itemsGridview.insert("",
                id=f'2-{self.ITEM_SELECTED.code}',
                text=2,
                index=ttb.END,
                values=(self.ITEM_SELECTED.code,
                    self.ITEM_SELECTED.description,
                    'Producto',
                   self.ITEM_SELECTED.cost if self.ITEM_SELECTED.currency == 2 else round(float(self.ITEM_SELECTED.cost)/float(self.BEXCHANGERATE.get()),2),
                    amount, 
                    price, 
                    total,
                    total if self.B_CURRENCY.get() == 2 else round(float(total)/float(self.BEXCHANGERATE.get()),2),),
                )
            else:
                self.checkItemExistInGrid(code=self.ITEM_SELECTED.code,itemtype=2,amount=amount, price=price)
           
            self.ITEM_SELECTED.reduce_existence(amount)
            return True
        else:
            messagebox.showwarning("Producto",'No se dispone de suficiento stock para cubrir esta peticion.', parent=self)

    def __add_service(self, amount, price):
        if not f'1-{self.ITEM_SELECTED.code}' in self.itemsGridview.get_children():
            
                total = price*amount
                self.itemsGridview.insert("",
                id=f'1-{self.ITEM_SELECTED.code}',
                text=1, 
                index=ttb.END,
                values=(self.ITEM_SELECTED.code,
                    self.ITEM_SELECTED.description,
                    'Servicio',
                    0,
                    amount, 
                    price, 
                    total,
                    total if self.B_CURRENCY.get() == 2 else round(float(total)/float(self.BEXCHANGERATE.get()),2),),
                )
        else:
                self.checkItemExistInGrid(code=self.ITEM_SELECTED.code,itemtype=1,amount=amount, price=price)
        return True


           
   
    
    def __add_item(self):
        if not self.ITEM_SELECTED:
            messagebox.showwarning('Producto', 'Debe Seleccionar un Producto!', parent=self)
        elif not str(self.amount_entry.get()).isnumeric():
            messagebox.showwarning('Producto', 'Debe Ingresar una Cantidad valida!', parent=self)
        elif self.ITEM_SELECTED.code != self.code_entry.get():
            messagebox.showwarning('Codigo', 'El codigo no se encuentra registrado!', parent=self)
        else:

            amount = int(self.amount_entry.get())
            price = float(self.price_combobox.get())
            code_202 = False
            
            if self.ITEM_MODE.get() == 0:
                code_202 = self.__add_product( amount, price, )
            else:
                code_202 = self.__add_service(amount, price)

            if code_202:
                self.__update_balance()
                self.__clean()
                self.code_entry.focus()
           
         
        
    def __clean(self):
        self.ITEM_SELECTED = None
        self.__itemDescription.set('')
        self.__itemDepartment.set('')
        self.__itemBrand.set('')
        self.__itemExistence.set('')
        self.__itemTax.set('')
        self.code_entry.delete(0, ttb.END)
        self.price_combobox.config(values=[])
        self.price_combobox.set('')
        self.amount_entry.delete(0, ttb.END)


    def __delete_record(self, selected = None):
        if selected == None:
            selected = self.itemsGridview.focus()
        if selected:  
            
            data = self.itemsGridview.item(selected, 'values')
            ID = self.itemsGridview.item(selected, 'text')

            if int(ID) == 2:
                product_selected = Product.findOneProduct(data[0])
                product_selected.return_existence(int(data[4]))
                
            self.itemsGridview.delete(selected)
            self.__update_balance()
            


    def __delete_all_record(self):
        ask = messagebox.askquestion('Retornar','Retornar todos los elementos al inentario?', parent=self)
        if ask == 'yes':
            for record in self.itemsGridview.get_children():
                self.__delete_record(record)


    def __next_page(self):
        if self.window_type != 'view':
            if self.__check_fields():
                if float(self.BEXCHANGERATE.get())<=0:
                    self.BEXCHANGERATE.set(DB.getCurrencyValues(2))
                messagebox.showinfo('Aviso','Datos Validados. Continuar con la sección de Items.', parent=self)
            else:
                messagebox.showwarning('Aviso','Existe algunos campos por rellenar o con datos erroneos. Por favor, verificar los datos ingresados.', parent=self)
                return
        
        self.__page.set(int(self.__page.get())+1)

    
    def __set_items(self, items = None):
        self.itemsGridview.delete(*self.itemsGridview.get_children())
        for item in items:
            self.itemsGridview.insert("",
                text=item.itemType,
                index=ttb.END,
                values=(item.itemId,
                    item.itemDescription,
                    item.get_type(),
                    item.cost,
                    item.quantity, 
                    item.price, 
                    item.total_price,
                    item.totalUSD),
        )
        del items
        self.__update_balance()



    
    def calculate_usdexchange(self):
        if self.B_CURRENCY.get() == 1:
            self.BAMOUNTUSD.set(round(float(self.__total.get())/float(self.BEXCHANGERATE.get()),2))
        else:
            self.BAMOUNTUSD.set(round(float(self.__total.get()),2))

        self.BTOTALPAID.set(0)
        self.BDEBT.set(self.BAMOUNTUSD.get())

    
    def set_payments(self):

        self.__documents_paid_gridview.delete(*self.__documents_paid_gridview.get_children())
        if self.__BILL:
           
            payments = DB.findPayments(self.__BILL.code)
            for payment in payments:
                record = Payment(**payment)
                self.__documents_paid_gridview.insert("",
                        ttb.END,
                        values=(
                            record.paymentDate.strftime('%d/%m/%Y'), record.document, record.reference, record.paymentType, record.get_currency(),
                            f'{record.get_currency_icon()} {record.amount}', f"$ {record.amountUSD}",  record.exchange_rate, record.description
                        ),)
                
    def close_confirmation(self):
        if self.window_type != 'view':
            ask = messagebox.askquestion('Aviso','Desea cerrar la ventana sin guardar los datos?',parent=self)
            if ask == 'yes':
                for record in self.itemsGridview.get_children():
                    data = self.itemsGridview.item(record, 'values')
                    ID = self.itemsGridview.item(record, 'text')
                    if int(ID) == 2:
                        quantity = 0
                        if self.__BILL:
                            quantity = Item.normalQuantity(self.__BILL.code, data[0])
                        product_selected = Product.findOneProduct(data[0])
                        product_selected.return_existence(int(data[4])-quantity)
            else:
                return
        self.destroy()

    def findItem_by_entry(self):
        if self.ITEM_MODE.get() == 0:
            self.__check_product_code()
        else:
            self.__check_service_code()


    def __check_service_code(self):
        result = Service.validate_code(self.code_entry.get())
        if result:
            producto = Service.findOneService(self.code_entry.get())
            self.__set_service(producto)
        else:
            messagebox.showinfo('Servicio','El codigo registrado no se encuentra vinculado a ningun Servicio.',parent=self)
          

    def __check_product_code(self):
        result = Product.validate_code(self.code_entry.get())
        if result:
            producto = Product.findOneProduct(self.code_entry.get())
            self.__set_product(producto)
        else:
            messagebox.showinfo('Producto','El codigo registrado no se encuentra vinculado a ningun producto.',parent=self)
          

# app = ttb.Window(themename='new')
# SGDB_Style()
# BillForm(window_type='create', title='Registrar Factura')
# app.mainloop()
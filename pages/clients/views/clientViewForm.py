import ttkbootstrap as ttb
import re
from tkinter import ttk
from ttkbootstrap.scrolled import ScrolledFrame

from assets.globals import GUI_COLORS, GUI_FONT, IMG_PATH
from assets.styles.styles import SGDB_Style
from customtkinter import CTkFrame
from PIL import Image, ImageTk
from components.buttons import ButtonImage
from assets.utils import resize_icon, resize_image
import tkinter as tk
from models.entitys.client import Client
from models.entitys.bills import Bill
from pages.Extras.payments import PaymentForm
from models.entitys.payment import Payment
FGCOLOR = 'white'

class ClientView(ttb.Toplevel):
    def __init__(self, master=None, window_type = 'create', client = None, title = ''):
        super().__init__(master,)
        self.withdraw()
        self.focus()

       
        
        self.window_title = title
        self.window_type = window_type

        ######### MODAL WINDOW CONFIG #########
        self.geometry('1200x700')
        self.title(title)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.transient()
        self.grab_set()
        self.config(background="#D9D9D9")
       




        ######### VARIABLES #########
        self.__CLIENT: Client = client
       ######### VARIABLES #########

        self.__rif = ttb.StringVar()
        self.__name = ttb.StringVar()
        self.__address = ttb.StringVar()
        self.__email = ttb.StringVar()
        self.__phone = ttb.StringVar()
        self.__website = ttb.StringVar()
        self.totalDebtVar  = ttb.DoubleVar()
        self.totalPaidVar  = ttb.DoubleVar()
        self.actualDebtVar  = ttb.DoubleVar()

        self.__createWidgets()

        if self.__CLIENT:
            self.__set_provider_info()
        self.place_window_center()
        self.deiconify()
    def __createWidgets(self):
        


        

        contentFrame = CTkFrame(self, fg_color='white',border_width=1,  border_color='#CFCFCF')
        contentFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=10, pady=10)
        contentFrame.columnconfigure(0, weight=1)
        contentFrame.rowconfigure(2, weight=1)


        self.__products_icon = resize_icon(Image.open(f"{IMG_PATH}/product.png"))


        titleFrame = CTkFrame(contentFrame, fg_color='#212946')
        titleFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=8, pady=(8,0))
        titleFrame.columnconfigure(0, weight=1)
        
        ttb.Label(titleFrame, image=self.__products_icon, compound='left', text=f' {self.window_title}', font=(GUI_FONT, 14, 'bold'), foreground='white', background='#212946').grid(row=0,column=0, padx=10, pady=10, sticky='nsew')

        buttons_frame = ttb.Frame(contentFrame, style='white.TFrame')
        buttons_frame.grid(row=1, column=0, sticky='nsew', padx=16, pady=(10,4))
        buttons_frame.columnconfigure(5, weight=1)

        self.state_filter = ttb.IntVar(value=1)

        ttb.Radiobutton(buttons_frame,style='primary.Outline.Toolbutton', command=self.__set_page,  variable=self.state_filter, 
            value=1, text='Datos Generales').grid(row=0, column=1, sticky='nsew', pady=10, padx=(0,8))

        ttb.Radiobutton(buttons_frame,style='primary.Outline.Toolbutton', command=self.__set_page,  variable=self.state_filter, 
            value=2, text='Deudas').grid(row=0, column=2, sticky='nsew', pady=10, padx=(0,8))

        ttb.Radiobutton(buttons_frame,style='primary.Outline.Toolbutton', command=self.__set_page,  variable=self.state_filter, 
            value=3, text='Historial').grid(row=0, column=3, sticky='nsew', pady=10, padx=(0,8))


        ttb.Separator(buttons_frame,orient='horizontal').grid(row=1, column=0, columnspan=6, sticky='nsew', pady=(0,0), padx=4)

        self.MAIN_FRAME = tk.Frame(contentFrame)
        self.MAIN_FRAME.config(background=FGCOLOR)
        self.MAIN_FRAME.grid(row=2, column=0, sticky='nsew', padx=10, pady=(6,10))
        self.MAIN_FRAME.columnconfigure(0, weight=1)
        self.MAIN_FRAME.rowconfigure(0, weight=1)


            ########### Description Section ###########

  



        ttb.Separator(self.MAIN_FRAME, bootstyle='light').grid(row=3, column=0, sticky='nsew')


        buttonss_section_frame = tk.Frame(self.MAIN_FRAME,)
        buttonss_section_frame.configure(background=FGCOLOR)
        buttonss_section_frame.grid(row=4, column=0, pady=(8,0), sticky='nsew')
        buttonss_section_frame.anchor('e')



        closeimg = Image.open(f"{IMG_PATH}/closen.png")
        self.closeimg = ImageTk.PhotoImage(closeimg.resize(resize_image(20, closeimg.size)))
        closeimgh = Image.open(f"{IMG_PATH}/closeh.png")
        self.closeimgh = ImageTk.PhotoImage(closeimgh.resize(resize_image(20, closeimgh.size)))
        closeimgp = Image.open(f"{IMG_PATH}/closep.png")
        self.closeimgp = ImageTk.PhotoImage(closeimgp.resize(resize_image(20, closeimgp.size)))
        self.closeBTN = ButtonImage(buttonss_section_frame, image=self.closeimg, img_h=self.closeimgh, command=self.destroy, img_p=self.closeimgp, style='flatw.light.TButton', text='CERRAR', compound='center',padding=0)
        self.closeBTN.grid(row=0, column=0, sticky='nsew', pady=2, padx=(0,4))

          
        self.secondPage()
        self.thirthPage()
        self.firstPage()

   
        self.__set_page()
        self.__set_form_state('readonly')
          
        



    def __set_page(self):
        for pages in self.MAIN_FRAME.winfo_children():
            if pages.winfo_ismapped():
                pages.grid_forget()
        if self.state_filter.get() == 1:
            self.__firstPage.grid(row=0, column=0, sticky='nsew')
        elif self.state_filter.get() == 2:
            self.__secondPage.grid(row=0, column=0, sticky='nsew')
        elif self.state_filter.get() == 3:
            self.__thirthPage.grid(row=0, column=0, sticky='nsew')
        





        
        
    def __set_form_state(self, state = 'normal'):
        for field in self.FIELDS:
            field.config(state=state)
            if field.winfo_class() == 'TEntry':
                field.config(cursor='xterm')
            else:
                field.config(cursor='hand2')

    def __clean_fields(self):
        self.__CLIENT = None

        for field in self.FORM_DATA:
            field.set('')



    def firstPage(self):
        self.__firstPage = ttb.Frame(self.MAIN_FRAME, style='white.TFrame')
     
        self.__firstPage.columnconfigure(1, weight=1)

        rif_label = ttb.Label(self.__firstPage, 
                                      anchor='w', 
                                      text='RIF', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        rif_label.grid(row=0, column=0, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        self.rifEntry = ttb.Entry(self.__firstPage, textvariable=self.__rif, width=30,)
        self.rifEntry.grid(row=1, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=4, columnspan=1)


        name_label = ttb.Label(self.__firstPage, 
                                      anchor='w', 
                                      text='Nombre', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        name_label.grid(row=0, column=1, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        self.nameEntry = ttb.Entry(self.__firstPage, width=80, textvariable=self.__name)
        self.nameEntry.grid(row=1, column=1, sticky='nsew',pady=(2,0),padx=4, ipady=4, columnspan=1)


        address_label = ttb.Label(self.__firstPage, 
                                      anchor='w', 
                                      text='Direccion', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        address_label.grid(row=2, column=0, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        self.addressEntry = ttb.Entry(self.__firstPage, textvariable=self.__address, width=50,  )
        self.addressEntry.grid(row=3, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=4, columnspan=2)


        moreInfoFrame = tk.Frame(self.__firstPage)
        moreInfoFrame.config(background=FGCOLOR)
        moreInfoFrame.grid(row=4, column=0, sticky='nsew', columnspan=2, pady=(0,12), padx=4)
        moreInfoFrame.columnconfigure(0, weight=1)
        moreInfoFrame.columnconfigure(1, weight=1)
    

        email_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Correo', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=('arial',11,'bold'))
        email_label.grid(row=0, column=0, padx=(0,4), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        self.emailEntry = ttb.Entry(moreInfoFrame, textvariable=self.__email )
        self.emailEntry.grid(row=1, column=0, sticky='nsew',padx=(0,4), ipady=4,)


        phoneNumber_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Telefono', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=('arial',11,'bold'))
        phoneNumber_label.grid(row=0, column=1, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        self.phoneNumberEntry = ttb.Entry(moreInfoFrame, textvariable=self.__phone  )
        self.phoneNumberEntry.grid(row=1, column=1, sticky='nsew',padx=(4,0), ipady=4)


        website_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Pagina Web', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=('arial',11,'bold'))
        website_label.grid(row=2, column=0, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew',)
        self.websiteEntry = ttb.Entry(moreInfoFrame, textvariable=self.__website )
        self.websiteEntry.grid(row=3, column=0, sticky='nsew',padx=(0,0), ipady=4,columnspan=2)

        self.FIELDS = [self.rifEntry,self.nameEntry, self.addressEntry, self.emailEntry, self.phoneNumberEntry, self.websiteEntry]

    
    def secondPage(self):
        self.__secondPage = tk.Frame(self.MAIN_FRAME)
        self.__secondPage.config(background=FGCOLOR)
        #self.__secondPage.grid(row=0, column=0, sticky='nsew')
        self.__secondPage.columnconfigure(0, weight=1)
        self.__secondPage.rowconfigure(2, weight=1)



        DPF_menu_bar = ttb.Frame(self.__secondPage, style='white.TFrame')
        DPF_menu_bar.grid(row=0, column=0, sticky='nsew', padx=4, pady=4)
        DPF_menu_bar.columnconfigure(2, weight=1)

    
        ttb.Separator(DPF_menu_bar, 
                      orient='vertical',
                      style='custom.primary.TSeparator'
        ,).grid(row=0, column=0, padx=4, pady=6, sticky='nsew')

        viewbtnimg = Image.open(f"{IMG_PATH}/view.png")
        self.viewbtnimg = resize_icon(viewbtnimg, (50,50))

        viewbtnimgh = Image.open(f"{IMG_PATH}/viewh.png")
        self.viewbtnimgh = resize_icon(viewbtnimgh, (50,50))

        viewbtnimgp = Image.open(f"{IMG_PATH}/viewp.png")
        self.viewbtnimgp = resize_icon(viewbtnimgp, (50,50))
        ButtonImage(DPF_menu_bar, image=self.viewbtnimg, img_h=self.viewbtnimgh,  img_p=self.viewbtnimgp, style='flatw.light.TButton', padding=0, ).grid(row=0, column=1, sticky='', pady=2, padx=(0,8))

        paybtnimg = Image.open(f"{IMG_PATH}/pay.png")
        self.paybtnimg = resize_icon(paybtnimg, (50,50))

        paybtnimgh = Image.open(f"{IMG_PATH}/payh.png")
        self.paybtnimgh = resize_icon(paybtnimgh, (50,50))

        paybtnimgp = Image.open(f"{IMG_PATH}/payp.png")
        self.paybtnimgp = resize_icon(paybtnimgp, (50,50))
        ButtonImage(DPF_menu_bar, image=self.paybtnimg, img_h=self.paybtnimgh,  img_p=self.paybtnimgp, command=self.payment, style='flatw.light.TButton', padding=0).grid(row=0, column=2, sticky='nsw', pady=2, padx=(0,8))

        ttb.Separator(DPF_menu_bar, bootstyle='dark').grid(row=1, column=0, columnspan=3, sticky='nsew')


        DEBT_INFO_FRAME = ttb.Frame(self.__secondPage, style='white.TFrame')
        DEBT_INFO_FRAME.grid(row=1, column=0, sticky='nsew', padx=4, pady=4)
        DEBT_INFO_FRAME.columnconfigure(2, weight=1)

        totaldebtFrame = CTkFrame(DEBT_INFO_FRAME, fg_color=GUI_COLORS['dark'], corner_radius=3)
        totaldebtFrame.grid(row=0, column=0, sticky='nsew',pady=(0,2),padx=(0,6))

        
        ttb.Label(totaldebtFrame, 
                  text='Total Doc. por Pagar $', 
                  font=(GUI_FONT,11,'bold'),foreground='#fff',
                  bootstyle='dark inverse',
                  anchor='center', padding='4 4'
        ).grid(row=0, column=0, sticky='nsew',pady=4,padx=4)

        total_2_pay_label = ttb.Entry(DEBT_INFO_FRAME, state='readonly', width=25, justify='center', textvariable=self.totalDebtVar)
        total_2_pay_label.grid(row=1, column=0, padx=(0,6), sticky='nsew', ipady=6)


        totalpaidFrame = CTkFrame(DEBT_INFO_FRAME, fg_color=GUI_COLORS['dark'], corner_radius=3)
        totalpaidFrame.grid(row=0, column=1, sticky='nsew',pady=(0,2),padx=(0,6))

        
        ttb.Label(totalpaidFrame, 
                  text='Total Pagado $.', 
                  font=(GUI_FONT,11,'bold'),foreground='#fff',
                  bootstyle='dark inverse',
                  anchor='center', padding='4 4'
        ).grid(row=0, column=0, sticky='nsew',pady=4,padx=4)

        totalPaidEntry = ttb.Entry(DEBT_INFO_FRAME, state='readonly', width=25, justify='center', textvariable=self.totalPaidVar)
        totalPaidEntry.grid(row=1, column=1, padx=(0,6), sticky='nsew', ipady=6)



        ADF = ttb.Frame(DEBT_INFO_FRAME, style='white.TFrame')
        ADF.grid(row=0, column=2, rowspan=2, sticky='nse')

        actualDebtFrame = CTkFrame(ADF, fg_color=GUI_COLORS['primary'], corner_radius=3)
        actualDebtFrame.grid(row=0, column=0, sticky='nsew',pady=(0,2),padx=(0,6))

        
        ttb.Label(actualDebtFrame, 
                  text='Total Deuda Actual $', 
                  font=(GUI_FONT,11,'bold'),foreground='#fff',
                  bootstyle='primary inverse',
                  anchor='center', padding='4 4'
        ).grid(row=0, column=0, sticky='nsew',pady=4,padx=4)

        actualDebtEntry = ttb.Entry(ADF, state='readonly', width=25, justify='center', textvariable=self.actualDebtVar)
        actualDebtEntry.grid(row=1, column=0, padx=(0,6), sticky='nsew', ipady=6)


       

        DOCUMENT_PAYMENT_SECTION = ttb.Notebook(self.__secondPage, bootstyle='primary')
        DOCUMENT_PAYMENT_SECTION.grid(row=2, column=0, sticky='nsew',padx=4,pady=4)

        document_to_pay_list_frame = ttb.Frame(DOCUMENT_PAYMENT_SECTION, style='white.TFrame')
        document_to_pay_list_frame.rowconfigure(0, weight=1)
        document_to_pay_list_frame.columnconfigure(0, weight=1)
  
        
        yscroll = ttb.Scrollbar(document_to_pay_list_frame, 
                                orient='vertical',
                                bootstyle="dark-round")
        yscroll.grid(row=0, column=1, padx=(0,1), pady=1,sticky='ns', rowspan=2)
        
        xscroll = ttb.Scrollbar(document_to_pay_list_frame, 
                                orient='horizontal',
                                bootstyle="dark-round")
        xscroll.grid(row=1, column=0, padx=1, pady=1,sticky='ew')


        columns = ('date', 'document', 'control','expiration_date','total_bs',
                   'total_pay','total_debt','exchange_rate','total_usd',
                   'currency',)

        self.__document_2_pay_gridview = ttb.Treeview(document_to_pay_list_frame,
                                columns=columns, show='headings',
                                bootstyle='dark', 
                                height=10,
                                selectmode='extended', 
                                yscrollcommand=yscroll.set,
                                xscrollcommand=xscroll.set)
        self.__document_2_pay_gridview.grid(row=0,column=0,padx=4,pady=4,sticky='nsew')

        # self.__document_2_pay_gridview.tag_configure('checked', image=self.__checkbox_icon)
        # self.__document_2_pay_gridview.tag_configure('unchecked', image=self.__unchecked_icon)

        # self.__document_2_pay_gridview.bind('<Double-1>', self.toggleCheck)

        yscroll.configure(command=self.__document_2_pay_gridview.yview)
        xscroll.configure(command=self.__document_2_pay_gridview.xview)


        self.__document_2_pay_gridview.heading(columns[1], anchor='center', text='Fecha')
        self.__document_2_pay_gridview.heading(columns[0], anchor='center', text='Documento')
        self.__document_2_pay_gridview.heading(columns[2], anchor='center', text='Vencimiento')
        self.__document_2_pay_gridview.heading(columns[3], anchor='center', text='Estatus')
        self.__document_2_pay_gridview.heading(columns[4], anchor='center', text='Moneda')
        self.__document_2_pay_gridview.heading(columns[7], anchor='center', text='Total $')
        self.__document_2_pay_gridview.heading(columns[8], anchor='center', text='T. Pagado $')
        self.__document_2_pay_gridview.heading(columns[9], anchor='center', text='T. Deuda $')
        self.__document_2_pay_gridview.heading(columns[6], anchor='center', text='Tasa de Cambio Bs.')
        self.__document_2_pay_gridview.heading(columns[5], anchor='center', text='T. Moneda Principal')
        

        self.__document_2_pay_gridview.column(columns[0], width=140, stretch=False, anchor='center')
        self.__document_2_pay_gridview.column(columns[1], width=140, stretch=False, anchor='center')
        self.__document_2_pay_gridview.column(columns[2], width=140, stretch=False, anchor='center')
        self.__document_2_pay_gridview.column(columns[3], width=140, stretch=False, anchor='center')
        self.__document_2_pay_gridview.column(columns[4], width=140, stretch=False, anchor='center')
        self.__document_2_pay_gridview.column(columns[5], width=140, stretch=False, anchor='center')
        self.__document_2_pay_gridview.column(columns[6], width=140, stretch=False, anchor='center')
        self.__document_2_pay_gridview.column(columns[7], width=140, stretch=False, anchor='center')
        self.__document_2_pay_gridview.column(columns[8], width=160, stretch=False, anchor='center')
        self.__document_2_pay_gridview.column(columns[9], width=160, stretch=False, anchor='center')
      
       

        DOCUMENT_PAYMENT_SECTION.add(document_to_pay_list_frame, text='Documentos')


        payments_made_frame = ttb.Frame(DOCUMENT_PAYMENT_SECTION,  style='white.TFrame')
        payments_made_frame.columnconfigure(0, weight=1)
        payments_made_frame.rowconfigure(1, weight=1)


        PMDF_menu_bar = ttb.Frame(payments_made_frame, 
                                  style='white.TFrame',
                                  padding='2 2')
        PMDF_menu_bar.grid(row=0, column=0, sticky='nsew', padx=4, pady=4)

    
        
        ttb.Label(PMDF_menu_bar, text='Consulta por Documento Asociado:', font=(GUI_FONT,10,'bold'), background='#fff').grid(row=0, column=0, sticky='nsew')


        self.paymentsSearchEntry = ttb.Entry(PMDF_menu_bar,width=30)
        self.paymentsSearchEntry.grid(row=0, column=1, sticky='nsew', padx=4, pady=6)
        self.paymentsSearchEntry.bind('<Return>', lambda e:self.set_payments())

        findimg = Image.open(f"{IMG_PATH}/searchbtn.png")
        self.findimg = ImageTk.PhotoImage(findimg.resize(resize_image(16, findimg.size)))
        findimgh = Image.open(f"{IMG_PATH}/searchbtnh.png")
        self.findimgh = ImageTk.PhotoImage(findimgh.resize(resize_image(16, findimgh.size)))
        findimgp = Image.open(f"{IMG_PATH}/searchbtnp.png")
        self.findimgp = ImageTk.PhotoImage(findimgp.resize(resize_image(16, findimgp.size)))

        self.findBTN = ButtonImage(PMDF_menu_bar, command=lambda:self.set_payments(),image=self.findimg, img_h=self.findimgh, img_p=self.findimgp, style='flatw.light.TButton', padding=0)
        self.findBTN.grid(row=0, column=2, sticky='', padx=(0,0))


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

    
    
      
        DOCUMENT_PAYMENT_SECTION.add(payments_made_frame, text='Pagos Efectuados')

    def set_documents(self, table = None, documentsFunc = None):
        table.delete(*table.get_children())
        if self.__CLIENT:
            documents = documentsFunc()
            for document in documents:
                bill = Bill(**document)

       

                totalMain = float(bill.total_amount)
                totalPaidUSD = round(float(bill.totalPaidUSD), 2)
                debtUSD = round(float(bill.debtUSD), 2)
                totalUSD = float(bill.totalUSD)
  
                table.insert("",
                        ttb.END,
                        values=(bill.code, bill.creationDate.strftime('%d/%m/%Y'),
                            bill.expirationDate.strftime('%d/%m/%Y'), bill.get_documentState(), 
                            bill.get_currency(), totalUSD, totalPaidUSD, debtUSD, bill.exchange_rate, totalMain), 
                        )

    def thirthPage(self):

        self.__thirthPage = tk.Frame(self.MAIN_FRAME)
        self.__thirthPage.config(background=FGCOLOR)
        #self.__thirthPage.grid(row=0, column=0, sticky='nsew')
        self.__thirthPage.columnconfigure(0, weight=1)
        self.__thirthPage.rowconfigure(1, weight=1)


        DRF_menu_bar = ttb.Frame(self.__thirthPage, 
                             style='white.TFrame',
                             padding='2 2')
        DRF_menu_bar.grid(row=0, column=0, sticky='nsew', padx=4, pady=4)


        range_selection_frame = ttb.Frame(DRF_menu_bar, style='white.TFrame')
        range_selection_frame.grid(row=0, column=0, sticky='nsew', padx=4, pady=4)
        

        ttb.Label(range_selection_frame,
                  text='Desde', background='#fff',
                  font=(GUI_FONT,10, 'bold')
        ).grid(row=0,column=0,sticky='nsew',padx=2, pady=2)

        self.start_date = ttb.DateEntry(range_selection_frame, dateformat='%d/%m/%Y',
                                   bootstyle='info')
        self.start_date.entry.config(textvariable=self.start_date)
        self.start_date.grid(row=0, column=1, padx=2)


        ttb.Label(range_selection_frame,
                  text='Hasta', background='#fff',
                   font=(GUI_FONT,10, 'bold')
        ).grid(row=0,column=2,sticky='nsew',padx=2, pady=2)

        self.end_date = ttb.DateEntry(range_selection_frame,dateformat='%d/%m/%Y',
                                   bootstyle='info')
        self.end_date.entry.config(textvariable=self.end_date)
        self.end_date.grid(row=0, column=3, padx=2)

        ttb.Separator(DRF_menu_bar, bootstyle='dark', orient='vertical').grid(row=0, column=1, padx=4)

        ttb.Label(DRF_menu_bar, text='Documento:', font=(GUI_FONT,11,'bold'), background='#fff').grid(row=0, column=2, sticky='nsew')


        self.SEARCHENTRY = ttb.Entry(DRF_menu_bar,width=30)
        self.SEARCHENTRY.grid(row=0, column=3, sticky='nsew', padx=4, pady=6)

        findimg = Image.open(f"{IMG_PATH}/searchbtn.png")
        self.findimg = ImageTk.PhotoImage(findimg.resize(resize_image(16, findimg.size)))
        findimgh = Image.open(f"{IMG_PATH}/searchbtnh.png")
        self.findimgh = ImageTk.PhotoImage(findimgh.resize(resize_image(16, findimgh.size)))
        findimgp = Image.open(f"{IMG_PATH}/searchbtnp.png")
        self.findimgp = ImageTk.PhotoImage(findimgp.resize(resize_image(16, findimgp.size)))

        self.findBTN = ButtonImage(DRF_menu_bar,   image=self.findimg, img_h=self.findimgh, img_p=self.findimgp, style='flatw.light.TButton', padding=0)
        self.findBTN.grid(row=0, column=4, sticky='', padx=(0,0))



    

        # row=2,column=0,padx=4,pady=4,sticky='nsew')
        
        document_all_list = ttb.Frame(self.__thirthPage)
        document_all_list.grid(row=1,column=0,padx=4,pady=4,sticky='nsew')
        document_all_list.rowconfigure(0, weight=1)
        document_all_list.columnconfigure(0, weight=1)

        yscroll = ttb.Scrollbar(document_all_list, 
                                orient='vertical',
                                bootstyle="dark-round")
        yscroll.grid(row=0, column=1, padx=(0,1), pady=1,sticky='ns', rowspan=2)
        
        xscroll = ttb.Scrollbar(document_all_list, 
                                orient='horizontal',
                                bootstyle="dark-round")
        xscroll.grid(row=1, column=0, padx=1, pady=1,sticky='ew')


        columns = ('date', 'document', 'control','expiration_date','total_bs',
                   'total_pay','total_debt','category','exchange_rate','total_usd',
                   )

        self.__document_all__gridview = ttb.Treeview(document_all_list,
                                columns=columns,show='headings',
                                bootstyle='dark', 
                                height=10,
                                selectmode='extended', 
                                yscrollcommand=yscroll.set,
                                xscrollcommand=xscroll.set)
        self.__document_all__gridview.grid(row=0,column=0,padx=4,pady=4,sticky='nsew')

        # self.__document_all__gridview.tag_configure('checked', image=self.__checkbox_icon)
        # self.__document_all__gridview.tag_configure('unchecked', image=self.__unchecked_icon)

        # self.__document_all__gridview.bind('<Double-1>', self.toggleCheck)

        yscroll.configure(command=self.__document_all__gridview.yview)
        xscroll.configure(command=self.__document_all__gridview.xview)


        self.__document_all__gridview.heading("#0",anchor='center', text='Aplicar')
        self.__document_all__gridview.heading(columns[1], anchor='center', text='Fecha')
        self.__document_all__gridview.heading(columns[0], anchor='center', text='Documento')
        self.__document_all__gridview.heading(columns[2], anchor='center', text='Vencimiento')
        self.__document_all__gridview.heading(columns[3], anchor='center', text='Estatus')
        self.__document_all__gridview.heading(columns[4], anchor='center', text='Moneda')
        self.__document_all__gridview.heading(columns[7], anchor='center', text='Total $')
        self.__document_all__gridview.heading(columns[8], anchor='center', text='T. Pagado $')
        self.__document_all__gridview.heading(columns[9], anchor='center', text='T. Deuda $')
        self.__document_all__gridview.heading(columns[6], anchor='center', text='Tasa de Cambio Bs.')
        self.__document_all__gridview.heading(columns[5], anchor='center', text='T. Moneda Principal')
        

        self.__document_all__gridview.column('#0', width=0, stretch=False, anchor='center')
        self.__document_all__gridview.column(columns[0], width=140, stretch=False, anchor='center')
        self.__document_all__gridview.column(columns[1], width=140, stretch=False, anchor='center')
        self.__document_all__gridview.column(columns[2], width=140, stretch=False, anchor='center')
        self.__document_all__gridview.column(columns[3], width=140, stretch=False, anchor='center')
        self.__document_all__gridview.column(columns[4], width=140, stretch=False, anchor='center')
        self.__document_all__gridview.column(columns[5], width=140, stretch=False, anchor='center')
        self.__document_all__gridview.column(columns[6], width=140, stretch=False, anchor='center')
        self.__document_all__gridview.column(columns[7], width=140, stretch=False, anchor='center')
        self.__document_all__gridview.column(columns[8], width=160, stretch=False, anchor='center')
        self.__document_all__gridview.column(columns[9], width=160, stretch=False, anchor='center')
   


        self.__document_all__gridview.tag_configure('paid', background='white')
        self.__document_all__gridview.tag_configure('debt', background='#FFBDBD')


    def __set_provider_info(self):
        self.__rif.set(self.__CLIENT.rif)
        self.__name.set(self.__CLIENT.name)
        self.__address.set(self.__CLIENT.address)
        self.__email.set(self.__CLIENT.email)
        self.__phone.set(self.__CLIENT.phone)
        self.__website.set(self.__CLIENT.website)
        self.set_documents(self.__document_2_pay_gridview, self.__CLIENT.get_debit_documents)
        self.set_documents(self.__document_all__gridview, self.__CLIENT.get_all_documents)
        self.set_payments()
        self.update_balance()

    def payment(self):
        documentSelected = self.__document_2_pay_gridview.focus()
        if documentSelected:
            value = self.__document_2_pay_gridview.item(documentSelected, 'values')
            document = Bill.findOneBill(int(value[0]))
            paymentWindow = PaymentForm(self, doc=document, callback = self.__set_provider_info)
            self.wait_window(paymentWindow)
            self.grab_set()
            self.transient()
        

    def set_payments(self):

        self.__documents_paid_gridview.delete(*self.__documents_paid_gridview.get_children())
        if self.__CLIENT:
           
            payments = self.__CLIENT.get_payments_records(self.paymentsSearchEntry.get())
            for payment in payments:
                record = Payment(**payment)
                self.__documents_paid_gridview.insert("",
                        ttb.END,
                        values=(
                            record.paymentDate.strftime('%d/%m/%Y'), record.document, record.reference, record.paymentType, record.get_currency(),
                            f'{record.get_currency_icon()} {record.amount}', f"$ {record.amountUSD}",  record.exchange_rate, record.description
                        ),)
                
    def update_balance(self):
        self.totalDebtVar.set(self.__CLIENT.get_total_debt())
        self.actualDebtVar.set(self.__CLIENT.get_actual_debt())
        self.totalPaidVar.set(self.__CLIENT.get_total_paid()) 

# app = ttb.Window(themename='new')
# SGDB_Style()
# ProductForm(window_type='edit', title='Modificar Producto')
# app.mainloop()
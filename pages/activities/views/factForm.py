import ttkbootstrap as ttb
from assets.globals import GUI_COLORS, IMG_PATH, GUI_FONT
from assets.utils import resize_image
from PIL import Image, ImageTk
from tkinter import messagebox
import tkinter as tk
from components.buttons import ButtonImage
from models.entitys.activity import Activity
from customtkinter import CTkFrame 
from assets.db.db_connection import DB
from assets.styles.styles import SGDB_Style
from datetime import datetime,timedelta
from models.entitys.bills import Bill
from models.entitys.activity import Activity
from pages.bills.views.itemscode import ItemsCodePosition
from assets.globals import on_combobox_change, validateFloat
import assets.globals as constGlobal
from tkinter.filedialog import askdirectory
FGCOLOR = 'white'


class FactForm(ttb.Toplevel):
    def __init__(self, master=None, activity = None, callback = None):
        super().__init__(master)
        SGDB_Style()
         
        self.callback = callback
        self.__ACTIVITY: Activity = activity
        self.__BILL = None
        ### VARS ####

        self.code_var = ttb.StringVar(value=self.__ACTIVITY.id)
        self.description_var = ttb.StringVar(value=self.__ACTIVITY.description)
        code = self.__ACTIVITY.budget_code
        self.budgetCode_var = ttb.StringVar(value=f"{'0'*(6-len(str(code)))+str(code)}")
        
        self.rif_var = ttb.StringVar(value=self.__ACTIVITY.client)
        self.client_var = ttb.StringVar(value=self.__ACTIVITY.get_client()[0])
        self.purchaseOrder_var = ttb.StringVar(value=self.__ACTIVITY.get_purchaseOrder())
        self.addres_var = ttb.StringVar(value=self.__ACTIVITY.address)
        self.date_var = ttb.StringVar(value=datetime.today().strftime('%d/%m/%Y'))
        self.enddate_var = ttb.StringVar()
        self.exchange_var = ttb.StringVar()

        values = self.__ACTIVITY.get_totals()
        self.__currency = ttb.IntVar()
        self.__currencyName = ttb.StringVar
        self.currency_var = ttb.StringVar(value=self.__ACTIVITY.get_currency(values[0]))
        self.currencyId_var = ttb.IntVar(value=values[0])
        self.budget_sub_total_var = ttb.StringVar(value=values[1])
        self.budget_iva_var = ttb.StringVar(value=values[2])
        self.budget_total_var = ttb.StringVar(value=values[3])
        self.BAMOUNTUSD = ttb.StringVar(value=0)
        self.BDEBT = ttb.DoubleVar(value=0)
        self.BTOTALPAID = ttb.DoubleVar(value=0)

        CURRENCY =  DB.getCurrencyList()
        self.CURRENCY_DICT = {row[1]:row[0] for row in CURRENCY}
        self.CURRENCY_DICT_VALUE = {row[0]:row[2] for row in CURRENCY}
        del CURRENCY

      
        self.create_widgets()

        self.title('Detalles de Actividad')
        # 
        self.config(background='#D0CECE')
        self.withdraw()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)  
        self.grab_set()
        self.transient()
        self.focus()
        self.anchor('center')

        self.place_window_center()
        self.iconbitmap('SIGAG.ico')
        self.deiconify()


    def create_widgets(self):

        contentFrame = CTkFrame(self, fg_color='white',border_width=1,  border_color='#CFCFCF')
        contentFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=10, pady=10)
        

       # self.__services_icon = resize_icon(Image.open(f"{IMG_PATH}/project.png"))


        titleFrame = CTkFrame(contentFrame, fg_color=GUI_COLORS['danger'])
        titleFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=8, pady=(8,0))
        ttb.Label(titleFrame,  compound='left', text=' Facturación', font=(GUI_FONT, 14, 'bold'), foreground='white', background=GUI_COLORS['danger']).grid(row=0,column=0, padx=10, pady=10, sticky='nsew')


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


        creatbtnimg = Image.open(f"{IMG_PATH}/registrar.png")
        self.creatbtnimg = ImageTk.PhotoImage(creatbtnimg.resize(resize_image(20, creatbtnimg.size)))
        creatbtnimgh = Image.open(f"{IMG_PATH}/registrarh.png")
        self.creatbtnimgh = ImageTk.PhotoImage(creatbtnimgh.resize(resize_image(20, creatbtnimgh.size)))
        creatbtnimgp = Image.open(f"{IMG_PATH}/registrarp.png")
        self.creatbtnimgp = ImageTk.PhotoImage(creatbtnimgp.resize(resize_image(20, creatbtnimgp.size)))

        self.createBTN = ButtonImage(buttonss_section_frame,  image=self.creatbtnimg, command=self.facturar,
                                     img_h=self.creatbtnimgh, img_p=self.creatbtnimgp, style='flatw.light.TButton', 
                                     text='FACTURAR', compound='center',padding=0)
        self.createBTN.grid(row=0, column=2, sticky='nsew', pady=2, padx=(0,4))

        self.__form()
        

   
     
    def __form(self):
        
      


        mainInforFrame = tk.Frame(self.mainContent)
        mainInforFrame.config(background=FGCOLOR)
        mainInforFrame.grid(row=0, column=0, sticky='nsew', pady=(0,2))
        mainInforFrame.columnconfigure(0, weight=1)
        mainInforFrame.columnconfigure(1, weight=1)
        mainInforFrame.columnconfigure(2, weight=1)

        code_label = ttb.Label(mainInforFrame, 
                                      anchor='w', 
                                      text='Codigo', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=(GUI_FONT,11,'bold'))
        code_label.grid(row=0, column=0, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.codeEntry = ttb.Entry(mainInforFrame, 
                                       state='readonly', justify='center',
                                       textvariable=self.code_var
                                      )
        self.codeEntry.grid(row=1, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=4, columnspan=1)


        purchaseOrder_label = ttb.Label(mainInforFrame, 
                                      anchor='w', 
                                      text='Orden de Compra', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=(GUI_FONT,11,'bold'))
        purchaseOrder_label.grid(row=0, column=1, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.purchaseOrderEntry = ttb.Entry(mainInforFrame, 
                                        state='readonly',justify='center',
                                        textvariable=self.purchaseOrder_var
                                      )
        self.purchaseOrderEntry.grid(row=1, column=1, sticky='nsew',pady=(2,0),padx=4, ipady=4, columnspan=1)


        rif_label = ttb.Label(mainInforFrame, 
                                      anchor='w', 
                                      text='RIF (Cliente)', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=(GUI_FONT,11,'bold'))
        rif_label.grid(row=2, column=0, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.rifEntry = ttb.Entry(mainInforFrame, 
                                       state='readonly',justify='center',
                                       textvariable=self.rif_var
                                      )
        self.rifEntry.grid(row=3, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=4,)



        budgetCode_label = ttb.Label(mainInforFrame, 
                                      anchor='w', 
                                      text='Cotizacion Vinculada', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=(GUI_FONT,11,'bold'))
        budgetCode_label.grid(row=2, column=1, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.budgetCodeEntry = ttb.Entry(mainInforFrame, 
                                       state='readonly',justify='center',
                                       textvariable=self.budgetCode_var
                                      )
        self.budgetCodeEntry.grid(row=3, column=1, sticky='nsew',pady=(2,0),padx=4, ipady=4,)





        client_label = ttb.Label(mainInforFrame, 
                                      anchor='w', 
                                      text='Cliente', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=(GUI_FONT,11,'bold'))
        client_label.grid(row=4, column=0, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew',columnspan=2)

        self.clientEntry = ttb.Entry(mainInforFrame, 
                                       state='readonly',
                                       textvariable=self.client_var
                                      )
        self.clientEntry.grid(row=5, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=4,columnspan=2)
        
    
        dateframe = tk.Frame(mainInforFrame)
        dateframe.config(background=FGCOLOR)
        dateframe.grid(row=6, column=0, sticky='nsew', pady=(0,2), columnspan=2)
        dateframe.columnconfigure(0, weight=1)
        dateframe.columnconfigure(1, weight=1)
        


        date_label = ttb.Label(dateframe, 
                                      anchor='w', 
                                      text='Fecha de Emisión', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=(GUI_FONT,11,'bold'))
        date_label.grid(row=0, column=0,  padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.dateEntry = ttb.Entry(dateframe, state='readonly',
                                       textvariable=self.date_var
                                      )
        self.dateEntry.grid(row=1, column=0,  sticky='nsew',pady=(2,0),padx=4, ipady=0,)


        endDate_label = ttb.Label(dateframe, 
                                      anchor='w', 
                                      text='Fecha de Vencimiento', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=(GUI_FONT,11,'bold'))
        endDate_label.grid(row=0, column=1, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.endDateEntry = ttb.DateEntry(dateframe, dateformat='%d/%m/%Y', startdate=datetime.today()+timedelta(days=30))
        self.endDateEntry.grid(row=1, column=1, sticky='nsew',pady=(2,0),padx=4, ipady=0,)







        initialCurrency_label = ttb.Label(mainInforFrame, 
                                      anchor='w', 
                                      text='Moneda Inicial', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=(GUI_FONT,11,'bold'))
        initialCurrency_label.grid(row=7, column=0, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.initialCurrencyEntry = ttb.Entry(mainInforFrame, 
                                       state='readonly',justify='center',
                                       textvariable=self.currency_var
                                      )
        self.initialCurrencyEntry.grid(row=8, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=4,)



        subtotal_label = ttb.Label(mainInforFrame, 
                                      anchor='w', 
                                      text='Sub Total', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=(GUI_FONT,11,'bold'))
        subtotal_label.grid(row=7, column=1, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.subtotalEntry = ttb.Entry(mainInforFrame, 
                                       state='readonly', justify='center',
                                       textvariable=self.budget_sub_total_var
                                      )
        self.subtotalEntry.grid(row=8, column=1, sticky='nsew',pady=(2,0),padx=4, ipady=4,)


        iva_label = ttb.Label(mainInforFrame, 
                                      anchor='w', 
                                      text='IVA', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=(GUI_FONT,11,'bold'))
        iva_label.grid(row=9, column=0, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.ivaEntry = ttb.Entry(mainInforFrame, 
                                       state='readonly',justify='center',
                                       textvariable=self.budget_iva_var
                                      )
        self.ivaEntry.grid(row=10, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=4,)



        total_label = ttb.Label(mainInforFrame, 
                                      anchor='w', 
                                      text='Total', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=(GUI_FONT,11,'bold'))
        total_label.grid(row=9, column=1, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.totalEntry = ttb.Entry(mainInforFrame, 
                                       state='readonly',justify='center',
                                       textvariable=self.budget_total_var
                                      )
        self.totalEntry.grid(row=10, column=1, sticky='nsew',pady=(2,0),padx=4, ipady=4,)


        notes_label = ttb.Label(mainInforFrame, 
                                      anchor='w', 
                                      text='Nota', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=(GUI_FONT,11,'bold'))
        notes_label.grid(row=11, column=0, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew', columnspan=2)

        self.notesEntry = ttb.Text(mainInforFrame, height=3)
        self.notesEntry.grid(row=12, column=0, sticky='nsew',pady=(2,4),padx=4, ipady=4, columnspan=2)
        self.notesEntry.config(highlightbackground=GUI_COLORS['info'], highlightthickness=1)
      
        currency_section = ttb.Frame(mainInforFrame, style='white.TFrame')
        currency_section.grid(row=14, column=0, sticky='nsw',pady=(2,8),padx=4, columnspan=2)


        currency_label = ttb.Label(currency_section, 
                                   anchor='w', 
                                   text='Moneda', 
                                   background=FGCOLOR,
                                   font=(GUI_FONT,11,'bold'))
        currency_label.grid(row=0, column=0, padx=5, pady=(4,0), ipadx=8,  ipady=4,sticky='nsew')

        self.currencyCombobox = ttb.Combobox(currency_section, values=list(self.CURRENCY_DICT.keys()), state='readonly', style='selectionOnly.TCombobox', textvariable=self.__currencyName, font=(GUI_FONT,10,'bold'))
        self.currencyCombobox.grid(row=1, column=0, padx=(4,10), pady=(4,0), sticky='nsew')
        self.currencyCombobox.bind("<<ComboboxSelected>>", lambda e: on_combobox_change(e,self.__currency, self.CURRENCY_DICT, self.currencyCombobox))
        self.currencyCombobox.current(0)
        self.__currency.set(1)

        exchangerate_label = ttb.Label(currency_section, 
                                      anchor='w', 
                                      text='Tasa de Cambio $', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=(GUI_FONT,11,'bold'))
        exchangerate_label.grid(row=0, column=1, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.exchangerateEntryDollar = ttb.Entry(currency_section, width=18, validate="key",validatecommand=(self.register(validateFloat), "%P"), justify='center', textvariable=self.exchange_var,)
        self.exchangerateEntryDollar.grid(row=1, column=1, sticky='nsew',pady=(4,0),padx=4, columnspan=1)
        self.exchangerateEntryDollar.insert(0,DB.getCurrencyValues())

    def facturar(self):
        if self.__BILL == None:
            self.__BILL = self.__billInstance()
            self.__BILL.create()
        ask = messagebox.askquestion('Documento de Aceptacion','Los items asociados disponen de documentos de aceptacion?', parent=self)
        if ask=='yes':
           
            window = ItemsCodePosition(self, bill=self.__BILL, )
            self.wait_window(window)
            
            if not window.success_code:
                messagebox.showwarning('Error','No se logro completar el proceso. Los documentos no fueron asignados.', parent=self)
                return False
        ask = messagebox.askquestion('Generar Factura en PDF', 'Desea generar un pdf de la factura?', parent=self)
        if ask == 'yes':
            path_to_save = askdirectory(parent=self)
            if path_to_save:
                self.__BILL.create_pdf(path_to_save, self)
            else:
                messagebox.showinfo('Aviso','Proceso Cancelado. No se genero el PDF del documento.', parent=self)
        self.destroy()
        self.callback()
        self.__BILL = None

    def calculate_usdexchange(self):
        if self.__currency.get() == 1:
            self.BAMOUNTUSD.set(round(float(self.budget_total_var.get())/float(self.exchange_var.get()),2))
        else:
            self.BAMOUNTUSD.set(round(float(self.budget_total_var.get()),2))

        self.BTOTALPAID.set(0)
        self.BDEBT.set(self.BAMOUNTUSD.get())


    def __billInstance(self):

        service_rate = 1
        document_rate = float(self.exchange_var.get())

        if self.__currency.get() == 2:
            service_rate, document_rate = document_rate, service_rate
        
        
        exchanger = lambda x: round(float(x),2) if self.currencyId_var.get() == self.__currency.get() else round(float(x) * document_rate/service_rate, 2)
        usdexchanger = lambda x: round(float(x),2) if self.currencyId_var.get() == 2 else round(float(x) /float(self.exchange_var.get()), 2)

        price_1 = exchanger(self.budget_sub_total_var.get())
        price_2 = exchanger(self.budget_iva_var.get())
        price_3 = exchanger(self.budget_total_var.get())
        price_4 = usdexchanger(self.budget_total_var.get())
    
        self.calculate_usdexchange()
        return Bill(
            description=self.description_var.get(),
            client=self.__ACTIVITY.client,
            currency=self.__currency.get(),
            purchaseOrder=self.purchaseOrder_var.get(),
            budget_code=self.budgetCode_var.get(),
            paymentStatus=1,
            sub_total=price_1,
            iva=price_2,
            total_amount=price_3,
            exchange_rate=self.exchange_var.get(),
            notes=self.notesEntry.get('1.0', ttb.END),
            expirationDate=datetime.strptime(self.endDateEntry.entry.get(),'%d/%m/%Y'),
            creationDate=datetime.strptime(self.dateEntry.get(),'%d/%m/%Y'),
            totalUSD=price_4,
            totalPaidUSD=0,
            debtUSD=price_4,
            creationUser=constGlobal.loggued_user.id
            )


# app =ttb.Window(themename='new')
# ac = Activity.findOneActivity(id=1)
# FactForm(app, activity=ac)

# app.mainloop()
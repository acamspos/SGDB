import ttkbootstrap as ttb
from assets.globals import GUI_COLORS, IMG_PATH
from assets.styles.styles import SGDB_Style
from assets.globals import minus_icon, plus_icon,delete_all_icon, money_icon, checked_icon, log_out_icon,indicator_icon, save_icon, cancel_icon, edit_icon,currency_icon
from assets.utils import resize_icon
from ttkbootstrap.tooltip import ToolTip
from tkinter import messagebox
import datetime
from models.entitys.bills import Bill
from models.entitys.payment import Payment
from models.entitys.purchase import PurchaseDocument
from assets.db.db_connection import DB

def checkDATE(var):
    try:
        datetime.strptime(var.get(),'%d/%m/%Y')
        return True
    except ValueError:
        var.set(datetime.today().strftime('%d/%m/%Y'))


def on_combobox_change(event, var, dictionary, combobox):
    ID = dictionary[combobox.get()]
    var.set(ID)


def on_validate(P, lenght = 20):
    # Verificar que la longitud del contenido no supere cierto límite
    return len(P) <= lenght  

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def validateInput(text):
        if text in '0123456789.' or isfloat(text):
            return True
        return False

def check_float_value(var=None, moder=None, indexr=None, value=None):
    if not isfloat(value.get()):
        value.set(value.get()[:-1])

class PaymentForm(ttb.Toplevel):
    def __init__(self, master = None, doc:PurchaseDocument | Bill= None, callback=None, full_payment_required = False):
        super().__init__(master, toolwindow=True)
        self.title('Registro de Pagos')
        vcmd = (self.register(lambda e: on_validate(e,lenght=10)), '%P')
        self.full_payment_required = full_payment_required
        ######### VARIABLES #########
        self.callback = callback
        self.__DOCUMENT:Bill = doc
        self.PAYMENT_AMOUNT = ttb.StringVar()
        self.PAYMENT_AMOUNT.trace_add('write',lambda v,i,m: check_float_value(v,i,m,value=self.PAYMENT_AMOUNT))
        self.PAYMENT_REFERENCES = ttb.StringVar()
        self.PAYMENT_EXCHANGE = ttb.StringVar()
        self.PAYMENT_EXCHANGE.trace_add('write',lambda v,i,m: check_float_value(v,i,m,value=self.PAYMENT_EXCHANGE))

   
        if type(doc) == Bill:
            self.doc_date = ttb.StringVar(value=self.__DOCUMENT.creationDate.strftime('%d/%m/%Y'))
        else:
            self.doc_date = ttb.StringVar(value=self.__DOCUMENT.dateOfIssue.strftime('%d/%m/%Y'))

        self.PAYMENT_DATE = ttb.StringVar(value=datetime.datetime.today().strftime('%d/%m/%Y'))

        self.doc_code = ttb.StringVar(value=self.__DOCUMENT.code)
        
        self.doc_exchange = ttb.StringVar(value=self.__DOCUMENT.exchange_rate if type(doc) == Bill else self.__DOCUMENT.exchangeRate)
        self.doc_total_debt = ttb.DoubleVar(value=f"{self.__DOCUMENT.get_currency()}{self.__DOCUMENT.totalUSD}")
        self.doc_debt_paid = ttb.DoubleVar(value=self.__DOCUMENT.totalPaidUSD)
        



        self.totalDebt = ttb.StringVar()
        self.totalDebt.trace_add('write',lambda v,i,m: self.calculateExchange(self.totalDebtExchange, self.totalDebt))
        self.totalDebtExchange = ttb.StringVar()
        

        self.actualDebt = ttb.StringVar()
        self.actualDebt.trace_add('write',lambda v,i,m: self.calculateExchange(self.actualDebtExchange, self.actualDebt))
        self.actualDebtExchange = ttb.StringVar()

        
        
        if self.__DOCUMENT.documentCondition == 'CONTADO':
            self.actualDebt.set(self.__DOCUMENT.totalUSD)
        else:
            self.actualDebt.set(self.__DOCUMENT.debtUSD)
        self.totalDebt.set(self.__DOCUMENT.totalUSD)



        self.totalToPay = ttb.StringVar(value=float(0))
        self.totalToPayExchange= ttb.StringVar(value=float(0))
        self.totalToPay.trace_add('write',lambda v,i,m: self.calculateExchange(self.totalToPayExchange, self.totalToPay))
     
        self.__currency = ttb.StringVar()
        self.__currency.trace_add('write', lambda v,i,m: self.check_exchangerate())
        
        
        ######### MODAL WINDOW CONFIG #########
        self.columnconfigure(0, weight=1)
        self.transient()
        self.grab_set()

        self.row_selected = None
       
        ######### GUI ICONS #########
        import PIL.Image as Im
        self.__delete_icon = resize_icon(Im.open(f"{IMG_PATH}/deleteone.png"), icon_size=(50,50))
        self.__delete_all_icon = resize_icon(Im.open(f"{IMG_PATH}/deleten.png"), icon_size=(50,50))
        self.__add_icon = resize_icon(Im.open(f"{IMG_PATH}/additem.png"), icon_size=(49,49))
        self.__money_icon = resize_icon(money_icon, icon_size=(80,80))
        self.__log_out_icon = resize_icon(log_out_icon)
        self.__checked_icon = resize_icon(checked_icon)
        self.__indicator_icon = resize_icon(indicator_icon, icon_size=(15,15))


        ###### TITLE SECTION ######
        page_title = ttb.Label(self, 
                               text=' PAGO DOCUMENTO', 
                               bootstyle='primary inverse', 
                               font=('arial',12, 'bold'), 
                               anchor='center')
        page_title.grid(row=0, column=0, ipady=5,  sticky='nsew')

        INFO_FRAME = ttb.Frame(self)
        INFO_FRAME.grid(row=1, column=0, sticky='nsew', padx=6, pady=4)

        FUNDS_SELECTION_FRAME = ttb.LabelFrame(INFO_FRAME, 
                                               text='Origen de Fondos', 
                                               padding='10 5')
        FUNDS_SELECTION_FRAME.grid(row=0, column=0, sticky='nsew', columnspan=2)
        FUNDS_SELECTION_FRAME.columnconfigure(0,weight=1)


        ttb.Label(FUNDS_SELECTION_FRAME, 
                  text='Documento', 
                  font=('arial',11,'bold'), 
                  bootstyle='danger'
        ).grid(row=0, column=0, sticky='nsew', pady=(12,6))

        self.doctEntry = ttb.Entry(FUNDS_SELECTION_FRAME, state='readonly', justify='center',
                     width=15, textvariable=self.doc_code)
        self.doctEntry.grid(row=1, column=0, ipady=4,padx=(0,6), sticky='nsew')


        ttb.Label(FUNDS_SELECTION_FRAME, 
                  text='Fecha del Pago', 
                  font=('arial',11,'bold'), 
                  bootstyle='danger'
        ).grid(row=0, column=1, sticky='nsew', pady=(12,6))

        self.dateEntry = ttb.DateEntry(FUNDS_SELECTION_FRAME,startdate=datetime.datetime.today(), dateformat='%d/%m/%Y')
        self.dateEntry.grid(row=1, column=1, ipady=4,padx=(0,6), sticky='nsew')
        self.dateEntry.entry.config(textvariable=self.PAYMENT_DATE, justify='center')
        self.dateEntry.entry.bind('<FocusOut>', lambda e: checkDATE(self.PAYMENT_DATE))


        ttb.Label(FUNDS_SELECTION_FRAME, 
                  text='Referencia', 
                  font=('arial',11,'bold'), 
                  bootstyle='danger'
        ).grid(row=0, column=2, sticky='nsew', pady=(12,6))

        self.REFERENCES_ENTRY = ttb.Entry(FUNDS_SELECTION_FRAME, textvariable=self.PAYMENT_REFERENCES, justify='center',
                                          validate="key", validatecommand=vcmd)
        self.REFERENCES_ENTRY.grid(row=1, column=2, ipady=4,padx=(0,6), sticky='nsew')


        ttb.Label(FUNDS_SELECTION_FRAME, 
                  text='Metodos de Pago', 
                  font=('arial',11,'bold'), 
                  bootstyle='danger'
        ).grid(row=2, column=0, sticky='nsew', pady=(12,6))

        PAYMENTS_METHODS = {'Transferencia Nacional':'Bs.',
                            'Transferencia Internacional USD':'USD $', 
                            'Pago movil':'Bs.', 
                            'Efectivo USD $':'USD $',
                            'Zelle':'USD $'}
        
        self.CURRENCYS_ID = {'Bs.':1,'USD $':2}

        self.COMBOBOX_FUNDS = ttb.Combobox(FUNDS_SELECTION_FRAME, 
            
                     style='selectionOnly.TCombobox',
                     values=list(PAYMENTS_METHODS.keys()),
                     state='readonly')
        self.COMBOBOX_FUNDS.grid(row=3, column=0,padx=(0,6), sticky='nsew')
        self.COMBOBOX_FUNDS.bind("<<ComboboxSelected>>", lambda e: on_combobox_change(e,self.__currency, PAYMENTS_METHODS, self.COMBOBOX_FUNDS))
        self.COMBOBOX_FUNDS.current(0)
        self.__currency.set('Bs.')


        ttb.Label(FUNDS_SELECTION_FRAME, 
                  text='Monto a Ingresar', 
                  font=('arial',11,'bold'), 
                  bootstyle='danger'
        ).grid(row=2, column=2, sticky='nsew', pady=(12,6))

        self.AMOUNT_ENTRY = ttb.Entry(FUNDS_SELECTION_FRAME, validate="key",validatecommand=(self.register(validateInput), "%S"),
                     width=20, textvariable=self.PAYMENT_AMOUNT, justify='center')
        self.AMOUNT_ENTRY.grid(row=3, column=2, ipady=4, sticky='nsew')


        ttb.Label(FUNDS_SELECTION_FRAME, 
                  text='Tasa de Cambio', 
                  font=('arial',11,'bold'), 
                  bootstyle='danger'
        ).grid(row=2, column=1, sticky='nsew', pady=(12,6))

        self.EXCHANGERATE_ENTRY = ttb.Entry(FUNDS_SELECTION_FRAME, justify='center', validatecommand=(self.register(validateInput), "%S"),
                     width=20, textvariable=self.PAYMENT_EXCHANGE,  validate="key")
        self.EXCHANGERATE_ENTRY.grid(row=3, column=1, ipady=4,padx=(0,6), sticky='nsew')




        ttb.Label(FUNDS_SELECTION_FRAME, 
                  text='Descripcion', 
                  font=('arial',11,'bold'), 
                  bootstyle='danger'
        ).grid(row=4, column=0, sticky='nsew', pady=(12,6))

        self.descriptionText = ttb.Text(FUNDS_SELECTION_FRAME, 
                     width=20, height=3 )
        self.descriptionText.grid(row=5, column=0, ipady=4, sticky='nsew', columnspan=3)

        buttons_frame = ttb.Frame(FUNDS_SELECTION_FRAME,)
        buttons_frame.grid(row=6, column=0, sticky='nsew', pady=10, padx=4)
        delete_all_btn = ttb.Button(buttons_frame,
                                bootstyle='danger outline',
                                image=self.__delete_all_icon,
                                compound='center', 
                                padding=2,
                                command=self.remove_all_payment)
        delete_all_btn.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        ToolTip(delete_all_btn, text="Devolver Todo", bootstyle=('info', 'inverse'),)

        self.delete_btn = ttb.Button(buttons_frame,
                            bootstyle='danger outline',
                            image=self.__delete_icon,
                            compound='center', 
                            command=self.remove_payment,
                            padding=2)
        self.delete_btn.grid(row=0, column=1, padx=5, pady=5,  sticky='nsew')

        ToolTip(self.delete_btn, text="Devolver", bootstyle=('info', 'inverse'),)

        self.add_btn = ttb.Button(buttons_frame,
                             bootstyle='success outline',
                             image=self.__add_icon, 
                             compound='left',
                             text=' Añadir monto Valor', 
                             command=self.check_data,
                             padding=2
                        )
        self.add_btn.grid(row=0, column=2, padx=5, pady=5,  sticky='nsew')

        payments_list_frame = ttb.Frame(INFO_FRAME, 
                                        bootstyle='light', 
                                        style='custom.TFrame', 
                                        relief='raised', 
                                        border=2, 
                                        height=200)
        payments_list_frame.grid(row=1, column=0, sticky='nsew', padx=4,pady=4, columnspan=2)
        payments_list_frame.columnconfigure(0, weight=1)
        payments_list_frame.rowconfigure(0, weight=1)
        payments_list_frame.grid_propagate(0)

        yscroll = ttb.Scrollbar(payments_list_frame, 
                                orient='vertical',
                                bootstyle="dark-round")
        yscroll.grid(row=0, column=1, padx=(0,1), pady=1,sticky='ns', rowspan=2)
        
        xscroll = ttb.Scrollbar(payments_list_frame, 
                                orient='horizontal',
                                bootstyle="dark-round")
        xscroll.grid(row=1, column=0, padx=1, pady=1,sticky='ew')

        columns = ('date','reference', 'paymenttype', 'currency', 'amount', 'amountUSD','exchangerate','details')

        self.__payments_record_gridview = ttb.Treeview(payments_list_frame,
                                columns=columns,
                                bootstyle='dark', 
                                height=4,
                                selectmode='extended', 
                                yscrollcommand=yscroll.set,
                                xscrollcommand=xscroll.set)
        self.__payments_record_gridview.grid(row=0,column=0,padx=2,pady=(1,0),sticky='nsew')
    

        yscroll.configure(command=self.__payments_record_gridview.yview)
        xscroll.configure(command=self.__payments_record_gridview.xview)

        self.__payments_record_gridview.heading("#0")
        self.__payments_record_gridview.heading(columns[0], anchor='center', text='Fecha')
        self.__payments_record_gridview.heading(columns[1], anchor='center', text='Referencia')
        self.__payments_record_gridview.heading(columns[2], anchor='center', text='Origen')
        self.__payments_record_gridview.heading(columns[3], anchor='center', text='Moneda')
        self.__payments_record_gridview.heading(columns[4], anchor='center', text='Monto Valor')
        self.__payments_record_gridview.heading(columns[5], anchor='center', text='Monto USD')
        self.__payments_record_gridview.heading(columns[6], anchor='center', text='Tasa de Cambio')
        self.__payments_record_gridview.heading(columns[7], anchor='w', text='Detalles')

        self.__payments_record_gridview.column('#0', width=0, stretch=False, anchor='w')
        self.__payments_record_gridview.column(columns[0], width=120, stretch=False, anchor='center')
        self.__payments_record_gridview.column(columns[1], width=160, stretch=False, anchor='center')
        self.__payments_record_gridview.column(columns[2], width=160, stretch=False, anchor='center')
        self.__payments_record_gridview.column(columns[3], width=160, stretch=False, anchor='center')
        self.__payments_record_gridview.column(columns[4], width=160, stretch=False, anchor='center')
        self.__payments_record_gridview.column(columns[5], width=160, stretch=False, anchor='center')
        self.__payments_record_gridview.column(columns[6], width=160, stretch=False, anchor='center')
        self.__payments_record_gridview.column(columns[7], width=200, stretch=False, anchor='w')




        payment_section_frame = ttb.Frame(INFO_FRAME)
        payment_section_frame.grid(row=2, column=0, sticky='nsew', padx=4,pady=4, columnspan=2)
        payment_section_frame.columnconfigure(0, weight=1)
       
        payment_balance_frame = ttb.LabelFrame(payment_section_frame, 
                                               text='Detalles de Deuda y Pago', 
                                               padding='10 5')
        payment_balance_frame.grid(row=0, column=0, sticky='nsew')
        payment_balance_frame.columnconfigure(0,weight=1)

        ttb.Label(payment_balance_frame, 
                    text='Saldo Actual.', 
                    anchor='center', 
                    foreground='grey'
        ).grid(row=0, column=0, pady=(0,4), padx=(0,12), sticky='nsew', rowspan=2)

        ttb.Label(payment_balance_frame, 
                    text='USD $', 
                    font=('Helvetica',11,'bold'), 
                    anchor='w'
        ).grid(row=0, column=1, pady=(0,4),  sticky='nsew')

        ttb.Label(payment_balance_frame, 
                    textvariable=self.totalToPay,
                    width=15, 
                    font=('Helvetica',11,'bold'), 
                    anchor='e'
        ).grid(row=0, column=2, pady=(0,4),  sticky='nsew')

        ttb.Label(payment_balance_frame, 
                    text='Bs.',
                    padding='5 5', 
                    bootstyle='light inverse', 
                    foreground=GUI_COLORS['danger'], 
                    font=('Helvetica',10,'bold'), 
                    anchor='w'
        ).grid(row=1, column=1, pady=(0,4), sticky='nsew')

        self.exchange_amount_doc = ttb.Label(payment_balance_frame, 
                    textvariable=self.totalToPayExchange,
                    padding='5 5', 
                    width=15, 
                    bootstyle='light inverse', 
                    foreground=GUI_COLORS['danger'], 
                    font=('Helvetica',10,'bold'), 
                    anchor='e'
        )
        self.exchange_amount_doc.grid(row=1, column=2, pady=(0,4), sticky='nsew')

        
        ttb.Label(payment_balance_frame,
                  bootstyle='dark inverse', 
                  padding='5 5', 
                  width=15, 
                  text='Total a Pagar', 
                  anchor='center', 
                  foreground='white',
                  font=('Helvetica',11,'bold')
        ).grid(row=2, column=0, pady=(0,2), sticky='nsew')

        ttb.Label(payment_balance_frame,
                  bootstyle='dark inverse', 
                  padding='5 5', 
                  text='USD $', 
                  font=('Helvetica',11,'bold'),
                  anchor='w'
        ).grid(row=2, column=1, pady=(0,2),  sticky='nsew')

        ttb.Label(payment_balance_frame,
                  bootstyle='dark inverse', 
                  padding='5 5', 
                  textvariable=self.totalDebt,
                  width=15, 
                  font=('Helvetica',11,'bold'), 
                  anchor='e'
        ).grid(row=2, column=2, pady=(0,2),  sticky='nsew')

        ttb.Label(payment_balance_frame, 
                    text='Bs.', 
                    padding='5 5', 
                    bootstyle='danger inverse', 
                    font=('Helvetica',10,'bold'), 
                    anchor='center'
        ).grid(row=3, column=0, columnspan=1, pady=(0,2), sticky='nsew')

        ttb.Label(payment_balance_frame,
                  bootstyle='light inverse', 
                  padding='5 5', 
                  text='Bs.', 
                  font=('Helvetica',11,'bold'),
                  anchor='w'
        ).grid(row=3, column=1, pady=(0,2),  sticky='nsew')

        self.l_debt_amount_exchange = ttb.Label(payment_balance_frame, 
                    textvariable=self.totalDebtExchange,
                    padding='5 5', 
                    width=15, 
                    bootstyle='light inverse', 
                    foreground=GUI_COLORS['danger'], 
                    font=('Helvetica',10,'bold'), 
                    anchor='e',)
        self.l_debt_amount_exchange.grid(row=3, column=2, pady=(0,2), sticky='nsew')


        ttb.Label(payment_balance_frame, 
                  padding='5 5', 
                  width=15, 
                  text='Falta para Completar', 
                  anchor='center',
                  font=('Helvetica',10)
        ).grid(row=4, column=0, sticky='nsew', rowspan=2)

        ttb.Label(payment_balance_frame, 
                  padding='5 5', 
                  text='USD $', 
                  font=('Helvetica',10), 
                  anchor='w'
        ).grid(row=4, column=1,  sticky='nsew')

        self.L_amount_2_complete = ttb.Label(payment_balance_frame, 
                  padding='5 5', 
                  textvariable=self.actualDebt,
                  width=15, 
                  font=('Helvetica',10),
                  anchor='e',
                  )
        self.L_amount_2_complete.grid(row=4, column=2,  sticky='nsew')

        ttb.Label(payment_balance_frame, 
                  padding='5 5', 
                  text='Bs.', 
                  font=('Helvetica',10), 
                  anchor='w',
        ).grid(row=5, column=1,  sticky='nsew')

        self.L_amount_2_complete_exchange = ttb.Label(payment_balance_frame, 
                  padding='5 5', 
                  textvariable=self.actualDebtExchange,
                  width=15, 
                  font=('Helvetica',10),
                  anchor='e',
        )
        self.L_amount_2_complete_exchange.grid(row=5, column=2,  sticky='nsew')


        payment_options_frame = ttb.LabelFrame(payment_section_frame, 
                                                text='Aplicacion', 
                                                padding='10 5')
        payment_options_frame.grid(row=0, column=1, sticky='nsew', padx=(6,0))
        payment_options_frame.anchor('center')

        ttb.Checkbutton(payment_options_frame, 
                    text='Generar Recibo'
        ).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='e')

        exit_btn = ttb.Button(payment_options_frame, 
                             image=self.__log_out_icon, 
                             bootstyle='dark outline', 
                             compound='left',
                             text=' Salir', 
                             padding='5 5',
                             command=self.destroy)
        exit_btn.grid(row=1, column=0, padx=5, pady=5)

        check_pay_btn = ttb.Button(payment_options_frame, 
                             image=self.__checked_icon, 
                             bootstyle='success outline', 
                             command=self.ApplyPayments,
                             compound='left',
                             text=' Aplicar Pago', 
                             padding='5 5',)
        check_pay_btn.grid(row=1, column=1, padx=5, pady=5)

        self.place_window_center()

    #########################################################################################################
    ############## VERIFICA SI EL MONTO A AGREGAR ES VALIDO PARA SER AGREGADO EN LOS REGISTROS ##############
    #########################################################################################################
    def calculateExchange(self, exchangeVariable, variable):
        rate = DB.getCurrencyValues(2)
        exchangeVariable.set(float(variable.get())*float(rate))


    def calculate_amount(self, amount, currency, tasa):
        currency_id = self.CURRENCYS_ID[currency]
        if int(currency_id) == int(1):
            round(float(self.__DOCUMENT.debtUSD)*(1/tasa)/(1/DB.getCurrencyValues(self.__DOCUMENT.currency)),2)
        elif int(currency_id) == int(3):
            round(float(self.__DOCUMENT.debtUSD)*(1/DB.getCurrencyValues(2))/(1/tasa),2)
        return amount

    def set_usd_amount(self, amount):
        if self.__DOCUMENT.currency == 2:
            return amount
        elif self.__DOCUMENT.currency == 1:
            return round(float(amount)*(1/float(self.__DOCUMENT.exchangeRate))/(1/DB.getCurrencyValues(1)),2)
        elif self.__DOCUMENT.currency == 3:
            return round(float(amount)*(1/DB.getCurrencyValues(2))/(1/float(self.__DOCUMENT.exchangeRate)),2)


    def check_data(self):
        if self.PAYMENT_AMOUNT.get() and self.PAYMENT_REFERENCES.get():
            amountToAdd = round(float(self.PAYMENT_AMOUNT.get()),2)
            actualDebt = round(float(self.actualDebt.get()),2)
            USDAMOUNT = self.calculate_exchange(amountToAdd, self.CURRENCYS_ID[self.__currency.get()],float(self.PAYMENT_EXCHANGE.get()))
            if USDAMOUNT <= actualDebt:
                self.add_payment_record(amountToAdd)
                self.updateBalance(amount=USDAMOUNT)
                self.cleanFields()
           

            else:
                messagebox.showwarning('Monto','El monto ingresado es superior a la deuda actual.', parent=self)
            if float(self.actualDebt.get())<=0:
                self.ApplyPayments()
        elif not self.PAYMENT_REFERENCES.get():
            messagebox.showinfo('Referencia','Especificar Referencia del pago.', parent=self)
        else:
            messagebox.showinfo('Monto','Ingrese el monto a Pagar.', parent=self)


    
    #########################################################################################################################
    ############## PERMITE AGREGAR INFORMACION DE PAGO EN EL GRIDVIEW Y ACTUALIZA LOS VALORES DE LAS VARIABLES ##############
    #########################################################################################################################
    def add_payment_record(self, amount, ):
        amount = round(float(self.AMOUNT_ENTRY.get()), 2)
        self.__payments_record_gridview.insert('',
            ttb.END,
            values=(
                self.PAYMENT_DATE.get(),
                self.PAYMENT_REFERENCES.get(),
                self.COMBOBOX_FUNDS.get(),
                self.__currency.get(),
                amount,
                round(self.calculate_exchange(amount=amount,currency=self.CURRENCYS_ID[self.__currency.get()],tasa=self.PAYMENT_EXCHANGE.get()),2),
                self.PAYMENT_EXCHANGE.get(),
                self.descriptionText.get('1.0', ttb.END).replace('\n','')))
     

    def updateBalance(self, actioType='add', amount=0):
        plus = 1
        if actioType!='add':
            plus = -1
        self.actualDebt.set(round(float(self.actualDebt.get())-float(amount)*plus,2))
        self.totalToPay.set(round(float(self.totalToPay.get())+float(amount)*plus,2))
       
        

    #################################################################
    ############## PERMITE DESHACER REGISTROS DE PAGOS ##############
    #################################################################
    def remove_payment(self, selected = None):
        if selected is None:
            selected = self.__payments_record_gridview.focus()
        if selected:
            item_selected = self.__payments_record_gridview.item(selected, 'values')
            self.updateBalance(actioType='minus', amount=item_selected[5])
            self.__payments_record_gridview.delete(selected)

    ###########################################################################
    ############## PERMITE DESHACER TODOS LOS REGISTROS DE PAGOS ##############
    ###########################################################################
    def remove_all_payment(self):
        ask = messagebox.askquestion('Devolucion', 'Desea retirar todos los pagos registrados?',parent=self)
        if ask == 'yes':
            for item in self.__payments_record_gridview.get_children():
                self.remove_payment(item)


    #########################################################################################
    ################# ACTUALIZA LOS MONTOS DE LAS CUENTAS DE LA INSTITUCION #################
    #########################################################################################
    
    def cleanFields(self):
        self.AMOUNT_ENTRY.delete(0,ttb.END)
        self.PAYMENT_DATE.set(datetime.datetime.today().strftime('%d/%m/%Y'))
        self.COMBOBOX_FUNDS.current(0)
        self.__currency.set('Bs.')
        self.PAYMENT_REFERENCES.set('')
        self.descriptionText.delete('1.0',ttb.END)

    def ApplyPayments(self):
        if len(self.__payments_record_gridview.get_children()) > 0:
            if self.__DOCUMENT.documentCondition == 'CONTADO' and self.__DOCUMENT.debtUSD>0:
                messagebox.showinfo('Documento', 'La condicion del documento es contado, debe registrar el monto completo.')
            else:
                if self.full_payment_required == True and float(self.actualDebt.get()) >0:
                   messagebox.showinfo('Aviso','Debe registrar el pago completo del documento.', parent=self)
                else:
                    ask = messagebox.askquestion('Aplicar','Desea procesar el pago?', parent=self)
                    if ask == 'yes':
                        payments = []
                        if type(self.__DOCUMENT) == Bill:
                            company = self.__DOCUMENT.client
                            typeDocument = 'VENTA'
                        else:
                            company = self.__DOCUMENT.provider
                            typeDocument = 'COMPRA'
                        for item in self.__payments_record_gridview.get_children():
                            item_selected = self.__payments_record_gridview.item(item, 'values')
                            payments.append([datetime.datetime.strptime(item_selected[0],'%d/%m/%Y').strftime('%Y-%m-%d'),
                                            item_selected[1], self.__DOCUMENT.code, company, item_selected[2], 
                                            typeDocument,self.CURRENCYS_ID[item_selected[3]], item_selected[4], item_selected[5],
                                            item_selected[6], item_selected[7]])
                        result = Payment.creatAll(payments)
                        if result:
                            messagebox.showinfo('Aviso','Pagos Registrados con exito.', parent=self)
                            self.destroy()
                            self.callback()
                    
        else:
            messagebox.showwarning("Pagos",' No existen pagos registrados.', parent=self)


    def check_exchangerate(self):
        if self.CURRENCYS_ID[self.__currency.get()] in [1,2]:
            self.PAYMENT_EXCHANGE.set(DB.getCurrencyValues(2))


    def calculate_exchange(self,amount, currency, tasa = None):
        if currency == 2:
            return float(amount)
        else:
            return float(amount)/float(tasa) 
            
           

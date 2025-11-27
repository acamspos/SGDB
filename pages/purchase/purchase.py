import ttkbootstrap as ttb
from assets.globals import GUI_COLORS, IMG_PATH, GUI_FONT
from assets.utils import resize_icon, resize_image
from PIL import Image, ImageTk
from customtkinter import CTkFrame
import tkinter as tk

from components.buttons import ButtonImage
from assets.styles.styles import SGDB_Style
from datetime import datetime, timedelta
from models.entitys.purchase import PurchaseDocument
# Configuración
from assets.db.db_connection import DB
from pages.purchase.views.purchaseform import PurchaseForm
from pages.purchase.views.reportes import Report
from tkinter import messagebox
from pages.Extras.payments import PaymentForm

class PurchasePage(ttb.Frame):
    def __init__(self, master=None):
        PART_COLOR = GUI_COLORS['bg']
        PART2_COLOR = GUI_COLORS['primary']

        super().__init__(master)

       
        
        ############# CONFIGURACION VENTANA #############
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        ############## ESTILOS PERSONALIZADOS ##############


        ########### VARIABLES ############

        self.START_DATE = ttb.StringVar()
        self.END_DATE = ttb.StringVar()

        ####################### ELEMENTOS DE LA INTERFAZ GRAFICA #######################

        ###### TSECCION DEL TITULO:

        self.__act_icon = Image.open(f'{IMG_PATH}/activities_title.png')
        self.__act_icon = ImageTk.PhotoImage(self.__act_icon.resize(resize_image(10, self.__act_icon.size)))
        
        page_img_label = ttb.Label(self, image=self.__act_icon, padding='0 0')
        page_img_label.grid(row=0, column=0, sticky='nsw', pady=(10, 4), padx=20)
        page_img_label.grid_propagate(0)
        page_img_label.anchor('w')

        page_title_label = ttb.Label(page_img_label, text='COMPRAS', padding='0 0', background='#203864',
                               font=('arial',15, 'bold'), foreground='#fff')
        page_title_label.grid(row=0, column=0, sticky='nsew',padx=(80,0))

        reportBTN = Image.open(f"{IMG_PATH}/report.png")
        self.reportBTN = ImageTk.PhotoImage(reportBTN.resize(resize_image(25, reportBTN.size)))

        
        reporthBTN = Image.open(f"{IMG_PATH}/reporth.png")
        self.reporthBTN = ImageTk.PhotoImage(reporthBTN.resize(resize_image(25, reporthBTN.size)))


        reportpBTN = Image.open(f"{IMG_PATH}/reportp.png")
        self.reportptBTN = ImageTk.PhotoImage(reportpBTN.resize(resize_image(25, reportpBTN.size)))

        ButtonImage(self, image=self.reportBTN, img_h=self.reporthBTN, img_p=self.reportptBTN, command=self.__report,style='flat.light.TButton', padding=0).grid(row=0, column=0, sticky='nse', pady=2, padx=6)


        ttb.Separator(self, orient='horizontal').grid(row=1, column=0, sticky='nsew',padx=20)

        ######### SECCION DE CONTENIDO:
    
        CONTENT_FRAME = ttb.Frame(self,)
        CONTENT_FRAME.grid(row=2, column=0, sticky='nsew',pady=10, padx=20)
        CONTENT_FRAME.columnconfigure(0, weight=1)
        CONTENT_FRAME.rowconfigure(0, weight=1)


        self.dashboard_content = CTkFrame(CONTENT_FRAME,fg_color='#fff',border_width=1, bg_color=PART_COLOR, border_color='#CFCFCF')
        self.dashboard_content.grid(row=0, column=0, sticky='nsew',padx=(0,8), )
        self.dashboard_content.columnconfigure(0, weight=1)
        self.dashboard_content.rowconfigure(3, weight=1)

        subtitle = CTkFrame(self.dashboard_content, corner_radius=6, fg_color=PART2_COLOR)
        subtitle.grid(row=0, column=0, sticky='nsew', padx=10, pady=(10,2))

        self.micon = resize_icon(Image.open(f'{IMG_PATH}/management.png'),(45,45))

        ttb.Label(subtitle, image=self.micon, background=PART2_COLOR, ).grid(row=0, column=0, rowspan=2, sticky='nsew', padx=(8), pady=8)

        ttb.Label(subtitle, text='Gestion de Compras', background=PART2_COLOR, font=(GUI_FONT,13,'bold'), foreground='#fff').grid(row=0, column=1, sticky='nsew', padx=(4,8), pady=(8,0))

        ttb.Label(subtitle, text='Inicio/Compras', background=PART2_COLOR, font=(GUI_FONT,9), foreground='#fff').grid(row=1, column=1, sticky='nsew', padx=(4,8), pady=(0,8))

        ttb.Separator(subtitle,orient='vertical').grid(row=0, column=2, sticky='nsew', rowspan=2, padx=(4,8), pady=8)

        ttb.Label(subtitle, text='Informe de Compras del Mes Octubre - 2023', background=PART2_COLOR, font=(GUI_FONT,13,'bold'), foreground='#fff').grid(row=0, column=3, rowspan=2, sticky='nsew', padx=(4,8), pady=4)

        ttb.Frame(self.dashboard_content, bootstyle='primary').grid(row=1, column=0, sticky='nsew', padx=10, pady=5)

        buttons_frame = tk.Frame(self.dashboard_content, background='red')
        buttons_frame.config(background='#fff')
        buttons_frame.grid(row=2, column=0, sticky='nsew', padx=10)
        buttons_frame.columnconfigure(4, weight=1)


        creatbtnimg = Image.open(f"{IMG_PATH}/create.png")
        self.creatbtnimg = resize_icon(creatbtnimg, (50,50))

        creatbtnimgh = Image.open(f"{IMG_PATH}/createh.png")
        self.creatbtnimgh = resize_icon(creatbtnimgh, (50,50))

        creatbtnimgp = Image.open(f"{IMG_PATH}/createp.png")
        self.creatbtnimgp = resize_icon(creatbtnimgp, (50,50))

        ButtonImage(buttons_frame, image=self.creatbtnimg, img_h=self.creatbtnimgh, img_p=self.creatbtnimgp,  style='flatw.light.TButton', padding=0, command=self.__open_create_form).grid(row=0, column=0, sticky='', pady=2, padx=(0,8))


        ttb.Separator(buttons_frame, orient='vertical',bootstyle='dark').grid(row=0, column=1, sticky='ew', padx=(0,8))


        viewbtnimg = Image.open(f"{IMG_PATH}/view.png")
        self.viewbtnimg = resize_icon(viewbtnimg, (50,50))

        viewbtnimgh = Image.open(f"{IMG_PATH}/viewh.png")
        self.viewbtnimgh = resize_icon(viewbtnimgh, (50,50))

        viewbtnimgp = Image.open(f"{IMG_PATH}/viewp.png")
        self.viewbtnimgp = resize_icon(viewbtnimgp, (50,50))
        self.viewBTN = ButtonImage(buttons_frame, image=self.viewbtnimg, state='disabled', img_h=self.viewbtnimgh,  img_p=self.viewbtnimgp, style='flatw.light.TButton', padding=0, command=self.__open_view_form)
        self.viewBTN.grid(row=0, column=2, sticky='', pady=2, padx=(0,8))

        ttb.Separator(buttons_frame, orient='vertical',bootstyle='dark').grid(row=0, column=3, sticky='ew', padx=(0,8))

        paybtnimg = Image.open(f"{IMG_PATH}/pay.png")
        self.paybtnimg = resize_icon(paybtnimg, (50,50))

        paybtnimgh = Image.open(f"{IMG_PATH}/payh.png")
        self.paybtnimgh = resize_icon(paybtnimgh, (50,50))

        paybtnimgp = Image.open(f"{IMG_PATH}/payp.png")
        self.paybtnimgp = resize_icon(paybtnimgp, (50,50))

        self.PAYBTN = ButtonImage(buttons_frame, command=self.payment, image=self.paybtnimg, img_h=self.paybtnimgh,  img_p=self.paybtnimgp, style='flatw.light.TButton', padding=0, state='disabled')
        self.PAYBTN.grid(row=0, column=4, sticky='nsw', pady=2, padx=(0,8))

      

        ttb.Separator(buttons_frame, orient='vertical',bootstyle='dark').grid(row=0, column=5, sticky='ew', padx=(0,8))


        date_option_frame = ttb.Frame(buttons_frame,style='white.TFrame' )
        date_option_frame.grid(row=0, column=6, sticky='nsew',pady=(2,4))

        ttb.Label(date_option_frame, text='Filtro de Fechas', font=(GUI_FONT,11,'bold'), background='white').grid(row=0, column=0, columnspan=5, pady=(0,2), sticky='nsew')

        def enable_dates_entry():
            if self.range_selection.get() in ['EL DIA','MES']:
                self.start_date.entry.config(state='normal')
                self.start_date.button.config(state='normal')
            else:
                if self.range_selection.get() == self.DATEFILTER[-2]:
                    state='normal'
                else:
                    state='disabled'
                    self.__findPurchases()
                for dateentry in [self.start_date, self.final_date]:
                    dateentry.entry.config(state=state)
                    dateentry.button.config(state=state)
                

        self.DATEFILTER = ('HOY','AYER','EL DIA','MES ACTUAL','MES ANTERIOR','MES','AÑO ACTUAL','AÑO ANTERIOR','POR RANGO','TODAS')

        self.range_selection = ttb.Combobox(date_option_frame, values=self.DATEFILTER, width=30, state='readonly')
        self.range_selection.grid(row=1, column=0, sticky='nsew', padx=6, pady=3)
        self.range_selection.bind("<<ComboboxSelected>>", lambda e:  enable_dates_entry())
        self.range_selection.current(0)
        

        ttb.Label(date_option_frame, text='Desde', background='#fff', font=(GUI_FONT,11,'bold')).grid(row=1, column=1, padx=(8,4))

        self.start_date = ttb.DateEntry(date_option_frame,width=14,dateformat='%d/%m/%Y',)
        self.start_date.grid(row=1, column=2, sticky='nsew')
        self.start_date.entry.config(state='disabled',textvariable=self.START_DATE)
        self.start_date.button.config(state='disabled')
      

        ttb.Label(date_option_frame, text='Hasta', background='#fff', font=(GUI_FONT,11,'bold')).grid(row=1, column=3, padx=(8,4))

        self.final_date = ttb.DateEntry(date_option_frame,width=14,dateformat='%d/%m/%Y')
        self.final_date.grid(row=1, column=4, sticky='nsew', padx=(0,6))
        self.final_date.entry.config(state='disabled',textvariable=self.END_DATE)
        self.final_date.button.config(state='disabled')
        
        
        searchbtnimg = Image.open(f"{IMG_PATH}/searchbtn.png")
        self.searchbtnimg = resize_icon(searchbtnimg, (50,50))

        searchbtnimgh = Image.open(f"{IMG_PATH}/searchbtnh.png")
        self.searchbtnimgh = resize_icon(searchbtnimgh, (50,50))

        searchbtnimgp = Image.open(f"{IMG_PATH}/searchbtnp.png")
        self.searchbtnimgp = resize_icon(searchbtnimgp, (50,50))

        ButtonImage(buttons_frame, command=self.__findPurchases, image=self.searchbtnimg, img_h=self.searchbtnimgh, img_p=self.searchbtnimgp, style='flatw.light.TButton', padding=0).grid(row=0, column=7, pady=2, padx=(10,0))

        grid_frame = tk.Frame(self.dashboard_content,)
        grid_frame.config(background='#fff')
        grid_frame.grid(row=3, column=0, columnspan=1, padx=10, pady=(0,10), sticky='nsew')
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.rowconfigure(0, weight=1)

        columns = ('dateregister','date','provider','rif','code','control','expiredate','currency','Total','totalpaid','debt','totalusd','exchange','status')

        yscroll = ttb.Scrollbar(grid_frame, 
                                orient='vertical',
                                bootstyle="dark-round")
        yscroll.grid(row=0, column=1, padx=1, pady=2,sticky='ns', rowspan=2)

        xscroll = ttb.Scrollbar(grid_frame, 
                                orient='horizontal',
                                bootstyle="dark-round")
        xscroll.grid(row=1, column=0, padx=1, pady=2,sticky='ew')

        self.budgetGridview = ttb.Treeview(grid_frame,columns=columns,show='headings', style='cust.primary.Treeview',
                                 height=10, padding=0, xscrollcommand=xscroll.set,
                                selectmode='extended', yscrollcommand=yscroll.set)
        self.budgetGridview.grid(row=0,column=0,padx=2,pady=(2,2),sticky='nsew')
        self.budgetGridview.bind('<<TreeviewSelect>>', lambda e: self.__enabled_view())
        
        yscroll.configure(command=self.budgetGridview.yview)
        xscroll.configure(command=self.budgetGridview.xview)

        self.budgetGridview.heading(columns[0],text='Fecha Registro',anchor='center')
        self.budgetGridview.heading(columns[1],text='Fecha Emision',anchor='center')
        self.budgetGridview.heading(columns[2],text='Proveedor',anchor='center')
        self.budgetGridview.heading(columns[3],text='RIF',anchor='center')
        self.budgetGridview.heading(columns[4],text='Documento',anchor='center')
        self.budgetGridview.heading(columns[5],text='Control',anchor='center')
        self.budgetGridview.heading(columns[6], anchor='center', text='Estatus')
        self.budgetGridview.heading(columns[7],text='Vencimiento',anchor='center')
        self.budgetGridview.heading(columns[8],text='Moneda',anchor='center')
        self.budgetGridview.heading(columns[9], anchor='center', text='Total')
        self.budgetGridview.heading(columns[10], anchor='center', text='Tasa de Cambio (Bs.)')
        self.budgetGridview.heading(columns[11], anchor='center', text='Total $')
        self.budgetGridview.heading(columns[12], anchor='center', text='Total Pagado $')
        self.budgetGridview.heading(columns[13], anchor='center', text='Total Deuda $')

        self.budgetGridview.column(columns[0], width=140, stretch=False, anchor='center')
        self.budgetGridview.column(columns[1], width=140, stretch=False, anchor='center')
        self.budgetGridview.column(columns[2], width=220, stretch=False, anchor='center')
        self.budgetGridview.column(columns[3], width=140, stretch=False, anchor='center')
        self.budgetGridview.column(columns[4], width=140, stretch=False, anchor='center')
        self.budgetGridview.column(columns[5], width=140, stretch=False, anchor='center')
        self.budgetGridview.column(columns[6], width=140, stretch=False, anchor='center')
        self.budgetGridview.column(columns[7], width=140, stretch=False, anchor='center')
        self.budgetGridview.column(columns[8], width=140, stretch=False, anchor='center')
        self.budgetGridview.column(columns[9], width=180, stretch=False, anchor='center')
        self.budgetGridview.column(columns[10], width=180, stretch=False, anchor='center')
        self.budgetGridview.column(columns[11], width=180, stretch=False, anchor='center')
        self.budgetGridview.column(columns[12], width=180, stretch=False, anchor='center')
        self.budgetGridview.column(columns[13], width=180, stretch=False, anchor='center')


        DATE = datetime.today().strftime('%d/%m/%Y')
        self.START_DATE.set(DATE)
        self.END_DATE.set(DATE)
      
        self.bind('<Map>', lambda e: self.__findPurchases())


    def __open_create_form(self):
        ask = messagebox.askquestion('Registrar','Desea crear un nuevo registro?')
        if ask == 'yes':
            window = PurchaseForm(self, window_type='create', title='Registrar Factura de Compra')
            self.wait_window(window)
            self.__findPurchases()


    def ____deletePurchase(self):
        selected =self.budgetGridview.focus()
        if selected:
            ask = messagebox.askokcancel('Eliminar', 'Desea eliminar el registro de la factura de compra?', parent=self)
            if ask =='yes':
                data = self.budgetGridview.item(selected, 'values')
                purchase = PurchaseDocument.findOnePurchase(data[4],data[3])
                purchase.delete()
                messagebox.showinfo('ELIMINADO','Registro Eliminado')
                self.__findPurchases()

    def __open_view_form(self):
        PurchaseForm(self, window_type='view', title='Detalles de Registro de Compra')


    def __enabled_view(self):
        if self.budgetGridview.selection()!= ():
            self.viewBTN.config(state='normal')
           
            self.deleteBTN.config(state='normal')
        else:
            self.viewBTN.config(state='disabled')
     
            self.deleteBTN.config(state='disabled')


    def __report(self):
        ask = messagebox.askokcancel('Reportes','Generar reporte de todos las facturas de compras registradas?')
        if ask == 'yes':
            window = Report(self)
    
    def set_date_filter(self):
        if self.range_selection.get() == self.DATEFILTER[0]:
            return datetime.today().strftime('%Y-%m-%d'), None
        elif self.range_selection.get() == self.DATEFILTER[1]:
            return (datetime.today() + timedelta(days=-1)).strftime('%Y-%m-%d'), None
        elif self.range_selection.get() == self.DATEFILTER[2]:
            return datetime.strptime(self.START_DATE.get(),'%d/%m/%Y').strftime('%Y-%m-%d'), None
        elif self.range_selection.get() == self.DATEFILTER[3]:
            return datetime.today().month, "MONTH"
        elif self.range_selection.get() == self.DATEFILTER[4]:
            return datetime.today().month-1, 'MONTH'
        elif self.range_selection.get() == self.DATEFILTER[5]:
            return datetime.strptime(self.START_DATE.get(),'%d/%m/%Y').month
        elif self.range_selection.get() == self.DATEFILTER[6]:
            return datetime.today().year, 'YEAR'
        elif self.range_selection.get() == self.DATEFILTER[7]:
            return datetime.today().year-1, 'YEAR'
        elif self.range_selection.get() == self.DATEFILTER[8]:
            date = lambda date: datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d')
            return [date(self.START_DATE.get()), date(self.END_DATE.get())], 'BETWEEN'
        else:
            return None, None   

        
    def __findPurchases(self):
        self.budgetGridview.delete(*self.budgetGridview.get_children())
        filter_date = self.set_date_filter()
        purchases = PurchaseDocument.findAll(date=filter_date[0], datefilter=filter_date[1])
        for purchase in purchases:
            pur = PurchaseDocument(**purchase)
            icon = pur.get_currency_icon()
            self.budgetGridview.insert("",
                            ttb.END,
                            text=pur.code,
                            values=(pur.registrationDate.strftime('%d/%m/%Y'),pur.dateOfIssue.strftime('%d/%m/%Y'), pur.get_company(),pur.provider,
                                    pur.code, pur.control,pur.get_documentState(),pur.expirationDate.strftime('%d/%m/%Y'),
                                    pur.get_currency(),f"{icon} {pur.total}", f"Bs. {pur.exchangeRate}",  f"$ {pur.totalUSD}", f"$ {pur.totalPaidUSD}", 
                                    f"$ {pur.debtUSD}"
                                    ), tags='row')
            
            del pur
    

       
    def __open_view_form(self):
        selected =self.budgetGridview.focus()
        if selected:
            data = self.budgetGridview.item(selected, 'values')
            purchase = PurchaseDocument.findOnePurchase(data[4],data[3])
            
            window = PurchaseForm(self, window_type='view',purchase=purchase)
            del data, purchase
            self.wait_window(window)
            self.__findPurchases()

    def payment(self):
        documentSelected = self.budgetGridview.focus()
        if documentSelected:
            value = self.budgetGridview.item(documentSelected, 'values')
            document = PurchaseDocument.findOnePurchase(value[4], value[3])
            paymentWindow = PaymentForm(self, doc=document, callback = self.__findPurchases)
            self.wait_window(paymentWindow)
            
            

    def __enabled_view(self):
        documentSelected = self.budgetGridview.focus()
       
        if documentSelected:
            value = self.budgetGridview.item(documentSelected, 'values')
            document = PurchaseDocument.findOnePurchase(value[4], value[3])
            self.viewBTN.config(state='normal')
            if document.documentState == 3:
                self.PAYBTN.config(state='disabled')
            else:
                self.PAYBTN.config(state='normal')
        else:
            self.viewBTN.config(state='disabled')
            self.PAYBTN.config(state='disabled')


    def check_documents_purchases(self):
        docs = PurchaseDocument.get_document_to_expirate()
        if len(docs):
            doclist = ''
            for index,doc in enumerate(docs):
                doclist = f'\n {index+1}.) Codigo: {doc.code} - Proveedor: {doc.provider}'
            messagebox.showwarning('Listado de Compras',f"Las siguientes facturas expiran el dia {(datetime.today() + timedelta(days=1)).strftime('%d/%m/%Y')}:\n{doclist}")


    def expiration_document_list_purchases(self):
        docs = PurchaseDocument.update_document_states()
        if len(docs):
            doclist = ''
            for index,doc in enumerate(docs):
                doclist = f'\n {index+1}.) Codigo: {doc[0]} - Proveedor: {doc[1]}'
            messagebox.showwarning('Listado de Compras',f'Las siguientes facturas han vencido:\n{doclist}')

if __name__=="__main__":
    app = ttb.Window(themename='new')
    app.geometry('1200x900')
    SGDB_Style()
    PurchasePage(app).pack()
    app.mainloop()
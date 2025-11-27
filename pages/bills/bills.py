import ttkbootstrap as ttb
from assets.globals import GUI_COLORS, IMG_PATH, GUI_FONT
from assets.utils import resize_icon, resize_image
from assets.globals import invoice_icon, budget_icon, project_icon, refresh_icon
from components.dcards import DashboardCard
from components.buttons import ButtonImage
from PIL import Image, ImageTk
from customtkinter import CTkFrame, CTkLabel
import tkinter as tk
from assets.styles.styles import SGDB_Style
from components.bcards import BCards
###### GRAPH LIBRARIES
from pages.Extras.payments import PaymentForm
from models.entitys.bills import Bill
from datetime import datetime, timedelta
from tkinter import messagebox
from pages.bills.views.billsForn import BillForm
import assets.globals as constGlobal

class BillPage(ttb.Frame):
    def __init__(self, master=None):
        SGDB_Style()
        super().__init__(master, height=50, width=50)
        PART_COLOR = GUI_COLORS['bg']
        PART2_COLOR = GUI_COLORS['danger']

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        ########## GUI ICONSr##########
        self.__dash_icon = Image.open(f'{IMG_PATH}/bill_title.png')
        self.__dash_icon = ImageTk.PhotoImage(self.__dash_icon.resize(resize_image(10, self.__dash_icon.size)))
  

        ######### PAGE TITLE #########


        ######### PAGE TITLE #########
        frame_title = ttb.Frame(self)
        frame_title.grid(row=0, column=0, sticky='nesw', pady=(10, 4), padx=20)
        frame_title.columnconfigure(0, weight=1)

        page_img = ttb.Label(frame_title, 
                               image=self.__dash_icon, 
                                padding='0 0',
                               )
        page_img.grid(row=0, column=0, sticky='nsw', pady=2, padx=2)
        page_img.grid_propagate(0)
        page_img.anchor('w')


        

        page_title = ttb.Label(page_img, 
                               text=' FACTURAS', 
                                padding='0 0',
                               background='#203864',
                               font=('arial',15, 'bold'), 
                               foreground='#fff')
        page_title.grid(row=0, column=0, sticky='nsew',padx=(80,0))

        reportBTN = Image.open(f"{IMG_PATH}/report.png")
        self.reportBTN = ImageTk.PhotoImage(reportBTN.resize(resize_image(25, reportBTN.size)))

        
        reporthBTN = Image.open(f"{IMG_PATH}/reporth.png")
        self.reporthBTN = ImageTk.PhotoImage(reporthBTN.resize(resize_image(25, reporthBTN.size)))

        ButtonImage(frame_title, image=self.reportBTN,style='flat.light.TButton', padding=0).grid(row=0, column=1, sticky='nsew', pady=2, padx=6)

        reportpBTN = Image.open(f"{IMG_PATH}/reportp.png")
        self.reportptBTN = ImageTk.PhotoImage(reportpBTN.resize(resize_image(25, reportpBTN.size)))

        ButtonImage(frame_title, image=self.reportBTN, img_h=self.reporthBTN, img_p=self.reportptBTN,style='flat.light.TButton', padding=0).grid(row=0, column=1, sticky='nsew', pady=2, padx=6)

        ttb.Separator(self, orient='horizontal',bootstyle='dark').grid(row=1, column=0, sticky='nsew',padx=20)

        ######### PAGE CONTENT #########
        self.bills_amount = ttb.IntVar(value=0)

        content = ttb.Frame(self)
        content.columnconfigure(1, weight=1)
        content.grid(row=2, column=0, sticky='nsew', padx=18, pady=(10,10))
        content.rowconfigure(1, weight=1)


        #### Grid Container ######
        self.dashboard_content = CTkFrame(content,fg_color='#fff',border_width=1, bg_color=PART_COLOR, border_color='#CFCFCF')
        self.dashboard_content.grid(row=0, column=1, sticky='nsew',padx=(0,8), rowspan=2)
        self.dashboard_content.columnconfigure(0, weight=1)
        self.dashboard_content.rowconfigure(3, weight=1)

        subtitle = CTkFrame(self.dashboard_content, corner_radius=6, fg_color=PART2_COLOR)
        subtitle.grid(row=0, column=0, sticky='nsew', padx=10, pady=(10,2))

        self.micon = resize_icon(Image.open(f'{IMG_PATH}/invoice.png'),(45,45))

        ttb.Label(subtitle, image=self.micon, background=PART2_COLOR, ).grid(row=0, column=0, rowspan=2, sticky='nsew', padx=(8), pady=8)

        ttb.Label(subtitle, text='Gestion de Facturas', background=PART2_COLOR, font=(GUI_FONT,13,'bold'), foreground='#fff').grid(row=0, column=1, sticky='nsew', padx=(4,8), pady=(8,0))

        ttb.Label(subtitle, text='Inicio/Productos', background=PART2_COLOR, font=(GUI_FONT,9), foreground='#fff').grid(row=1, column=1, sticky='nsew', padx=(4,8), pady=(0,8))

        ttb.Frame(self.dashboard_content, bootstyle='primary').grid(row=1, column=0, sticky='nsew', padx=10, pady=5)

        buttons_frame = tk.Frame(self.dashboard_content, background='red')
        buttons_frame.config(background='#fff')
        buttons_frame.grid(row=2, column=0, sticky='nsew', padx=10)
        buttons_frame.columnconfigure(6, weight=1)


        creatbtnimg = Image.open(f"{IMG_PATH}/create.png")
        self.creatbtnimg = resize_icon(creatbtnimg, (50,50))

        creatbtnimgh = Image.open(f"{IMG_PATH}/createh.png")
        self.creatbtnimgh = resize_icon(creatbtnimgh, (50,50))

        creatbtnimgp = Image.open(f"{IMG_PATH}/createp.png")
        self.creatbtnimgp = resize_icon(creatbtnimgp, (50,50))


        ButtonImage(buttons_frame, image=self.creatbtnimg, img_h=self.creatbtnimgh, img_p=self.creatbtnimgp, command=self.__open_create_form, style='flatw.light.TButton', padding=0).grid(row=0, column=0, sticky='nsew', pady=2, padx=(0,8))


        ttb.Separator(buttons_frame, orient='vertical',bootstyle='dark').grid(row=0, column=1, sticky='ew', padx=(0,8))

        viewbtnimg = Image.open(f"{IMG_PATH}/view.png")
        self.viewbtnimg = resize_icon(viewbtnimg, (50,50))

        viewbtnimgh = Image.open(f"{IMG_PATH}/viewh.png")
        self.viewbtnimgh = resize_icon(viewbtnimgh, (50,50))

        viewbtnimgp = Image.open(f"{IMG_PATH}/viewp.png")
        self.viewbtnimgp = resize_icon(viewbtnimgp, (50,50))
        self.viewBTN = ButtonImage(buttons_frame, image=self.viewbtnimg, img_h=self.viewbtnimgh,  img_p=self.viewbtnimgp, style='flatw.light.TButton', padding=0, command=self.__open_view_form)
        self.viewBTN.grid(row=0, column=2, sticky='', pady=2, padx=(0,8))

        paybtnimg = Image.open(f"{IMG_PATH}/pay.png")
        self.paybtnimg = resize_icon(paybtnimg, (50,50))

        paybtnimgh = Image.open(f"{IMG_PATH}/payh.png")
        self.paybtnimgh = resize_icon(paybtnimgh, (50,50))

        paybtnimgp = Image.open(f"{IMG_PATH}/payp.png")
        self.paybtnimgp = resize_icon(paybtnimgp, (50,50))
        self.payBTN=ButtonImage(buttons_frame, image=self.paybtnimg, img_h=self.paybtnimgh,  img_p=self.paybtnimgp, command=self.payment,style='flatw.light.TButton', padding=0)
        self.payBTN.grid(row=0, column=3, sticky='nsew', pady=2, padx=(0,8))


        anularimg = Image.open(f"{IMG_PATH}/anular.png")
        self.anularimg = resize_icon(anularimg,(50,50))

        anularimgh = Image.open(f"{IMG_PATH}/anularh.png")
        self.anularimgh = resize_icon(anularimgh, (50,50))

        anularimgp = Image.open(f"{IMG_PATH}/anularp.png")
        self.anularimgp = resize_icon(anularimgp, (50,50))

        self.anularBTN = ButtonImage(buttons_frame, image=self.anularimg, img_h=self.anularimgh, img_p=self.anularimgp, command=self.anular, style='flatw.light.TButton', padding=0)
        self.anularBTN.grid(row=0, column=4, sticky='nsew', pady=2, padx=(0,8))


        deletebtnimg = Image.open(f"{IMG_PATH}/deletebtn.png")
        self.deletebtnimg = resize_icon(deletebtnimg, (50,50))

        deletebtnimgh = Image.open(f"{IMG_PATH}/deletebtnh.png")
        self.deletebtnimgh = resize_icon(deletebtnimgh, (50,50))

        deletebtnimgp = Image.open(f"{IMG_PATH}/deletebtnp.png")
        self.deletebtnimgp = resize_icon(deletebtnimgp, (50,50))

        self.deleteBTN = ButtonImage(buttons_frame, command=self.__deleteBill, image=self.deletebtnimg, img_h=self.deletebtnimgh, img_p=self.deletebtnimgp,  style='flatw.light.TButton', padding=0)



        self.SEARCHENTRY = ttb.Entry(buttons_frame, bootstyle='info', width=30)
        self.SEARCHENTRY.grid(row=0,column=6, ipady=2, padx=(4,8), pady=12, sticky='nsew')
        
        searchbtnimg = Image.open(f"{IMG_PATH}/searchbtn.png")
        self.searchbtnimg = resize_icon(searchbtnimg, (50,50))

        searchbtnimgh = Image.open(f"{IMG_PATH}/searchbtnh.png")
        self.searchbtnimgh = resize_icon(searchbtnimgh, (50,50))

        searchbtnimgp = Image.open(f"{IMG_PATH}/searchbtnp.png")
        self.searchbtnimgp = resize_icon(searchbtnimgp, (50,50))

        ButtonImage(buttons_frame, image=self.searchbtnimg, img_h=self.searchbtnimgh, img_p=self.searchbtnimgp, command=lambda: self.__searchBills(), style='flatw.light.TButton', padding=0).grid(row=0, column=7, pady=2, padx=(0,0))

        grid_frame = tk.Frame(self.dashboard_content,)
        grid_frame.config(background='#fff')
        grid_frame.grid(row=3, column=0, columnspan=1, padx=10, pady=(0,10), sticky='nsew')
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.rowconfigure(0, weight=1)

        columns = ('code', 'pasymentStatus', 'total','documentState','description', 'client','creationDate','expirationDate','currency','exchangeRate','uc','up')

        yscroll = ttb.Scrollbar(grid_frame, 
                                orient='vertical',
                                bootstyle="dark-round")
        yscroll.grid(row=0, column=1, padx=1, pady=2,sticky='ns', rowspan=2)

        xscroll = ttb.Scrollbar(grid_frame, 
                                orient='horizontal',
                                bootstyle="dark-round")
        xscroll.grid(row=1, column=0, padx=1, pady=2,sticky='ew')

        self.budgetsGridView = ttb.Treeview(grid_frame,columns=columns,show='headings', style='cust.primary.Treeview',
                                 height=10, padding=0, xscrollcommand=xscroll.set,
                                selectmode='extended', yscrollcommand=yscroll.set)
        self.budgetsGridView.grid(row=0,column=0,padx=2,pady=(2,2),sticky='nsew')

        yscroll.configure(command=self.budgetsGridView.yview)
        xscroll.configure(command=self.budgetsGridView.xview)

        

        self.budgetsGridView.heading(columns[0],anchor='center', text='Codigo')
        self.budgetsGridView.heading(columns[1], anchor='center', text='Status del Pago')
        self.budgetsGridView.heading(columns[2], anchor='center', text='Moneda')
        self.budgetsGridView.heading(columns[3],anchor='center', text='Total')
        self.budgetsGridView.heading(columns[4], anchor='center', text='Estado')
        self.budgetsGridView.heading(columns[5],anchor='center', text='Description')
        self.budgetsGridView.heading(columns[6], anchor='center', text='Cliente')
        self.budgetsGridView.heading(columns[7],anchor='center', text='Fecha de Creacion')
        self.budgetsGridView.heading(columns[8], anchor='center', text='Fecha de Vencimiento')
        self.budgetsGridView.heading(columns[9], anchor='center', text='Tasa de Cambio')
        self.budgetsGridView.heading(columns[10], anchor='center', text='Creador')
        self.budgetsGridView.heading(columns[11], anchor='center', text='Procesamiento')

        self.budgetsGridView.column(columns[0],width=100,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[1],width=130,stretch=True,anchor='center')
        self.budgetsGridView.column(columns[2],width=90,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[3],width=140,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[4],width=120,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[5],width=300,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[6],width=200,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[7],width=160,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[8],width=170,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[9],width=140,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[10],width=160,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[11],width=160,stretch=False,anchor='center')
        self.budgetsGridView.bind('<<TreeviewSelect>>', lambda e: self.__enabled_view())

        

        ####### AMOUNT RECORD WIDGET #########



        profitCard = CTkFrame(content, fg_color='#06283D')
        profitCard.grid(row=0, column=0, sticky='nsew', padx=(0,5),pady=(0,5))
        profitCard.columnconfigure(0, weight=1)
        profitCard.rowconfigure(2, weight=1)

        efeIcon = Image.open(f"{IMG_PATH}/product_icon.png")
        self.efeIcon = resize_icon(efeIcon, (45,45))

        ttb.Label(profitCard, text=" # Facturas", image=self.efeIcon, compound='left', background='#06283D', foreground='#fff', font=(GUI_FONT,12,'bold')).grid(row=0, column=0, sticky='nsew', padx=(20,20),pady=(15,5))
        ttb.Frame(profitCard, style='white.TFrame', height=1).grid(row=1, column=0,  pady=0,sticky='nsew', padx=20)
        cont = CTkFrame(profitCard, fg_color='#fff')
        cont.grid(row=2, column=0, sticky='nsew', padx=20,pady=(10,5))
        cont.columnconfigure(0, weight=1)
        cont.rowconfigure(0, weight=1)

        ttb.Label(cont, textvariable=self.bills_amount, background='#fff', anchor='center', foreground=GUI_COLORS['primary'], font=(GUI_FONT,14,'bold')).grid(row=0, column=0, sticky='nsew', padx=20,pady=10)


        ttb.Label(profitCard, text="Cantidad de Facturas", justify='center', background='#06283D', anchor='center', foreground='#fff', font=(GUI_FONT,10)).grid(row=3, column=0, sticky='nsew', padx=20,pady=(0,15))



        ####### Product to End ###########

        budgetsStateFrame = CTkFrame(content, corner_radius=10, fg_color='#212946', 
                                     border_width=2, border_color='#D0CECE')
        budgetsStateFrame.grid(row=1, column=0, padx=(1,5), sticky='nsew')
        budgetsStateFrame.columnconfigure(0, weight=1)

        ttb.Label(budgetsStateFrame, text='Ultimas 10 Facturas', font=(GUI_FONT,13,'bold'), 
                  foreground='#fff', background='#212946', anchor='w'
                ).grid(row=0, column=0, sticky='nsew', padx=20,pady=(15,5))
        
        self.r_i = resize_icon(Image.open(f'{IMG_PATH}/refresh_b.png'))
        self.r_i_h = resize_icon(Image.open(f'{IMG_PATH}/refresh_b_h.png'))

        refresh = ButtonImage(budgetsStateFrame, compound='left',  style='212946.TButton', 
                   padding=0, image=self.r_i,
                   img_h=self.r_i_h, img_p=self.r_i)
        refresh.grid(row=0, column=0, pady=(20,5), padx=20, sticky='ne')

        content = tk.Frame(budgetsStateFrame)
        content.grid(row=1, column=0, sticky='nsew', padx=20,pady=(10,10))
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)
        content.columnconfigure(2, weight=1)
        content.config(background='#212946')

    

        ttb.Label(content, text='Codigo', width=15,  background='#212946', anchor='center', font=(GUI_FONT,11,'bold'),foreground='white').grid(row=0, column=0, sticky='nsew')
        ttb.Label(content, text='Monto', width=15, background='#212946', anchor='center', font=(GUI_FONT,11,'bold'),foreground='white',).grid(row=0, column=1, sticky='nsew')
        ttb.Label(content, text='Fecha', width=10,  background='#212946', anchor='center', font=(GUI_FONT,11,'bold'),foreground='white').grid(row=0, column=2, sticky='nsew')

        ttb.Separator(content, bootstyle='danger').grid(row=1, column=0, sticky='nsew', columnspan=3, pady=(0,8))


        self.billslist = tk.Frame(content,)
        self.billslist.grid(row=2, column=0, columnspan=3, padx=2, pady=2, sticky='nsew')
        self.billslist.columnconfigure(0, weight=1)
        self.billslist.columnconfigure(1, weight=1)
        self.billslist.columnconfigure(2, weight=1)
        self.billslist.config(background='#212946')

        self.bind("<Map>",lambda e: self.update_pages())
        self.__enabled_view()
        
    def set_privileges(self):
        if constGlobal.loggued_user.rol == 1:
            self.deleteBTN.grid(row=0, column=5, sticky='nsew', pady=2, padx=(0,8))
        else:
            self.deleteBTN.grid_forget()

    def update_pages(self):
        self.__ten_bills()
        self.__searchBills()
        self.check_documents_bills()
        self.expiration_document_list_bills()
        self.set_privileges()
        
    
    def __ten_bills(self):
        for wid in self.billslist.winfo_children():
            wid.destroy()
        bills = Bill.lastFive(num_docs=10)
        if bills:
            for index, b in enumerate(bills):
                bill = Bill(**b)

                ttb.Label(self.billslist, text=f"Factura #{'0'*(6-len(str(bill.code)))+str(bill.code)}", anchor='center', foreground='#fff', background='#212946', font=(GUI_FONT,10,'bold'), ).grid(row=index*2, column=0, sticky='nsew', padx=(4,6), pady=(0,4))
                ttb.Label(self.billslist,width=10, text=f"{bill.get_currency_icon()} {bill.total_amount}" if bill.documentState !=4 else 'ANULADA', anchor='center', foreground='#fff' if bill.documentState !=4 else 'red', background='#212946', font=(GUI_FONT,10), ).grid(row=index*2, column=1, sticky='nsew', padx=(4,6), pady=(0,4))
                ttb.Label(self.billslist, width=10, text=bill.creationDate.strftime("%d-%m-%Y"), foreground=GUI_COLORS['success'],anchor='center',
                            background='#212946', font=(GUI_FONT,10), ).grid(row=index*2, column=2, padx=(0,6), pady=(0,4))
            
                ttb.Frame(self.billslist, height=1, bootstyle='info').grid(row=index*2+1, column=0, padx=12, columnspan=3, sticky='nsew', pady=(0,10))


    def __open_create_form(self):
        ask = messagebox.askquestion('Registrar','Desea crear un nuevo registro?')
        if ask == 'yes':
            window = BillForm(self, window_type='create', title='Registrar Factura')
            self.wait_window(window)
            self.__searchBills()


 

    def __get_selected_budget_code(self,):
        selected = self.budgetsGridView.focus()

        if selected:
            code = self.budgetsGridView.item(selected, 'values')[0]
           
            return Bill.findOneBill(int(code))


    def __open_view_form(self):
        budget = self.__get_selected_budget_code()
    
        if budget:
            BillForm(self, window_type='view', title='Detalles de Factura', bill=budget)
  
        del budget


    def __deleteBill(self):
        documentSelected = self.budgetsGridView.focus()
        if documentSelected:
            ask = messagebox.askquestion('Eliminar', 'Desea eliminar el registro de la factura?', parent=self)
            if ask == 'yes':
                value = self.budgetsGridView.item(documentSelected, 'values')
                document = Bill.findOneBill(value[0])
                document.deleteBill()
                messagebox.showinfo('Aviso','Factura Eliminada satisfactoriamente.', parent=self)
                self.__searchBills()


    def anular(self):
        documentSelected = self.budgetsGridView.focus()
        if documentSelected:
            ask = messagebox.askquestion('Anular', 'Desea Anular la factura seleccionada?', parent=self)
            if ask == 'yes':
                
                value = self.budgetsGridView.item(documentSelected, 'values')
                document = Bill.findOneBill(value[0])
                document.rejectBill(constGlobal.loggued_user.id)
                messagebox.showinfo('Aviso','Factura Anulada satisfactoriamente.', parent=self)
                self.__searchBills()


    def payment(self):
        documentSelected = self.budgetsGridView.focus()
        if documentSelected:
            value = self.budgetsGridView.item(documentSelected, 'values')
            document = Bill.findOneBill(value[0])
            paymentWindow = PaymentForm(self, doc=document, callback = self.__searchBills)
            self.wait_window(paymentWindow)
           


    def __enabled_view(self):
        documentSelected = self.budgetsGridView.focus()
        if documentSelected:
            value = self.budgetsGridView.item(documentSelected, 'values')
            document = Bill.findOneBill(value[0])
            self.viewBTN.config(state='normal')
            if document.documentState < 3:
                self.anularBTN.config(state='normal')
                self.payBTN.config(state='normal')
            else:
                self.anularBTN.config(state='disabled')
                self.payBTN.config(state='disabled')
            self.deleteBTN.config(state='normal')
    
        else:
            self.viewBTN.config(state='disabled')
            self.anularBTN.config(state='disabled')
            self.payBTN.config(state='disabled')
            self.deleteBTN.config(state='disabled')

    
    def __searchBills(self):
        self.budgetsGridView.delete(*self.budgetsGridView.get_children())

        items = Bill.findAllBills(value=self.SEARCHENTRY.get())

        self.budgetsGridView.tag_configure('normal', background='white')
        self.budgetsGridView.tag_configure('anulada', background='#E67A7A')

        for bill in items:


            self.budgetsGridView.insert("",ttb.END,values=(
                f"{'0'*(6-len(str(bill[0])))+str(bill[0])}",
                bill[1] if bill[10] != 4 else 'ANULADA',
                bill[2],
                bill[3],
                bill[4],
                bill[5],
                bill[6],
                bill[7],
                bill[8],
                bill[9],
                bill[10],
                bill[11] if bill[11] else '-'


        ),tags='anulada' if bill[12] ==4 else 'normal')
        self.__ten_bills()
        print(Bill.totalCountBills())
        self.bills_amount.set(int(Bill.totalCountBills()))

    def check_documents_bills(self):
        docs = Bill.get_document_to_expirate()
        if len(docs):
            doclist = ''
            for index,doc in enumerate(docs):
                doclist = f'\n {index+1}.) Codigo: {doc.code} - Proveedor: {doc.client}'
            messagebox.showwarning('Listado de Ventas',f"Las siguientes facturas expiran el dia {(datetime.today() + timedelta(days=1)).strftime('%d/%m/%Y')}:\n{doclist}")


    def expiration_document_list_bills(self):
        docs = Bill.update_document_states()
        if len(docs):
            doclist = ''
            for index,doc in enumerate(docs):
                doclist = f'\n {index+1}.) Codigo: {doc[0]} - Proveedor: {doc[1]}'
            messagebox.showwarning('Listado de Ventas',f'Las siguientes facturas han vencido:\n{doclist}')




if __name__=="__main__":
    app = ttb.Window(themename='new')
    BillPage(app).pack()
    app.mainloop()
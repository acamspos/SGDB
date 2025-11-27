import ttkbootstrap as ttb
from assets.globals import GUI_COLORS, IMG_PATH, GUI_FONT
from assets.utils import resize_icon, resize_image
from PIL import Image, ImageTk
from customtkinter import CTkFrame
import tkinter as tk

from components.buttons import ButtonImage
from assets.styles.styles import SGDB_Style

# Configuración
from assets.db.db_connection import DB
from models.entitys.budget import Budget
from models.entitys.bills import Bill
from tkinter import messagebox

class BillSelection(ttb.Toplevel):
    def __init__(self, master=None, callback=None, selectionMode = False, filter_status = None):
        PART_COLOR = GUI_COLORS['bg']
        PART2_COLOR = GUI_COLORS['primary']

        super().__init__(master)
        
        ############# CONFIGURACION VENTANA #############
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.geometry('1200x850')
        ############## ESTILOS PERSONALIZADOS ##############
        self.transient()
        self.grab_set()
        self.config(background="#D9D9D9")
        self.focus()
        ########### VARIABLES DE PAGINACION ############
        self.callback = callback
        self.filter_status = filter_status
        self.__currency = ttb.IntVar(value=1)
        self.__currency.trace_add('write',self.currency_callback)
        ####################### ELEMENTOS DE LA INTERFAZ GRAFICA #######################

        ###### TSECCION DEL TITULO:

        CURRENCY =  DB.getCurrencyList()
        self.CURRENCY_DICT = {row[1]:row[0] for row in CURRENCY}
        self.CURRENCY_DICT_VALUE = {row[0]:row[2] for row in CURRENCY}
        del CURRENCY


        ######### SECCION DE CONTENIDO:
    

        self.CONTENT_FRAME = CTkFrame(self,fg_color='#fff')
        self.CONTENT_FRAME.grid(row=0, column=0, sticky='nsew',padx=10, pady=10, )
        self.CONTENT_FRAME.columnconfigure(0, weight=1)
        self.CONTENT_FRAME.rowconfigure(3, weight=1)

        subtitle = CTkFrame(self.CONTENT_FRAME, corner_radius=6, fg_color=PART2_COLOR)
        subtitle.grid(row=0, column=0, sticky='nsew', padx=10, pady=(10,2))

        self.micon = resize_icon(Image.open(f'{IMG_PATH}/product.png'),(45,45))

        ttb.Label(subtitle, image=self.micon, background=PART2_COLOR, ).grid(row=0, column=0, rowspan=2, sticky='nsew', padx=(8), pady=8)

        ttb.Label(subtitle, text='Busqueda de Facturas Anuladas', background=PART2_COLOR, anchor='sw', font=(GUI_FONT,13,'bold'), foreground='#fff').grid(row=0, column=1, sticky='nsew', padx=(4,8), pady=(8,0))

        ttb.Label(subtitle, text='Inicio / Facturación / Busqueda', background=PART2_COLOR, anchor='nw', font=(GUI_FONT,9), foreground='#fff').grid(row=1, column=1, sticky='nsew', padx=(4,8), pady=(0,8))


     
        ttb.Frame(self.CONTENT_FRAME, bootstyle='primary').grid(row=1, column=0, sticky='nsew', padx=10, pady=5)

        buttons_frame = tk.Frame(self.CONTENT_FRAME, background='red')
        buttons_frame.config(background='#fff')
        buttons_frame.grid(row=2, column=0, sticky='nsew', padx=10)
        buttons_frame.columnconfigure(6, weight=1)


        selectimg = Image.open(f"{IMG_PATH}/select.png")
        self.selectimg = resize_icon(selectimg, (50,50))

        selectimgh = Image.open(f"{IMG_PATH}/selecth.png")
        self.selectimgh = resize_icon(selectimgh, (50,50))

        selectimgp = Image.open(f"{IMG_PATH}/selectp.png")
        self.selectimgp = resize_icon(selectimgp, (50,50))

        ButtonImage(buttons_frame, image=self.selectimg, img_h=self.selectimgh, img_p=self.selectimgp,  style='flatw.light.TButton', padding=0).grid(row=0, column=0, sticky='', pady=2, padx=(0,8))


        ttb.Separator(buttons_frame, orient='vertical',bootstyle='dark').grid(row=0, column=1, sticky='ew', padx=(0,8))


        
        self.searchEntry = ttb.Entry(buttons_frame,width=30)
        self.searchEntry.grid(row=0, column=6, ipady=3, sticky='e', padx=(0,6))
        self.searchEntry.bind('<Return>', lambda e: self.__searchBudgets())



        searchbtnimg = Image.open(f"{IMG_PATH}/searchbtn.png")
        self.searchbtnimg = resize_icon(searchbtnimg, (50,50))

        searchbtnimgh = Image.open(f"{IMG_PATH}/searchbtnh.png")
        self.searchbtnimgh = resize_icon(searchbtnimgh, (50,50))

        searchbtnimgp = Image.open(f"{IMG_PATH}/searchbtnp.png")
        self.searchbtnimgp = resize_icon(searchbtnimgp, (50,50))

        ButtonImage(buttons_frame, command=self.__searchBudgets, image=self.searchbtnimg, img_h=self.searchbtnimgh, img_p=self.searchbtnimgp, style='flatw.light.TButton', padding=0).grid(row=0, column=7, pady=2, padx=(10,0))

        grid_frame = tk.Frame(self.CONTENT_FRAME,)
        grid_frame.config(background='#fff')
        grid_frame.grid(row=3, column=0, columnspan=1, padx=10, pady=(0,10), sticky='nsew')
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.rowconfigure(0, weight=1)

        columns = ('code','description','state','type','client','address','representative','creationDate','currency',
                   'sub_total','iva','total_amount')
        yscroll = ttb.Scrollbar(grid_frame, 
                                orient='vertical',
                                bootstyle="dark-round")
        yscroll.grid(row=0, column=1, padx=1, pady=2,sticky='ns', rowspan=2)

        xscroll = ttb.Scrollbar(grid_frame, 
                                orient='horizontal',
                                bootstyle="dark-round")
        xscroll.grid(row=1, column=0, padx=1, pady=2,sticky='ew')

        self.budgetsGridView = ttb.Treeview(grid_frame,columns=columns,show='headings', style='cust.primary.Treeview',
                                 height=14, padding=0, xscrollcommand=xscroll.set,
                                selectmode='extended', yscrollcommand=yscroll.set)
        self.budgetsGridView.grid(row=0,column=0,padx=2,pady=(2,2),sticky='nsew')

        yscroll.configure(command=self.budgetsGridView.yview)
        xscroll.configure(command=self.budgetsGridView.xview)

        self.budgetsGridView.heading(columns[0],anchor='center', text='Codigo')
        self.budgetsGridView.heading(columns[1], anchor='center', text='Orden de Compra')
        self.budgetsGridView.heading(columns[2], anchor='center', text='Moneda')
        self.budgetsGridView.heading(columns[3],anchor='center', text='Total')
        self.budgetsGridView.heading(columns[4], anchor='center', text='Estado')
        self.budgetsGridView.heading(columns[5],anchor='center', text='Description')
        self.budgetsGridView.heading(columns[6], anchor='center', text='Cliente')
        self.budgetsGridView.heading(columns[7],anchor='center', text='Fecha de Creacion')
        self.budgetsGridView.heading(columns[8], anchor='center', text='Fecha de Vencimiento')
        self.budgetsGridView.heading(columns[9], anchor='center', text='Tasa de Cambio')


        self.budgetsGridView.column(columns[0],width=200,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[1],width=250,stretch=True,anchor='center')
        self.budgetsGridView.column(columns[2],width=250,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[3],width=250,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[4],width=250,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[5],width=250,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[6],width=250,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[7],width=250,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[8],width=250,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[9],width=250,stretch=False,anchor='center')

        self.budgetsGridView.tag_configure('row', background='#E7E6E6')
       
        if selectionMode:
            self.budgetsGridView.bind('<Double-1>', lambda e: self.__select_product())

        self.__searchBudgets()

    def __select_product(self):
        selected = self.budgetsGridView.focus()

        if selected:
            code = int(self.budgetsGridView.item(selected, 'values')[0])
       
            self.destroy()
            if self.callback:
                bill =Bill.findOneBill(code)
                self.callback(bill)
                self.master.grab_set()
                self.master.transient()
            del code



    def currency_callback(self, var, mode, index):
        self.__searchBudgets()


    def __searchBudgets(self):
        self.budgetsGridView.delete(*self.budgetsGridView.get_children())

        items = Bill.findRejectsBills()

        self.budgetsGridView.tag_configure('normal', background='white')
        self.budgetsGridView.tag_configure('anulada', background='#E67A7A')

        for bill in items:
            bill = Bill(**bill)

            self.budgetsGridView.insert("",ttb.END,values=(
                f"{'0'*(6-len(str(bill.code)))+str(bill.code)}",
                bill.purchaseOrder,
                bill.get_currency(),
                bill.total_amount,
                bill.documentState,
                bill.description,
                bill.get_company(),
                bill.creationDate,
                bill.expirationDate,
                bill.exchange_rate,


        ),)



        
            
            


# if __name__=="__main__":
#     app = ttb.Window(themename='new')
  
#     SGDB_Style()
#     BudgetSelection(app, filter_status=2)
#     app.mainloop()
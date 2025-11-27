import ttkbootstrap as ttb
import tkinter as tk
from assets.globals import IMG_PATH, GRAPH_PATH
from assets.globals import inventory_icon, dashboard_icon, budget_icon, invoice_icon, project_icon, statistics_icon, menu_icon
from assets.globals import pages_dict,pages_dash_access, check_internet_connection
from PIL import Image
import assets.globals as GLOBALS
from tkinter import messagebox
from window.LOGIN import Login
import assets.utils as SGDB_func
from assets.utils import display_page, set_homepage
from models.entitys.activity import Activity
import assets.globals as constGlobal
import threading
###### Import Main Pages #######
from assets.styles.styles import SGDB_Style
from pages.homepage.homepage import Homepage
from pages.dashboard.dashboard import Dashboard
from pages.budgets.budgets import BudgetMainForm
from pages.Products.product import ProductPage
from pages.Service.service import ServicePage
from pages.Machinery.machinery import MachineryPage
from pages.activities.activity import ActivityPage
from pages.bills.bills import BillPage
from pages.statistics.statisticc import StatisticsPage
from pages.purchase.purchase import PurchasePage
from pages.providers.providers import ProviderModule
from pages.clients.clients import ClientModule
from pages.representative.representative import RepresentativeModule
from pages.users.users import UsersPage
from pages.backup.respaldo import BackUp
from models.entitys.purchase import PurchaseDocument
from models.entitys.bills import Bill
from datetime import datetime, timedelta
from pages.Extras.exchange import ExchangeForm
from pages.Extras.emailSender import EmailSender

import matplotlib.pyplot as plt
plt.style.use(GRAPH_PATH)
# Images Functions 
BTN_POS = 60

class Main(ttb.Window):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        style = SGDB_Style()
        self.withdraw()
        self.log_in(self.open_app)
        self.title('SGAG')
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.img_logo = tk.PhotoImage(file=f"{str(IMG_PATH)}/logo.png")
        self.tk.call('wm', 'iconphoto', self._w, "-default", self.img_logo)
        self.iconphoto(True, self.img_logo)
        self.wm_iconphoto(True, self.img_logo)
        self.wm_iconphoto(True, self.img_logo)
        self.iconbitmap(f"{str(IMG_PATH)}/SIGAG.ico")

    def log_in(self, func):
        window = Login(self, func)
        
    def open_emailsender(self):
        if check_internet_connection:
            EmailSender(self,)
        else:
            messagebox.showwarning('Conexión','No hay conexión para enviar correos electronicos.')

    def log_out(self):
        self.withdraw()
        
        self.log_in(self.open_app_changin_user)


    def GUI_geometry(self):
        SYSTEM_WIDTH = self.winfo_screenwidth()
        SYSTEM_HEIGHT = self.winfo_screenheight()

        WIDTH = round(SYSTEM_WIDTH*0.90)
        HEIGHT = round(SYSTEM_HEIGHT*0.80)

        pwidth = (SYSTEM_WIDTH-WIDTH)//2
        pheight = (SYSTEM_HEIGHT-HEIGHT)//2

        self.geometry(str(WIDTH)+"x"+str(HEIGHT)+"+"+str(pwidth)+"+"+str(pheight-60))
        self.minsize(width=WIDTH,height=HEIGHT)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0,weight=1)
        self.config(relief='flat')

    
    def GUI_menubar(self):
        #### Creating Menu ####
        menubar = ttb.Menu(self,)       
        #### Setting Menu in the GUI ####
        self.config(menu=menubar)
        #### Creating Reports Menu Option #####

        companiesOption = ttb.Menu(menubar)
        companiesOption.add_command(label='Clientes', command=lambda: self.open_popups(ClientModule))
        companiesOption.add_command(label='Representantes', command=RepresentativeModule)
        companiesOption.add_separator()
        companiesOption.add_command(label='Proveedores', command=lambda: self.open_popups(ProviderModule))


  

        config_menu = ttb.Menu(menubar)
        
        config_menu.add_command(label='Tasa de Cambio', command=ExchangeForm)
        config_menu.add_separator()
        config_menu.add_command(label='Cerra Sesion', command=self.log_out)
        config_menu.add_command(label='Salir',command=self.destroy)

        #add the menus to the menubar
        menubar.add_cascade(label="Clientes & Proveedores",menu=companiesOption)
        menubar.add_cascade(label="Opciones",menu=config_menu)
        menubar.add_cascade(label='Correos',command=self.open_emailsender)


    def GUI_widgets(self):
        global pages_dict, pages_dash_access

        
        ######### GUI ICONS #########
        self.__inventory_icon = SGDB_func.resize_icon(inventory_icon)
        self.__dashboard_icon = SGDB_func.resize_icon(dashboard_icon)
        self.__budget_icon = SGDB_func.resize_icon(budget_icon)
        self.__bill_icon = SGDB_func.resize_icon(invoice_icon)
        self.__project_icon = SGDB_func.resize_icon(project_icon)
        self.__statistics_icon = SGDB_func.resize_icon(statistics_icon)

        self.__menu_icon = SGDB_func.resize_icon(menu_icon)

        self.__purchase_icon = SGDB_func.resize_icon(Image.open(f'{IMG_PATH}/purchase.png'))
        self.__service_icon = SGDB_func.resize_icon(Image.open(f'{IMG_PATH}/service.png'))
        self.__machinery_icon = SGDB_func.resize_icon(Image.open(f'{IMG_PATH}/machinery.png'))
        self.__users_icon = SGDB_func.resize_icon(Image.open(f'{IMG_PATH}/users.png'))
        self.__db_icon = SGDB_func.resize_icon(Image.open(f'{IMG_PATH}/db.png'))
        
        
        ########## GUI BODY SECTION ##########
        
        self.main_body = ttb.Frame(self,)
        self.main_body.grid(row=0, column=0, sticky='nsew', padx=(60, 0), )
        self.main_body.columnconfigure(0, weight=1)
        self.main_body.rowconfigure(0, weight=1)
        self.main_body.grid_propagate(0)
        

        ######### Lateral Menu Section #########
        self.aside_menu_frame = ttb.Frame(self, bootstyle='primary', width=60,borderwidth=0, relief='flat')
        self.aside_menu_frame.place(x=0, y=0, relheight=1.0)

        ########### Buttons ##########
        
        self.displayButton = ttb.Button(self.aside_menu_frame, style='aside.TButton', image=self.__menu_icon , 
                                        text='   MENU', compound='left', cursor='hand2', command=lambda:self.open_panel())
        self.displayButton.grid(row=0, column=0, sticky='nsew', ipady=3)
        self.aside_menu_frame.rowconfigure(14, weight=1)
        self.aside_menu_frame.grid_propagate(0)

        
        ttb.Separator(self.aside_menu_frame, 
                      orient="horizontal",
        ).grid(row=1, column=0, sticky='we', pady=(5,30))

            ###### Pages Buttons Frame ######

       
        
        self.dashboardButton = ttb.Button(self.aside_menu_frame,style='aside.TButton', image=self.__dashboard_icon, 
                                          text='   Dashboard', cursor='hand2',compound='left', 
                                          command=lambda:display_page(callback=self.close_panel,page=pages_dict['dashboard'],butt=self.dashboardButton))
        self.dashboardButton.grid(row=3, column=0, ipady=3,pady=2, sticky='nsew')
   

        self.budgetsButton = ttb.Button(self.aside_menu_frame,style='aside.TButton', image=self.__budget_icon, 
                                        text='   Cotización', cursor='hand2',compound='left',  
                                        command=lambda:display_page(callback=self.close_panel,page=pages_dict['budget'],butt=self.budgetsButton))
        self.budgetsButton.grid(row=4, column=0, ipady=3,pady=2, sticky='nsew')


        self.projectsButton = ttb.Button(self.aside_menu_frame,style='aside.TButton', image=self.__project_icon, 
                                         text='   Actividades', compound='left',
                                         command=lambda:display_page(callback=self.close_panel,page=pages_dict['activity'],butt=self.projectsButton))
        self.projectsButton.grid(row=5, column=0, ipady=3,pady=2, sticky='nsew')


        self.billButton = ttb.Button(self.aside_menu_frame,style='aside.TButton',image=self.__bill_icon, 
                                     text='   Facturación',cursor='hand2',compound='left',   
                                     command=lambda:display_page(callback=self.close_panel,page=pages_dict['bill'],butt=self.billButton))
        self.billButton.grid(row=6, column=0, ipady=3,pady=2, sticky='nsew')
        

        self.productButton = ttb.Button(self.aside_menu_frame,style='aside.TButton', image=self.__inventory_icon, 
                                          text='   Productos', cursor='hand2',compound='left',  
                                          command=lambda:display_page(callback=self.close_panel,page=pages_dict['product'],butt=self.productButton))
        self.productButton.grid(row=7, column=0, ipady=3,pady=2, sticky='nsew')


        self.machineryButton = ttb.Button(self.aside_menu_frame,style='aside.TButton', image=self.__machinery_icon, 
                                          text='   Maquinaria', cursor='hand2',compound='left',  
                                          command=lambda:display_page(callback=self.close_panel,page=pages_dict['machinery'],butt=self.machineryButton))
        self.machineryButton.grid(row=8, column=0, ipady=3,pady=2, sticky='nsew')
        

        self.serviceButton = ttb.Button(self.aside_menu_frame,style='aside.TButton', image=self.__service_icon, 
                                          text='   Servicios', cursor='hand2',compound='left',  
                                          command=lambda:display_page(callback=self.close_panel,page=pages_dict['service'],butt=self.serviceButton))
        self.serviceButton.grid(row=9, column=0, ipady=3,pady=2, sticky='nsew')

        self.purchaseButton = ttb.Button(self.aside_menu_frame,style='aside.TButton', image=self.__purchase_icon, 
                                          text='   Compras', cursor='hand2',compound='left',  
                                          command=lambda:display_page(callback=self.close_panel,page=pages_dict['purchase'],butt=self.purchaseButton))
        self.purchaseButton.grid(row=10, column=0, ipady=3,pady=2, sticky='nsew')


        self.statisticsButton = ttb.Button(self.aside_menu_frame,style='aside.TButton', image=self.__statistics_icon, 
                                           text='   Estadisticas', cursor='hand2', compound='left', 
                                           command=lambda:display_page(callback=self.close_panel,page=pages_dict['statistic'],butt=self.statisticsButton))
        self.statisticsButton.grid(row=11, column=0, ipady=3,pady=2, sticky='nsew')


        self.usersButton = ttb.Button(self.aside_menu_frame,style='aside.TButton', image=self.__users_icon, 
                                          text='   Usuarios', cursor='hand2',compound='left',  
                                          command=lambda:display_page(callback=self.close_panel,page=pages_dict['users'],butt=self.usersButton)
                                    )
        


        self.backupssButton = ttb.Button(self.aside_menu_frame,style='aside.TButton', image=self.__db_icon, 
                                           text='   Respaldos', cursor='hand2', compound='left',
                                           command=lambda:display_page(callback=self.close_panel,page=pages_dict['backup'],butt=self.backupssButton)
                                           )
        
        
        #self.BUTTONS_LIST = [self.homebutton,self.dashboardButton,self.budgetsButton, self.billButton,self.projectsButton,self.productButton, self.statisticsButton]

        ttb.Separator(self.aside_menu_frame, 
                      orient="horizontal"
        ).grid(row=14, column=0, sticky='wes', pady=(0,0))

            ###### Log user button ######
  
        self.__logout_icon = SGDB_func.resize_icon(Image.open(f'{IMG_PATH}/exit.png'))

        self.logoutBtb = ttb.Button(self.aside_menu_frame,
                                           style='aside.TButton', 
                                           image=self.__logout_icon, 
                                           text='   Cerrar Sesion', cursor='hand2',
                                           command=lambda: self.log_out(),
                                           compound='left', )
        self.logoutBtb.grid(row=15, column=0,  pady=0,ipady=3, sticky='nsew')

        ########## Create Principal Pages ##########
        self.pages()
        pages_dash_access.extend([[pages_dict['activity'],self.projectsButton],[pages_dict['bill'],self.billButton]])
   
    def open_popups(self,window):
        if constGlobal.loggued_user.rol==3:
            messagebox.showwarning('Privilegios','Para acceder a este modulo debe presentar un rol superior.')
        else:
            window(self)


    def set_privileges(self):
        display_page()
        if constGlobal.loggued_user.rol == 1:
            self.usersButton.grid(row=12, column=0, ipady=3,pady=2, sticky='nsew')
            self.backupssButton.grid(row=13, column=0, ipady=3,pady=2, sticky='nsew')
        else:
            self.usersButton.grid_forget()
            self.backupssButton.grid_forget()
            if constGlobal.loggued_user.rol > 2:
                self.statisticsButton.grid_forget()
        
        
    def create_pages(self):
        app = threading.Thread(target=self.pages)
        app.start()

    def open_app(self, user = None):
        self.GUI_geometry()
        self.GUI_menubar()
        self.GUI_widgets()
        self.set_privileges()
        self.wm_state('zoomed')
        self.deiconify()
        

    def open_app_changin_user(self, user = None): 
        self.wm_state('zoomed')
        self.set_privileges()
        self.update_idletasks()
        self.deiconify()
    

    def pages(self):
        global pages_dict
        pages_dict['homepage'] = Homepage(self.main_body)
        set_homepage(pages_dict['homepage'])
        
        pages_dict['dashboard'] = Dashboard(self.main_body)
        pages_dict['activity'] = ActivityPage(self.main_body)
        pages_dict['budget'] = BudgetMainForm(self.main_body)
        pages_dict['product'] = ProductPage(self.main_body)
        pages_dict['service'] = ServicePage(self.main_body)
        pages_dict['machinery'] = MachineryPage(self.main_body)
        pages_dict['bill'] = BillPage(self.main_body)
        pages_dict['statistic'] = StatisticsPage(self.main_body)
        pages_dict['purchase'] = PurchasePage(self.main_body)
        pages_dict['users'] = UsersPage(self.main_body)
        pages_dict['backup'] = BackUp(self.main_body)

     
        
        
    
      



    
    def open_panel(self):
        global BTN_POS
        width = self.aside_menu_frame['width']
     
       
        width += 20
        self.aside_menu_frame.configure(width=width)  

        if width >= self.displayButton.winfo_width():
            self.aside_menu_frame.grid_propagate(1)
        

            self.displayButton.configure(command=self.close_panel)
        else:
            self.after(1, self.open_panel)


    def close_panel(self):
        global BTN_POS
  
        self.aside_menu_frame.grid_propagate(0)
        self.aside_menu_frame.config(width=60)
        self.displayButton.configure(command=self.open_panel)

    def activities_completed(self):
        acts = Activity.activities_to_complete()
        if len(acts):
            act_list = ""
            for act in acts:
                act = Activity(**act)
                act_list += f"\n Actividad #{act.id} - Cotz.: {act.budget_code}"
                act.complete_activity()
            messagebox.showinfo('Actividades', f"Actividades Completadas:\n {act_list}")


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
   

    def alerts(self):
        self.activities_completed()
        self.check_documents_bills()
        self.expiration_document_list_bills()
        self.check_documents_purchases()
        self.expiration_document_list_purchases()
       
        
            


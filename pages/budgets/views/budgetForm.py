import ttkbootstrap as ttb
from assets.globals import GUI_COLORS, IMG_PATH, GUI_FONT
from assets.utils import resize_image, resize_icon
from PIL import Image, ImageTk
from tkinter import messagebox
import tkinter as tk
from components.buttons import ButtoLabel, ButtonImage
from ttkbootstrap.scrolled import ScrolledFrame
from models.entitys.activity import Activity
from customtkinter import CTkFrame #767171
from assets.db.db_connection import DB
from assets.styles.styles import SGDB_Style
from tkinter import ttk
from models.entitys.budget import Budget, Item
from models.entitys.product import Product
from models.entitys.service import Service
from pages.clients.clients import ClientModule
from pages.budgets.views.budget_selection import BudgetSelection
from pages.representative.representative import RepresentativeModule
from pages.Products.views.product_search import ProductSelection
from pages.Service.views.service_search import ServiceSelection
from datetime import datetime
from pages.Products.views.product_form import ProductForm
from pages.Service.views.service_form import ServiceForm
from assets.globals import limitar_longitud, validate_number, on_combobox_change, on_validate_length, validateFloat
FGCOLOR = 'white'
import assets.globals as constGlobal
from assets.globals import check_internet_connection
from pages.Extras.emailSender import EmailSender
from tkinter.filedialog import askdirectory




class BudgetForm(ttb.Toplevel):
    def __init__(self, master=None,  title='',window_type='', budget = None, callback = None, *args, **kwargs):
        super().__init__(master,background='red')
        self.withdraw()
        self.protocol("WM_DELETE_WINDOW", self.close_confirmation)
        self.callback = callback

        self.window_title = title
        self.window_type = window_type
        self.title(title)
        self.anchor('center')
        
        
        
        code = str(Budget.getNextBudgetCode())
        self.ITEM_MODE = ttb.IntVar(value=0)
        self.__BUDGET: Budget = budget
        ##### VARIABLES ###########
    
        if not code.isdigit():
            code = '1'
        self.__code = ttb.StringVar(value=f"{'0'*(6-len(code))+code}")
        del code
        self.__description  = ttb.StringVar()
        self.__description.trace_add('write', lambda v,i,m: self.set_info_textarea(variable=self.__description, textarea=self.descriptionEntry))
        self.__address = ttb.StringVar()
        self.__address.trace_add('write', lambda v,i,m: self.set_info_textarea(variable=self.__address, textarea=self.addressEntry))
        self.__clientRIF = ttb.StringVar()
        self.__clientName = ttb.StringVar()
        self.__representativeId = ttb.StringVar()
        self.__representativeName = ttb.StringVar()
        self.__currency = ttb.IntVar()
        self.__currencyName = ttb.StringVar()

        self.__exchangeRate  = ttb.StringVar()
        
        self.__processingDate = ttb.StringVar()
        self.__creationDate = ttb.StringVar()
        self.__deliveryDays = ttb.StringVar()
        self.__validateDays = ttb.StringVar()
        self.__type = ttb.StringVar()
        self.__typeName = ttb.StringVar()


        self.__itemDescription = ttb.StringVar()
        self.__itemDepartment = ttb.StringVar()
        self.__itemBrand = ttb.StringVar()
        self.__itemExistence = ttb.StringVar()
        self.__itemTax = ttb.StringVar()

        self.__subTotal = ttb.DoubleVar()
        self.__iva = ttb.DoubleVar()
        self.__total = ttb.DoubleVar()


        self.__FORM_DATA = [self.__code, self.__description, self.__address, self.__clientRIF, self.__representativeId,self.__currency, self.__exchangeRate,self.__deliveryDays, self.__validateDays, self.__type]
      
        self.create_widgets()

        if budget:
            self.__set_budget_callback(budget)

        self.config(background='#D0CECE')
        #
        self.focus()
        self.grab_set()
        self.transient()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)  
        #
        self.place_window_center()
        self.deiconify()

    def close_confirmation(self):
        if self.window_type != 'view':
            ask = messagebox.askquestion('Aviso','Desea cerrar la ventana sin guardar los datos?',parent=self)
            if ask == 'yes':
                for record in self.itemsGridview.get_children():
                    data = self.itemsGridview.item(record, 'values')
                    ID = self.itemsGridview.item(record, 'text')
                    if int(ID) == 2:
                        quantity = 0
                        if self.__BUDGET:
                            quantity = Item.normalQuantity(self.__BUDGET.code, data[0])
                        product_selected = Product.findOneProduct(data[0])
                        product_selected.return_existence(int(data[4])-quantity)

                if self.window_type!='create':
                    items = self.__BUDGET.findItems()
                    for item in items:
                       
                        if item.itemType==2 and f'2-{item.itemId}' not in self.itemsGridview.get_children():
                            product_selected = Product.findOneProduct(item.itemId)
                            product_selected.reduce_existence(item.quantity)
            else:
                return
        self.destroy()


    def create_widgets(self):
        contentFrame = CTkFrame(self, fg_color='white',border_width=1,  border_color='#CFCFCF')
        contentFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=10, pady=10)

        # self.__services_icon = resize_icon(Image.open(f"{IMG_PATH}/project.png"))

        titleFrame = CTkFrame(contentFrame, fg_color='#212946')
        titleFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=8,  ipady=4,pady=(8,0))
        titleFrame.anchor('w')
        titleFrame.columnconfigure(0, weight=1)
        ttb.Label(titleFrame,  compound='left', text=self.window_title, font=(GUI_FONT, 14, 'bold'), foreground='white', background="#212946").grid(row=0,column=0, padx=10, pady=10, sticky='nsew')


        if self.window_type != 'view':
            folderBTN = Image.open(f"{IMG_PATH}/billsfile.png")
            self.folderBTN = ImageTk.PhotoImage(folderBTN.resize(resize_image(18, folderBTN.size)))
            folderBTNh = Image.open(f"{IMG_PATH}/billsfileh.png")
            self.folderBTNh = ImageTk.PhotoImage(folderBTNh.resize(resize_image(18, folderBTNh.size)))
            folderBTNp = Image.open(f"{IMG_PATH}/billsfilep.png")
            self.folderBTNp = ImageTk.PhotoImage(folderBTNp.resize(resize_image(18, folderBTNp.size)))

            self.billsfileBTN = ButtonImage(titleFrame,  command=lambda:BudgetSelection(self,self.__set_budget_callback, selectionMode=True, filter_status=1), image=self.folderBTN, img_h=self.folderBTNh, img_p=self.folderBTNp, style='212946.TButton', padding=0)
            self.billsfileBTN.grid(row=0, column=1, sticky='nsew', pady=2, padx=(0,4))


        elif self.window_type == 'view':
            pdfBTN = Image.open(f"{IMG_PATH}/pdf.png")
            self.pdfBTN = ImageTk.PhotoImage(pdfBTN.resize(resize_image(11, pdfBTN.size)))
            pdfBTNh = Image.open(f"{IMG_PATH}/pdfh.png")
            self.pdfBTNh = ImageTk.PhotoImage(pdfBTNh.resize(resize_image(11, pdfBTNh.size)))
            pdfBTNp = Image.open(f"{IMG_PATH}/pdfp.png")
            self.pdfBTNp = ImageTk.PhotoImage(pdfBTNp.resize(resize_image(11, pdfBTNp.size)))

            self.pdfBTN = ButtonImage(titleFrame,  command=lambda:self.create_pdf(), image=self.pdfBTN, img_h=self.pdfBTNh, img_p=self.pdfBTNp, style='212946.TButton', padding=0)
            self.pdfBTN.grid(row=0, column=3, sticky='nsew', pady=2, padx=(0,4))
       
        approveImg = Image.open(f"{IMG_PATH}/approve.png")
        self.approveImg = ImageTk.PhotoImage(approveImg.resize(resize_image(22, approveImg.size)))
        approveImgh = Image.open(f"{IMG_PATH}/approveh.png")
        self.approveImgh = ImageTk.PhotoImage(approveImgh.resize(resize_image(22, approveImgh.size)))
        approveImgp = Image.open(f"{IMG_PATH}/approvep.png")
        self.approveImgp = ImageTk.PhotoImage(approveImgp.resize(resize_image(22, approveImgp.size)))

        self.approveBTN = ButtonImage(titleFrame, text='   APROBAR', compound='center',  command=self.approve_budget, image=self.approveImg, img_h=self.approveImgh, img_p=self.approveImgp, style='212946.TButton', padding=0)
        

        rejectImg = Image.open(f"{IMG_PATH}/reject.png")
        self.rejectImg = ImageTk.PhotoImage(rejectImg.resize(resize_image(22, rejectImg.size)))
        rejectImgh = Image.open(f"{IMG_PATH}/rejecth.png")
        self.rejectImgh = ImageTk.PhotoImage(rejectImgh.resize(resize_image(22, rejectImgh.size)))
        rejectImgp = Image.open(f"{IMG_PATH}/rejectp.png")
        self.rejectImgp = ImageTk.PhotoImage(rejectImgp.resize(resize_image(22, rejectImgp.size)))

        self.rejectBTN = ButtonImage(titleFrame,  text='    RECHAZAR', compound='center', command=self.reject_budget, image=self.rejectImg, img_h=self.rejectImgh, img_p=self.rejectImgp, style='212946.TButton', padding=0)
        
        processImg = Image.open(f"{IMG_PATH}/editn.png")
        self.processImg = ImageTk.PhotoImage(processImg.resize(resize_image(22, processImg.size)))
        processImgh = Image.open(f"{IMG_PATH}/edith.png")
        self.processImgh = ImageTk.PhotoImage(processImgh.resize(resize_image(22, processImgh.size)))
        processImgp = Image.open(f"{IMG_PATH}/editp.png")
        self.processImgp = ImageTk.PhotoImage(processImgp.resize(resize_image(22, processImgp.size)))

        self.processBTN = ButtonImage(titleFrame,  text='PROCESAR', compound='center', command=self.process_budget, image=self.processImg, img_h=self.processImgh, img_p=self.processImgp, style='212946.TButton', padding=0)
        
        


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
        buttonss_section_frame.columnconfigure(0, weight=1)



        self.pageNum = ttb.Label(buttonss_section_frame, text='Pagina: 1/2',font=(GUI_FONT,12,'bold'), background='#fff', bootstyle='dark')
        self.pageNum.grid(row=0, column=0, sticky='nsew', padx=(6,0))



        closeimg = Image.open(f"{IMG_PATH}/closen.png")
        self.closeimg = ImageTk.PhotoImage(closeimg.resize(resize_image(20, closeimg.size)))
        closeimgh = Image.open(f"{IMG_PATH}/closeh.png")
        self.closeimgh = ImageTk.PhotoImage(closeimgh.resize(resize_image(20, closeimgh.size)))
        closeimgp = Image.open(f"{IMG_PATH}/closep.png")
        self.closeimgp = ImageTk.PhotoImage(closeimgp.resize(resize_image(20, closeimgp.size)))
        self.closeBTN = ButtonImage(buttonss_section_frame, image=self.closeimg, img_h=self.closeimgh, command=self.close_confirmation, img_p=self.closeimgp, style='flatw.light.TButton', text='CERRAR', compound='center',padding=0)
        self.closeBTN.grid(row=0, column=1, sticky='nsew', pady=2, padx=(0,4))

        
        #self.__form_fields =[self.codeEntry, self.descriptionEntry, self.departmentEntry, self.brandEntry, self.providerEntry, self.taxCombobox, self.measurementCombobox, self.currencyCombobox, self.costEntry, self.directCostEntry, self.indirectCostEntry,
                           #self.priceEntry1, self.priceEntry2, self.priceEntry3, self.profitEntry1, self.profitEntry2, self.profitEntry3, self.mainStockEntry, self.depositEntry1, self.depositEntry2, self.depositEntry3, self.depositEntry4]
        
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

        self.createBTN = ButtonImage(buttonss_section_frame,  command=self.__next_page, image=self.creatbtnimg, img_h=self.creatbtnimgh, img_p=self.creatbtnimgp, style='flatw.light.TButton', text='CONTINUAR', compound='center',padding=0)
        self.createBTN.grid(row=0, column=3, sticky='nsew', pady=2, padx=(0,4))


        self.__page = ttb.StringVar(value=1)
        self.__page.trace_add('write', lambda i,m,v: self.__set_page())

        self.__secondPage()
        self.__firstPage()

        if self.window_type == 'view':
            self.__set_form_state('readonly')
            self.currencyCombobox.config(state='disabled')
            self.typeCombobox.config(state='disabled')
            self.validateDaysEntry.config(state='disabled')
            self.deliverytimeEntry.configure(state='disabled')
        else:
            self.__set_form_state()

    

    def __next_page(self):
        if self.window_type != 'view':
            if self.__check_fields():
                messagebox.showinfo('Aviso','Datos Validados. Continuar con la sección de Items.', parent=self)
                if int(self.__type.get()) == 1:
                    self.__change_item_mode(set_manual=1)
                if float(self.__exchangeRate.get())<=0:
                    self.__exchangeRate.set(DB.getCurrencyValues(2))
            else:

                messagebox.showwarning('Aviso','Existe algunos campos por rellenar o con datos erroneos. Por favor, verificar los datos ingresados.', parent=self)
                return
        
        self.__page.set(int(self.__page.get())+1)

    def __back_page(self):
        self.__page.set(int(self.__page.get())-1)

    def __set_page(self):
        page = int(self.__page.get())
    
        if page == 2:
            if self.window_type != 'view':
                if int(self.__type.get()) == 3:
                    self.changeBTN.grid(row=0, column=8, sticky='nsew', pady=2, padx=10)
                if self.__BUDGET:
                    self.createBTN.config(command=self.__updateBudget,text='REGISTRAR')
                else:
                    self.createBTN.configure(text='REGISTRAR', command=self.__createBudget)
            else:
                self.createBTN.grid_forget()
            self.second_page.tkraise()
            self.backBTN.grid(row=0, column=2, sticky='nsew', pady=2, padx=(0,4))

        else:
           
            if not self.createBTN.winfo_ismapped():
                self.createBTN.grid(row=0, column=3, sticky='nsew', pady=2, padx=(0,4))


            self.createBTN.configure(text='CONTINUAR',command=self.__next_page)
            if page == 1:
                self.backBTN.grid_forget()
                self.firstPage.tkraise()
      
        self.pageNum.config(text=f'Pagina: {page}/2')


        
    def __secondPage(self):
        self.second_page = tk.Frame(self.mainContent)
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

            self.createNewItemBTN = ButtonImage(buttons_menu_frame,  command=lambda:self.__create_items,text='F4',compound='left', image=self.createimg, img_h=self.createimgh, img_p=self.createimgp, style='white.TButton', padding=0)
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
                                font=(GUI_FONT,12),validate="key", validatecommand=(self.register(lambda e: on_validate_length(e,lenght=20)), '%P')
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
        ttb.Label(tags_frames, textvariable=self.__currencyName, font=(GUI_FONT,11,'bold'), bootstyle='danger', anchor='center', width=8, padding='10 5').grid(row=0, column=6, sticky='nsew', pady=2)
   
     
    def __firstPage(self):
        
      


        self.firstPage = tk.Frame(self.mainContent)
        self.firstPage.config(background=FGCOLOR)
        self.firstPage.grid(row=0, column=0, sticky='nsew', pady=(0,2))
        self.firstPage.columnconfigure(1, weight=1)

        code_label = ttb.Label(self.firstPage, 
                                      anchor='w', 
                                      text='Codigo', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        code_label.grid(row=0, column=0, padx=(4,0), pady=(4,0), ipadx=8,  ipady=4, sticky='nsew')

        self.codeEntry = ttb.Entry(self.firstPage, textvariable=self.__code,
                                       width=30, state='readonly',justify='center',)
        self.codeEntry.grid(row=1, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=4, columnspan=1)


        description_label = ttb.Label(self.firstPage, 
                                      anchor='w', 
                                      text='Descripcion', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        description_label.grid(row=0, column=1, padx=(4,0), pady=(4,0), ipadx=8,  ipady=4, sticky='nsew')


        self.descriptionEntry = ttb.Text(self.firstPage, height=2)
        self.descriptionEntry.grid(row=1, column=1, sticky='nsew',pady=(2,0),padx=4, ipady=4)
        self.descriptionEntry.bind('<KeyPress>', lambda e: limitar_longitud(self.descriptionEntry, 400))
        self.descriptionEntry.bind('<KeyRelease>', lambda e: limitar_longitud(self.descriptionEntry, 400))
        self.descriptionEntry.bind('Control-v', lambda e: limitar_longitud(self.descriptionEntry, 400))



        

        address_label = ttb.Label(self.firstPage, 
                                     anchor='w', 
                                     text='Direccion', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=('arial',11,'bold'))
        address_label.grid(row=4, column=0, padx=(4,0), pady=(4,0), ipadx=8,  ipady=4, sticky='nsew')


      


        self.addressEntry = ttb.Text(self.firstPage, height=2)
        self.addressEntry.grid(row=5, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=4, columnspan=2)
        self.addressEntry.bind('<KeyPress>', lambda e: limitar_longitud(self.addressEntry, 400))
        self.addressEntry.bind('<KeyRelease>', lambda e: limitar_longitud(self.addressEntry, 400))
        self.addressEntry.bind('Control-v', lambda e: limitar_longitud(self.addressEntry, 400))

        moreInfoFrame = tk.Frame(self.firstPage)
        moreInfoFrame.config(background=FGCOLOR)
        moreInfoFrame.grid(row=6, column=0, sticky='nsew', columnspan=2, pady=(0,12))
        moreInfoFrame.columnconfigure(0, weight=1)
        moreInfoFrame.columnconfigure(1, weight=1)
     

        
      

        client_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Cliente', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=('arial',11,'bold'))
        client_label.grid(row=0, column=0, padx=(4,0), pady=(4,0), ipadx=8,  ipady=4, sticky='nsew')
        
        client_frame = tk.Frame(moreInfoFrame)
        client_frame.config(background=FGCOLOR)
        client_frame.grid(row=1, column=0, sticky='nsew' ,pady=(4,0),padx=(4,10),)
        client_frame.columnconfigure(1,weight=1)

        client_frame.anchor('w')
        
        self.clientRIFEntry = ttb.Entry(client_frame,state='readonly', justify='center', textvariable=self.__clientRIF)
        self.clientRIFEntry.grid(row=0, column=0, sticky='nsw')


        self.clientNameEntry = ttb.Entry(client_frame,state='readonly', textvariable=self.__clientName)
        self.clientNameEntry.grid(row=0, column=1, sticky='nsew',padx=(6,0), ipady=4,)

        if self.window_type != 'view':
        
            self.client_search_btn = ttb.Button(client_frame, 
                                            command=self.__open_client_selection,
                                            text='...',
                                            bootstyle='dark')
            self.client_search_btn.grid(row=0, column=2, padx=2, sticky='nsew', pady=1)





        
        

        
        representante_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Representante', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=('arial',11,'bold'))
        representante_label.grid(row=0, column=1, padx=(4,0), pady=(4,0), ipadx=8,  ipady=4, sticky='nsew')
        
        representante_frame = tk.Frame(moreInfoFrame)
        representante_frame.config(background=FGCOLOR)
        representante_frame.grid(row=1, column=1, sticky='nsew' ,pady=(4,0),padx=(4,10),)
        representante_frame.columnconfigure(1,weight=1)

        representante_frame.anchor('w')
        
        self.representanteRIFEntry = ttb.Entry(representante_frame, state='readonly', justify='center',textvariable=self.__representativeId)
        self.representanteRIFEntry.grid(row=0, column=0, sticky='nsw')

        self.representativeNameEntry = ttb.Entry(representante_frame, state='readonly',textvariable=self.__representativeName  )
        self.representativeNameEntry.grid(row=0, column=1, sticky='nsew',padx=(6,0), ipady=4,)

        if self.window_type != 'view':
        
            self.representante_search_btn = ttb.Button(representante_frame, 
                                            command=self.__open_representative_selection,
                                            text='...',
                                            bootstyle='dark')
            self.representante_search_btn.grid(row=0, column=2, padx=2, sticky='nsew', pady=1)



        currency_label = ttb.Label(moreInfoFrame, 
                                   anchor='w', 
                                   text='Moneda', 
                                   background=FGCOLOR,
                                   font=(GUI_FONT,11,'bold'))
        currency_label.grid(row=2, column=0, padx=5, pady=(4,0), ipadx=8,  ipady=4,sticky='nsew')
     
        
        self.currencyCombobox = ttb.Combobox(moreInfoFrame, state='readonly',
                                    style='list.TCombobox')
        self.currencyCombobox.grid(row=3, column=0, padx=(4,10), pady=(4,0), sticky='nsew')


        CURRENCY =  DB.getCurrencyList()
        self.CURRENCY_DICT = {row[1]:row[0] for row in CURRENCY}
        self.CURRENCY_DICT_VALUE = {row[0]:row[2] for row in CURRENCY}
        del CURRENCY



        def set_exchange_rate(var,index,mode):
            value = self.CURRENCY_DICT_VALUE[self.__currency.get()]
            if value == 1:
                value = 0.0
            self.__exchangeRate.set(value)

     
        
        self.currencyCombobox = ttb.Combobox(moreInfoFrame, values=list(self.CURRENCY_DICT.keys()), state='readonly', style='selectionOnly.TCombobox', textvariable=self.__currencyName, font=(GUI_FONT,10,'bold'))
        self.currencyCombobox.grid(row=3, column=0, padx=(4,10), pady=(4,0), sticky='nsew')
        self.currencyCombobox.bind("<<ComboboxSelected>>", lambda e: on_combobox_change(e,self.__currency, self.CURRENCY_DICT, self.currencyCombobox))
        self.currencyCombobox.current(0)
        self.__currency.trace_add('write', set_exchange_rate)
        self.__currency.set(1)



        exchangeratelabel = ttb.Label(moreInfoFrame, 
                                   anchor='w', 
                                   text='Tasa de Cambio', 
                                   background=FGCOLOR,
                                   font=(GUI_FONT,11,'bold'))
        exchangeratelabel.grid(row=2, column=1, padx=5, pady=(4,0), ipadx=8,  ipady=4,sticky='nsew')
     
        
        self.exchangerateEntry = ttb.Entry(moreInfoFrame, textvariable=self.__exchangeRate,validate="key",validatecommand=(self.register(validateFloat), "%P"), justify='center')
        self.exchangerateEntry.grid(row=3, column=1, padx=(4,10), pady=(2,0), sticky='nsew')



        deliverytimelabel = ttb.Label(moreInfoFrame, 
                                   anchor='w', 
                                   text='Tiempo de Entrega (Dias)', 
                                   background=FGCOLOR,
                                   font=(GUI_FONT,11,'bold'))
        deliverytimelabel.grid(row=4, column=0, padx=5, pady=(4,0), ipadx=8,  ipady=4,sticky='nsew')
     
        
        self.deliverytimeEntry = ttb.Combobox(moreInfoFrame, values=['INMEDIATA','15','30','Personalizado'],state='readonly',font=(GUI_FONT,10,'bold'),
                                    style='selectionOnly.TCombobox', textvariable=self.__deliveryDays)
        self.deliverytimeEntry.grid(row=5, column=0, padx=(4,10), pady=(2,0), sticky='nsew')
        self.deliverytimeEntry.bind("<<ComboboxSelected>>", lambda e: self.selection_days(self.__deliveryDays,"Entrega"))



        validateDayslabel = ttb.Label(moreInfoFrame, 
                                   anchor='w', 
                                   text='Dias de Validez', 
                                   background=FGCOLOR,
                                   font=(GUI_FONT,11,'bold'))
        validateDayslabel.grid(row=4, column=1, padx=5, pady=(4,0), ipadx=8,  sticky='nsew')
     
        
        self.validateDaysEntry =  ttb.Combobox(moreInfoFrame, values=['5','10','15','30','Personalizado'],state='readonly',font=(GUI_FONT,10,'bold'),
                                    style='selectionOnly.TCombobox', textvariable=self.__validateDays)
        self.validateDaysEntry.grid(row=5, column=1, padx=(4,10), pady=(2,0), sticky='nsew')
        self.validateDaysEntry.bind("<<ComboboxSelected>>", lambda e: self.selection_days(self.__validateDays,"Validez"))




        type_label = ttb.Label(moreInfoFrame, 
                                   anchor='w', 
                                   text='Tipo de Cotizacion', 
                                   background=FGCOLOR,
                                   font=(GUI_FONT,11,'bold'))
        type_label.grid(row=6, column=0, padx=5, pady=(4,0), ipadx=8,  ipady=4,sticky='nsew')


        TYPE =  DB.getBudgetsTypeList()
        TYPE_DICT = {row[1]:row[0] for row in TYPE}
        del TYPE

        
        self.typeCombobox = ttb.Combobox(moreInfoFrame, values=list(TYPE_DICT.keys()),state='readonly',textvariable=self.__typeName,font=(GUI_FONT,10,'bold'),
                                   style='selectionOnly.TCombobox',)
        self.typeCombobox.grid(row=7, column=0, padx=(4,10), pady=(2,0), sticky='nsew')
        self.typeCombobox.bind("<<ComboboxSelected>>", lambda e: on_combobox_change(e,self.__type, TYPE_DICT, self.typeCombobox))
        self.typeCombobox.current(0)
        self.__type.set(1)

        self.BUDGET_FIELDS = [ self.descriptionEntry, self.addressEntry, self.exchangerateEntry]


        self.creationDateLabel = ttb.Label(moreInfoFrame, 
                                   anchor='w', 
                                   text='Fecha de Creacion', 
                                   background=FGCOLOR,
                                   font=(GUI_FONT,11,'bold'))
        
     
        
        self.creationDate = ttb.Entry(moreInfoFrame, textvariable=self.__creationDate, state='readonly')


        self.processingDateLabel = ttb.Label(moreInfoFrame, 
                                   anchor='w', 
                                   text='Fecha de Procesamiento', 
                                   background=FGCOLOR,
                                   font=(GUI_FONT,11,'bold'))
        
     
        
        self.processingDate = ttb.Entry(moreInfoFrame, textvariable=self.__processingDate, state='readonly')

        



    def approve_budget(self):
        ask = messagebox.askquestion('Procesar',"Confirmacion de aprobacion de Cotizacion. Ejecutar accion?", parent=self)
        if ask == 'yes':
            self.__BUDGET.approve(constGlobal.loggued_user.id)
            self.__set_order_code()
            self.__set_budget_callback(self.__BUDGET.code)
            self.callback()
            self.place_window_center()
            messagebox.showinfo('Aviso','Cotizacion Aprobada!', parent=self)

    def reject_budget(self):
        ask = messagebox.askquestion('Procesar',"Confirmacion para rechazar Cotizacion. Ejecutar accion?", parent=self)
        if ask == 'yes':
            self.__BUDGET.reject(constGlobal.loggued_user.id)
            self.__set_budget_callback(self.__BUDGET.code)
            self.callback()
            messagebox.showinfo('Aviso','Cotizacion Rechazada!', parent=self)
    
    def process_budget(self):
        ask = messagebox.askquestion('Procesar',"Confirmacion para procesar la Cotizacion. Ejecutar accion?", parent=self)
        if ask == 'yes':
            self.__BUDGET.process(constGlobal.loggued_user.id)
            self.callback()
            self.__set_budget_callback(self.__BUDGET.code)
            
            messagebox.showinfo('Aviso','Cotizacion Procesada!', parent=self)


    def __selection_options(self):
        if self.itemsGridview.selection()!= ():
            self.deleteoneBTN.config(state='normal')
        else:
            self.deleteoneBTN.config(state='disabled')


    def selection_days(self, var, title):
        option_selected = var.get()
        if option_selected == 'Personalizado':
            self.set_personalized_days(var, title)



   


    def __set_form_state(self, state = 'normal'):
        fieldsButtons = []
        fieldsButtons.extend(self.BUDGET_FIELDS)
        for field in fieldsButtons:
            if field.winfo_class() != 'TEntry' and state=='readonly':
                newstate='disabled'
                field.config(state=newstate)
                del newstate

                self.descriptionEntry.config(background='#D3D6DF', highlightcolor=GUI_COLORS['primary'], borderwidth=1)
                self.addressEntry.config(background='#D3D6DF', highlightcolor=GUI_COLORS['primary'], borderwidth=1)
            else:
                field.config(state=state)

        del fieldsButtons
        
    
    def set_personalized_days(self, variable, title):

        def set_days():
            if self.daysEntry.get():
                variable.set(self.daysEntry.get())
                window.destroy()
            else:
                messagebox.showwarning('Seleccionar',f'Debes Ingresar los días de {title}.', parent=self)

        window = ttb.Toplevel(title='Seleccion de Dias', toolwindow=True)
        window.resizable(0,0)
        window.focus()
        window.grab_set()
        auxFrame = CTkFrame(window, fg_color='white')
        auxFrame.grid(row=0, column=0, padx=10, pady=10)


        code_label = ttb.Label(auxFrame, 
                                      anchor='w', 
                                      text=f'Días de {title}', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        code_label.grid(row=0, column=0, padx=(4,4), pady=(4,0), ipadx=8,  ipady=4, sticky='nsew')

        self.daysEntry = ttb.Entry(auxFrame,   width=30, justify='center',validate="key",
                                    validatecommand=(self.register(validate_number), "%S"))
        self.daysEntry.grid(row=1, column=0, sticky='nsew',pady=(2,8),padx=10, ipady=4, columnspan=1)
        self.daysEntry.focus()

        addimg = Image.open(f"{IMG_PATH}/greenButton.png")
        self.addimg = ImageTk.PhotoImage(addimg.resize(resize_image(19, addimg.size)))
        addimgh = Image.open(f"{IMG_PATH}/greenButtonh.png")
        self.addimgh = ImageTk.PhotoImage(addimgh.resize(resize_image(19, addimgh.size)))
        addimgp = Image.open(f"{IMG_PATH}/greenButtonp.png")
        self.addimgp = ImageTk.PhotoImage(addimgp.resize(resize_image(19, addimgp.size)))

        self.selectDaysBTN = ButtonImage(auxFrame,  command=set_days, compound='center', text='SELECCIONAR',image=self.addimg, img_h=self.addimgh, img_p=self.addimgp, style='flatw.light.TButton', padding=0)
        self.selectDaysBTN.grid(row=2, column=0, sticky='', pady=(0,8), padx=(4))

        self.wait_window(window)
        if variable.get() == 'Personalizado':
            variable.set('')
        self.grab_set()


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
        self.__clientRIF.set(client.rif)
        self.__clientName.set(client.name)


    def __open_representative_selection(self):
        if self.__clientRIF.get():
            select_window = RepresentativeModule( callback = self.__set_representative_info, selectionMode=True, filter_company=self.__clientRIF.get())
            self.wait_window(select_window)
            self.grab_set()
            self.transient()
        else:
            messagebox.showwarning('Aviso','Debes seleccionar un cliente antes de poder seleccionar a un proveedor.', parent=self)

 

    def __set_representative_info(self,repre):
        self.__representativeId.set(repre.id)
        self.__representativeName.set(repre.name)


    def __check_fields(self):
 
        self.__description.set(self.descriptionEntry.get('1.0', ttb.END).replace('\n',''))
        self.__address.set(self.addressEntry.get('1.0', ttb.END).replace('\n',''))

        return not '' in [value.get() for value in self.__FORM_DATA] and not 0 in [value.get() for value in self.__FORM_DATA] 
    

    def __open_selection_items_modals(self):
        if self.ITEM_MODE.get() == 0:
            window = ProductSelection(self, callback=self.__set_product, selectionMode=True)
        else:
            window = ServiceSelection(self, callback=self.__set_service, selectionMode=True)

    
    def __set_product(self, product):
        self.__clean()
        self.code_entry.insert(0, product.code)

        currency = self.__currency.get()

        product_rate = 1
        document_rate = float(self.__exchangeRate.get())

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
       
        currency = self.__currency.get()

        service_rate = 1
        document_rate = float(self.__exchangeRate.get())

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

    

    def budgetInstance(self):
        return Budget(
            code=int(self.__code.get()),
            description=self.__description.get(),
            client=self.__clientRIF.get(),
            address=self.__address.get(),
            representative=self.__representativeId.get(),
            creationDate=datetime.today().strftime('%Y-%m-%d'),
            deliveryDays=self.__deliveryDays.get() if self.__deliveryDays.get().isdigit() else 0,
            validationDays=self.__validateDays.get(),
            currency=self.__currency.get(),
            state=1,
            exchange_rate=self.__exchangeRate.get(),
            type=int(self.__type.get()),
            sub_total=self.__subTotal.get(),
            iva=self.__iva.get(),
            total_amount=self.__total.get(),
            creationUser=constGlobal.loggued_user.id
        )
    

    def getItemsList(self):
        items = []
        all_items = self.itemsGridview.get_children()

        for item_id in all_items:
            typeI = self.itemsGridview.item(item_id, 'text')

            values = self.itemsGridview.item(item_id, 'values')
  
            items.append({'itemType':int(typeI), 'itemId':values[0],'itemDescription':values[1],'quantity':values[4],'cost':values[3],
                          'price':values[-2], 'total_price':values[-2],'totalUSD':values[-1], 'currency':self.__currency.get(), 'date':datetime.today().strftime('%Y-%m-%d')})
        return items
    


    def __updateBudget(self):
        if self.__check_item_list():
            ask = messagebox.askquestion('Modificar','Modificar Cotizacion?', parent=self)
            if ask == 'yes':
                budget = self.budgetInstance()
                budget.update(items=self.getItemsList())
                messagebox.showinfo('Aviso','Cotizacion actualizada satisfactoriamente.', parent=self)
                ask_2 = messagebox.askquestion('Procesar','Desea procesar la cotizacion?', parent=self)
                if ask_2 == 'yes':
                    budget.process(constGlobal.loggued_user.id)
                    ask_3 = messagebox.askquestion('Pdf','Generar PDF de la cotizacion?', parent=self)
                    if ask_3 == 'yes':
                        path = askdirectory(parent=self)
                        if path:
                            document = budget.create_pdf(path, parent=self)

                            if check_internet_connection and document:
                                ask_3 = messagebox.askquestion('Email','Desea enviar la cotizacion por correo?', parent=self)
                                if ask_3 =='yes':
                                    user = budget.collect_data_for_email()
                                    EmailSender(self, user=user,file=document)
                        else:
                            messagebox.showinfo('Aviso','Proceso Cancelado. No se genero el PDF del documento.', parent=self)
                else:
                    messagebox.showinfo('Actualizacion','Cotizacion Almacenada en modo edicion.', parent=self)
                self.destroy()

        else:
            messagebox.showwarning('Aviso','Debe selecionar los items que estaran vinculados a esta cotizacion!', parent=self)

    

    def __createBudget(self):
        if self.__check_item_list():
            ask = messagebox.askquestion('Crear','Crear nuevo Cotizacion?', parent=self)
            if ask == 'yes':
                newBudget = self.budgetInstance()
                newBudget.create(items=self.getItemsList())
                messagebox.showinfo('Aviso','Cotizacion creada satisfactoriamente.', parent=self)
                ask_2 = messagebox.askquestion('Procesar','Desea procesar la cotizacion?', parent=self)
                if ask_2 == 'yes':
                    newBudget.process(constGlobal.loggued_user.id)
                    ask_3 = messagebox.askquestion('Pdf','Generar PDF de la cotizacion?', parent=self)
                    if ask_3 == 'yes':
                        path = askdirectory(parent=self)
                        if path:
                            document = newBudget.create_pdf(path,parent=self)

                            if document:
                                ask_3 = messagebox.askquestion('Email','Desea enviar la cotizacion por correo?', parent=self)
                                if ask_3 =='yes':
                                    users = newBudget.collect_data_for_email()
                                    EmailSender(self, user=users,file=document)
                        else:
                            messagebox.showinfo('Aviso','Proceso Cancelado. No se genero el PDF del documento.', parent=self)
                else:
                    messagebox.showinfo('Registro','Cotizacion Almacenada en modo edicion.', parent=self)
                self.destroy()

        else:
            messagebox.showwarning('Aviso','Debe selecionar los items que estaran vinculados a esta cotizacion!', parent=self)

                
    def __check_item_list(self):
        return len(self.itemsGridview.get_children()) > 0


    def editProductRecord(self):
        if self.__check_fields():
            ask = messagebox.askquestion('Modificar','Modificar el Registro de Producto?', parent=self)
            if ask == 'yes':
                self.__field_num_entrys()
                newProdcut = self.productInstance()
                newProdcut.update()
                messagebox.showinfo('Aviso','Registro modificado satisfactoriamente.', parent=self)
          
        else:
            messagebox.showwarning('Aviso','Existen algunos campos invalidos o faltan por rellenar.', parent=self)

    
    
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
        self.itemsGridview.item(f"{itemtype}-{code}", values=(data[0],data[1],data[2],data[3],newAmount,price, total,total if self.__currency.get() == 2 else round(float(total)/float(self.__exchangeRate.get()),2),))
        
       

    def __add_product(self, amount, price):
        if amount <= self.ITEM_SELECTED.stock:
            if not f'2-{self.ITEM_SELECTED.code}' in self.itemsGridview.get_children():
                total = round(price*amount,2)
                self.itemsGridview.insert("",
                id=f'2-{self.ITEM_SELECTED.code}',
                text=2,
                index=ttb.END,
                values=(self.ITEM_SELECTED.code,
                    self.ITEM_SELECTED.description,
                    'Producto',
                   self.ITEM_SELECTED.cost if self.ITEM_SELECTED.currency == 2 else round(float(self.ITEM_SELECTED.cost)/float(self.__exchangeRate.get()),2),
                    amount, 
                    price, 
                    total,
                    total if self.__currency.get() == 2 else round(float(total)/float(self.__exchangeRate.get()),2),),
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
                    total if self.__currency.get() == 2 else round(float(total)/float(self.__exchangeRate.get()),2),),
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

    def __set_order_code(self):
        def set_purchaseOrder():
            CODE = self.ORDENPURCHESA.get()
            if CODE:
                ask = messagebox.askquestion('Confirmacion', f'El codigo de Compra para la cotizacion sera: {CODE}?',parent=window)
                if ask == 'yes':
                    self.__BUDGET.setPurchaseOrder(CODE)
                    window.destroy()
                
            

        window = ttb.Toplevel(title='Orden de Compraa', toolwindow=True)
        window.resizable(0,0)
        window.focus()
        window.grab_set()
        auxFrame = CTkFrame(window, fg_color='white')
        auxFrame.grid(row=0, column=0, padx=10, pady=10)


        code_label = ttb.Label(auxFrame, 
                                      anchor='w', 
                                      text=f'Codigo de Orden de Compra', 
                                      bootstyle='primary', 
                                      background='#fff',
                                      font=('arial',11,'bold'))
        code_label.grid(row=0, column=0, padx=(4,4), pady=(4,0), ipadx=8,  ipady=4, sticky='nsew')

        self.ORDENPURCHESA = ttb.Entry(auxFrame,   width=30, justify='center',)
        self.ORDENPURCHESA.grid(row=1, column=0, sticky='nsew',pady=(2,8),padx=10, ipady=4, columnspan=1)
        self.ORDENPURCHESA.focus()

   

        addimg = Image.open(f"{IMG_PATH}/greenButton.png")
        self.addimg = ImageTk.PhotoImage(addimg.resize(resize_image(19, addimg.size)))
        addimgh = Image.open(f"{IMG_PATH}/greenButtonh.png")
        self.addimgh = ImageTk.PhotoImage(addimgh.resize(resize_image(19, addimgh.size)))
        addimgp = Image.open(f"{IMG_PATH}/greenButtonp.png")
        self.addimgp = ImageTk.PhotoImage(addimgp.resize(resize_image(19, addimgp.size)))

        self.acceptBTN = ButtonImage(auxFrame,  command=set_purchaseOrder, compound='center', text='ACEPTAR',image=self.addimg, img_h=self.addimgh, img_p=self.addimgp, style='flatw.light.TButton', padding=0)
        self.acceptBTN.grid(row=2, column=0, sticky='', pady=(0,8), padx=(4))
        window.place_window_center()
        self.wait_window(window)
        self.grab_set()
        self.transient()
        self.focus()
       
    def create_pdf(self):
        ask = messagebox.askquestion('PDF','Crear pdf de la Cotización?', parent=self)
        if ask == 'yes':
          
            path = askdirectory(parent=self)
            if path:
                document = self.__BUDGET.create_pdf(path,parent=self)

                if document:
                    ask_3 = messagebox.askquestion('Email','Desea enviar la cotizacion por correo?', parent=self)
                    if ask_3 =='yes':
                        users = self.__BUDGET.collect_data_for_email()
                        EmailSender(self, user=users,file=document)
            else:
                messagebox.showinfo('Aviso','Proceso Cancelado. No se genero el PDF del documento.', parent=self)
           
            
    
    def __set_items(self):
        self.itemsGridview.delete(*self.itemsGridview.get_children())
        items = self.__BUDGET.findItems()
        for item in items:
            self.itemsGridview.insert("",id=f'{item.itemType}-{item.itemId}',
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


    def __set_budget_data(self):
        self.__code.set(f"{'0'*(6-len(str(self.__BUDGET.code)))+str(self.__BUDGET.code)}")
        self.__description.set(self.__BUDGET.description)
        self.__address.set(self.__BUDGET.address)
        self.__clientRIF.set(self.__BUDGET.client)
        self.__clientName.set(self.__BUDGET.get_company())
        self.__representativeId.set(self.__BUDGET.representative)
        self.__representativeName.set(self.__BUDGET.get_representative())
        self.__currency.set(self.__BUDGET.currency)
        self.__currencyName.set(self.__BUDGET.get_currency())
        self.__exchangeRate.set(self.__BUDGET.exchange_rate)
        self.__deliveryDays.set(self.__BUDGET.deliveryDays)
        self.__validateDays.set(self.__BUDGET.validationDays)
        self.__type.set(self.__BUDGET.type)
        self.__typeName.set(self.__BUDGET.get_type())
        self.__creationDate.set(self.__BUDGET.creationDate.strftime('%d/%m/%Y'))
        if self.__BUDGET.processed == True:
            self.__processingDate.set(self.__BUDGET.processingDate.strftime('%d/%m/%Y'))

        self.__set_items()

    def __set_budget_callback(self, code):
        self.__BUDGET = Budget.findOneBudget(code)
        if self.__BUDGET.state==2:
            self.approveBTN.grid(row=0, column=1, sticky='nsew', pady=2, padx=(0,4))
            self.rejectBTN.grid(row=0, column=2, sticky='nsew', pady=2, padx=(0,4))
            self.processBTN.grid_forget()
        elif self.__BUDGET.state==1:
            self.approveBTN.grid_forget()
            self.rejectBTN.grid_forget()
            self.processBTN.grid(row=0, column=3, sticky='nsew', pady=2, padx=(0,4))
        else:
            self.approveBTN.grid_forget()
            self.rejectBTN.grid_forget()
            self.processBTN.grid_forget()

        if self.window_type == 'view':
            self.creationDateLabel.grid(row=6, column=1, padx=5, pady=(4,0), ipadx=8,  ipady=4,sticky='nsew')
            self.creationDate.grid(row=7, column=1, padx=(4,10), pady=(2,0), sticky='nsew')
        if self.__BUDGET.processed == True:
            self.processingDateLabel.grid(row=8, column=0, padx=5, pady=(4,0), ipadx=8,  ipady=4,sticky='nsew')
            self.processingDate.grid(row=9, column=0, padx=(4,10), pady=(2,0), sticky='nsew',ipady=4)
        self.__page.set(1)
        self.__set_budget_data()

    def __create_items(self):
        if self.ITEM_MODE.get() == 0:
            window = ProductForm(self, window_type='create')
        else:
            window = ServiceForm(self, window_type='create')
        self.wait_window(window)
        self.grab_set()
        self.transient()

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
          

# app =ttb.Window(themename='new')

# BudgetForm(app, title='Crear Cotizacion',window_type='create')
# app.mainloop()
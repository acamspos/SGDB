import ttkbootstrap as ttb
from assets.globals import GUI_COLORS, IMG_PATH, GUI_FONT
from assets.utils import resize_icon, resize_image
from assets.globals import invoice_icon, budget_icon, project_icon, refresh_icon
from components.buttons import ButtonImage
from PIL import Image, ImageTk
from customtkinter import CTkFrame
import tkinter as tk
from assets.styles.styles import SGDB_Style
from components.bcards import BCards
###### GRAPH LIBRARIES

from pages.Products.views.product_form import ProductForm
from tkinter import messagebox
from models.entitys.product import Product
from assets.db.db_connection import DB
import assets.globals as constGlobal
from pages.Products.views.reportes import Report

class ProductPage(ttb.Frame):
    def __init__(self, master=None):
        SGDB_Style()
        super().__init__(master, height=50, width=50)
        PART_COLOR = GUI_COLORS['bg']
        PART2_COLOR = '#212946'

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        ########## GUI ICONSr##########
        self.__dash_icon = Image.open(f'{IMG_PATH}/product_title.png')
        self.__dash_icon = ImageTk.PhotoImage(self.__dash_icon.resize(resize_image(10, self.__dash_icon.size)))
        self.numRecords = ttb.IntVar(value=0)

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
                               text=' PRODUCTOS', 
                                padding='0 0',
                               background='#212946',
                               font=('arial',15, 'bold'), 
                               foreground='#fff')
        page_title.grid(row=0, column=0, sticky='nsew',padx=(80,0))


        reportBTN = Image.open(f"{IMG_PATH}/report.png")
        self.reportBTN = ImageTk.PhotoImage(reportBTN.resize(resize_image(25, reportBTN.size)))

        
        reporthBTN = Image.open(f"{IMG_PATH}/reporth.png")
        self.reporthBTN = ImageTk.PhotoImage(reporthBTN.resize(resize_image(25, reporthBTN.size)))


        reportpBTN = Image.open(f"{IMG_PATH}/reportp.png")
        self.reportptBTN = ImageTk.PhotoImage(reportpBTN.resize(resize_image(25, reportpBTN.size)))

        ButtonImage(frame_title, image=self.reportBTN, img_h=self.reporthBTN, img_p=self.reportptBTN, command=self.__report,style='flat.light.TButton', padding=0).grid(row=0, column=1, sticky='nsew', pady=2, padx=6)

        ttb.Separator(self, orient='horizontal',bootstyle='dark').grid(row=1, column=0, sticky='nsew',padx=20)

        ######### PAGE CONTENT #########
      

        content = ttb.Frame(self)
        content.columnconfigure(0, weight=1)
        content.grid(row=2, column=0, sticky='nsew', padx=18, pady=(10,10))
        content.rowconfigure(1, weight=1)


        #### Grid Container ######
        self.dashboard_content = CTkFrame(content,fg_color='#D9D9D9',border_width=1, bg_color=PART_COLOR, border_color='#CFCFCF')
        self.dashboard_content.grid(row=0, column=0, sticky='nsew',padx=(0,8), rowspan=2)
        self.dashboard_content.columnconfigure(0, weight=1)
        self.dashboard_content.rowconfigure(3, weight=1)

        subtitle = CTkFrame(self.dashboard_content, corner_radius=6, fg_color=PART2_COLOR)
        subtitle.grid(row=0, column=0, sticky='nsew', padx=10, pady=(10,2))

        self.micon = resize_icon(Image.open(f'{IMG_PATH}/management.png'),(45,45))

        ttb.Label(subtitle, image=self.micon, background=PART2_COLOR, ).grid(row=0, column=0, rowspan=2, sticky='nsew', padx=(8), pady=8)

        ttb.Label(subtitle, text='Gestion de Inventario', background=PART2_COLOR, font=(GUI_FONT,13,'bold'), foreground='#fff').grid(row=0, column=1, sticky='nsew', padx=(4,8), pady=(8,0))

        ttb.Label(subtitle, text='Inicio/Productos', background=PART2_COLOR, font=(GUI_FONT,9), foreground='#fff').grid(row=1, column=1, sticky='nsew', padx=(4,8), pady=(0,8))

        ttb.Frame(self.dashboard_content, bootstyle='primary').grid(row=1, column=0, sticky='nsew', padx=10, pady=5)

        buttons_frame = tk.Frame(self.dashboard_content, background='red')
        buttons_frame.config(background='#D9D9D9')
        buttons_frame.grid(row=2, column=0, sticky='nsew', padx=10)
        buttons_frame.columnconfigure(5, weight=1)


        creatbtnimg = Image.open(f"{IMG_PATH}/create.png")
        self.creatbtnimg = resize_icon(creatbtnimg, (50,50))

        creatbtnimgh = Image.open(f"{IMG_PATH}/createh.png")
        self.creatbtnimgh = resize_icon(creatbtnimgh, (50,50))

        creatbtnimgp = Image.open(f"{IMG_PATH}/createp.png")
        self.creatbtnimgp = resize_icon(creatbtnimgp, (50,50))

        ButtonImage(buttons_frame, image=self.creatbtnimg, img_h=self.creatbtnimgh, img_p=self.creatbtnimgp, command=self.__open_create_form, style='#D9D9D9.TButton', padding=0).grid(row=0, column=0, sticky='nsew', pady=2, padx=(0,8))


        ttb.Separator(buttons_frame, orient='vertical',bootstyle='dark').grid(row=0, column=1, sticky='ew', padx=(0,8))

        viewbtnimg = Image.open(f"{IMG_PATH}/view.png")
        self.viewbtnimg = resize_icon(viewbtnimg, (50,50))

        viewbtnimgh = Image.open(f"{IMG_PATH}/viewh.png")
        self.viewbtnimgh = resize_icon(viewbtnimgh, (50,50))

        viewbtnimgp = Image.open(f"{IMG_PATH}/viewp.png")
        self.viewbtnimgp = resize_icon(viewbtnimgp, (50,50))
        self.viewBTN = ButtonImage(buttons_frame, image=self.viewbtnimg, img_h=self.viewbtnimgh, command=self.__open_view_form, img_p=self.viewbtnimgp, style='#D9D9D9.TButton', padding=0)
        self.viewBTN.grid(row=0, column=2, sticky='nsew', pady=2, padx=(0,8))


        editbtnimg = Image.open(f"{IMG_PATH}/editbtn.png")
        self.editbtnimg = resize_icon(editbtnimg,(50,50))

        editbtnimgh = Image.open(f"{IMG_PATH}/editbtnh.png")
        self.editbtnimgh = resize_icon(editbtnimgh, (50,50))

        editbtnimgp = Image.open(f"{IMG_PATH}/editbtnp.png")
        self.editbtnimgp = resize_icon(editbtnimgp, (50,50))

        self.editBTN = ButtonImage(buttons_frame, image=self.editbtnimg, img_h=self.editbtnimgh, img_p=self.editbtnimgp, style='#D9D9D9.TButton', padding=0, command=self.__open_edit_form)
        self.editBTN.grid(row=0, column=3, sticky='nsew', pady=2, padx=(0,8))


        deletebtnimg = Image.open(f"{IMG_PATH}/deletebtn.png")
        self.deletebtnimg = resize_icon(deletebtnimg, (50,50))

        deletebtnimgh = Image.open(f"{IMG_PATH}/deletebtnh.png")
        self.deletebtnimgh = resize_icon(deletebtnimgh, (50,50))

        deletebtnimgp = Image.open(f"{IMG_PATH}/deletebtnp.png")
        self.deletebtnimgp = resize_icon(deletebtnimgp, (50,50))

        self.deleteBTN = ButtonImage(buttons_frame, image=self.deletebtnimg, command=self.__deleteProduct, img_h=self.deletebtnimgh, img_p=self.deletebtnimgp, style='#D9D9D9.TButton', padding=0)
 


        self.SEARCHENTRY = ttb.Entry(buttons_frame, bootstyle='info', width=30)
        self.SEARCHENTRY.grid(row=0,column=5, ipady=2, padx=(0,8), sticky='e')
        self.SEARCHENTRY.bind('<Return>', lambda e: self.__findProducts())
        
        searchbtnimg = Image.open(f"{IMG_PATH}/searchbtn.png")
        self.searchbtnimg = resize_icon(searchbtnimg, (50,50))

        searchbtnimgh = Image.open(f"{IMG_PATH}/searchbtnh.png")
        self.searchbtnimgh = resize_icon(searchbtnimgh, (50,50))

        searchbtnimgp = Image.open(f"{IMG_PATH}/searchbtnp.png")
        self.searchbtnimgp = resize_icon(searchbtnimgp, (50,50))

        ButtonImage(buttons_frame, image=self.searchbtnimg, img_h=self.searchbtnimgh, command=self.__findProducts, img_p=self.searchbtnimgp, style='#D9D9D9.TButton', padding=0).grid(row=0, column=6, pady=2, padx=(0,0))

        grid_frame = tk.Frame(self.dashboard_content,)
        grid_frame.config(background='#D9D9D9')
        grid_frame.grid(row=3, column=0, columnspan=1, padx=10, pady=(0,10), sticky='nsew')
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.rowconfigure(0, weight=1)

        columns = ('code', 'description', 'brand','department','provider', 'measurement','currency')

        yscroll = ttb.Scrollbar(grid_frame, 
                                orient='vertical',
                                bootstyle="dark-round")
        yscroll.grid(row=0, column=1, padx=1, pady=2,sticky='ns', rowspan=2)

        xscroll = ttb.Scrollbar(grid_frame, 
                                orient='horizontal',
                                bootstyle="dark-round")
        xscroll.grid(row=1, column=0, padx=1, pady=2,sticky='ew')

        self.productGridview = ttb.Treeview(grid_frame,columns=columns,show='headings', style='cust.primary.Treeview',
                                 height=10, padding=0, xscrollcommand=xscroll.set,
                                selectmode='extended', yscrollcommand=yscroll.set)
        self.productGridview.grid(row=0,column=0,padx=2,pady=(2,2),sticky='nsew')

        yscroll.configure(command=self.productGridview.yview)
        xscroll.configure(command=self.productGridview.xview)

        self.productGridview.heading(columns[0],text='Codigo', anchor='w')
        self.productGridview.heading(columns[1],text='Descripcion', anchor='w')
        self.productGridview.heading(columns[2], text='Marca', anchor='w')
        self.productGridview.heading(columns[3], text='Departamento', anchor='w')
        self.productGridview.heading(columns[4],text='Proveedor', anchor='w')
        self.productGridview.heading(columns[5], text='Medida', anchor='w')
        self.productGridview.heading(columns[6], text='Moneda', anchor='w')

        self.productGridview.column(columns[0],width=140,stretch=False,anchor='w')
        self.productGridview.column(columns[1],width=400,stretch=True, minwidth=450,anchor='w')
        self.productGridview.column(columns[2],width=160,stretch=False,anchor='w')
        self.productGridview.column(columns[3],width=160,stretch=False,anchor='w')
        self.productGridview.column(columns[4],width=160,stretch=False,anchor='w')
        self.productGridview.column(columns[5],width=160,stretch=False,anchor='w')
        self.productGridview.column(columns[6],width=160,stretch=False,anchor='w')
        
        self.productGridview.bind('<<TreeviewSelect>>', lambda e: self.__enabled_view())
        ####### AMOUNT RECORD WIDGET #########

        processCardImg = Image.open(f"{IMG_PATH}/amount_card.png")
        processIconImg = Image.open(f"{IMG_PATH}/product_icon.png")
        process_card = BCards(content, 
                                    bg_color=GUI_COLORS['bg'],
                                     background_color='#222A35',
                                     value=self.numRecords, 
                                     title='# Registros',
                                     sub_title='Cantidad de Registros',
                                     card_background=processCardImg,
                                     icon=processIconImg)
        process_card.grid(row=0, column=1, padx=(0,5), pady=(0,5), sticky='n')

        ####### Product to End ###########

        budgetsStateFrame = CTkFrame(content, corner_radius=10, fg_color='#212946', 
                                     border_width=2, border_color='#D0CECE')
        budgetsStateFrame.grid(row=1, column=1, padx=(1,5), sticky='nsew')
        budgetsStateFrame.columnconfigure(0, weight=1)

        ttb.Label(budgetsStateFrame, text='Por Agotarse', font=(GUI_FONT,13,'bold'), 
                  foreground='#fff', background=PART2_COLOR, anchor='w'
                ).grid(row=0, column=0, sticky='nsew', padx=20,pady=(15,5))
        
        self.r_i = resize_icon(Image.open(f'{IMG_PATH}/refresh_b.png'))
        self.r_i_h = resize_icon(Image.open(f'{IMG_PATH}/refresh_b_h.png'))

        refresh = ButtonImage(budgetsStateFrame, compound='left',  style='212946.TButton', 
                   padding=0, image=self.r_i,
                   img_h=self.r_i_h, img_p=self.r_i)
        refresh.grid(row=0, column=0, pady=(20,5), padx=20, sticky='ne')

        self.OutofStockList = tk.Frame(budgetsStateFrame)
        self.OutofStockList.grid(row=1, column=0, sticky='nsew', padx=20,pady=(10,10))
        self.OutofStockList.columnconfigure(0, weight=1)
        self.OutofStockList.config(background=PART2_COLOR)

        

        ttb.Label(self.OutofStockList, text='Codigo',  background=PART2_COLOR, font=(GUI_FONT,11,'bold'),foreground='white').grid(row=0, column=0, sticky='nsew')
        ttb.Label(self.OutofStockList, text='Existencia',  background=PART2_COLOR, font=(GUI_FONT,11,'bold'),foreground='white', anchor='center').grid(row=0, column=1, sticky='nsew')

        ttb.Separator(self.OutofStockList, bootstyle='danger').grid(row=1, column=0, sticky='nsew', columnspan=2, pady=(0,8))

        self.producsList = tk.Frame(self.OutofStockList)
        self.producsList.config(background=PART2_COLOR)
        self.producsList.grid(row=2, column=0, sticky='nsew', padx=2,pady=(0,10), columnspan=2)
        self.producsList.columnconfigure(0, weight=1)


       
        self.bind("<Map>",lambda e: self.update_pages())

    def update_pages(self):
        self.__findProducts()
        self.set_privileges()
      
    
    def set_privileges(self):
        if constGlobal.loggued_user.rol == 1:
            self.deleteBTN.grid(row=0, column=4, sticky='nsew', pady=2, padx=(0,8))
        else:
            self.deleteBTN.grid_forget()

    def __set_out_of_stock_list(self):
        for wid in self.producsList.winfo_children():
            wid.destroy()
        products = Product.getProductsOutOfStock()
        if products:
            for index, product in enumerate(products):
                ttb.Label(self.producsList, text=product['code'], anchor='w', foreground='#fff', background='#212946', font=(GUI_FONT,10,'bold')).grid(row=index*2, column=0, sticky='nsew', padx=(4,6), pady=(0,4))
                if int(product['stock']) == 0:
                    ttb.Label(self.producsList, text='Agotado', foreground=GUI_COLORS['danger'],
                            background='#212946', font=(GUI_FONT,10,'bold')).grid(row=index*2, column=1, padx=(0,6), pady=(0,4))
                else:
                    ttb.Label(self.producsList, text=f"{product['stock']} restantes", foreground=GUI_COLORS['warning'],
                            background='#212946', font=(GUI_FONT,10,'bold')).grid(row=index*2, column=1, padx=(0,6), pady=(0,4))
                ttb.Frame(self.producsList, height=1, bootstyle='info').grid(row=index*2+1, column=0, padx=12, columnspan=2, sticky='nsew', pady=(0,10))

    def __report(self):
        ask = messagebox.askquestion('Reportes','Generar reporte de todos los productos registrados?')
        if ask == 'yes':
            Report(self,title='Productos')

    

    def __enabled_view(self):
        if self.productGridview.selection()!= ():
            self.viewBTN.config(state='normal')
            self.editBTN.config(state='normal')
            self.deleteBTN.config(state='normal')
        else:
            self.viewBTN.config(state='disabled')
            self.editBTN.config(state='disabled')
            self.deleteBTN.config(state='disabled')




    def __findProducts(self):
        self.productGridview.delete(*self.productGridview.get_children())
        products = Product.findAllProduct(name=self.SEARCHENTRY.get())
        if products:
            for product in products:
            
                self.productGridview.insert("",
                                ttb.END,
                                values=(product[0],product[1],product[2],product[3],product[4],product[5],product[6]), tags='row')
            del products
            self.__set_out_of_stock_list()
            self.numRecords.set(DB.countProductRecords())

    def __deleteProduct(self):
        ask = messagebox.askquestion('Eliminar', 'Desea eliminar el registro del producto?', parent=self)
        if ask == 'yes':
            product = self.__get_selected_product()
            product.delete()
            del product
            messagebox.showinfo('Aviso','Producto Eliminado satisfactoriamente.', parent=self)
            self.__findProducts()

    def __open_create_form(self):
        ask = messagebox.askquestion('Registrar','Desea crear un nuevo producto?', parent=self)
        if ask == 'yes':
            waitwindow = ProductForm(self, window_type='create', title='Registrar Producto',)
            waitwindow.wait_window()
            self.__findProducts()


    def __open_edit_form(self):
            product = self.__get_selected_product()
            if product:
                ask = messagebox.askquestion('Modificar','Desea modificar el registro seleccionado?', parent=self)
                if ask == 'yes':
                    waitwindow = ProductForm(self, window_type='edit', title='Modificar Proveedor', product=product)
                    waitwindow.wait_window()
                    self.__findProducts()
            del product

    def __get_selected_product(self,):
        selected = self.productGridview.focus()

        if selected:
            code = self.productGridview.item(selected, 'values')[0]
            provider = Product.findOneProduct(code)
            return provider


    def __open_view_form(self):
        product = self.__get_selected_product()

        if product:
            ProductForm(self, window_type='view', title='Detalles del Producto', product=product)

        del product
 




if __name__=="__main__":
    app = ttb.Window(themename='new')
  
    SGDB_Style()
    ProductPage(app).pack()
    app.mainloop()
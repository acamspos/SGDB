import ttkbootstrap as ttb
from assets.globals import GUI_COLORS, IMG_PATH, GUI_FONT
from assets.utils import resize_icon
from PIL import Image, ImageTk
from customtkinter import CTkFrame
import tkinter as tk

from components.buttons import ButtonImage
from assets.styles.styles import SGDB_Style

# Configuración
from assets.db.db_connection import DB
from models.entitys.machinery import Machinery

from tkinter import messagebox

class MachinerySelection(ttb.Toplevel):
    def __init__(self, master=None, callback=None, selectionMode = False, machinery_filter = None):
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
        self.machinery_filter = machinery_filter
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

        self.micon = resize_icon(Image.open(f'{IMG_PATH}/machinery.png'),(45,45))

        ttb.Label(subtitle, image=self.micon, background=PART2_COLOR, ).grid(row=0, column=0, rowspan=2, sticky='nsew', padx=(8), pady=8)

        ttb.Label(subtitle, text='Busqueda de Maquinaria', background=PART2_COLOR, anchor='sw', font=(GUI_FONT,13,'bold'), foreground='#fff').grid(row=0, column=1, sticky='nsew', padx=(4,8), pady=(8,0))

        ttb.Label(subtitle, text='Inicio / Maquinaria / Busqueda', background=PART2_COLOR, anchor='nw', font=(GUI_FONT,9), foreground='#fff').grid(row=1, column=1, sticky='nsew', padx=(4,8), pady=(0,8))


     
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

        self.__currency_icon = resize_icon(Image.open(f"{IMG_PATH}/currencyyellow.png"))
        currencyOption_mb = ttb.Menubutton(buttons_frame, 
                                    compound=ttb.LEFT,
                                    style='white.TMenubutton',
                                    image=self.__currency_icon)
        currencyOption_mb.grid(row=0,column=2,sticky='nsew',padx=6, pady=2)
        
        def set_currency(label, TAG):
            ID = self.CURRENCY_DICT[label]
            TAG.config(text=label)
            self.__currency.set(ID)

        menu3 = ttb.Menu(currencyOption_mb,tearoff=True,)
        for option in list(self.CURRENCY_DICT.keys()):
            menu3.add_command(label=option, command=lambda x=option:set_currency(x,self.currency_label))

        currencyOption_mb['menu'] = menu3

        self.currency_label = ttb.Label(buttons_frame,
                                    text='Bs.',
                                    background='#fff',
                                    font=('arial', 11, 'bold'), 
                                    anchor='center')
        self.currency_label.grid(row=0, column=3, padx=4, pady=8, ipady=2)


        ttb.Separator(buttons_frame, orient='vertical',bootstyle='dark').grid(row=0, column=5, sticky='ew', padx=(0,8))


        
        self.SEARCHENTRY = ttb.Entry(buttons_frame,width=30)
        self.SEARCHENTRY.grid(row=0, column=6, ipady=3, sticky='e', padx=(0,6))
        self.SEARCHENTRY.bind('<Return>', lambda e: self.search_value())



        searchbtnimg = Image.open(f"{IMG_PATH}/searchbtn.png")
        self.searchbtnimg = resize_icon(searchbtnimg, (50,50))

        searchbtnimgh = Image.open(f"{IMG_PATH}/searchbtnh.png")
        self.searchbtnimgh = resize_icon(searchbtnimgh, (50,50))

        searchbtnimgp = Image.open(f"{IMG_PATH}/searchbtnp.png")
        self.searchbtnimgp = resize_icon(searchbtnimgp, (50,50))

        ButtonImage(buttons_frame, command=self.search_value, image=self.searchbtnimg, img_h=self.searchbtnimgh, img_p=self.searchbtnimgp, style='flatw.light.TButton', padding=0).grid(row=0, column=7, pady=2, padx=(10,0))

        grid_frame = tk.Frame(self.CONTENT_FRAME,)
        grid_frame.config(background='#fff')
        grid_frame.grid(row=3, column=0, columnspan=1, padx=10, pady=(0,10), sticky='nsew')
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.rowconfigure(0, weight=1)

        columns = columns = ('code', 'description', 'brand','model')

        yscroll = ttb.Scrollbar(grid_frame, 
                                orient='vertical',
                                bootstyle="dark-round")
        yscroll.grid(row=0, column=1, padx=1, pady=2,sticky='ns', rowspan=2)

        xscroll = ttb.Scrollbar(grid_frame, 
                                orient='horizontal',
                                bootstyle="dark-round")
        xscroll.grid(row=1, column=0, padx=1, pady=2,sticky='ew')

        self.machineryGridView = ttb.Treeview(grid_frame,columns=columns,show='headings', style='cust.primary.Treeview',
                                 height=14, padding=0, xscrollcommand=xscroll.set,
                                selectmode='extended', yscrollcommand=yscroll.set)
        self.machineryGridView.grid(row=0,column=0,padx=2,pady=(2,2),sticky='nsew')

        yscroll.configure(command=self.machineryGridView.yview)
        xscroll.configure(command=self.machineryGridView.xview)

        self.machineryGridView.heading(columns[0],text='Codigo', anchor='w')
        self.machineryGridView.heading(columns[1],text='Descripcion', anchor='w')
        self.machineryGridView.heading(columns[2], text='Marca', anchor='w')
        self.machineryGridView.heading(columns[3], text='Modelo', anchor='w')

        self.machineryGridView.column(columns[0],width=150,stretch=False,anchor='w')
        self.machineryGridView.column(columns[1],width=300,stretch=True, minwidth=450,anchor='w')
        self.machineryGridView.column(columns[2],width=150,stretch=False,anchor='w')
        self.machineryGridView.column(columns[3],width=150,stretch=False,anchor='w')


        self.machineryGridView.tag_configure('row', background='#E7E6E6')

       
        if selectionMode:
            self.machineryGridView.bind('<Double-1>', lambda e: self.__select_machinery())

 
        
        self.search_value()

    def __select_machinery(self):
        selected = self.machineryGridView.focus()

        if selected:
            code = self.machineryGridView.item(selected, 'values')[0]
            machinery = Machinery.findOneMachinery(code=code)
            self.destroy()
            if self.callback:
                self.callback(machinery)
            del machinery

   

    def currency_callback(self, var, mode, index):
        self.search_value()


    def search_value(self):
        self.machineryGridView.delete(*self.machineryGridView.get_children())

        items = Machinery.findAllMachinerys(self.SEARCHENTRY.get(), self.machinery_filter)

        for item in items:
            
            machinery = Machinery(**item)

    

            self.machineryGridView.insert("",ttb.END,values=(
                machinery.code,
                machinery.description,
                machinery.get_brand(),
                machinery.get_model(),
            ),)

            
            


if __name__=="__main__":
    app = ttb.Window(themename='new')
  
    SGDB_Style()
    MachinerySelection(app)
    app.mainloop()
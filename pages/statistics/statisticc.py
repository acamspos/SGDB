import ttkbootstrap as ttb
from assets.globals import GUI_COLORS, IMG_PATH, GUI_FONT
from assets.utils import resize_icon, resize_image
from PIL import Image, ImageTk
from customtkinter import CTkFrame, CTkLabel
from models.entitys.activity import Activity
from ttkbootstrap.scrolled import ScrolledFrame
import tkinter as tk
from math import ceil
from components.buttons import ButtonImage
from assets.styles.styles import SGDB_Style
from components.bcards import BCards
# Configuración
from assets.db.db_connection import DB
from pages.activities.views.ActivitieCard import ActivityRow
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta
import threading

def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

date = lambda x: datetime.strptime(x, '%d/%m/%Y').strftime('%Y-%m-%d')

class StatisticsPage(ttb.Frame):
    def __init__(self, master=None):

        super().__init__(master)
        
        ############# CONFIGURACION VENTANA #############
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)
        self.master.rowconfigure(0, weight=1)
        
        ############## ESTILOS PERSONALIZADOS ##############


        ########### VARIABLES DE PAGINACION ############
        self.pag = ttb.IntVar(value=1)

        self.__ELEMENTS_PER_PAGE = 12
        self.__actualPage = ttb.IntVar(value=1)
        self.__totalPage = ttb.IntVar(value=1)
        self.growthRate = ttb.StringVar(value='0')
        self.UtilityRate = ttb.StringVar(value='0')
        self.totalBilled = ttb.DoubleVar(value=1)
        self.totalGain = ttb.DoubleVar(value=0)
        self.totalCharged = ttb.DoubleVar(value=0)




        self.__APPROVE_RATIO = ttb.StringVar(value='0%')
        self.__TOTAL_BILL = ttb.StringVar(value='0')
        self.__INVENTORY_COST = ttb.StringVar(value='$0')
        self.__SERVICES_COMPLETE = ttb.StringVar(value='0')

        self.__MACHINERY = ttb.StringVar(value='0')
        self.__PRODUCTS = ttb.StringVar(value='0')
        self.__SERVICES = ttb.StringVar(value='0')
        self.__CLIENTS = ttb.StringVar(value='0')
        self.__PROVIDERS = ttb.StringVar(value='0')
        self.__ALL_ACTIVITY = ttb.StringVar(value='0')
        self.__ALL_TASKS = ttb.StringVar(value='0')



        self.totalSpent = ttb.DoubleVar(value=1)
        self.totalPaid = ttb.DoubleVar(value=0)

        date = datetime.today()
        self.STARTDATE_SALES_FLOW = ttb.StringVar(value=datetime(year=date.year,month=1,day=1).strftime('%d/%m/%Y'))
        self.ENDDATE_SALES_FLOW = ttb.StringVar(value=date.strftime('%d/%m/%Y'))

        self.STARTDATE_INCOMES_EXPENSES = ttb.StringVar(value=datetime(year=date.year,month=1,day=1).strftime('%d/%m/%Y'))
        self.ENDDATE_INCOMES_EXPENSES = ttb.StringVar(value=date.strftime('%d/%m/%Y'))

        self.STARTDATE_PVSS = ttb.StringVar(value=datetime(year=date.year,month=1,day=1).strftime('%d/%m/%Y'))
        self.ENDDATE_PVSS = ttb.StringVar(value=date.strftime('%d/%m/%Y'))
   

        ####################### ELEMENTOS DE LA INTERFAZ GRAFICA #######################

        ###### TSECCION DEL TITULO:

        self.__act_icon = Image.open(f'{IMG_PATH}/activities_title.png')
        self.__act_icon = ImageTk.PhotoImage(self.__act_icon.resize(resize_image(10, self.__act_icon.size)))
        
        page_img_label = ttb.Label(self, image=self.__act_icon, padding='0 0')
        page_img_label.grid(row=0, column=0, sticky='nsw', pady=(10, 4), padx=20)
        page_img_label.grid_propagate(0)
        page_img_label.anchor('w')

        page_title_label = ttb.Label(page_img_label, text='ESTADISTICAS', padding='0 0', background='#203864',
                               font=('arial',15, 'bold'), foreground='#fff')
        page_title_label.grid(row=0, column=0, sticky='nsew',padx=(80,0))

        ttb.Separator(self, orient='horizontal').grid(row=1, column=0, sticky='nsew',padx=(20,0))

        ######### SECCION DE CONTENIDO:

        buttons_frame = tk.Frame(self, background='red')
        buttons_frame.grid(row=2, column=0, sticky='nsew', padx=16, pady=(0,4))
        buttons_frame.columnconfigure(5, weight=1)

        self.state_filter = ttb.IntVar(value=1)

        ttb.Radiobutton(buttons_frame,style='warning.Outline.Toolbutton', command=self.__set_page,  variable=self.state_filter, value=1, text='Finanzas').grid(row=0, column=1, sticky='nsew', pady=10, padx=(0,8))


        ttb.Radiobutton(buttons_frame,style='warning.Outline.Toolbutton', command=self.__set_page,  variable=self.state_filter, value=2, text='Rendimiento').grid(row=0, column=2, sticky='nsew', pady=10, padx=(0,8))

        ttb.Radiobutton(buttons_frame,style='warning.Outline.Toolbutton', command=self.__set_page,  variable=self.state_filter, value=3, text='Cuantitativos').grid(row=0, column=3, sticky='nsew', pady=10, padx=(0,8))


        ttb.Separator(buttons_frame,orient='horizontal').grid(row=1, column=0, columnspan=6, sticky='nsew', pady=(0,0), padx=4)
    
        self.CONTENT_FRAME = ttb.Frame(self,)
        self.CONTENT_FRAME.grid(row=3, column=0, sticky='nsew',pady=10, padx=20)
        self.CONTENT_FRAME.columnconfigure(0, weight=1)
        self.CONTENT_FRAME.rowconfigure(0, weight=1)
        self.__quantityStatistics()
        self.__capacidadStatistics()
        self.__finanzasStatistics()

        
        self.setted_page = None
        self.__set_page()

    def __set_page(self):
        if self.setted_page:
            self.setted_page.grid_forget()
        if self.state_filter.get() == 1:
            self.setted_page = self.finanzasFrame
            
        elif self.state_filter.get() == 2:
            self.setted_page = self.capacidadFrame
            
        elif self.state_filter.get() == 3:
            self.setted_page = self.quantityFrame
            
        if self.setted_page:
            self.setted_page.grid(row=0, column=0, sticky='nsew')


    def __quantityStatistics(self):
        import random
        self.quantityFrame = ttb.Frame(self.CONTENT_FRAME)
        self.quantityFrame.bind('<Map>', lambda e: self.update_cuantitativos_stats())
        self.quantityFrame.columnconfigure(0, weight=1)
        self.quantityFrame.columnconfigure(1, weight=1)


        self.quantityFrame.rowconfigure(1, weight=1)


        FRAME_METRICS_M = CTkFrame(self.quantityFrame, fg_color='#fff', border_width=1, border_color='#D0CECE')
        FRAME_METRICS_M.grid(row=0, column=0, sticky='nsew', pady=5, columnspan=2)
        FRAME_METRICS_M.rowconfigure(0, weight=1)
        FRAME_METRICS_M.columnconfigure(0, weight=2)
        FRAME_METRICS_M.columnconfigure(1, weight=1)


        metersFrame = ttb.Frame(FRAME_METRICS_M,style='white.TFrame')
        metersFrame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        metersFrame.rowconfigure(0, weight=1)
        metersFrame.columnconfigure(0, weight=1)
        metersFrame.columnconfigure(1, weight=1)
        metersFrame.anchor('center')

        self.activity_meter = ttb.Meter(metersFrame,
            metersize=190,
            amounttotal=250,
            padding=5,  stripethickness=20,
            amountused=203,bootstyle='info',subtextstyle='info',
            metertype="semi",
            subtext="Actividades Finalizadas",
            interactive=False,
            style='white.TFrame'
        )
        self.activity_meter.grid(row=0, column=0, padx=10, pady=(5,0))
        self.activity_meter.config(style='white.TFrame')

        contentFrame =  CTkFrame(metersFrame, fg_color=GUI_COLORS['info'], border_width=1, border_color='#D0CECE')
        contentFrame.grid(row=1, column=0, padx=10, pady=(0,5), sticky='nsew', )
        contentFrame.columnconfigure(0, weight=1)
        contentFrame.columnconfigure(3, weight=1)
        contentFrame.anchor('center')


        ttb.Label(contentFrame, text='Total Actividades:',background=GUI_COLORS['info'], foreground='#fff', font=(GUI_FONT,12,'bold'), anchor='w').grid(row=1, column=0, padx=6, pady=4, sticky='nsew')
        ttb.Label(contentFrame, textvariable=self.__ALL_ACTIVITY,background=GUI_COLORS['info'], foreground='#fff', font=(GUI_FONT,12,),anchor='w').grid(row=1, column=1, padx=6, pady=6, sticky='nsew')



        self.task_meter = ttb.Meter(metersFrame,
            metersize=190,
            amounttotal=1,
            padding=5,  stripethickness=20,
            amountused=1,bootstyle='danger',subtextstyle='danger',
            metertype="semi",
            subtext="Tareas Completadas",
            interactive=False,
            style='white.TFrame'
        )
        self.task_meter.grid(row=0, column=1, padx=10, pady=(5,0))
        self.task_meter.config(style='white.TFrame')
        

        contentFrame =  CTkFrame(metersFrame, fg_color=GUI_COLORS['danger'], )
        contentFrame.grid(row=1, column=1, padx=10, pady=(0,5), sticky='nsew', )
        contentFrame.anchor('center')
        
        ttb.Label(contentFrame, text='Total de Tareas:',background=GUI_COLORS['danger'], foreground='#fff', font=(GUI_FONT,12,'bold'), anchor='w').grid(row=1, column=0, padx=6, sticky='nsew')
        ttb.Label(contentFrame, textvariable=self.__ALL_TASKS,background=GUI_COLORS['danger'], foreground='#fff', font=(GUI_FONT,12,),anchor='w').grid(row=1, column=1, padx=6, sticky='nsew')


      
       
        metricsFrame = ttb.Frame(FRAME_METRICS_M, style='white.TFrame')
        metricsFrame.grid(row=0, column=1, columnspan=1, sticky='nsew',padx=5, pady=10,)
        metricsFrame.columnconfigure(0, weight=1)
        metricsFrame.columnconfigure(1, weight=1)
        metricsFrame.columnconfigure(2, weight=1)

       
        

        profitCard = CTkFrame(metricsFrame, fg_color=GUI_COLORS['primary'])
        profitCard.grid(row=0, column=0, sticky='nsew', padx=5,pady=(0,0))
        profitCard.columnconfigure(0, weight=1)
        profitCard.rowconfigure(2, weight=1)

        machinaryIcon = Image.open(f"{IMG_PATH}/machicon.png")
        self.machinaryIcon = resize_icon(machinaryIcon, (45,45))

        ttb.Label(profitCard, text=" Cantidad de Equipos", image=self.machinaryIcon, compound='left', background=GUI_COLORS['primary'], foreground='#fff', font=(GUI_FONT,12,'bold')).grid(row=0, column=0, sticky='nsew', padx=(20,20),pady=(15,5))
        ttb.Frame(profitCard, style='white.TFrame', height=1).grid(row=1, column=0,  pady=0,sticky='nsew', padx=20)
        cont = CTkFrame(profitCard, fg_color='#fff')
        cont.grid(row=2, column=0, sticky='nsew', padx=20,pady=(10,5))
        cont.columnconfigure(0, weight=1)
        cont.rowconfigure(0, weight=1)

        ttb.Label(cont, textvariable=self.__MACHINERY, background='#fff', anchor='center', foreground=GUI_COLORS['danger'], font=(GUI_FONT,14,'bold')).grid(row=0, column=0, sticky='nsew', padx=20,pady=10)


        ttb.Label(profitCard, text="Cantidad de Activos", justify='center', background=GUI_COLORS['primary'], anchor='center', foreground='#fff', font=(GUI_FONT,10)).grid(row=3, column=0, sticky='nsew', padx=20,pady=(0,15))

        profitCard = CTkFrame(metricsFrame, fg_color=GUI_COLORS['primary'])
        profitCard.grid(row=0, column=1, sticky='nsew', padx=5,pady=(0,0), columnspan=2)
        profitCard.columnconfigure(0, weight=1)
        profitCard.rowconfigure(2, weight=1)

        productIcon = Image.open(f"{IMG_PATH}/product_icon.png")
        self.productIcon = resize_icon(productIcon, (45,45))

        ttb.Label(profitCard, text=" Cantidad de Productos", image=self.productIcon, compound='left', background=GUI_COLORS['primary'], foreground='#fff', font=(GUI_FONT,12,'bold')).grid(row=0, column=0, sticky='nsew', padx=(20,20),pady=(15,5))
        ttb.Frame(profitCard, style='white.TFrame', height=1).grid(row=1, column=0,  pady=0,sticky='nsew', padx=20)
        cont = CTkFrame(profitCard, fg_color='#fff')
        cont.grid(row=2, column=0, sticky='nsew', padx=20,pady=(10,5))
        cont.columnconfigure(0, weight=1)
        cont.rowconfigure(0, weight=1)

        ttb.Label(cont, textvariable=self.__PRODUCTS, background='#fff', anchor='center', foreground=GUI_COLORS['danger'], font=(GUI_FONT,14,'bold')).grid(row=0, column=0, sticky='nsew', padx=20,pady=10)


        ttb.Label(profitCard, text="Cantidad de Activos", justify='center', background=GUI_COLORS['primary'], anchor='center', foreground='#fff', font=(GUI_FONT,10)).grid(row=3, column=0, sticky='nsew', padx=20,pady=(0,15))



        profitCard = CTkFrame(metricsFrame, fg_color=GUI_COLORS['primary'])
        profitCard.grid(row=0, column=3, sticky='nsew', padx=5,pady=(0,0))
        profitCard.columnconfigure(0, weight=1)
        profitCard.rowconfigure(2, weight=1)

        serviceicon = Image.open(f"{IMG_PATH}/serviceicon.png")
        self.serviceicon = resize_icon(serviceicon, (45,45))

        ttb.Label(profitCard, text=" Cantidad de Servicios", image=self.serviceicon, compound='left', background=GUI_COLORS['primary'], foreground='#fff', font=(GUI_FONT,12,'bold')).grid(row=0, column=0, sticky='nsew', padx=(20,20),pady=(15,5))
        ttb.Frame(profitCard, style='white.TFrame', height=1).grid(row=1, column=0,  pady=0,sticky='nsew', padx=20)
        cont = CTkFrame(profitCard, fg_color='#fff')
        cont.grid(row=2, column=0, sticky='nsew', padx=20,pady=(10,5))
        cont.columnconfigure(0, weight=1)
        cont.rowconfigure(0, weight=1)

        ttb.Label(cont, textvariable=self.__SERVICES, background='#fff', anchor='center', foreground=GUI_COLORS['danger'], font=(GUI_FONT,14,'bold')).grid(row=0, column=0, sticky='nsew', padx=20,pady=10)


        ttb.Label(profitCard, text="Cantidad de Activos", justify='center', background=GUI_COLORS['primary'], anchor='center', foreground='#fff', font=(GUI_FONT,10)).grid(row=3, column=0, sticky='nsew', padx=20,pady=(0,15))



        ############# SECOND ROW ##################

        profitCard = CTkFrame(metricsFrame, fg_color=GUI_COLORS['primary'])
        profitCard.grid(row=1, column=0, sticky='nsew', padx=5,pady=(5,0), columnspan=2)
        profitCard.columnconfigure(0, weight=1)
        profitCard.rowconfigure(2, weight=1)

        billsicon = Image.open(f"{IMG_PATH}/billsicon.png")
        self.billsicon = resize_icon(billsicon, (45,45))

        ttb.Label(profitCard, text=" Cantidad de Clientes", image=self.billsicon, compound='left', background=GUI_COLORS['primary'], foreground='#fff', font=(GUI_FONT,12,'bold')).grid(row=0, column=0, sticky='nsew', padx=(20,20),pady=(15,5))
        ttb.Frame(profitCard, style='white.TFrame', height=1).grid(row=1, column=0,  pady=0,sticky='nsew', padx=20)
        cont = CTkFrame(profitCard, fg_color='#fff')
        cont.grid(row=2, column=0, sticky='nsew', padx=20,pady=(10,5))
        cont.columnconfigure(0, weight=1)
        cont.rowconfigure(0, weight=1)

        ttb.Label(cont, textvariable=self.__CLIENTS, background='#fff', anchor='center', foreground=GUI_COLORS['danger'], font=(GUI_FONT,14,'bold')).grid(row=0, column=0, sticky='nsew', padx=20,pady=10)


        ttb.Label(profitCard, text="Cantidad total de Clientes registrados", justify='center', background=GUI_COLORS['primary'], anchor='center', foreground='#fff', font=(GUI_FONT,10)).grid(row=3, column=0, sticky='nsew', padx=20,pady=(0,15))

        profitCard = CTkFrame(metricsFrame, fg_color=GUI_COLORS['primary'])
        profitCard.grid(row=1, column=2, sticky='nsew', padx=5,pady=(5,0), columnspan=2)
        profitCard.columnconfigure(0, weight=1)
        profitCard.rowconfigure(2, weight=1)

        aaIcon = Image.open(f"{IMG_PATH}/charticon.png")
        self.aaIcon = resize_icon(aaIcon, (45,45))

        ttb.Label(profitCard, text=" Cantidad de Proveedores", image=self.aaIcon, compound='left', background=GUI_COLORS['primary'], foreground='#fff', font=(GUI_FONT,12,'bold')).grid(row=0, column=0, sticky='nsew', padx=(20,20),pady=(15,5))
        ttb.Frame(profitCard, style='white.TFrame', height=1).grid(row=1, column=0,  pady=0,sticky='nsew', padx=20)
        cont = CTkFrame(profitCard, fg_color='#fff')
        cont.grid(row=2, column=0, sticky='nsew', padx=20,pady=(10,5))
        cont.columnconfigure(0, weight=1)
        cont.rowconfigure(0, weight=1)

        ttb.Label(cont, textvariable=self.__PROVIDERS, background='#fff', anchor='center', foreground=GUI_COLORS['danger'], font=(GUI_FONT,14,'bold')).grid(row=0, column=0, sticky='nsew', padx=20,pady=10)


        ttb.Label(profitCard, text="Cantidad total de Proveedores Registrados", justify='center', background=GUI_COLORS['primary'], anchor='center', foreground='#fff', font=(GUI_FONT,10)).grid(row=3, column=0, sticky='nsew', padx=20,pady=(0,15))






        graph_frame2 = CTkFrame(self.quantityFrame, corner_radius=10, fg_color='#212946', 
                                     border_width=2, border_color='#D0CECE', height=250)
        graph_frame2.grid(row=1, column=0, sticky='nsew',padx=4, pady=(5,))
        graph_frame2.anchor('center')
        graph_frame2.rowconfigure(1, weight=1)
        graph_frame2.columnconfigure(0, weight=1)

        ttb.Label(graph_frame2, text='Cotizaciones Aprobadas vs Rechazadas', font=(GUI_FONT,12,'bold'), foreground='white', background='#212946', anchor='w').grid(row=0, column=0,padx=15,pady=(15,5), sticky='nsew')


        
   
        #sns.set(style="whitegrid")
        fig = Figure(figsize=(5, 5), dpi=120)
        fig.subplots_adjust(left=0.01, right=0.98,bottom=0.1, top=0.98)
        self.ax_budgets = fig.add_subplot(111)

        
        self.canvas_budgets = FigureCanvasTkAgg(fig, master=graph_frame2)
        canvas_widget = self.canvas_budgets.get_tk_widget()
        canvas_widget.grid(row=1, column=0, sticky='nsew',padx=4, pady=(2,10))
        canvas_widget.bind('<Map>', lambda e:self.update())



        graph_frame2 = CTkFrame(self.quantityFrame, corner_radius=10, fg_color='#212946', 
                                     border_width=2, border_color='#D0CECE', height=250)
        graph_frame2.grid(row=1, column=1, sticky='nsew',padx=4, pady=(5,))
        graph_frame2.anchor('center')
        graph_frame2.rowconfigure(1, weight=1)
        graph_frame2.columnconfigure(0, weight=1)

        ttb.Label(graph_frame2, text='Facturas - Total Cobrado vs Total por Cobrar', font=(GUI_FONT,12,'bold'), foreground='white', background='#212946', anchor='w').grid(row=0, column=0,padx=15,pady=(15,5), sticky='nsew')


        
   
        #sns.set(style="whitegrid")
        fig = Figure(figsize=(5, 5), dpi=120)
        fig.subplots_adjust(left=0.01, right=0.98,bottom=0.1, top=0.98)
        self.ax_bills = fig.add_subplot(111)

        
        self.canvas_bills = FigureCanvasTkAgg(fig, master=graph_frame2)
        canvas_widget = self.canvas_bills.get_tk_widget()
        canvas_widget.grid(row=1, column=0, sticky='nsew',padx=4, pady=(2,10))
        canvas_widget.bind('<Map>', lambda e:self.update())

    def __capacidadStatistics(self):
    
        self.capacidadFrame = ttb.Frame(self.CONTENT_FRAME)
        self.capacidadFrame.bind('<Map>', lambda e:self.update_rendimiento_stats())
        self.capacidadFrame.columnconfigure(1, weight=1)

        self.capacidadFrame.rowconfigure(0, weight=1)
        self.capacidadFrame.rowconfigure(1, weight=1)



        metricsFrame = ttb.Frame(self.capacidadFrame)
        metricsFrame.grid(row=0, column=0, columnspan=1, sticky='nsew',padx=4, pady=5, rowspan=2)
        metricsFrame.columnconfigure(0, weight=1)
        metricsFrame.rowconfigure(0, weight=1)
        metricsFrame.rowconfigure(1, weight=1)
        metricsFrame.rowconfigure(2, weight=1)
        metricsFrame.rowconfigure(3, weight=1)
        metricsFrame.anchor('center')
        

        profitCard = CTkFrame(metricsFrame, fg_color=GUI_COLORS['primary'])
        profitCard.grid(row=0, column=0, sticky='nsew', padx=0,pady=(0,5))
        profitCard.columnconfigure(0, weight=1)
        profitCard.rowconfigure(2, weight=1)

        efeIcon = Image.open(f"{IMG_PATH}/charticon.png")
        self.efeIcon = resize_icon(efeIcon, (45,45))

        ttb.Label(profitCard, text=" Ratio de Aprobacion", image=self.efeIcon, compound='left', background=GUI_COLORS['primary'], foreground='#fff', font=(GUI_FONT,12,'bold')).grid(row=0, column=0, sticky='nsew', padx=(20,20),pady=(15,5))
        ttb.Frame(profitCard, style='white.TFrame', height=1).grid(row=1, column=0,  pady=0,sticky='nsew', padx=20)
        cont = CTkFrame(profitCard, fg_color='#fff')
        cont.grid(row=2, column=0, sticky='nsew', padx=20,pady=(10,5))
        cont.columnconfigure(0, weight=1)
        cont.rowconfigure(0, weight=1)

        ttb.Label(cont, textvariable=self.__APPROVE_RATIO, background='#fff', anchor='center', foreground=GUI_COLORS['warning'], font=(GUI_FONT,14,'bold')).grid(row=0, column=0, sticky='nsew', padx=20,pady=10)


        ttb.Label(profitCard, text="Ratio de cotizaciones Aprobadas", justify='center', background=GUI_COLORS['primary'], anchor='center', foreground='#fff', font=(GUI_FONT,10)).grid(row=3, column=0, sticky='nsew', padx=20,pady=(0,15))


        profitCard = CTkFrame(metricsFrame, fg_color=GUI_COLORS['primary'])
        profitCard.grid(row=1, column=0, sticky='nsew', padx=0,pady=(5,5))
        profitCard.columnconfigure(0, weight=1)
        profitCard.rowconfigure(2, weight=1)

        afaIcon = Image.open(f"{IMG_PATH}/charticon.png")
        self.afaIcon = resize_icon(afaIcon, (45,45))

        ttb.Label(profitCard, text=" Total de Ventas", image=self.afaIcon, compound='left', background=GUI_COLORS['primary'], foreground='#fff', font=(GUI_FONT,12,'bold')).grid(row=0, column=0, sticky='nsew', padx=(20,20),pady=(15,5))
        ttb.Frame(profitCard, style='white.TFrame', height=1).grid(row=1, column=0,  pady=0,sticky='nsew', padx=20)
        cont = CTkFrame(profitCard, fg_color='#fff')
        cont.grid(row=2, column=0, sticky='nsew', padx=20,pady=(10,5))
        cont.columnconfigure(0, weight=1)
        cont.rowconfigure(0, weight=1)

        ttb.Label(cont, textvariable=self.__TOTAL_BILL, background='#fff', anchor='center', foreground=GUI_COLORS['warning'], font=(GUI_FONT,14,'bold')).grid(row=0, column=0, sticky='nsew', padx=20,pady=10)


        ttb.Label(profitCard, text="Cantidad de ventas realizadas", justify='center', background=GUI_COLORS['primary'], anchor='center', foreground='#fff', font=(GUI_FONT,10)).grid(row=3, column=0, sticky='nsew', padx=20,pady=(0,15))



        profitCard = CTkFrame(metricsFrame, fg_color=GUI_COLORS['primary'])
        profitCard.grid(row=2, column=0, sticky='nsew', padx=0,pady=(5,5))
        profitCard.columnconfigure(0, weight=1)
        profitCard.rowconfigure(2, weight=1)

        ifiIcon = Image.open(f"{IMG_PATH}/charticon.png")
        self.ifiIcon = resize_icon(ifiIcon, (45,45))

        ttb.Label(profitCard, text=" Costo de Inventario", image=self.ifiIcon, compound='left', background=GUI_COLORS['primary'], foreground='#fff', font=(GUI_FONT,12,'bold')).grid(row=0, column=0, sticky='nsew', padx=(20,20),pady=(15,5))
        ttb.Frame(profitCard, style='white.TFrame', height=1).grid(row=1, column=0,  pady=0,sticky='nsew', padx=20)
        cont = CTkFrame(profitCard, fg_color='#fff')
        cont.grid(row=2, column=0, sticky='nsew', padx=20,pady=(10,5))
        cont.columnconfigure(0, weight=1)
        cont.rowconfigure(0, weight=1)

        ttb.Label(cont, textvariable=self.__INVENTORY_COST, background='#fff', anchor='center', foreground=GUI_COLORS['warning'], font=(GUI_FONT,14,'bold')).grid(row=0, column=0, sticky='nsew', padx=20,pady=10)


        ttb.Label(profitCard, text="Valor en $ del inventario", justify='center', background=GUI_COLORS['primary'], anchor='center', foreground='#fff', font=(GUI_FONT,10)).grid(row=3, column=0, sticky='nsew', padx=20,pady=(0,15))

        profitCard = CTkFrame(metricsFrame, fg_color=GUI_COLORS['primary'])
        profitCard.grid(row=3, column=0, sticky='nsew', padx=0,pady=(5,0))
        profitCard.columnconfigure(0, weight=1)
        profitCard.rowconfigure(2, weight=1)

        ofoIcon = Image.open(f"{IMG_PATH}/charticon.png")
        self.ofoIcon = resize_icon(ofoIcon, (45,45))

        ttb.Label(profitCard, text=" Servicios Realizados", image=self.ofoIcon, compound='left', background=GUI_COLORS['primary'], foreground='#fff', font=(GUI_FONT,12,'bold')).grid(row=0, column=0, sticky='nsew', padx=(20,20),pady=(15,5))
        ttb.Frame(profitCard, style='white.TFrame', height=1).grid(row=1, column=0,  pady=0,sticky='nsew', padx=20)
        cont = CTkFrame(profitCard, fg_color='#fff')
        cont.grid(row=2, column=0, sticky='nsew', padx=20,pady=(10,5))
        cont.columnconfigure(0, weight=1)
        cont.rowconfigure(0, weight=1)

        ttb.Label(cont, textvariable=self.__SERVICES_COMPLETE, background='#fff', anchor='center', foreground=GUI_COLORS['warning'], font=(GUI_FONT,14,'bold')).grid(row=0, column=0, sticky='nsew', padx=20,pady=10)


        ttb.Label(profitCard, text="Cantidad de Servicios Ejecutados", justify='center', background=GUI_COLORS['primary'], anchor='center', foreground='#fff', font=(GUI_FONT,10)).grid(row=3, column=0, sticky='nsew', padx=20,pady=(0,15))



        graph_frame2 = CTkFrame(self.capacidadFrame, corner_radius=10, fg_color='#212946', 
                                     border_width=2, border_color='#D0CECE', height=250)
        graph_frame2.grid(row=0, column=1, sticky='nsew',padx=4, pady=(5,))
        graph_frame2.anchor('center')
        graph_frame2.rowconfigure(1, weight=1)
        graph_frame2.columnconfigure(0, weight=1)

        ttb.Label(graph_frame2, text='Productos mas Vendidos', font=(GUI_FONT,12,'bold'), foreground='white', background='#212946', anchor='w').grid(row=0, column=0,padx=15,pady=(15,5), sticky='nsew')

        
        
   
        #sns.set(style="whitegrid")
        fig = Figure(figsize=(5, 5), dpi=100)
        fig.subplots_adjust(left=0.05, right=0.98,bottom=0.2, top=0.95)
        self.ax_top_products = fig.add_subplot(111)

 
        
        self.canvas_top_products = FigureCanvasTkAgg(fig, master=graph_frame2)
        canvas_widget = self.canvas_top_products.get_tk_widget()
        canvas_widget.grid(row=1, column=0, sticky='nsew',padx=4, pady=(2,10))
        canvas_widget.bind('<Map>', lambda e:self.update())


        graph_frame2 = CTkFrame(self.capacidadFrame, corner_radius=10, fg_color='#212946', 
                                     border_width=2, border_color='#D0CECE', height=250)
        graph_frame2.grid(row=1, column=1, sticky='nsew',padx=4, pady=(5,5))
        graph_frame2.anchor('center')
        graph_frame2.rowconfigure(1, weight=1)
        graph_frame2.columnconfigure(0, weight=1)

        ttb.Label(graph_frame2, text='Ingresos de Productos vs Servicios', font=(GUI_FONT,12,'bold'), foreground='white', background='#212946', anchor='w').grid(row=0, column=0,padx=15,pady=(15,5), sticky='nsew')

        moreInfoFrame = tk.Frame(graph_frame2)
        moreInfoFrame.config(background='#212946')
        moreInfoFrame.grid(row=0, column=1, sticky='nsew', padx=(0,20),pady=(20,0))
        moreInfoFrame.columnconfigure(0, weight=1)
        moreInfoFrame.columnconfigure(1, weight=1)
        moreInfoFrame.columnconfigure(2, weight=1)

     
        from datetime import datetime
     
        startDate_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Inicio', 
                                     bootstyle='primary',
                                     background='#212946',foreground='#fff',
                                     font=(GUI_FONT,11,'bold'))
        startDate_label.grid(row=0, column=0, padx=5, pady=(2,0), ipadx=8, sticky='nsew')
        
        date = datetime.today()
        self.startDateEntry = ttb.DateEntry(moreInfoFrame, width=20, style='212946.TEntry',dateformat='%d/%m/%Y', startdate=datetime(year=date.year, month=1, day=1))
        self.startDateEntry.grid(row=1, column=0, sticky='nsew',pady=(2,0),padx=4,)
        self.startDateEntry.entry.config(textvariable=self.STARTDATE_PVSS)


        endDate_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Final', 
                                     bootstyle='primary',
                                     background='#212946',foreground='#fff',
                                     font=(GUI_FONT,11,'bold'))
        endDate_label.grid(row=0, column=1, padx=5, pady=(2,0), ipadx=8, sticky='nsew')

        
        
        self.endDateEntry = ttb.DateEntry(moreInfoFrame, width=20, style='212946.TEntry',dateformat='%d/%m/%Y', startdate=datetime.today())
        self.endDateEntry.grid(row=1, column=1, sticky='nsew',pady=(2,0),padx=4,)
        self.endDateEntry.entry.config(textvariable=self.ENDDATE_PVSS)

        findimg = Image.open(f"{IMG_PATH}/find.png")
        self.findimg = ImageTk.PhotoImage(findimg.resize(resize_image(18, findimg.size)))
        findimgh = Image.open(f"{IMG_PATH}/findh.png")
        self.findimgh = ImageTk.PhotoImage(findimgh.resize(resize_image(18, findimgh.size)))
        findimgp = Image.open(f"{IMG_PATH}/findp.png")
        self.findimgp = ImageTk.PhotoImage(findimgp.resize(resize_image(18, findimgp.size)))

        self.findBTNPS = ButtonImage(moreInfoFrame,  command=lambda:self.update_p_vs_s_chart(), image=self.findimg, img_h=self.findimgh, 
                                   img_p=self.findimgp, style='212946.TButton', padding=0)
        self.findBTNPS.grid(row=0, column=2, sticky='sew', pady=2, padx=(10,5), rowspan=2)


        fig = Figure(figsize=(5, 5), dpi=100)
        fig.subplots_adjust(left=0.05, right=0.98,bottom=0.15, top=0.95)
        self.ax_pvss = fig.add_subplot(111)

        

        
        self.canvas_pvss = FigureCanvasTkAgg(fig, master=graph_frame2)
        canvas_widget = self.canvas_pvss.get_tk_widget()
        canvas_widget.grid(row=1, column=0, sticky='nsew',padx=4, pady=(2,10), columnspan=2)
        canvas_widget.bind('<Map>', lambda e:self.update())



    def __finanzasStatistics(self):
        import random
        
        self.finanzasFrame = ttb.Frame(self.CONTENT_FRAME)
        self.finanzasFrame.bind('<Map>', lambda e:self.update_finanzas_stats())
        self.finanzasFrame.rowconfigure(0, weight=1)
        self.finanzasFrame.rowconfigure(1, weight=1)
        self.finanzasFrame.columnconfigure(0, weight=1)



        metersFrame = CTkFrame(self.finanzasFrame, fg_color='#fff', border_width=1, border_color='#D0CECE')
        metersFrame.grid(row=0, column=1, sticky='nsew')
        metersFrame.rowconfigure(1, weight=1)
    

        
        self.totalBilledMeter = ttb.Meter(metersFrame,
            metersize=180,
            amounttotal=35000,
            padding=5,  stripethickness=20,
            amountused=15000,bootstyle='info',subtextstyle='info',
            metertype="semi",
            subtext="Total Cobrado",textfont='-size 14 -weight bold',
            textright='USD $',
            interactive=False,
            style='white.TFrame'
        )
        self.totalBilledMeter.grid(row=1, column=0, padx=10, pady=(10,0))
        self.totalBilledMeter.config(style='white.TFrame')

    
        contentFrame =  CTkFrame(metersFrame, fg_color=GUI_COLORS['info'], border_width=1, border_color='#D0CECE')
        contentFrame.grid(row=2, column=0, padx=20, pady=(0,10), sticky='nsew', )
        contentFrame.anchor('center')


        ttb.Label(contentFrame, text='Total Facturado USD $:',background=GUI_COLORS['info'], foreground='#fff', font=(GUI_FONT,12,'bold'), anchor='center').grid(row=1, column=0, padx=6, pady=(6,0), sticky='nsew')
        self.totalBilledLabel = ttb.Label(contentFrame, textvariable=self.totalBilled,background=GUI_COLORS['info'], foreground='#fff', font=(GUI_FONT,12,),anchor='center')
        self.totalBilledLabel.grid(row=2, column=0, padx=6, pady=(0,6), sticky='nsew')



        self.totalSpentmeter = ttb.Meter(metersFrame,
            metersize=180,
            amounttotal=12000,
            padding=5,  stripethickness=20,
            amountused=3200,bootstyle='danger',subtextstyle='danger',
            metertype="semi",
            subtext="Total Deudas Pagado",textfont='-size 14 -weight bold',
            textright='USD $',
            interactive=False,
            style='white.TFrame'
        )
        self.totalSpentmeter.grid(row=1, column=1, padx=10, pady=(10,0))
        self.totalSpentmeter.config(style='white.TFrame')
        

        contentFrame =  CTkFrame(metersFrame, fg_color=GUI_COLORS['danger'], )
        contentFrame.grid(row=2, column=1, padx=20, pady=(0,10), sticky='nsew', )
        contentFrame.anchor('center')
        
        ttb.Label(contentFrame, text='Total Gastado USD $:',background=GUI_COLORS['danger'], foreground='#fff', font=(GUI_FONT,12,'bold'), anchor='center').grid(row=1, column=0, padx=6, pady=(6,0), sticky='nsew')
        ttb.Label(contentFrame, textvariable=self.totalSpent,background=GUI_COLORS['danger'], foreground='#fff', font=(GUI_FONT,12,),anchor='center').grid(row=2, column=0, padx=6, pady=(0,6), sticky='nsew')



        graph_frame = CTkFrame(self.finanzasFrame,corner_radius=10, fg_color='#212946', 
                                     border_width=2, border_color='#D0CECE', height=260)
        graph_frame.grid(row=0, column=0, sticky='nsew',padx=4, pady=(6,0))
        graph_frame.anchor('center')

        graph_frame.columnconfigure(0, weight=1)
        graph_frame.rowconfigure(1, weight=1)

        ttb.Label(graph_frame, text='Flujo de Ventas Anual', font=(GUI_FONT,12,'bold'), foreground='white', background='#212946', anchor='w').grid(row=0, column=0,padx=20,pady=(20,15), sticky='nsew')
        
        moreInfoFrame = tk.Frame(graph_frame)
        moreInfoFrame.config(background='#212946')
        moreInfoFrame.grid(row=0, column=1, sticky='nsew', padx=(0,20),pady=(20,0))
        moreInfoFrame.columnconfigure(0, weight=1)
        moreInfoFrame.columnconfigure(1, weight=1)
        moreInfoFrame.columnconfigure(2, weight=1)

     
        from datetime import datetime
     
        startDate_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Inicio', 
                                     bootstyle='primary',
                                     background='#212946',foreground='#fff',
                                     font=(GUI_FONT,11,'bold'))
        startDate_label.grid(row=0, column=0, padx=5, pady=(2,0), ipadx=8, sticky='nsew')
        
        date = datetime.today()
        self.startDateEntry = ttb.DateEntry(moreInfoFrame, width=20, style='212946.TEntry',dateformat='%d/%m/%Y', startdate=datetime(year=date.year, month=1, day=1))
        self.startDateEntry.grid(row=1, column=0, sticky='nsew',pady=(2,0),padx=4,)
        self.startDateEntry.entry.config(textvariable=self.STARTDATE_SALES_FLOW)


        endDate_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Final', 
                                     bootstyle='primary',
                                     background='#212946',foreground='#fff',
                                     font=(GUI_FONT,11,'bold'))
        endDate_label.grid(row=0, column=1, padx=5, pady=(2,0), ipadx=8, sticky='nsew')

        
        
        self.endDateEntry = ttb.DateEntry(moreInfoFrame, width=20, style='212946.TEntry',dateformat='%d/%m/%Y', startdate=datetime.today())
        self.endDateEntry.grid(row=1, column=1, sticky='nsew',pady=(2,0),padx=4,)
        self.endDateEntry.entry.config(textvariable=self.ENDDATE_SALES_FLOW)

        findimg = Image.open(f"{IMG_PATH}/find.png")
        self.findimg = ImageTk.PhotoImage(findimg.resize(resize_image(18, findimg.size)))
        findimgh = Image.open(f"{IMG_PATH}/findh.png")
        self.findimgh = ImageTk.PhotoImage(findimgh.resize(resize_image(18, findimgh.size)))
        findimgp = Image.open(f"{IMG_PATH}/findp.png")
        self.findimgp = ImageTk.PhotoImage(findimgp.resize(resize_image(18, findimgp.size)))

        self.findBTN = ButtonImage(moreInfoFrame,  command=lambda:self.update_sales_flow_chart(), image=self.findimg, img_h=self.findimgh, 
                                   img_p=self.findimgp, style='212946.TButton', padding=0)
        self.findBTN.grid(row=0, column=2, sticky='sew', pady=2, padx=(10,5), rowspan=2)



        

        fig = Figure(figsize=(3,3), dpi=100)
        #fig.set_facecolor('#313B52')
        fig.subplots_adjust(left=0.08, right=0.98,bottom=0.15, top=0.95)
        self.ax_sales_flow = fig.add_subplot(111)
        
    


  
  
        self.canvas_sales_flow = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas_widget = self.canvas_sales_flow.get_tk_widget()
        canvas_widget.grid(row=1, column=0, sticky='nsew',padx=2, pady=(6,10), columnspan=2)
        canvas_widget.bind('<Map>', lambda e:self.update())




        metricsFrame = CTkFrame(self.finanzasFrame, fg_color='#fff', border_width=1, border_color='#D0CECE')
        metricsFrame.grid(row=1, column=1, columnspan=1, sticky='nsew',padx=4, pady=(6,0))
        metricsFrame.columnconfigure(0, weight=1)
        metricsFrame.rowconfigure(0, weight=1)
        metricsFrame.rowconfigure(1, weight=1)
        metricsFrame.anchor('center')
 
    
        
        
        profitCard = CTkFrame(metricsFrame, fg_color=GUI_COLORS['primary'])
        profitCard.grid(row=0, column=0, sticky='nsew', padx=(10,10),pady=(10,5))
        
        profitCard.columnconfigure(1, weight=1)
        profitCard.rowconfigure(2, weight=1)

        growthIcon = Image.open(f"{IMG_PATH}/charticon.png")
        self.growthIcon = resize_icon(growthIcon, (35,35))

        ttb.Label(profitCard, text=" Tasa de Crecimiento", image=self.growthIcon, compound='left', background=GUI_COLORS['primary'], foreground='#fff', font=(GUI_FONT,13,'bold')).grid(row=0, column=0, columnspan=2, sticky='nsew', padx=(20,20),pady=(15,5))
        ttb.Frame(profitCard, style='white.TFrame', height=1).grid(row=1, column=0, columnspan=2,  pady=0,sticky='nsew', padx=20)
        cont = CTkFrame(profitCard, fg_color='#fff', width=120, height=50)
        cont.grid_propagate(0)
        cont.grid(row=2, column=0, sticky='nsew', padx=(20,0),pady=(10,20))
        cont.columnconfigure(0, weight=1)
        cont.rowconfigure(0, weight=1)

        self.growthRateLabel = ttb.Label(cont, textvariable=self.growthRate, background='#fff', anchor='center', foreground=GUI_COLORS['danger'], font=(GUI_FONT,14,'bold'))
        self.growthRateLabel.grid(row=0, column=0, sticky='nsew', padx=8,pady=8)


        ttb.Label(profitCard, text="Tasa de Crecimiento\n con respecto al mes pasado", justify='center', background=GUI_COLORS['primary'],
                  anchor='center', foreground='#fff', font=(GUI_FONT,12)).grid(row=2, column=1, sticky='nsew', padx=(10,20),pady=(0,15))


        profitCard = CTkFrame(metricsFrame, fg_color=GUI_COLORS['success'])
        profitCard.grid(row=1, column=0, sticky='nsew', padx=(10,10),pady=(5,10))
       
        profitCard.columnconfigure(1, weight=1)
        profitCard.rowconfigure(2, weight=1)

        utilityicon = Image.open(f"{IMG_PATH}/profiticon.png")
        self.utilityicon = resize_icon(utilityicon, (35,35))

        ttb.Label(profitCard, text=" Margen de Utilidad", image=self.utilityicon, compound='left', background=GUI_COLORS['success'], foreground='#fff', font=(GUI_FONT,13,'bold')).grid(row=0, column=0,columnspan=2, sticky='nsew', padx=(20,20),pady=(15,5))
        ttb.Frame(profitCard, style='white.TFrame', height=1).grid(row=1, column=0,  pady=0,sticky='nsew', padx=20, columnspan=2)
        cont = CTkFrame(profitCard, fg_color='#fff', width=120, height=50)
        cont.grid_propagate(0)
        cont.grid(row=2, column=0, sticky='nsew', padx=(20,0),pady=(10,20))
        cont.columnconfigure(0, weight=1)
        cont.rowconfigure(0, weight=1)

        self.UtilityRateLabel = ttb.Label(cont, textvariable=self.UtilityRate, background='#fff', anchor='center', foreground=GUI_COLORS['danger'], font=(GUI_FONT,14,'bold'))
        self.UtilityRateLabel.grid(row=0, column=0, sticky='nsew', padx=8,pady=8)


        ttb.Label(profitCard, text="En funcion a los ingresos\n por Productos y Sevivicos", justify='center', background=GUI_COLORS['success'], anchor='center', foreground='#fff', font=(GUI_FONT,12)).grid(row=2, column=1, sticky='nsew', padx=(10,20),pady=(0,15))

      
        graph2_frame = CTkFrame(self.finanzasFrame,corner_radius=10, fg_color='#212946', 
                                     border_width=2, border_color='#D0CECE', height=260)
        graph2_frame.grid(row=1, column=0, sticky='nsew',padx=4, pady=(6,0))
        graph2_frame.anchor('center')

        graph2_frame.columnconfigure(0, weight=1)
        graph2_frame.rowconfigure(1, weight=1)

        ttb.Label(graph2_frame, text='Ingresos y Gastos Mensuales ($)', font=(GUI_FONT,12,'bold'), foreground='white', background='#212946', anchor='w').grid(row=0, column=0,padx=20,pady=(20,15), sticky='nsew')
        moreInfoFrame = tk.Frame(graph2_frame)
        moreInfoFrame.config(background='#212946')
        moreInfoFrame.grid(row=0, column=1, sticky='nsew', padx=(0,20),pady=(20,0))
        moreInfoFrame.columnconfigure(0, weight=1)
        moreInfoFrame.columnconfigure(1, weight=1)
        moreInfoFrame.columnconfigure(2, weight=1)

     
        startDate_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Inicio', 
                                     bootstyle='primary',
                                     background='#212946',foreground='#fff',
                                     font=(GUI_FONT,11,'bold'))
        startDate_label.grid(row=0, column=0, padx=5, pady=(2,0), ipadx=8, sticky='nsew')
        
        date = datetime.today()
        self.startDateEntry = ttb.DateEntry(moreInfoFrame, width=20, style='212946.TEntry',dateformat='%d/%m/%Y', startdate=datetime(year=date.year, month=1, day=1))
        self.startDateEntry.grid(row=1, column=0, sticky='nsew',pady=(2,0),padx=4,)
        self.startDateEntry.entry.config(textvariable=self.STARTDATE_INCOMES_EXPENSES)


        endDate_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Final', 
                                     bootstyle='primary',
                                     background='#212946',foreground='#fff',
                                     font=(GUI_FONT,11,'bold'))
        endDate_label.grid(row=0, column=1, padx=5, pady=(2,0), ipadx=8, sticky='nsew')

        
        
        self.endDateEntry = ttb.DateEntry(moreInfoFrame, width=20, style='212946.TEntry',dateformat='%d/%m/%Y', startdate=datetime.today())
        self.endDateEntry.grid(row=1, column=1, sticky='nsew',pady=(2,0),padx=4,)
        self.endDateEntry.entry.config(textvariable=self.ENDDATE_INCOMES_EXPENSES)

        findimg = Image.open(f"{IMG_PATH}/find.png")
        self.findimg = ImageTk.PhotoImage(findimg.resize(resize_image(18, findimg.size)))
        findimgh = Image.open(f"{IMG_PATH}/findh.png")
        self.findimgh = ImageTk.PhotoImage(findimgh.resize(resize_image(18, findimgh.size)))
        findimgp = Image.open(f"{IMG_PATH}/findp.png")
        self.findimgp = ImageTk.PhotoImage(findimgp.resize(resize_image(18, findimgp.size)))


        self.findBTN = ButtonImage(moreInfoFrame,  command=lambda:self.update_income_expenses_chart(), image=self.findimg, img_h=self.findimgh, img_p=self.findimgp, style='212946.TButton', padding=0)
        self.findBTN.grid(row=0, column=2, sticky='sew', pady=2, padx=(10,5), rowspan=2)

  
        # Crear el gráfico de barras
        figura = Figure(figsize=(3, 3), dpi=100)
        figura.subplots_adjust(left=0.08, right=0.98,bottom=0.15, top=0.95)
        self.ax_incomes_expenses = figura.add_subplot(111)

  



        # Crear el lienzo para mostrar el gráfico en Tkinter
        self.canvas_incomes_expenses = FigureCanvasTkAgg(figura, master=graph2_frame)
        lienzo_widget = self.canvas_incomes_expenses.get_tk_widget()
        lienzo_widget.grid(row=1, column=0, sticky='nsew',padx=2, pady=(6,10), columnspan=2)

        lienzo_widget.bind('<Map>', lambda e:self.update())

    
    def update_finanzas_stats(self):
        growthratevalue = DB.growthRateDB()
        if growthratevalue > 0:
            self.growthRateLabel.config(foreground=GUI_COLORS['success'])
        else:
            self.growthRateLabel.config(foreground=GUI_COLORS['danger'])
        self.growthRate.set(f"{growthratevalue}%")


        Utilityratevalue = DB.UtilityRateDB()
        if Utilityratevalue > 0:
            self.UtilityRateLabel.config(foreground=GUI_COLORS['success'])
        else:
            self.UtilityRateLabel.config(foreground=GUI_COLORS['danger'])
        self.UtilityRate.set(f"{Utilityratevalue}%")

        data = DB.totalGainDB()
        self.totalBilledMeter.configure(amounttotal = data[1],amountused = data[0])
        if data[1] == 1:
            data[1] = 0
        self.totalBilled.set(data[1])
 

        dataSpent = DB.totalSpentDB()
        self.totalSpentmeter.configure(amounttotal = dataSpent[1],amountused = dataSpent[0])
        # self.totalSpentmeter.configure(amountused = dataSpent[0])
        if dataSpent[1] == 1:
            dataSpent[1] = 0
        self.totalSpent.set(dataSpent[1])


        self.update_sales_flow_chart()
        self.update_income_expenses_chart()

 
        

    def get_sales_flow_graph(self, start, end):
        import arrow
        
        DATA_GRAPH = {f"{arrow.Arrow(month=row[1], year=row[0],day=1).format('MMMM - YYYY', locale='es')}".capitalize():
                      row[2] for row in DB.get_sales_flow(start, end) }
        return DATA_GRAPH
    
    def get_expenses_income_data(self, start, end):
        import arrow

        data =  DB.get_income_expenses(start, end)
        start = datetime.strptime(start, '%Y-%m-%d')
        end = datetime.strptime(end, '%Y-%m-%d')
        dict_data = {}
        while start <= end:
            dict_data[f"{arrow.Arrow(month=start.month, year=start.year,day=1).format('MMMM - YYYY', locale='es')}".capitalize()] = [0,0]
            start += relativedelta(months=1)
        

        for row in data[0]:
            dict_data[f"{arrow.Arrow(month=row[1], year=row[0],day=1).format('MMMM - YYYY', locale='es')}".capitalize()][0] = row[-1]
       
        for row in data[1]:
            dict_data[f"{arrow.Arrow(month=row[1], year=row[0],day=1).format('MMMM - YYYY', locale='es')}".capitalize()][1] = row[-1]
        
        dates = dict_data.keys()
        incomes = [value[0] for value in dict_data.values()]
        expenses = [value[1] for value in dict_data.values()]

        
        return [dates,incomes,expenses]
    
    def update_sales_flow_chart(self):
        self.ax_sales_flow.clear()
        
        interval_1 = date(self.STARTDATE_SALES_FLOW.get()) 
        interval_2 = date(self.ENDDATE_SALES_FLOW.get())
        if interval_1>interval_2:
            interval_2 = interval_1
            self.ENDDATE_SALES_FLOW.set(self.STARTDATE_SALES_FLOW.get())
        DB.get_income_expenses(startDate=interval_1, endDate=interval_2)
        data = self.get_sales_flow_graph(start=interval_1, end=interval_2)
        self.get_expenses_income_data(start=interval_1, end=interval_2)
       
        if data != (0,0) and list(data) != {}:
            dates = list(data.keys())
            values = list(data.values())

            self.ax_sales_flow.plot(dates, values, color=GUI_COLORS['danger'], marker='o',linewidth=3,)
            for i, valor in enumerate(values):
                self.ax_sales_flow.text(dates[i], valor + 2, str(valor), ha='center', va='bottom')
            
            self.canvas_sales_flow.draw()
            self.canvas_sales_flow.flush_events()
    
    def update_top_products_chart(self):
        self.ax_top_products.clear()

        products = DB.top_10_products_DB()

        if products:

            productos = {f"{row[0]}\n{row[1]}":int(row[2]) for row in products}

            bars = self.ax_top_products.bar(productos.keys(), productos.values(), color=GUI_COLORS['danger'], edgecolor='white')
            self.ax_top_products.tick_params(axis='x', labelsize=11)  
            #ax.set_xticklabels(productos, rotation=45, ha='right', fontsize='small')

            # Agregar etiquetas con los valores en las barras
            for bar, venta in zip(bars, productos.values()):
                yval = bar.get_height()
                self.ax_top_products.text(bar.get_x() + bar.get_width()/2, yval, round(venta, 2), ha='center', va='bottom')
            self.canvas_top_products.draw()
            self.canvas_top_products.flush_events()

    def update_income_expenses_chart(self):
        self.ax_incomes_expenses.clear()
        
        interval_1 = date(self.STARTDATE_INCOMES_EXPENSES.get()) 
        interval_2 = date(self.ENDDATE_INCOMES_EXPENSES.get())
        if interval_1>interval_2:
            interval_2 = interval_1
            self.ENDDATE_INCOMES_EXPENSES.set(self.STARTDATE_INCOMES_EXPENSES.get())
        
        data = self.get_expenses_income_data(start=interval_1, end=interval_2)
       
        if data:
           
            ancho_barra = 0.35
            x = range(len(data[0]))

            barra_ingresos = self.ax_incomes_expenses.bar(x, data[1], width=ancho_barra, label='Ingresos',color=GUI_COLORS['secondary'])
            barra_gastos = self.ax_incomes_expenses.bar([i + ancho_barra for i in x], data[2], width=ancho_barra, label='Gastos',color=GUI_COLORS['danger'])

            self.ax_incomes_expenses.set_xticks([i + ancho_barra / 2 for i in x])
            self.ax_incomes_expenses.set_xticklabels(data[0])
         
            for bar, ingresos in zip(barra_ingresos, data[1]):
                yval = bar.get_height()
                self.ax_incomes_expenses.text(bar.get_x() + bar.get_width()/2, yval, round(ingresos, 2), ha='center', va='bottom')

            for bar, gastos in zip(barra_gastos, data[2]):
                yval = bar.get_height()
                self.ax_incomes_expenses.text(bar.get_x() + bar.get_width()/2, yval, round(gastos, 2), ha='center', va='bottom')

            self.ax_incomes_expenses.legend()
            self.canvas_incomes_expenses.draw()
            self.canvas_incomes_expenses.flush_events()

    
    def update_rendimiento_stats(self):
        self.__APPROVE_RATIO.set(f"{DB.approve_ratio_DB()}%")
        self.__TOTAL_BILL.set(DB.count_total_bills_DB())
        self.__INVENTORY_COST.set(f"${DB.inventory_cost_DB()}")
        self.__SERVICES_COMPLETE.set(DB.total_services_complete_DB())
        self.update_top_products_chart()
        self.update_p_vs_s_chart()
    

        
        

    def get_p_vs_s_data(self, start, end):
        import arrow

        data =  DB.get_products_vs_services(start, end)
        start = datetime.strptime(start, '%Y-%m-%d')
        end = datetime.strptime(end, '%Y-%m-%d')
        dict_data = {}
        while start <= end:
            dict_data[f"{arrow.Arrow(month=start.month, year=start.year,day=1).format('MMMM - YYYY', locale='es')}".capitalize()] = [0,0]
            start += relativedelta(months=1)
        

        for row in data[0]:
            dict_data[f"{arrow.Arrow(month=row[1], year=row[0],day=1).format('MMMM - YYYY', locale='es')}".capitalize()][0] = row[-1]
       
        for row in data[1]:
            dict_data[f"{arrow.Arrow(month=row[1], year=row[0],day=1).format('MMMM - YYYY', locale='es')}".capitalize()][1] = row[-1]
        
        dates = dict_data.keys()
        product = [value[0] for value in dict_data.values()]
        service = [value[1] for value in dict_data.values()]

        return [dates,product,service]

    def update_p_vs_s_chart(self):
        self.ax_pvss.clear()
        
        interval_1 = date(self.STARTDATE_PVSS.get()) 
        interval_2 = date(self.ENDDATE_PVSS.get())
        if interval_1>interval_2:
            interval_2 = interval_1
            self.ENDDATE_PVSS.set(self.STARTDATE_PVSS.get())
        
        data = self.get_p_vs_s_data(start=interval_1, end=interval_2)
       
        if data:
           

            self.ax_pvss.plot(data[0], data[1], label='Productos', marker='o')
            self.ax_pvss.plot(data[0], data[2], label='Servicios', marker='o')

   
            self.ax_pvss.legend()
            self.canvas_pvss.draw()
            self.canvas_pvss.flush_events()

    def update_cuantitativos_stats(self):
        self.__CLIENTS.set(DB.get_total_clients())
        self.__PROVIDERS.set(DB.get_total_providers())
        self.__PRODUCTS.set(DB.get_total_products())
        self.__SERVICES.set(DB.get_total_services())
        self.__MACHINERY.set(DB.get_total_machinery())

        data = DB.get_activity_completed()

        self.__ALL_ACTIVITY.set(data[1])

        if data[1] == 0:
            data[1] = 1
        self.activity_meter.configure(amounttotal = data[1],amountused = data[0])
        

 

        dataSpent = DB.get_task_completed()
        self.__ALL_TASKS.set(data[1])
        if dataSpent[1]==0:
            dataSpent[1] = 1
        self.task_meter.configure(amounttotal = dataSpent[1],amountused = dataSpent[0])

        self.update_budget_AR_chart()
        self.update_bills_fact_cobrar_chart()

    
    def update_budget_AR_chart(self):
        self.ax_budgets.clear()
        
        data = DB.total_aprobado_vs_rechazada_DB()
       
        if not None in data and data !=[0,0]: 
            
            etiquetas = ['Aprobadas','Rechazadas']

            wedges, texts, autotexts = self.ax_budgets.pie(data,labels=etiquetas, autopct='%1.1f%%', startangle=90, colors=[GUI_COLORS['secondary'], GUI_COLORS['danger']],wedgeprops=dict(width=0.4,edgecolor='white'))
            position = [(-0.5, -0.6),(0.5, 0.6)]
            for autotext, pos in zip(autotexts, position):
                autotext.set_fontweight('bold')
                autotext.set_position(pos)
            
            self.ax_budgets.legend(loc='upper left', bbox_to_anchor=(-0.6, 1.0))
            self.ax_budgets.tick_params(axis='x', labelsize=12)  
            self.canvas_budgets.draw()
            self.canvas_budgets.flush_events()

    
    def update_bills_fact_cobrar_chart(self):
        self.ax_bills.clear()
        
        data = DB.total_COBRAR_VS_FACTURADO_DB()
        if not None in data and data !=[0,0]: 
            etiquetas = ['Cobrado', 'Por Cobrar']

            wedges, texts, autotexts = self.ax_bills.pie(data,labels=etiquetas, autopct='%1.1f%%', startangle=90, colors=[GUI_COLORS['secondary'], GUI_COLORS['danger']],wedgeprops=dict(width=0.4,edgecolor='white'))
            position = [(-0.5, -0.6),(0.5, 0.6)]
            for autotext, pos in zip(autotexts, position):
                autotext.set_fontweight('bold')
                autotext.set_position(pos)

            self.ax_bills.legend(loc='upper left', bbox_to_anchor=(-0.6, 1.0))
            self.ax_bills.tick_params(axis='x', labelsize=12)   
            self.canvas_bills.draw()
            self.canvas_bills.flush_events()


        

if __name__=="__main__":

    app = ttb.Window(themename='new')
    SGDB_Style()
    StatisticsPage(app).pack()
    app.mainloop()
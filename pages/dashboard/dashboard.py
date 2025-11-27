import ttkbootstrap as ttb
from assets.globals import GUI_COLORS, IMG_PATH, GUI_FONT
from assets.utils import resize_icon, resize_image
from assets.globals import invoice_icon, budget_icon, project_icon, refresh_icon
from components.dcards import DashboardCard
from components.buttons import ButtonImage
from PIL import Image, ImageTk
from customtkinter import CTkFrame, CTkLabel
import tkinter as tk
from assets.db.db_connection import DB
###### GRAPH LIBRARIES
from models.entitys.activity import Activity
from models.entitys.budget import Budget
from models.entitys.bills import Bill
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
from assets.utils import display_page
from assets.globals import pages_dash_access
from datetime import datetime, timedelta
import arrow


class Dashboard(ttb.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        PART_COLOR = '#212946'

        ########## PAGE CONFIG ##########
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        ########## GUI ICONSr##########
        self.__dash_icon = Image.open(f'{IMG_PATH}/dashboard_title.png')
        self.__dash_icon = ImageTk.PhotoImage(self.__dash_icon.resize(resize_image(10, self.__dash_icon.size)))
        self.__TOTAL_BILL = ttb.StringVar(value="$0")
        self.__TOTAL_PURCHASES = ttb.StringVar(value="$0")
        self.__TOTAL_BUDGETS = ttb.StringVar(value=0)
        self.__TOTAL_ACTIVITY = ttb.StringVar(value=0)

        ######### PAGE TITLE #########


        page_img = ttb.Label(self, 
                               image=self.__dash_icon, 
                                padding='0 0',
                               )
        page_img.grid(row=0, column=0, sticky='nsw', pady=(10, 4), padx=20)
        page_img.grid_propagate(0)
        page_img.anchor('w')

        page_title = ttb.Label(page_img, 
                               text='DASHBOARD', 
                                padding='0 0',
                               background='#203864',
                               font=('arial',15, 'bold'), 
                               foreground='#fff')
        page_title.grid(row=0, column=0, sticky='nsew',padx=(80,0))



        ttb.Separator(self, orient='horizontal').grid(row=1, column=0, sticky='nsew',padx=20)

        ######### PAGE CONTENT #########
        self.dashboard_content = ttb.Frame(self,)
        self.dashboard_content.grid(row=2, column=0, sticky='nsew', padx=20, pady=10)
        self.dashboard_content.columnconfigure(0,weight=1)
        self.dashboard_content.rowconfigure(2,weight=1)
        self.dashboard_content.rowconfigure(1,weight=1)

        ############ Metrics Section ############
        metrics_frame = ttb.Frame(self.dashboard_content, height=160)
        metrics_frame.grid(row=0, column=0, sticky='nsew',)
  
        BIL = Image.open(f'{IMG_PATH}/card_bils.png')
        PUB = Image.open(f'{IMG_PATH}/card_purchase.png')
        TOL = Image.open(f'{IMG_PATH}/card_total.png')
        TASKS = Image.open(f'{IMG_PATH}/card_tasks.png')

   
        DashboardCard(metrics_frame, card_background=BIL, background='#00B050', title='Total Ventas', var=self.__TOTAL_BILL).grid(row=0, column=0,padx=(0,6))
        DashboardCard(metrics_frame,card_background=PUB, background='#5B9BD5', title='Total Compras',var=self.__TOTAL_PURCHASES).grid(row=0, column=1,padx=(0,6))
        DashboardCard(metrics_frame, card_background=TOL, background='#F1536E', title='Total Ordenes',var=self.__TOTAL_BUDGETS).grid(row=0, column=2,padx=(0,6))
        DashboardCard(metrics_frame, card_background=TASKS, background='#FDA005',title='Total Actividades',var=self.__TOTAL_ACTIVITY).grid(row=0, column=3)
        

        
       


        self.r_i = resize_icon(Image.open(f'{IMG_PATH}/refresh_b.png'))
        self.r_i_h = resize_icon(Image.open(f'{IMG_PATH}/refresh_b_h.png'))

        budgetsStateFrame = CTkFrame(self.dashboard_content, corner_radius=10, fg_color=PART_COLOR, 
                                     border_width=2, border_color='#D0CECE')
        budgetsStateFrame.grid(row=0, column=1, rowspan=3, padx=(6,0), sticky='nsew')
        budgetsStateFrame.columnconfigure(0, weight=1)
        budgetsStateFrame.rowconfigure(1, weight=1)
        budgetsStateFrame.rowconfigure(3, weight=1)

        

        ttb.Label(budgetsStateFrame, text='ACTIVIDADES', font=(GUI_FONT,13,'bold'), 
                  foreground='#fff', background=PART_COLOR, anchor='w'
                ).grid(row=0, column=0, sticky='nsew', padx=20,pady=(10,5))

        refresh = ButtonImage(budgetsStateFrame, compound='left',  style='212946.TButton', 
                   padding=0, image=self.r_i,
                   img_h=self.r_i_h, img_p=self.r_i)
        refresh.grid(row=0, column=0, pady=(10,5), padx=10, sticky='ne')

        content = tk.Frame(budgetsStateFrame, background=PART_COLOR)
        content.grid(row=1, column=0, sticky='nsew', padx=20,pady=0)
        content.columnconfigure(0, weight=1)
        content.config(background=PART_COLOR)
        
    
        ttb.Label(content, text='Descripcion', width=20, background=PART_COLOR, font=(GUI_FONT,11,'bold'),foreground='white').grid(row=0, column=0, sticky='nsew')
        ttb.Label(content, text='Estado',  background=PART_COLOR, font=(GUI_FONT,11,'bold'),foreground='white', anchor='center').grid(row=0, column=1, sticky='nsew')

        ttb.Separator(content, bootstyle='danger').grid(row=1, column=0, sticky='nsew', columnspan=2, pady=(0,8))
      
        self.actiList = tk.Frame(content, background=PART_COLOR)
        self.actiList.grid(row=2, column=0, sticky='nsew', padx=2,pady=(0,5), columnspan=2)
        self.actiList.columnconfigure(0, weight=1)

        self.actiList.config(background=PART_COLOR)
    

        ttb.Button(content, text='Mas información', bootstyle='warning', command=lambda: display_page(page=pages_dash_access[0][0], butt=pages_dash_access[0][1])).grid(row=12, column=0, columnspan=2, pady=4,ipady=5, sticky='nsew')
        
        
        ttb.Label(budgetsStateFrame, text='FACTURAS', font=(GUI_FONT,13,'bold'), 
                  foreground='#fff', background=PART_COLOR, anchor='w'
                ).grid(row=2, column=0, sticky='nsew', padx=20,pady=(10,5))

        refresh = ButtonImage(budgetsStateFrame, compound='left',  style='212946.TButton', 
                   padding=0, image=self.r_i,
                   img_h=self.r_i_h, img_p=self.r_i)
        refresh.grid(row=2, column=0, pady=(10,5), padx=20, sticky='ne')

        self.billsSet = tk.Frame(budgetsStateFrame, background=PART_COLOR)
        self.billsSet.grid(row=3, column=0, sticky='nsew', padx=20,pady=(0,5))
        self.billsSet.columnconfigure(0, weight=1)

        self.billsSet.config(background=PART_COLOR)
    
        ttb.Label(self.billsSet, text='Codigo', width=20, background=PART_COLOR, font=(GUI_FONT,11,'bold'),foreground='white').grid(row=0, column=0, sticky='nsew')
        ttb.Label(self.billsSet, text='Estado',  background=PART_COLOR, font=(GUI_FONT,11,'bold'),foreground='white', anchor='center').grid(row=0, column=1, sticky='nsew')

        ttb.Separator(self.billsSet, bootstyle='danger').grid(row=1, column=0, sticky='nsew', columnspan=2, pady=(0,8))
        self.billslist = tk.Frame(self.billsSet,)
        self.billslist.grid(row=2, column=0, columnspan=2, padx=2, pady=2, sticky='nsew')
        self.billslist.columnconfigure(0, weight=1)
        self.billslist.config(background=PART_COLOR)


        ttb.Button(self.billsSet, text='Mas información', bootstyle='warning',command=lambda: display_page(page=pages_dash_access[1][0], butt=pages_dash_access[1][1])).grid(row=3, column=0, columnspan=2, pady=4, ipady=5, sticky='nsew')
        self.create_graphs()
        self.bind('<Map>', lambda e:self.update_metrics())

    def updates_dashboard_metrics(self):
        self.__TOTAL_BILL.set(f"${round(DB.total_bill_DB(),2)}")
        self.__TOTAL_PURCHASES.set(f'${round(DB.total_Purchases_DB(),2)}')
        self.__TOTAL_BUDGETS.set(round(DB.total_budgets_DB(),2))
        self.__TOTAL_ACTIVITY.set(round(DB.total_activity_DB(),2))
    
    def __five_bills(self):
        for wid in self.billslist.winfo_children():
            wid.destroy()
        bills = Bill.lastFive()
        if bills:
            for index, b in enumerate(bills):
               
                bill = Bill(**b)
                
                ttb.Label(self.billslist, text=f"Factura #: {'0'*(6-len(str(bill.code)))+str(bill.code)}", width=20,background='#212946', foreground='white', anchor='w',
                    font=(GUI_FONT,10)).grid(row=index*2, column=0, sticky='nsew', pady=(0,0))
            
        
                ttb.Frame(self.billslist, bootstyle='info', height=1).grid(row=index*2+1, column=0, sticky='nsew', columnspan=2, pady=(4,6))

                CTkLabel(self.billslist, text=bill.creationDate.strftime("%d-%m-%Y"), fg_color='#5B9BD5', bg_color='#212946',
                                anchor='center', corner_radius=4, text_color='white').grid(row=index*2, column=1, sticky='nsew', pady=(0,2), ipadx=2, ipady=2,)
        
    def __fiveActivity(self):
        for wid in self.actiList.winfo_children():
            wid.destroy()
        activity = Activity.lastFive()
        if activity:
            for index, a in enumerate(activity):
                activity = Activity(**a)
               
                ttb.Label(self.actiList, text=f'Actividad #{activity.id}', width=20,background='#212946', foreground='white', anchor='w',
                    font=(GUI_FONT,10)).grid(row=index*2, column=0, sticky='nsew', pady=(0,0))
            
        
                ttb.Frame(self.actiList, bootstyle='info', height=1).grid(row=index*2+1, column=0, sticky='nsew', columnspan=2, pady=(4,6))

                CTkLabel(self.actiList, text=activity.get_stage(), fg_color='#5B9BD5', bg_color='#212946',
                                anchor='center', corner_radius=4, text_color='white').grid(row=index*2, column=1, sticky='nsew', pady=(0,2), ipadx=2, ipady=2,)
        

    def get_graph_data(self,data):
    
        date = datetime.today()

        start = datetime(year=date.year,month=date.month, day=1)
        end = date

        dict_data = {}
        while start <= end:
           
            dict_data[arrow.Arrow(month=start.month, year=start.year,day=start.day).format('DD-MMMM', locale='es')] = 0
            start += timedelta(days=1)
        if data:
            for row in data: 
                dict_data[arrow.Arrow(month=row[0].month, year=row[0].year,day=row[0].day).format('DD-MMMM', locale='es')] = row[-1]
        
      
        return dict_data


    def update_chart(self):
        self.sells_ax.clear()
        aras = Bill.countBills()
        
        DICT = self.get_graph_data(aras)
        days = DICT.keys()
        amount = DICT.values()

        self.sells_ax.plot(days, amount,color='#E74C3BB0', marker='o')
        self.sells_ax.set_xticks(self.sells_ax.get_xticks())
        self.sells_ax.set_xticklabels(self.sells_ax.get_xticklabels(), rotation=90)
        self.sells_ax.set_ylim(-0.005)
        self.sells_canvas.draw()
        self.sells_canvas.flush_events()


        self.cotizaciones_ax.clear()
        DICT2 = self.get_graph_data( Budget.countBudgets())

        days = DICT2.keys()
        amount = DICT2.values()

        self.cotizaciones_ax.plot(days, amount,color='#E74C3BB0', marker='o')
        self.cotizaciones_ax.set_xticks(self.cotizaciones_ax.get_xticks())
        self.cotizaciones_ax.set_xticklabels(self.cotizaciones_ax.get_xticklabels(), rotation=90)
        self.cotizaciones_ax.set_ylim(-0.005)
        self.cot_canvas.draw()
        self.cot_canvas.flush_events()
        

        self.updates_dashboard_metrics()



        
    def update_metrics(self):
        import threading


        self.__fiveActivity()
        self.__five_bills()
        self.update_chart()

        self.update_idletasks()

    def create_graphs(self):

        date = datetime.today()
        month = arrow.Arrow(month=date.month, year=date.year,day=date.day).format('MMMM', locale='es').capitalize()
         ############ Metrics Section ############212946
        graph_frame = CTkFrame(self.dashboard_content,corner_radius=10, fg_color='#212946', 
                                     border_width=2, border_color='#D0CECE', height=260)
        graph_frame.grid(row=1, column=0, sticky='nsew',padx=4, pady=(6,0))
        graph_frame.anchor('center')
        graph_frame.columnconfigure(0, weight=1)
        graph_frame.rowconfigure(1, weight=1)
        
        ttb.Label(graph_frame, text=f'Cantidad de Ventas por Dias - Mes:{month}', font=(GUI_FONT,12,'bold'), foreground='white', background='#212946', anchor='w').grid(row=0, column=0,padx=10,pady=(15,5), sticky='nsew')


    

        # Create a Seaborn line plot
        #sns.set_style("darkgrid")
        
        fig = Figure(figsize=(11, 3), dpi=80)
  
        fig.subplots_adjust(left=0.05, right=0.98,bottom=0.2, top=0.95)
        
        self.sells_ax = fig.add_subplot(111)
        
     
        

        # Embed the Seaborn plot into the Tkinter window
        self.sells_canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas_widget = self.sells_canvas.get_tk_widget()
        canvas_widget.grid(row=1, column=0, sticky='nsew',padx=2, pady=(2,10))
        canvas_widget.bind('<Map>', lambda e:self.update())


        graph_frame2 = CTkFrame(self.dashboard_content,corner_radius=10, fg_color='#212946', 
                                     border_width=2, border_color='#D0CECE', height=250)
        graph_frame2.grid(row=2, column=0, sticky='nsew',padx=4, pady=(6,0))
        graph_frame2.anchor('center')
        graph_frame2.rowconfigure(1, weight=1)
        graph_frame2.columnconfigure(0, weight=1)

        ttb.Label(graph_frame2, text=f'Cantidad de Cotizacines por Dias - Mes:{month}', font=(GUI_FONT,12,'bold'), foreground='white', background='#212946', anchor='w').grid(row=0, column=0,padx=10,pady=(15,5), sticky='nsew')


        


        #sns.set(style="whitegrid")
        fig = Figure(figsize=(11, 3), dpi=80)
        fig.subplots_adjust(left=0.05, right=0.98,bottom=0.2, top=0.95)
        self.cotizaciones_ax = fig.add_subplot(111)



        
        self.cot_canvas = FigureCanvasTkAgg(fig, master=graph_frame2)
        canvas_widget = self.cot_canvas.get_tk_widget()
        canvas_widget.grid(row=1, column=0, sticky='nsew',padx=2, pady=(2,10))
        canvas_widget.bind('<Map>', lambda e:self.update())

   

        ########################################
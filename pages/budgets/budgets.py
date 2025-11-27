import ttkbootstrap as ttb
from assets.globals import GUI_COLORS, IMG_PATH, GUI_FONT
from assets.utils import resize_icon, resize_image
from assets.globals import budget_icon, search_icon, edit_icon, add_icon, delete_icon, process_icon, refresh_icon,filter_icon
from components.bcards import BCards
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageTk
from customtkinter import CTkFrame
from tkinter import messagebox

from components.buttons import ButtonImage
from models.entitys.budget import Budget
from pages.budgets.views.budgetForm import BudgetForm
from pages.budgets.views.reportes import Report
import assets.globals as constGlobal

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


class BudgetMainForm(ttb.Frame):
    def __init__(self, master=None):

        super().__init__(master)

        ########## PAGE CONFIG ##########
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.grid_propagate(0)

        ########## GUI ICONS ##########


        self.__budget_icon = Image.open(f'{IMG_PATH}/budget_title.png')
        self.__budget_icon = ImageTk.PhotoImage(self.__budget_icon.resize(resize_image(10, self.__budget_icon.size)))

        self.__filter = resize_icon(filter_icon, icon_size=(20,20))

        self.sin_procesar = ttb.IntVar(value=7)
        self.en_proceso = ttb.IntVar(value=5)
        self.aprobada = ttb.IntVar(value=3)
        self.rechazada = ttb.IntVar(value=4)

    

        self.FILTER_STATE = None
        self.MAIN_FILTER = ttb.StringVar(value='b.code')
        self.MAIN_FILTER.trace_add('write',lambda v,i,m: self.__searchBudgets())

        ######### PAGE TITLE #########
        frame_title = ttb.Frame(self)
        frame_title.grid(row=0, column=0, sticky='nesw', pady=(10, 4), padx=20)
        frame_title.columnconfigure(0, weight=1)

        page_img = ttb.Label(frame_title, 
                               image=self.__budget_icon, 
                                padding='0 0',
                               )
        page_img.grid(row=0, column=0, sticky='nsw', pady=2, padx=2)
        page_img.grid_propagate(0)
        page_img.anchor('w')

        def open_report():
            Report(self,title='Cotizaciones')

        reportBTN = Image.open(f"{IMG_PATH}/report.png")
        self.reportBTN = ImageTk.PhotoImage(reportBTN.resize(resize_image(25, reportBTN.size)))

        
        reporthBTN = Image.open(f"{IMG_PATH}/reporth.png")
        self.reporthBTN = ImageTk.PhotoImage(reporthBTN.resize(resize_image(25, reporthBTN.size)))


        reportpBTN = Image.open(f"{IMG_PATH}/reportp.png")
        self.reportptBTN = ImageTk.PhotoImage(reportpBTN.resize(resize_image(25, reportpBTN.size)))

        ButtonImage(frame_title, image=self.reportBTN, img_h=self.reporthBTN, img_p=self.reportptBTN, command=open_report,style='flat.light.TButton', padding=0).grid(row=0, column=1, sticky='nsew', pady=2, padx=6)


        

        page_title = ttb.Label(page_img, 
                               text='COTIZACION', 
                                padding='0 0',
                               background='#203864',
                               font=('arial',15, 'bold'), 
                               foreground='#fff')
        page_title.grid(row=0, column=0, sticky='nsew',padx=(80,0))

       


        ttb.Separator(self, orient='horizontal').grid(row=1, column=0, sticky='nsew',padx=20)

        ######### PAGE CONTENT #########
        budget_page_content_frame = ttb.Frame(self,)
        budget_page_content_frame.grid(row=2, column=0, sticky='nsew', padx=20, pady=10)
        budget_page_content_frame.rowconfigure(1, weight=1)
        budget_page_content_frame.columnconfigure(1, weight=1)

            ############# Budget Grid View Section #############
       
            #### Metrics Card Section ####
        metrics_card_Frame = CTkFrame(budget_page_content_frame, fg_color='#D9D9D9', border_width=2, border_color='#D0CECE')
        metrics_card_Frame.grid(row=0, column=0, sticky='nsew', padx=4, pady=4)
        metrics_card_Frame.columnconfigure(0, weight=1)
        metrics_card_Frame.columnconfigure(1, weight=1)

        MCF_TITLE = CTkFrame(metrics_card_Frame,  fg_color=GUI_COLORS['primary'])
        MCF_TITLE.grid(row=0, column=0, columnspan=2, pady=(5,5), padx=5, sticky='nsew')

        self.stats = resize_icon(Image.open(f'{IMG_PATH}/stats.png'))
        ttb.Label(MCF_TITLE, background=GUI_COLORS['primary'], foreground='white', font=(GUI_FONT, 12,'bold'),
                 text=' '*3+'Resumen de Cotizaciones', image=self.stats, compound='left').grid(row=0, column=0, padx=4, pady=8)


        editCardImg = Image.open(f"{IMG_PATH}/edit_card.png")
        editIconImg = Image.open(f"{IMG_PATH}/edit_icon.png")
        nonProcess_card = BCards(metrics_card_Frame, 
                                     background_color=GUI_COLORS['warning'],
                                     value=self.sin_procesar, 
                                     title='Editables',
                                     sub_title='Cotizaciones Sin Procesar',
                                     card_background=editCardImg,
                                     icon=editIconImg)
        nonProcess_card.grid(row=1, column=0, padx=(5,5), pady=(0,5), sticky='nsew')


        processCardImg = Image.open(f"{IMG_PATH}/process_card.png")
        processIconImg = Image.open(f"{IMG_PATH}/process_icon.png")
        process_card = BCards(metrics_card_Frame, 
                                     background_color=GUI_COLORS['primary'],
                                     value=self.en_proceso, 
                                     title='En Proceso',
                                     sub_title='Cotizaciones En Proceso',
                                     card_background=processCardImg,
                                     icon=processIconImg)
        process_card.grid(row=1, column=1, padx=(0,5), pady=(0,5), sticky='nsew')


        approveCardImg = Image.open(f"{IMG_PATH}/approve_card.png")
        approveIconImg = Image.open(f"{IMG_PATH}/approve_icon.png")
        approve_card = BCards(metrics_card_Frame, 
                                     background_color=GUI_COLORS['success'],
                                     value=self.aprobada, 
                                     title='Aprobadas',
                                     sub_title='Cotizaciones Aprobadas',
                                     card_background=approveCardImg,
                                     icon=approveIconImg)
        approve_card.grid(row=2, column=0, padx=(5,5), pady=(0,5), sticky='nsew')



        cancelCardImg = Image.open(f"{IMG_PATH}/cancel_card.png")
        cancelIconImg = Image.open(f"{IMG_PATH}/cancel_icon.png")
        denied_card = BCards(metrics_card_Frame, 
                                     background_color=GUI_COLORS['danger'],
                                     value=self.rechazada, 
                                     title='Rechazadas',
                                     sub_title='Cotizaciones Rechazadas',
                                     card_background=cancelCardImg,
                                     icon=cancelIconImg)
        denied_card.grid(row=2, column=1, padx=(0,5), pady=(0,5), sticky='nsew')

        

        graph_frame2 = CTkFrame(budget_page_content_frame, corner_radius=10, fg_color='#212946', 
                                     border_width=2, border_color='#D0CECE', height=250)
        graph_frame2.grid(row=1, column=0, sticky='nsew',padx=4, pady=(0,4))
        graph_frame2.anchor('center')
        graph_frame2.rowconfigure(1, weight=1)
        graph_frame2.columnconfigure(0, weight=1)

        ttb.Label(graph_frame2, text='Cotizaciones', font=(GUI_FONT,12,'bold'), foreground='white', background='#212946', anchor='w').grid(row=0, column=0,padx=15,pady=(15,5), sticky='nsew')


        
   
        #sns.set(style="whitegrid")
        fig = Figure(figsize=(5, 3), dpi=80)
        fig.subplots_adjust(left=0.05, right=0.98,bottom=0.15, top=0.95)
        self.ax = fig.add_subplot(111)

        data = {
            'Sin Procesar': self.sin_procesar.get(),
            'En Proceso': self.en_proceso.get(),
            'Rechazadas': self.rechazada.get(),
            'Aprobadas': self.aprobada.get(),
        }
        languages = data.keys()
        popularity = data.values()

        self.ax.bar(languages, popularity, color=[GUI_COLORS['warning']+'B0',GUI_COLORS['primary']+'B0',GUI_COLORS['danger']+'B0',GUI_COLORS['success']+'B0'], edgecolor='white')
        self.ax.tick_params(axis='x', labelsize=12)  
        
        self.canvas = FigureCanvasTkAgg(fig, master=graph_frame2)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=1, column=0, sticky='nsew',padx=4, pady=(2,10))
        self.canvas_widget.bind('<Map>', lambda e:self.update())
       
      
        ###########################################

        table_frame = CTkFrame(budget_page_content_frame, fg_color='#fff',border_width=1, border_color='#CFCFCF')
        table_frame.grid(row=0, column=1, rowspan=2, padx=4, pady=4,sticky = 'nsew')
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(3, weight=1)

        subtitle = CTkFrame(table_frame, corner_radius=6, fg_color=GUI_COLORS['primary'])
        subtitle.grid(row=0, column=0, sticky='nsew', padx=10, pady=(10,2), columnspan=2)

        self.micon = resize_icon(Image.open(f'{IMG_PATH}/management.png'),(45,45))

        ttb.Label(subtitle, image=self.micon, background=GUI_COLORS['primary'], ).grid(row=0, column=0, rowspan=2, sticky='nsew', padx=(8), pady=8)

        ttb.Label(subtitle, text='Gestion de Cotizaciones', background=GUI_COLORS['primary'], font=(GUI_FONT,13,'bold'), foreground='#fff', anchor='sw').grid(row=0, column=1, sticky='nsew', padx=(4,8), pady=(8,0))

        ttb.Label(subtitle, text='Inicio / Cotizaciones', background=GUI_COLORS['primary'], font=(GUI_FONT,9), foreground='#fff', anchor='nw').grid(row=1, column=1, sticky='nsew', padx=(4,8), pady=(0,8))

        ttb.Separator(subtitle,orient='vertical').grid(row=0, column=2, sticky='nsew', rowspan=2, padx=(4,8), pady=8)



        ttb.Frame(table_frame, bootstyle='primary').grid(row=1, column=0, sticky='nsew', padx=10, pady=5, columnspan=2)




        buttons_frame = ttb.Frame(table_frame, style='white.TFrame')
  
        buttons_frame.grid(row=2, column=0, sticky='nsew', columnspan=2, padx=4, pady=(4,0))
        buttons_frame.columnconfigure(8, weight=1)


        


        creatbtnimg = Image.open(f"{IMG_PATH}/create.png")
        self.creatbtnimg = resize_icon(creatbtnimg, (50,50))

        creatbtnimgh = Image.open(f"{IMG_PATH}/createh.png")
        self.creatbtnimgh = resize_icon(creatbtnimgh, (50,50))

        creatbtnimgp = Image.open(f"{IMG_PATH}/createp.png")
        self.creatbtnimgp = resize_icon(creatbtnimgp, (50,50))

        ButtonImage(buttons_frame, command=self.__open_create_form, image=self.creatbtnimg, img_h=self.creatbtnimgh, 
                    img_p=self.creatbtnimgp,  style='flatw.light.TButton', padding=0).grid(row=0, column=0, sticky='nsew', pady=2, padx=(5,8))


        ttb.Separator(buttons_frame, orient='vertical',bootstyle='dark').grid(row=0, column=1, sticky='ew', padx=(0,8))

        viewbtnimg = Image.open(f"{IMG_PATH}/view.png")
        self.viewbtnimg = resize_icon(viewbtnimg, (50,50))

        viewbtnimgh = Image.open(f"{IMG_PATH}/viewh.png")
        self.viewbtnimgh = resize_icon(viewbtnimgh, (50,50))

        viewbtnimgp = Image.open(f"{IMG_PATH}/viewp.png")
        self.viewbtnimgp = resize_icon(viewbtnimgp, (50,50))
        self.viewBTN = ButtonImage(buttons_frame, image=self.viewbtnimg, img_h=self.viewbtnimgh,  img_p=self.viewbtnimgp, command=self.__open_view_form, style='flatw.light.TButton', padding=0, state='disabled')
        self.viewBTN.grid(row=0, column=2, sticky='nsew', pady=2, padx=(0,8))


        editbtnimg = Image.open(f"{IMG_PATH}/editbtn.png")
        self.editbtnimg = resize_icon(editbtnimg,(50,50))

        editbtnimgh = Image.open(f"{IMG_PATH}/editbtnh.png")
        self.editbtnimgh = resize_icon(editbtnimgh, (50,50))

        editbtnimgp = Image.open(f"{IMG_PATH}/editbtnp.png")
        self.editbtnimgp = resize_icon(editbtnimgp, (50,50))

        self.editBTN = ButtonImage(buttons_frame, image=self.editbtnimg, img_h=self.editbtnimgh, img_p=self.editbtnimgp, command=self.__open_edit_form, style='flatw.light.TButton', padding=0, state='disabled',)
        self.editBTN.grid(row=0, column=3, sticky='nsew', pady=2, padx=(0,8))


        deletebtnimg = Image.open(f"{IMG_PATH}/deletebtn.png")
        self.deletebtnimg = resize_icon(deletebtnimg, (50,50))

        deletebtnimgh = Image.open(f"{IMG_PATH}/deletebtnh.png")
        self.deletebtnimgh = resize_icon(deletebtnimgh, (50,50))

        deletebtnimgp = Image.open(f"{IMG_PATH}/deletebtnp.png")
        self.deletebtnimgp = resize_icon(deletebtnimgp, (50,50))

        self.deleteBTN = ButtonImage(buttons_frame, command=self.__deleteBudget, image=self.deletebtnimg, img_h=self.deletebtnimgh, img_p=self.deletebtnimgp, style='flatw.light.TButton', padding=0, state='disabled')


        processBTNimg = Image.open(f"{IMG_PATH}/processBTN.png")
        self.processBTNimg = resize_icon(processBTNimg,(50,50))

        processBTNimgh = Image.open(f"{IMG_PATH}/processBTNH.png")
        self.processBTNimgh = resize_icon(processBTNimgh, (50,50))

        processBTNimgp = Image.open(f"{IMG_PATH}/processBTNP.png")
        self.processBTNimgp = resize_icon(processBTNimgp, (50,50))

        self.processBTN = ButtonImage(buttons_frame, image=self.processBTNimg, img_h=self.processBTNimgh, img_p=self.processBTNimgp, command=self.__open_process_form, style='flatw.light.TButton', padding=0, state='disabled',)
        self.processBTN.grid(row=0, column=5, sticky='nsew', pady=2, padx=(0,8))

        


        searchOption_mb = ttb.Menubutton(buttons_frame, 
                                  compound=ttb.LEFT,
                                    style='white.TMenubutton',
                                    image=self.__filter)
        searchOption_mb.grid(row=0,column=6,sticky='nsew',padx=(15,5), pady=2)

        menu2 = ttb.Menu(searchOption_mb,tearoff=True,)

        menu2.add_command(label='Codigo', command=lambda: self.MAIN_FILTER.set('b.code'))
        menu2.add_command(label='Cliente', command=lambda: self.MAIN_FILTER.set('c.name'))
        menu2.add_command(label='Descripcion', command=lambda: self.MAIN_FILTER.set('b.description'))

        menu2.add_separator()

       


        def __set_state_filter(state_value):
            self.FILTER_STATE = state_value
            self.__searchBudgets()


        status_options = ttb.Menu(menu2)

        status_options.add_command(
            label='Todas',
            command=lambda: __set_state_filter(None)
        )

        status_options.add_command(
            label='Sin procesar',
            command=lambda: __set_state_filter(1)
        )

        status_options.add_command(
            label='En Proceso',
            command=lambda: __set_state_filter(2)
        )

        status_options.add_command(
            label='Aprobadas',
            command=lambda: __set_state_filter(3)
        )

        status_options.add_command(
            label='Rechazadas',
            command=lambda: __set_state_filter(4)
        )


        menu2.add_cascade(
            label="Status",
            menu=status_options)
        
        menu2.add_separator()

        menu2.add_command(label='Mostrar todos', command=lambda: self.MAIN_FILTER.set('code'))


        searchOption_mb['menu'] = menu2


        self.filter_label = ttb.Label(buttons_frame, 
                               background='#fff',
                               text='Codigo:', 
                               font=('arial',10,'bold'), 
                               anchor='center', width=7)
        self.filter_label.grid(row=0, column=7, padx=8, pady=4, sticky='nsw')

        self.SEARCHENTRY = ttb.Entry(buttons_frame, bootstyle='info', width=30)
        self.SEARCHENTRY.grid(row=0,column=8, ipady=2, padx=(0,8), pady=4, sticky='nsew')
        self.SEARCHENTRY.bind('<Return>', lambda e: self.__searchBudgets())
        
        searchbtnimg = Image.open(f"{IMG_PATH}/searchbtn.png")
        self.searchbtnimg = resize_icon(searchbtnimg, (50,50))

        searchbtnimgh = Image.open(f"{IMG_PATH}/searchbtnh.png")
        self.searchbtnimgh = resize_icon(searchbtnimgh, (50,50))

        searchbtnimgp = Image.open(f"{IMG_PATH}/searchbtnp.png")
        self.searchbtnimgp = resize_icon(searchbtnimgp, (50,50))

        ButtonImage(buttons_frame, image=self.searchbtnimg, command=self.__searchBudgets, img_h=self.searchbtnimgh, img_p=self.searchbtnimgp, style='flatw.light.TButton', padding=0).grid(row=0, column=9, pady=2, padx=(0,0))



    
        yscroll = ttb.Scrollbar(table_frame, 
                                orient='vertical',
                                bootstyle="dark-round")
        yscroll.grid(row=3, column=1, padx=(0,8), pady=(4,8),sticky='ns', rowspan=2)

        xscroll = ttb.Scrollbar(table_frame, 
                                orient='horizontal',
                                bootstyle="dark-round")
        xscroll.grid(row=4, column=0, padx=(8,2), pady=(2,8),sticky='ew')

        columns = ('code','description','state','type','client','address','representative','creationDate','currency',
                   'sub_total','iva','total_amount','uc','up')

        self.budgetsGridView = ttb.Treeview(table_frame,columns=columns,show='headings',
                                bootstyle='dark', height=10, xscrollcommand=xscroll.set,
                                selectmode='extended', yscrollcommand=yscroll.set)
        self.budgetsGridView.grid(row=3,column=0,padx=(8,2),pady=(4,2),sticky='nsew')

        yscroll.configure(command=self.budgetsGridView.yview)
        xscroll.configure(command=self.budgetsGridView.xview)

        self.budgetsGridView.heading(columns[0],anchor='center', text='Codigo')
        self.budgetsGridView.heading(columns[1], anchor='center', text='Descripcion')
        self.budgetsGridView.heading(columns[2],anchor='center', text='Status')
        self.budgetsGridView.heading(columns[3], anchor='center', text='Tipo')
        self.budgetsGridView.heading(columns[4],anchor='center', text='Cliente')
        self.budgetsGridView.heading(columns[5], anchor='center', text='Direccion')
        self.budgetsGridView.heading(columns[6],anchor='center', text='Representante')
        self.budgetsGridView.heading(columns[7], anchor='center', text='Fecha')
        self.budgetsGridView.heading(columns[8], anchor='center', text='Moneda')
        self.budgetsGridView.heading(columns[9], anchor='center', text='Sub Total')
        self.budgetsGridView.heading(columns[10], anchor='center', text='IVA')
        self.budgetsGridView.heading(columns[11], anchor='center', text='Total')
        self.budgetsGridView.heading(columns[12], anchor='center', text='Creador')
        self.budgetsGridView.heading(columns[13], anchor='center', text='Procesamiento')

        self.budgetsGridView.column(columns[0],width=160,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[1],width=300,stretch=True,anchor='center')
        self.budgetsGridView.column(columns[2],width=200,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[3],width=200,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[4],width=300,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[5],width=200,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[6],width=200,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[7],width=200,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[8],width=200,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[9],width=200,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[10],width=200,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[11],width=200,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[12],width=200,stretch=False,anchor='center')
        self.budgetsGridView.column(columns[13],width=200,stretch=False,anchor='center')

        self.budgetsGridView.bind('<<TreeviewSelect>>', lambda e: self.__enabled_view())

       
        
        self.bind('<Map>',lambda e: self.update_page())

    def rejected_cotz(self):
        COTZ = Budget.reject_by_time()
        print(COTZ)

        if len(COTZ):
            doclist = ''
            for index,doc in enumerate(COTZ):
                doc = doc[0]
                doclist = f"\n - Cotizacion: {'0'*len(str(doc))+str(doc)}"
            messagebox.showwarning('RECHAZADAS', f"Las siguientes cotizaciones fueron rechazadas:{doclist}")


    def update_page(self):
        self.__searchBudgets()
        self.__update_metrics()
        self.set_privileges()
        self.rejected_cotz()

    def set_privileges(self):
        if constGlobal.loggued_user.rol == 1:
            self.deleteBTN.grid(row=0, column=4, sticky='nsew', pady=2, padx=(0,8))
        else:
            self.deleteBTN.grid_forget()
  
    def __enabled_view(self):
        if self.budgetsGridView.selection()!= ():
            self.viewBTN.config(state='normal')
            budget = Budget.findOneBudget(self.__get_selected_budget_code())
            if budget.editable:    
                self.editBTN.config(state='normal')
            else:
                self.editBTN.config(state='disabled')
            if budget.state<3:    
                self.processBTN.config(state='normal')
            else:
                self.processBTN.config(state='disabled')
            
            del budget
            self.deleteBTN.config(state='normal')
        else:
            self.viewBTN.config(state='disabled')
            self.editBTN.config(state='disabled')
            self.deleteBTN.config(state='disabled')
            self.processBTN.config(state='disabled')

    def update_chart(self):
        self.ax.clear()
        data = {
            'Sin Procesar': self.sin_procesar.get(),
            'En Proceso': self.en_proceso.get(),
            'Rechazadas': self.rechazada.get(),
            'Aprobadas': self.aprobada.get(),
        }

        languages = data.keys()
        popularity = data.values()

        self.ax.bar(languages, popularity, color=[GUI_COLORS['warning']+'B0',GUI_COLORS['primary']+'B0',GUI_COLORS['danger']+'B0',GUI_COLORS['success']+'B0'], edgecolor='white')
        self.canvas.draw()
        self.canvas.flush_events()



        
    def __open_create_form(self):
        ask = messagebox.askquestion('Registrar','Desea crear una Cotizacion?', parent=self)
        if ask == 'yes':
            waitwindow = BudgetForm(self, window_type='create', title='Registrar Cotizacion',)
            waitwindow.wait_window()
            self.__searchBudgets()
            self.__update_metrics()

    def __searchBudgets(self):
        self.budgetsGridView.delete(*self.budgetsGridView.get_children())

        items = Budget.findAllBudgets(value=self.SEARCHENTRY.get(), condition_field=self.MAIN_FILTER.get(), filter_status = self.FILTER_STATE)

        for budget in items:
            


            self.budgetsGridView.insert("",ttb.END,values=(
                f"{'0'*(6-len(str(budget[0])))+str(budget[0])}",
                budget[1],
                budget[2],
                budget[3],
                budget[4],
                budget[5],
                budget[6],
                budget[7],
                budget[8],
                budget[9],
                budget[10],
                budget[11],
                budget[12],
                budget[13],
            ),)

        self.__update_metrics()

    def approve_reject_form(self, budget):
        self.processForm = ttb.Toplevel(title='Procesamiento Final')
        self.processForm.config(background='white')
        self.processForm.resizable(0,0)
        self.processForm.focus()
        self.processForm.grab_set()
        self.processForm.transient()

        approveImg = Image.open(f"{IMG_PATH}/approve.png")
        self.approveImg = ImageTk.PhotoImage(approveImg.resize(resize_image(22, approveImg.size)))
        approveImgh = Image.open(f"{IMG_PATH}/approveh.png")
        self.approveImgh = ImageTk.PhotoImage(approveImgh.resize(resize_image(22, approveImgh.size)))
        approveImgp = Image.open(f"{IMG_PATH}/approvep.png")
        self.approveImgp = ImageTk.PhotoImage(approveImgp.resize(resize_image(22, approveImgp.size)))

        self.approveBTN = ButtonImage(self.processForm, text='   APROBAR', compound='center',  command=lambda:self.approve_budget(budget), image=self.approveImg, img_h=self.approveImgh, img_p=self.approveImgp, style='flatw.light.TButton', padding=0)
        self.approveBTN.grid(row=0, column=0, padx=(10,5), pady=10)

        rejectImg = Image.open(f"{IMG_PATH}/reject.png")
        self.rejectImg = ImageTk.PhotoImage(rejectImg.resize(resize_image(22, rejectImg.size)))
        rejectImgh = Image.open(f"{IMG_PATH}/rejecth.png")
        self.rejectImgh = ImageTk.PhotoImage(rejectImgh.resize(resize_image(22, rejectImgh.size)))
        rejectImgp = Image.open(f"{IMG_PATH}/rejectp.png")
        self.rejectImgp = ImageTk.PhotoImage(rejectImgp.resize(resize_image(22, rejectImgp.size)))

        self.rejectBTN = ButtonImage(self.processForm,  text='    RECHAZAR', compound='center', command=lambda:self.reject_budget(budget), image=self.rejectImg, img_h=self.rejectImgh, img_p=self.rejectImgp, style='flatw.light.TButton', padding=0)
        self.rejectBTN.grid(row=0, column=1, padx=(5,10), pady=10)
        self.processForm.place_window_center()

    def __set_order_code(self, budget):
        def set_purchaseOrder():
            CODE = self.ORDENPURCHESA.get()
            if CODE:
                ask = messagebox.askquestion('Confirmación', f'El codigo de Compra para la cotizacion sera: {CODE}?',parent=window)
                if ask == 'yes':
                    budget.setPurchaseOrder(CODE)
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
       

    def approve_budget(self,budget):
        ask = messagebox.askquestion('Procesar',"Confirmación de aprobacion de Cotizacion. Ejecutar accion?", parent=self.processForm)
        if ask == 'yes':
            budget.approve(constGlobal.loggued_user.id)
            self.__set_order_code(budget)
            self.processForm.destroy()
            messagebox.showinfo('Aviso','Cotizacion Aprobada!', parent=self)
            self.update_page()

    def reject_budget(self, budget):
        ask = messagebox.askquestion('Procesar',"Confirmación para rechazar Cotizacion. Ejecutar accion?", parent=self.processForm)
        if ask == 'yes':
            budget.reject(constGlobal.loggued_user.id)
            self.processForm.destroy()
            messagebox.showinfo('Aviso','Cotizacion Rechazada!', parent=self)
            
            self.update_page()

    def __open_process_form(self):
        code = self.__get_selected_budget_code()
        budget = Budget.findOneBudget(code)
        if budget:
            if budget.state == 1:
                ask = messagebox.askquestion('Procesar','Desea procesar el registro seleccionado?', parent=self)
                if ask == 'yes':
                    budget.process(constGlobal.loggued_user.id)
                    messagebox.showinfo('Aviso','Cotizacion Procesada!', parent=self)
                    self.update_page()
            elif budget.state==2:
                self.approve_reject_form(budget)
        del budget


    def __open_edit_form(self):
            budget = self.__get_selected_budget_code()
            if budget:
                ask = messagebox.askquestion('Modificar','Desea modificar el registro seleccionado?', parent=self)
                if ask == 'yes':
                    waitwindow = BudgetForm(self, window_type='edit', title='Modificar Cotizacion', budget=budget)
                    waitwindow.wait_window()
                    self.__searchBudgets()
                    self.__update_metrics()
            del budget

    def __get_selected_budget_code(self,):
        selected = self.budgetsGridView.focus()

        if selected:
            code = self.budgetsGridView.item(selected, 'values')[0]
            return code


    def __open_view_form(self):
        budget = self.__get_selected_budget_code()

        if budget:
            BudgetForm(self, window_type='view', title='Detalles de la Cotización', budget=budget, callback=self.__update_metrics)
        self.__update_metrics()
        del budget


    def __deleteBudget(self):
        ask = messagebox.askquestion('Eliminar', 'Desea eliminar el registro de la cotizacion?', parent=self)
        if ask == 'yes':
            code = self.__get_selected_budget_code()
            budget = Budget.findOneBudget(code).delete()
            if budget:
                del code, budget
                messagebox.showinfo('Aviso','Cotizacion Eliminada satisfactoriamente.', parent=self)
                self.__searchBudgets()
                self.__update_metrics()
            else:
                messagebox.showinfo('Aviso','La Cotizacion no puede ser Eliminada. Ya ha sido procesada.', parent=self)



    def __update_metrics(self):
        self.aprobada.set(Budget.countApproveBudgets())
        self.rechazada.set(Budget.countRejectBudgets())
        self.en_proceso.set(Budget.countProcessBudgets())
        self.sin_procesar.set(Budget.countEditableBudgets())
        self.update_chart()
#######################################


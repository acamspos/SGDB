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
from tkinter import messagebox

class ActivityPage(ttb.Frame):
    def __init__(self, master=None):
        PART_COLOR = GUI_COLORS['bg']
        PART2_COLOR = GUI_COLORS['primary']

        super().__init__(master)
        
        ############# CONFIGURACION VENTANA #############
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        
        ############## ESTILOS PERSONALIZADOS ##############


        ########### VARIABLES DE PAGINACION ############
        self.pag = ttb.IntVar(value=1)

        self.__ELEMENTS_PER_PAGE = 12
        self.__actualPage = ttb.IntVar(value=1)
        self.__totalPage = ttb.IntVar(value=1)
   
        self.__programdas = ttb.IntVar()
        self.__enCurso = ttb.IntVar()
        self.__completed  = ttb.IntVar()
        self.__cancel = ttb.IntVar()

        ####################### ELEMENTOS DE LA INTERFAZ GRAFICA #######################

        ###### TSECCION DEL TITULO:

        self.__act_icon = Image.open(f'{IMG_PATH}/activities_title.png')
        self.__act_icon = ImageTk.PhotoImage(self.__act_icon.resize(resize_image(10, self.__act_icon.size)))
        
        page_img_label = ttb.Label(self, image=self.__act_icon, padding='0 0')
        page_img_label.grid(row=0, column=0, sticky='nsw', pady=(10, 4), padx=20)
        page_img_label.grid_propagate(0)
        page_img_label.anchor('w')

        page_title_label = ttb.Label(page_img_label, text='ACTIVIDADES', padding='0 0', background='#203864',
                               font=('arial',15, 'bold'), foreground='#fff')
        page_title_label.grid(row=0, column=0, sticky='nsew',padx=(80,0))

        ttb.Separator(self, orient='horizontal').grid(row=1, column=0, sticky='nsew',padx=20)

        ######### SECCION DE CONTENIDO:
    
        CONTENT_FRAME = ttb.Frame(self,)
        CONTENT_FRAME.grid(row=2, column=0, sticky='nsew',pady=10, padx=20)
        CONTENT_FRAME.columnconfigure(0, weight=1)
        CONTENT_FRAME.rowconfigure(0, weight=1)





        metrics_card_Frame = CTkFrame(CONTENT_FRAME, fg_color='#fff', border_width=1, border_color='#D0CECE')
        metrics_card_Frame.grid(row=0, column=0, sticky='nsew', padx=4, pady=4)
        metrics_card_Frame.columnconfigure(0, weight=1)
        metrics_card_Frame.rowconfigure(4, weight=1)


        subtitle = CTkFrame(metrics_card_Frame, corner_radius=6, fg_color=PART2_COLOR)
        subtitle.grid(row=0, column=0, sticky='nsew', padx=10, pady=(10,2))

        self.micon = resize_icon(Image.open(f'{IMG_PATH}/management.png'),(45,45))

        ttb.Label(subtitle, image=self.micon, background=PART2_COLOR, ).grid(row=0, column=0, rowspan=2, sticky='nsew', padx=(8), pady=8)

        ttb.Label(subtitle, text='Gestion de Actividades', background=PART2_COLOR, font=(GUI_FONT,13,'bold'), foreground='#fff').grid(row=0, column=1, sticky='nsew', padx=(4,8), pady=(8,0))

        ttb.Label(subtitle, text='Inicio/Actividades', background=PART2_COLOR, font=(GUI_FONT,9), foreground='#fff').grid(row=1, column=1, sticky='nsew', padx=(4,8), pady=(0,8))

        ttb.Frame(metrics_card_Frame, bootstyle='primary').grid(row=1, column=0, sticky='nsew', padx=10, pady=5)

        buttons_frame = tk.Frame(metrics_card_Frame, background='red')
        buttons_frame.config(background='#fff')
        buttons_frame.grid(row=2, column=0, sticky='nsew', padx=16)
        buttons_frame.columnconfigure(5, weight=1)

        self.state_filter = ttb.IntVar(value=0)

        ttb.Radiobutton(buttons_frame,style='warning.Outline.Toolbutton', command=self.set_activities_card, variable=self.state_filter, value=0, text='TODAS').grid(row=0, column=0, sticky='nsew', pady=2, padx=(0,8))


        ttb.Radiobutton(buttons_frame,style='warning.Outline.Toolbutton', command=self.set_activities_card, variable=self.state_filter, value=1, text='PROGRAMADAS').grid(row=0, column=1, sticky='nsew', pady=2, padx=(0,8))

        ttb.Radiobutton(buttons_frame,style='warning.Outline.Toolbutton', command=self.set_activities_card, variable=self.state_filter, value=2, text='EN EJECUCIÓN').grid(row=0, column=2, sticky='nsew', pady=2, padx=(0,8))

        ttb.Radiobutton(buttons_frame,style='warning.Outline.Toolbutton', command=self.set_activities_card, variable=self.state_filter, value=3, text='COMPLETADAS').grid(row=0, column=3, sticky='nsew', pady=2, padx=(0,8))
       
        ttb.Entry(buttons_frame,  width=30).grid(row=0,column=5, ipady=2, padx=(0,8), sticky='e')
        
        searchbtnimg = Image.open(f"{IMG_PATH}/searchbtn.png")
        self.searchbtnimg = resize_icon(searchbtnimg, (40,40))

        searchbtnimgh = Image.open(f"{IMG_PATH}/searchbtnh.png")
        self.searchbtnimgh = resize_icon(searchbtnimgh, (40,40))

        searchbtnimgp = Image.open(f"{IMG_PATH}/searchbtnp.png")
        self.searchbtnimgp = resize_icon(searchbtnimgp, (40,40))

        ButtonImage(buttons_frame, image=self.searchbtnimg, img_h=self.searchbtnimgh, img_p=self.searchbtnimgp, style='flatw.light.TButton', command=self.set_activities_card, padding=0).grid(row=0, column=6, pady=2, padx=(0,0))

        ttb.Frame(metrics_card_Frame, bootstyle='primary').grid(row=3, column=0, sticky='nsew', padx=10, pady=5)

        cardsFrame = CTkFrame(CONTENT_FRAME, fg_color='#fff', border_width=1, border_color='#D0CECE')
        cardsFrame.grid(row=0, column=1, sticky='nsew', padx=4, pady=4)
        cardsFrame.columnconfigure(0, weight=1)
        cardsFrame.anchor('center')


        editCardImg = Image.open(f"{IMG_PATH}/edit_card.png")
        editIconImg = Image.open(f"{IMG_PATH}/edit_icon.png")
        nonProcess_card = BCards(cardsFrame, 
                                     bg_color='#fff',
                                     background_color=GUI_COLORS['warning'],
                                    value=self.__programdas,
                                     title='Programadas',
                                     sub_title='Actividades Sin Realizar',
                                     card_background=editCardImg,
                                     icon=editIconImg)
        nonProcess_card.grid(row=0, column=0, padx=(5,5), pady=(5,5), sticky='nsew')



        processCardImg = Image.open(f"{IMG_PATH}/process_card.png")
        processIconImg = Image.open(f"{IMG_PATH}/process_icon.png")
        process_card = BCards(cardsFrame, 
                                     bg_color='#fff',
                                     background_color=GUI_COLORS['primary'],
                                    value=self.__enCurso,
                                     title='En Ejecución',
                                     sub_title='Actividades En Ejecucion',
                                     card_background=processCardImg,
                                     icon=processIconImg)
        process_card.grid(row=1, column=0, padx=(5,5), pady=(5,5), sticky='nsew')


        approveCardImg = Image.open(f"{IMG_PATH}/approve_card.png")
        approveIconImg = Image.open(f"{IMG_PATH}/approve_icon.png")
        approve_card = BCards(cardsFrame, 
                                     bg_color='#fff',
                                     background_color=GUI_COLORS['success'],
                                     value=self.__completed,
                                     title='Completadas',
                                     sub_title='Actividades Completadas',
                                     card_background=approveCardImg,
                                     icon=approveIconImg)
        approve_card.grid(row=2, column=0, padx=(5,5), pady=(5,5), sticky='nsew')



        cancelCardImg = Image.open(f"{IMG_PATH}/cancel_card.png")
        cancelIconImg = Image.open(f"{IMG_PATH}/cancel_icon.png")
        denied_card = BCards(cardsFrame, 
                                     bg_color='#fff',
                                     background_color=GUI_COLORS['danger'],
                                     value=self.__cancel,
                                     title='Canceladas',
                                     sub_title='Actividades Canceladas',
                                     card_background=cancelCardImg,
                                     icon=cancelIconImg)
        denied_card.grid(row=3, column=0, padx=(5,5), pady=(5,5), sticky='nsew')

    
        self.cards_scroll_frame = ScrolledFrame(metrics_card_Frame, style='white.TFrame', bootstyle='dark')
        self.cards_scroll_frame.grid(row=4, column=0, sticky='nsew',pady=(10,5), padx=6)
        self.cards_scroll_frame.columnconfigure(0, weight=1)

        

        self.paginacion_frame = ttb.Frame(metrics_card_Frame, style='white.TFrame')
        self.paginacion_frame.grid(row=5, column=0, sticky='nsew', padx=12, pady=6)
        self.paginacion_frame.anchor('e')


        self.pre_page_btn = resize_icon(Image.open(f'{IMG_PATH}/pre_page.png'), (40,40))
        pre_btn = ButtonImage(self.paginacion_frame, image=self.pre_page_btn, padding=0, style='flatw.light.TButton', )
        pre_btn.grid(row=0,column=0, sticky='ne')


        pag_entry = ttb.Entry(self.paginacion_frame, width=4, justify='center', textvariable=self.pag)
        pag_entry.grid(row=0, column=1, sticky='nsew',padx=8, pady=4)


        self.next_page_btn = resize_icon(Image.open(f'{IMG_PATH}/next_page.png'), (40,40))
        next_btn = ButtonImage(self.paginacion_frame, image=self.next_page_btn, padding=0, style='flatw.light.TButton', )
        next_btn.grid(row=0,column=2, sticky='ne')


  
        self.bind('<Map>',lambda e: self.update_page())
    
    def update_page(self):
        self.activities_to_expire()
        self.set_activities_card()

    def activities_to_expire(self):
        COTZ = Activity.get_avtivity_to_end()
        COTZ = [f'id: {row[0]} - Cotización: {row[1]}' for row in COTZ]
        codes = ',\n'.join(COTZ)
        if len(COTZ)>0:
            messagebox.showinfo('RECHAZADAS', f'Las siguientes cotizaciones fueron rechazadas:\n{codes}')

    def unpload_activities(self):
        if self.state_filter.get()==0:
            activities = DB.find_activities()
            if activities:
                return [Activity(**row) for row in activities]
        else:
            filterActivities = DB.find_activities(state=self.state_filter.get())
            if filterActivities:
                return [Activity(**row) for row in filterActivities]
            

    


    def set_activities_card(self):
        for task in (self.cards_scroll_frame.winfo_children()):
            task.destroy()
     
        start = (self.__actualPage.get()-1 )* self.__ELEMENTS_PER_PAGE
        end = start +  self.__ELEMENTS_PER_PAGE

        data = self.unpload_activities()
        if data:
            if self.__totalPage.get() == self.__actualPage.get() and len(data)<12:
                end = None

            for index, act in enumerate(data[start:end]):
                ActivityRow(self.cards_scroll_frame, mw=self, callback=self.complete_task,  activity=act).grid(row=index, column=0, sticky='nsew',padx=(10,20),pady=(10,20))
            
            self.cards_scroll_frame.yview_moveto(0)
        self.__update_metrics()


    def complete_task(self,):
        self.set_activities_card()
        self.__update_metrics()


    def __update_metrics(self):
        self.__programdas.set(Activity.countProgramada())
        self.__cancel.set(Activity.countCancelded())
        self.__enCurso.set(Activity.countProcess())
        self.__completed.set(Activity.countCompleted())
    



# app = ttb.Window(themename='new')
# SGDB_Style()

# ActivityPage(app).pack(expand=True,fill='both')
# app.mainloop()
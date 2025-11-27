import ttkbootstrap as ttb
from assets.globals import GUI_COLORS, IMG_PATH, GUI_FONT
from assets.utils import resize_image, resize_icon
from PIL import Image, ImageTk
from tkinter import messagebox
import tkinter as tk
from components.buttons import ButtoLabel, ButtonImage
from ttkbootstrap.scrolled import ScrolledFrame
from customtkinter import CTkFrame
from models.entitys.activity import Activity


from assets.db.db_connection import DB
from pages.activities.views.startform import StartActivityForm
from pages.activities.views.tasks import TaskForm
from pages.activities.views.task_machinery import MachineryActivityForm
from pages.activities.views.factForm import FactForm
from models.entitys.activity import Activity


colors = {
    2:'#fff',
    3:'#fff',
    4:"#fff",
    1:'#fff'

}

info_img = Image.open(f'{IMG_PATH}/info.png')


complete_img = Image.open(f'{IMG_PATH}/complete.png')
complete_h_img = Image.open(f'{IMG_PATH}/complete_h.png')
complete_p_img = Image.open(f'{IMG_PATH}/complete_p.png')

#### Incomplete img

incomplete_img = Image.open(f'{IMG_PATH}/incomplete.png')
incomplete_h_img = Image.open(f'{IMG_PATH}/incomplete_h.png')
incomplete_p_img = Image.open(f'{IMG_PATH}/incomplete_p.png')

###### Repro Img

repro_img = Image.open(f'{IMG_PATH}/repro.png')
repro_h_img = Image.open(f'{IMG_PATH}/repro_h.png')
repro_p_img = Image.open(f'{IMG_PATH}/repro_p.png')

machineryBtn_img = Image.open(f'{IMG_PATH}/machineryBtn.png')
machineryBtn_h_img = Image.open(f'{IMG_PATH}/machineryBtnh.png')
machineryBtn_p_img = Image.open(f'{IMG_PATH}/machineryBtnp.png')




############## Redimensionar #############

complete_img = complete_img.resize(resize_image(14,complete_img.size))
complete_h_img = complete_h_img.resize(resize_image(14,complete_h_img.size))
complete_p_img = complete_p_img.resize(resize_image(14,complete_p_img.size))

           
incomplete_img = incomplete_img.resize(resize_image(14,incomplete_img.size))
incomplete_h_img = incomplete_h_img.resize(resize_image(14,incomplete_h_img.size))
incomplete_p_img = incomplete_p_img.resize(resize_image(14,incomplete_p_img.size))

repro_img = repro_img.resize(resize_image(14,repro_img.size))
repro_h_img = repro_h_img.resize(resize_image(14,repro_h_img.size))
repro_p_img = repro_p_img.resize(resize_image(14,repro_p_img.size))

machineryBtn_img = machineryBtn_img.resize((56,56))
machineryBtn_h_img = machineryBtn_h_img.resize((56,56))
machineryBtn_p_img = machineryBtn_p_img.resize((56,56))

##################

start_img = Image.open(f'{IMG_PATH}/start.png')
start_img = start_img.resize(resize_image(14,start_img.size))

start_h_img = Image.open(f'{IMG_PATH}/start_h.png')
start_h_img = start_h_img.resize(resize_image(14,start_h_img.size))

start_p_img = Image.open(f'{IMG_PATH}/start_p.png')
start_p_img = start_p_img.resize(resize_image(14,start_p_img.size))

creditnote_img = Image.open(f'{IMG_PATH}/creditnote.png')
creditnote_h_img = Image.open(f'{IMG_PATH}/creditnote_h.png')
creditnote_p_img = Image.open(f'{IMG_PATH}/creditnote_p.png')


invoice_btn_img = Image.open(f'{IMG_PATH}/invoice_btn.png')
invoice_btn_h_img = Image.open(f'{IMG_PATH}/invoice_btn_h.png')
invoice_btn_p_img = Image.open(f'{IMG_PATH}/invoice_btn_p.png')


creditnote_img = creditnote_img.resize(resize_image(14,creditnote_img.size))
creditnote_h_img = creditnote_h_img.resize(resize_image(14,creditnote_h_img.size))
creditnote_p_img = creditnote_p_img.resize(resize_image(14,creditnote_p_img.size))

invoice_btn_img = invoice_btn_img.resize(resize_image(14,invoice_btn_img.size))
invoice_btn_h_img = invoice_btn_h_img.resize(resize_image(14,invoice_btn_h_img.size))
invoice_btn_p_img = invoice_btn_p_img.resize(resize_image(14,invoice_btn_p_img.size))





def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")






class ActivityRow(ttb.Frame):
    def __init__(self, master=None, mw = None, activity = None, callback=None, *args, **kwargs):
        global info_img
        super().__init__(master, height=70, style='white.TFrame', *args, **kwargs)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid_propagate(0)
        self.__ACTIVITY:Activity = activity
        self.bg_color = colors [self.__ACTIVITY.stage]

        self.callback  = callback
        self.mw = mw
        self.numTaskVar = ttb.StringVar(value=f"{self.__ACTIVITY.get_num_tasks_complete()}/{self.__ACTIVITY.get_num_tasks()}")
       
        self.activitie_title_type = ttb.Label(self, text=f'{self.__ACTIVITY.get_stage().upper()} - {self.__ACTIVITY.budget_code}', font=(GUI_FONT,12,'bold'),anchor='sw',background=self.bg_color)
        self.activitie_title_type.grid(row=0, column=0, padx=(5,0),pady=0,sticky='nsew', columnspan=4)
        
        self.TaksLabel = ttb.Label(self, text=f"Tareas:",font=(GUI_FONT,11,'bold'), background=self.bg_color)
        self.TaksLabel.grid(row=1, column=0, padx=(5,0),pady=0,sticky='nsew')
        


        self.numTaksLabel = ttb.Label(self,textvariable=self.numTaskVar,font=(GUI_FONT,11), background=self.bg_color)
        self.numTaksLabel.grid(row=1, column=1, padx=(2,0),pady=0,sticky='nsew')
        
        ttb.Label(self, text=f"-",font=(GUI_FONT,11), background=self.bg_color).grid(row=1, column=2, padx=5,pady=0,sticky='nsew')

        description = self.__ACTIVITY.description[:100]+ '...'

        self.description_label = ttb.Label(self, text=description,
                                           background=self.bg_color, 
                                           font=('Aptos Narrow',10,),  
                                           foreground='#7F7F7F', 
                                           justify='left', anchor='sw',
                                           )
        self.description_label.grid(row=1, column=3, padx=(5,0),pady=(0,0), sticky='nsew',ipady=0)

        
        ttb.Separator(self, bootstyle='light').grid(row=2,column=0, columnspan=5, padx=10, pady=(8,0), sticky='nsew')
        self.buttons_frame = None
        self.set_buttons()


    def set_buttons(self):

        if self.buttons_frame != None:
            self.buttons_frame.destroy()

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.grid(row=0, column=4, rowspan=2, sticky='nsew', padx=(20,0),)
        self.buttons_frame.config(background=self.bg_color)
        self.buttons_frame.anchor('center')

        if self.__ACTIVITY.stage ==  2:
            
            self.taskManagment_img = ImageTk.PhotoImage(complete_img)
            self.taskManagment_h_img = ImageTk.PhotoImage(complete_h_img)
            self.taskManagment_p_img = ImageTk.PhotoImage(complete_p_img)

           
            self.incomplete_img = ImageTk.PhotoImage(incomplete_img)
            self.incomplete_h_img = ImageTk.PhotoImage(incomplete_h_img)
            self.incomplete_p_img = ImageTk.PhotoImage(incomplete_p_img)

            self.machineryBtn_img = ImageTk.PhotoImage(machineryBtn_img)
            self.machineryBtn_h_img = ImageTk.PhotoImage(machineryBtn_h_img)
            self.machineryBtn_p_img = ImageTk.PhotoImage(machineryBtn_p_img)

            self.buttons_frame.columnconfigure(2, weight=1)

            self.machinery_btn = ButtoLabel(self.buttons_frame, command=lambda:self.open_machineryList_modal(), image=self.machineryBtn_img, img_h=self.machineryBtn_h_img, background=self.bg_color, img_p=self.machineryBtn_p_img, padding=0)
            self.machinery_btn.grid(row=0, column=0, padx=(0,10),pady=(0,0),sticky='nsew')

            self.taskManagment_btn = ButtoLabel(self.buttons_frame, command=lambda:self.open_taskList_modal(), image=self.taskManagment_img, img_h=self.taskManagment_h_img, background=self.bg_color, img_p=self.taskManagment_p_img, padding=0)
            self.taskManagment_btn.grid(row=0, column=1, padx=(0,10),pady=(0,0),sticky='nsew')

            self.incomplete_btn = ButtoLabel(self.buttons_frame, command=lambda:self.__cancel_activity(), image=self.incomplete_img, img_h=self.incomplete_h_img, background=self.bg_color, img_p=self.incomplete_p_img, padding=0)
            self.incomplete_btn.grid(row=0, column=2, padx=(0,10),pady=(0,0),sticky='nsew')


        elif self.__ACTIVITY.stage ==  3:
            
            self.creditnote_img = ImageTk.PhotoImage(creditnote_img)
            self.creditnote_h_img = ImageTk.PhotoImage(creditnote_h_img)
            self.creditnote_p_img = ImageTk.PhotoImage(creditnote_p_img)

            self.invoice_btn_img = ImageTk.PhotoImage(invoice_btn_img)
            self.invoice_btn_h_img = ImageTk.PhotoImage(invoice_btn_h_img)
            self.invoice_btn_p_img = ImageTk.PhotoImage(invoice_btn_p_img)

            self.creditnote_btn = ButtoLabel(self.buttons_frame, command=self.create_creditNote, image=self.creditnote_img, img_h=self.creditnote_h_img, background=self.bg_color, img_p=self.creditnote_p_img, padding=0, )
            self.creditnote_btn.grid(row=0, column=0,padx=(0,10),pady=(0,0),sticky='e')

            self.invoice_btn = ButtoLabel(self.buttons_frame, command=lambda: self.create_bill(), image=self.invoice_btn_img, img_h=self.invoice_btn_h_img, background=self.bg_color, img_p=self.invoice_btn_p_img, padding=0)
            self.invoice_btn.grid(row=0, column=1, padx=(0,10),pady=(0,0),sticky='nsew')

        elif self.__ACTIVITY.stage ==  1:
            self.buttons_frame.columnconfigure(1, weight=1)

            self.start_img = ImageTk.PhotoImage(start_img)
            self.start_h_img = ImageTk.PhotoImage(start_h_img)
            self.start_p_img = ImageTk.PhotoImage(start_p_img)

            self.start_btn = ButtoLabel(self.buttons_frame, command=lambda:self.__init_activity(), image=self.start_img, img_h=self.start_h_img, background=self.bg_color, img_p=self.start_p_img, padding=0, )
            self.start_btn.grid(row=0, column=0, padx=(0,10),pady=(0,0),sticky='nsew')
    

    def open_taskList_modal(self):
        modal = TaskForm(self, activity=self.__ACTIVITY, callback=self.completed_task)
        self.wait_window(modal)
        self.numTaskVar.set(f"{self.__ACTIVITY.get_num_tasks_complete()}/{self.__ACTIVITY.get_num_tasks()}")
        if self.__ACTIVITY.complete:
            
            self.create_bill()

    def open_machineryList_modal(self):
        mach = self.__ACTIVITY.get_machinery()
        if mach and len(mach)>0:
            modal = MachineryActivityForm(self, activity=self.__ACTIVITY, callback=self.completed_task)
            self.wait_window(modal)
        else:
            messagebox.showinfo('Aviso','La actividad no tiene equipos/maquinaria asociadas.', parent=self)
       


    def __init_activity(self):
        ask = messagebox.askquestion(title='Iniciar', message=f'Desea dar inicio a la actividad asociada a la cotizacion {self.__ACTIVITY.budget_code}?', parent=self)

        if ask == 'yes':
            window = StartActivityForm(self, activity=self.__ACTIVITY, callback=lambda: self.update_card(2))

    def __cancel_activity(self):
        ask = messagebox.askquestion(title='Cancelar', message=f'Desea cancelar la actividad asociada a la cotizacion {self.__ACTIVITY.budget_code}?', parent=self)

        if ask == 'yes':
            self.update_card(4)
            messagebox.showinfo('Aviso','Actividad cancelada!', parent=self)


    def update_card(self, stage):
        self.__ACTIVITY.update_stage(stage)
        self.set_buttons()
        

    def completed_task(self):
        self.__ACTIVITY.update_stage(3)
        self.__ACTIVITY.update_machinery_state()
        self.set_buttons()


    
    def facturar(self):
        self.__ACTIVITY.update_process()
        self.__ACTIVITY.update()
        if self.__ACTIVITY.complete:
            messagebox.showinfo(title='Facturacion', message='La actividad ha sido facturada con exito.', parent=self)
            self.callback()
        
    
    def create_bill(self):
        ask = messagebox.askquestion(title='Facturar', message='Desea generar la factura de esta actividad?', parent=self)
    
        if ask=='yes':
            modal = FactForm(self, activity=self.__ACTIVITY, callback=self.facturar)
            self.wait_window(modal)
            
                

    def create_creditNote(self):
        if messagebox.askquestion(title='Nota de Entrega', message='Desea generar una nota de entrega de esta actividad?', parent=self):
            pass
        

    def create_form(self):
        title_bar = ttb.Frame(self.content, )
        title_bar.grid(row=0, column=0, padx=4, pady=4, sticky='nsew')
        title_bar.columnconfigure(0, weight=1)

        ttb.Label(title_bar, text='ACTIVIDAD - PROYECTO', font=(GUI_FONT,15,'bold'), bootstyle='info', anchor='center').grid(row=0, column=0,sticky='nsew',)
        ttb.Frame(title_bar, bootstyle='primary', height=2).grid(row=1, column=0, columnspan=3, pady=(6,0), sticky='nsew')

        self.cancel_img = resize_icon(Image.open(f'{IMG_PATH}/close_btn.png'))
        self.cancel_imgh = resize_icon(Image.open(f'{IMG_PATH}/close_btn_h.png'))
        self.cancel_imgp = resize_icon(Image.open(f'{IMG_PATH}/close_btn_p.png'))

        cancel_btn = ButtonImage(title_bar, image=self.cancel_img, img_h=self.cancel_imgh, img_p=self.cancel_imgp, command=self.form.destroy, style='flatw.light.TButton', cursor='hand2')
        cancel_btn.grid(row=0, column=0, sticky='e')

        info_frame = ScrolledFrame(self.content, autohide=False)
        info_frame.grid(row=1, column=0, padx=4, pady=(4,0), sticky='nsew')
        info_frame.columnconfigure(0, weight=1)
        
        self.aux_frame = ttb.Frame(info_frame)
        self.aux_frame.grid(row=0, column=0, sticky='nsew', padx=(0,14))
        self.aux_frame.columnconfigure(0, weight=1)
        self.aux_frame.columnconfigure(1, weight=1)

        self.type_icon = Image.open(f'{IMG_PATH}/task.png')
        self.type_icon = resize_icon(self.type_icon, (25,25))

        ttb.Label(self.aux_frame, text=' Tipo de Actividad', font=('helvetica',13,'bold'), foreground='#222A35', compound='left',image=self.type_icon, anchor='sw').grid(row=0, column=0, columnspan=2, sticky='nsew', padx=4, pady=(0,6))

        taskType = ttb.Entry(self.aux_frame, bootstyle='dark')
        taskType.insert(0, self.__ACTIVITY.get_type())
        taskType.config( state='readonly')
        taskType.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=4, pady=(0,12))

        self.description_icon = Image.open(f'{IMG_PATH}/description.png')
        self.description_icon = resize_icon(self.description_icon, (25,25))

        ttb.Label(self.aux_frame, text=' Descripcion', font=('helvetica',13,'bold'), foreground='#222A35', compound='left',image=self.description_icon, anchor='sw').grid(row=2, column=0, columnspan=2, sticky='nsew', padx=4, pady=(0,6))

        descriptionEntry = ttb.Text(self.aux_frame, height=4)
        descriptionEntry.insert('1.0', self.__ACTIVITY.description)
        descriptionEntry.config( state='disabled')
        descriptionEntry.grid(row=3, column=0, columnspan=2, sticky='nsew', padx=4, pady=(0,12))

        self.clientc_icon = Image.open(f'{IMG_PATH}/clientc.png')
        self.clientc_icon = resize_icon(self.clientc_icon, (25,25))

        ttb.Label(self.aux_frame, text=' Clientes', font=('helvetica',13,'bold'), foreground='#222A35', compound='left',image=self.clientc_icon, anchor='sw').grid(row=4, column=0, columnspan=2, sticky='nsew', padx=4, pady=(0,6))

        clientEntry = ttb.Entry(self.aux_frame, bootstyle='dark')
        clientEntry.grid(row=5, column=0, columnspan=2, sticky='nsew', padx=4, pady=(0,12))
        clientEntry.insert(0, self.__ACTIVITY.get_client())
        clientEntry.config( state='readonly')

        self.date_act_icon = Image.open(f'{IMG_PATH}/date_act.png')
        self.date_act_icon = resize_icon(self.date_act_icon, (25,25))

        ttb.Label(self.aux_frame, text=' Fecha', font=('helvetica',13,'bold'), foreground='#222A35', compound='left',image=self.date_act_icon, anchor='sw').grid(row=6, column=0, sticky='nsew', padx=4, pady=(0,6))

        dateEntry = ttb.Entry(self.aux_frame, bootstyle='dark', justify='center')
        dateEntry.grid(row=7, column=0, sticky='nsew', padx=4, pady=(0,12))
        dateEntry.insert(0, self.__ACTIVITY.start_date)
        dateEntry.config( state='readonly')

        self.stage_icon = Image.open(f'{IMG_PATH}/stage.png')
        self.stage_icon = resize_icon(self.stage_icon, (25,25))

        ttb.Label(self.aux_frame, text=' Estado', font=('helvetica',13,'bold'), foreground='#222A35', compound='left',image=self.stage_icon, anchor='sw').grid(row=6, column=1, sticky='nsew', padx=4, pady=(0,6))

        stageEntry = ttb.Entry(self.aux_frame, bootstyle='dark', justify='center')
        stageEntry.grid(row=7, column=1, sticky='nsew', padx=4, pady=(0,12))
        stageEntry.insert(0, self.__ACTIVITY.get_stage())
        stageEntry.config( state='readonly')

        self.marker_icon = Image.open(f'{IMG_PATH}/marker.png')
        self.marker_icon = resize_icon(self.marker_icon, (25,25))

        ttb.Label(self.aux_frame, text=' Ubicacion', font=('helvetica',13,'bold'), foreground='#222A35', compound='left',image=self.marker_icon, anchor='sw').grid(row=8, column=0, columnspan=2, sticky='nsew', padx=4, pady=(0,6))

        addressEntry = ttb.Entry(self.aux_frame, bootstyle='dark')
        addressEntry.grid(row=9, column=0, columnspan=2, sticky='nsew', padx=4, pady=(0,12))

        self.machinery_icon = Image.open(f'{IMG_PATH}/machinery.png')
        self.machinery_icon = resize_icon(self.machinery_icon, (25,25))
    
        self.check_list()
        ttb.Frame(self.content, bootstyle='primary', height=2).grid(row=2, column=0, padx=(6,21), pady=(0,6), sticky='nsew')



    def check_list(self):
        ttb.Label(self.aux_frame, text=' Lisado de Items', font=('helvetica',13,'bold'), foreground='#222A35', compound='left',image=self.machinery_icon, anchor='sw').grid(row=10, column=0, columnspan=2, sticky='nsew', padx=4, pady=(0,6))

        grid = ttb.Frame(self.aux_frame, relief='solid', border=1, style='grid.TFrame', height=10)
        grid.grid(row=11, column=0, columnspan=2, sticky='nsew', ipady=1)
        grid.anchor('nw')
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        grid.columnconfigure(2, weight=1)

        if self.__ACTIVITY.type == 1:
            ttb.Label(grid, text='Id', font=(GUI_FONT,11,'bold'), bootstyle='primary inverse', padding=5).grid(row=0, column=0, padx=(0,1), sticky='nsew')

            ttb.Label(grid, text='Equipo/Maquinaria', font=(GUI_FONT,11,'bold'), bootstyle='primary inverse', padding=5).grid(row=0, column=1, padx=(1,1), sticky='nsew')

            ttb.Label(grid, text='Status', font=(GUI_FONT,11,'bold'), bootstyle='primary inverse', padding=5).grid(row=0, column=2, padx=(1,0), sticky='nsew')

            ttb.Separator(grid, orient='horizontal').grid(row=1, column=0, columnspan=3, pady=(0,6))

            for x in range(2,6):
                ttb.Label(grid, text=f'R0-{x-1}', font=(GUI_FONT,11,), bootstyle='primary', padding=5).grid(row=x, column=0, padx=(2), sticky='nsew', pady=(0,8))

                ttb.Label(grid, text='Filtro mrw - 5 uni', font=(GUI_FONT,11,), bootstyle='primary', padding=5).grid(row=x, column=1, padx=(2), sticky='nsew', pady=(0,8))

                ttb.Label(grid, text='Disponible', font=(GUI_FONT,11,'bold'), style='dispo.TLabel', padding=5, relief='solid', borderwidth=1, anchor='center').grid(row=x, column=2, padx=(8), sticky='nsew', pady=(0,8))

            ttb.Label(grid, text=f'R0-{x-1}', font=(GUI_FONT,11,'bold'), bootstyle='primary', padding=5).grid(row=6, column=0, padx=(2), sticky='nsew', pady=(0,8))

            ttb.Label(grid, text='Filtro mrw - 5 uni', font=(GUI_FONT,11,), bootstyle='primary', padding=5).grid(row=6, column=1, padx=(2), sticky='nsew', pady=(0,8))

            ttb.Label(grid, text='No Disponible', font=(GUI_FONT,11,), style='nodispo.TLabel', padding=5, relief='solid', borderwidth=1, anchor='center').grid(row=6, column=2, padx=(8), sticky='nsew', pady=(0,8))

        else:
            ttb.Label(grid, text='Id', font=(GUI_FONT,11,'bold'), bootstyle='primary inverse', padding=5).grid(row=0, column=0, padx=(0,1), sticky='nsew')

            ttb.Label(grid, text='Producto', font=(GUI_FONT,11,'bold'), bootstyle='primary inverse', padding=5).grid(row=0, column=1, padx=(1,1), sticky='nsew')

            ttb.Label(grid, text='Cantidad', font=(GUI_FONT,11,'bold'), bootstyle='primary inverse', padding=5).grid(row=0, column=2, padx=(1,0), sticky='nsew')

            ttb.Separator(grid, orient='horizontal').grid(row=1, column=0, columnspan=3, pady=(0,6))

            for x in range(2,6):
                ttb.Label(grid, text=f'R0-{x-1}', font=(GUI_FONT,11), bootstyle='primary', padding=5).grid(row=x, column=0, padx=(2), sticky='nsew', pady=(0,8))

                ttb.Label(grid, text='Filtro 23', font=(GUI_FONT,11), bootstyle='primary', padding=5).grid(row=x, column=1, padx=(2), sticky='nsew', pady=(0,8))

                ttb.Label(grid, text=x, font=(GUI_FONT,11,'bold'), foreground=GUI_COLORS['warning'], padding=5, anchor='center').grid(row=x, column=2, padx=(8), sticky='nsew', pady=(0,8))

        
    def bind(self, sequence=None, command=None, add=True):
        super().bind(sequence, command, add)
        
        


       

       
            
   
if __name__=="__main__":
    app = ttb.Window(themename='new')
    ac = Activity.findOneActivity(id=2)
    a= ActivityRow(app, activity=ac)
    a.pack(padx=10, pady=10)

    app.mainloop()
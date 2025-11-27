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
from datetime import datetime
from models.entitys.task import Task
FGCOLOR = 'white'
from models.entitys.activity import Activity

class TaskForm(ttb.Toplevel):
    def __init__(self, master=None, activity = None, callback = None, *args, **kwargs):
        super().__init__(master,background='red')
        SGDB_Style()
        
        self.minsize(width=750,height=507)
        self.title('Seleccion de Maquinaria')

        self.config(background='#D0CECE')
        self.withdraw()
        self.focus()

        self.transient()
        
        self.anchor('center')
  
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)  
        self.grab_set()

        self.callback = callback
        self.__ACTIVITY: Activity = activity
        self.__code = ttb.StringVar(value=self.__ACTIVITY.id)
        self.__BudgetCode = ttb.StringVar(value=f"{'0'*(6-len(str(self.__ACTIVITY.budget_code)))+str(self.__ACTIVITY.budget_code)}")
        self.__description = ttb.StringVar(value=self.__ACTIVITY.description)
        self.__rif = ttb.StringVar(value=self.__ACTIVITY.client)
        self.__client = ttb.StringVar(value=self.__ACTIVITY.get_client()[0])
        self.__address = ttb.StringVar(value=self.__ACTIVITY.address)

        self.create_widgets()
        self.place_window_center()
        self.deiconify()
        

    def create_widgets(self):
        contentFrame = CTkFrame(self, fg_color='white',border_width=1,  border_color='#CFCFCF')
        contentFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=10, pady=10)
        contentFrame.columnconfigure(0, weight=1)
        contentFrame.rowconfigure(1, weight=1)        

        self.__services_icon = resize_icon(Image.open(f"{IMG_PATH}/task_icon.png"))


        titleFrame = CTkFrame(contentFrame, fg_color=GUI_COLORS['primary'])
        titleFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=8, pady=(8,0))
        ttb.Label(titleFrame, image=self.__services_icon, compound='left', text='  Gestor de Tareas', font=(GUI_FONT, 14, 'bold'), foreground='white', background=GUI_COLORS['primary']).grid(row=0,column=0, padx=10, pady=10, sticky='nsew')


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



        closeimg = Image.open(f"{IMG_PATH}/closen.png")
        self.closeimg = ImageTk.PhotoImage(closeimg.resize(resize_image(20, closeimg.size)))
        closeimgh = Image.open(f"{IMG_PATH}/closeh.png")
        self.closeimgh = ImageTk.PhotoImage(closeimgh.resize(resize_image(20, closeimgh.size)))
        closeimgp = Image.open(f"{IMG_PATH}/closep.png")
        self.closeimgp = ImageTk.PhotoImage(closeimgp.resize(resize_image(20, closeimgp.size)))
        self.closeBTN = ButtonImage(buttonss_section_frame, image=self.closeimg, img_h=self.closeimgh, command=self.destroy, img_p=self.closeimgp, style='flatw.light.TButton', text='CERRAR', compound='center',padding=0)
        self.closeBTN.grid(row=0, column=0, sticky='nsew', pady=2, padx=(0,4))



        processimg = Image.open(f"{IMG_PATH}/registrar.png")
        self.processimg = ImageTk.PhotoImage(processimg.resize(resize_image(20, processimg.size)))
        processimgh = Image.open(f"{IMG_PATH}/registrarh.png")
        self.processimgh = ImageTk.PhotoImage(processimgh.resize(resize_image(20, processimgh.size)))
        processimgp = Image.open(f"{IMG_PATH}/registrarp.png")
        self.processimgp = ImageTk.PhotoImage(processimgp.resize(resize_image(20, processimgp.size)))

        self.processBTN = ButtonImage(buttonss_section_frame, command=self.process_activity, image=self.processimg, img_h=self.processimgh, img_p=self.processimgp, style='flatw.light.TButton', text='PROCESAR', compound='center',padding=0)
        self.processBTN.grid(row=0, column=2, sticky='nsew', pady=2, padx=(0,4))

        self.create_othersWidgets()
        self.__set_tasks()

    def create_othersWidgets(self):
            
        task_list_frame = tk.Frame(master=self.mainContent, width=800, height=600)
        task_list_frame.configure(background='#fff')
        task_list_frame.grid(row=1, column=0, padx=10, pady=(5,10), sticky='nsew')
        task_list_frame.columnconfigure(0, weight=1)
        task_list_frame.rowconfigure(4, weight=1)

        codeFrame = ttb.Frame(task_list_frame, style='white.TFrame')
        codeFrame.grid(row=0, column=0, sticky='nsew', padx=4, pady=(0,0))
        codeFrame.columnconfigure(1, weight=1)

      
        ttb.Label(codeFrame, text='ID:', bootstyle='dark', background="#fff", foreground=GUI_COLORS['dark'], font=('arial',12,'bold'), justify='center', anchor='w').grid(row=0, column=0, sticky='nsw', padx=(0,20),pady=5)
        
        ttb.Entry(codeFrame, state='readonly', textvariable=self.__code, justify='center').grid(row=1, column=0, sticky='nsew', padx=(1,20))


        ttb.Label(codeFrame, text='Cotizacion Vinculada:', bootstyle='dark', background="#fff", foreground=GUI_COLORS['dark'], font=('arial',12,'bold'), justify='center', anchor='w').grid(row=0, column=1, sticky='nsw', padx=5,pady=5)
        
        ttb.Entry(codeFrame, state='readonly', textvariable=self.__BudgetCode, justify='center').grid(row=1, column=1, sticky='nsew', padx=(5,1),)


        description_label = ttb.Label(codeFrame, 
                                      anchor='w', 
                                      text='Descripcion', 
                                      bootstyle='dark', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        description_label.grid(row=2, column=0, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew', columnspan=2)


        self.descriptionEntry = ttb.Text(codeFrame, height=2)
        self.descriptionEntry.grid(row=3, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=4, columnspan=2)
        self.descriptionEntry.insert('1.0', self.__description.get())
        self.descriptionEntry.config(state='disabled')
        self.descriptionEntry.config(background='#D3D6DF', highlightbackground=GUI_COLORS['info'], highlightthickness=1)

        ttb.Label(codeFrame, text='RIF:', bootstyle='dark', background="#fff", foreground=GUI_COLORS['dark'], font=('arial',12,'bold'), justify='center', anchor='w').grid(row=4, column=0, sticky='nsw', padx=(0,20),pady=5)
        
        ttb.Entry(codeFrame, state='readonly', textvariable=self.__rif, justify='center').grid(row=5, column=0, sticky='nsew', padx=(1,20))


        ttb.Label(codeFrame, text='Cliente:', bootstyle='dark', background="#fff", foreground=GUI_COLORS['dark'], font=('arial',12,'bold'), justify='center', anchor='w').grid(row=4, column=1, sticky='nsw', padx=5,pady=5)
        
        ttb.Entry(codeFrame, state='readonly', textvariable=self.__client, justify='center').grid(row=5, column=1, sticky='nsew', padx=(5,1),)


        address_label = ttb.Label(codeFrame, 
                                      anchor='w', 
                                      text='Direcciones', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        address_label.grid(row=7, column=0, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew', columnspan=2)


        self.addressEntry = ttb.Text(codeFrame, height=3)
        self.addressEntry.grid(row=8, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=4, columnspan=2)
        self.addressEntry.insert('1.0', self.__address.get())
        self.addressEntry.config(state='disabled')
        self.addressEntry.config(background='#D3D6DF', highlightbackground=GUI_COLORS['info'], highlightthickness=1)



        ttb.Separator(task_list_frame, bootstyle='dark').grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

        miniTitle = CTkFrame(task_list_frame, fg_color=GUI_COLORS['dark'], corner_radius=4)
        miniTitle.grid(row=3, column=0, padx=4, pady=(0,8), sticky='nsew')
        ttb.Label(miniTitle, text='TAREAS',  font=('arial',14,'bold'), background=GUI_COLORS['dark'], foreground='white', padding=10).grid(row=0, column=0, padx=4,pady=4, sticky='w')

        self.scroll_frame_content = ScrolledFrame(task_list_frame, style='white.TFrame', bootstyle='round dark')
        self.scroll_frame_content.grid(row=4, column=0, sticky='nsew', padx=4)
        self.scroll_frame_content.columnconfigure(0, weight=3)
        self.scroll_frame_content.columnconfigure(1, weight=3)
        self.scroll_frame_content.columnconfigure(2, weight=1)
        self.scroll_frame_content.columnconfigure(3, weight=1)

        ttb.Label(self.scroll_frame_content, background='#fff', justify='center', text=f'Tipo', font=('arial',11,'bold'),).grid(row=0, column=0, sticky='nsew')

        ttb.Label(self.scroll_frame_content, background='#fff', justify='center', text=f'Descripcion', font=('arial',11,'bold'),).grid(row=0, column=1, sticky='nsew')

        ttb.Label(self.scroll_frame_content, background='#fff', justify='center', text=f'Cantidad', font=('arial',11,'bold'),).grid(row=0, column=2, sticky='')

        ttb.Label(self.scroll_frame_content, background='#fff', justify='center', text=f'Estado', anchor='center', font=('arial',11,'bold'),).grid(row=0, column=3, sticky='nsew',padx=(0,18))

        ttb.Separator(self.scroll_frame_content, bootstyle='dark').grid(row=1, column=0, columnspan=4, pady=(10,10), padx=(0,18),sticky='nsew')
 

        self.variables = []
        self.checkboxes = []

    def change_task_state(self,index, idT):
            DB.update_task(idT=idT,state=self.variables[index].get())
            self.check_activit_progress()

    
    def check_activit_progress(self):
            if 0 not in [x.get() for x in self.variables]:
                self.processBTN.config(state='normal')
            else:
                self.processBTN.config(state='disabled')

    def process_activity(self):
        ask = messagebox.askquestion(title='Confirmacion', message='Desea Procesar esta Actividad?', parent=self)
        if ask == 'yes':
            self.callback()
            self.destroy()

    def __set_tasks(self):
        tasks = self.__ACTIVITY.get_tasks()
        if tasks:
            for index, task in enumerate(tasks):
                newTask = Task(**task)
                #ttb.Label(self.cont, text=f'Task #{index+1}', font=('arial',11,'bold'), foreground=GUI_COLORS['danger'], padding=5, ).grid(row=index*2+2, column=0, sticky='nsew',padx=5,pady=5)
                ttb.Label(self.scroll_frame_content, background='#fff', justify='center', text=f'{newTask.get_type()}', font=('arial',11),).grid(row=index*2+2, column=0, sticky='nsew')

                ttb.Label(self.scroll_frame_content, background='#fff', text=f'{newTask.get_description()}',width=30, font=('arial',11),).grid(row=index*2+2, column=1, sticky='nsew')

                ttb.Label(self.scroll_frame_content, background='#fff', justify='center', text=f'{newTask.amount}', font=('arial',11),).grid(row=index*2+2, column=2, sticky='')

                state_var = ttb.IntVar(value=newTask.complete)# Variable para almacenar el estado del checkbox (1 para marcado, 0 para desmarcado)
                
                if newTask.item_type == 1:
                     text_check = 'Ejecutado'
                else:
                     text_check = 'Entregado'


                checkButton = ttk.Checkbutton(self.scroll_frame_content, text=text_check, style='custom.success.TCheckbutton', onvalue=1, offvalue=0, variable=state_var, command=lambda index=index, idT=newTask.id: self.change_task_state(index,idT))
                
                # Agregar la variable a la lista de self.variables y el Checkbutton a la lista de Checkbuttons
                self.variables.append(state_var)
                self.checkboxes.append(checkButton)
                
                checkButton.grid(row=index*2+2, column=3, sticky='', padx=(0,26))

                ttb.Separator(self.scroll_frame_content, bootstyle='light').grid(row=index*2+3, column=0, columnspan=4, padx=(0,18),pady=(10,15),sticky='nsew')
 
            self.check_activit_progress()

        
# app =ttb.Window(themename='new')
# ac = Activity.findOneActivity(id=1)

# TaskForm(app, activity=ac)

# app.mainloop()
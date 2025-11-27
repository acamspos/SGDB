import ttkbootstrap as ttb
from assets.globals import GUI_COLORS, IMG_PATH, GUI_FONT
from assets.utils import resize_image, resize_icon
from PIL import Image, ImageTk
from tkinter import messagebox
import tkinter as tk
from components.buttons import ButtonImage
from models.entitys.activity import Activity
from customtkinter import CTkFrame #767171
from tkinter import ttk
from datetime import datetime
from pages.Machinery.views.machinery_search import MachinerySelection
from models.entitys.machinery import Machinery
from models.entitys.activity import Activity
FGCOLOR = 'white'


class StartActivityForm(ttb.Toplevel):
    def __init__(self, master=None, activity = None, callback = None):
        super().__init__(master)
        self.withdraw()
       
        
        self.callback = callback
        self.__ACTIVITY: Activity = activity

        self.code_var = ttb.StringVar(value=f"{'0'*(6-len(str(self.__ACTIVITY.budget_code)))+str(self.__ACTIVITY.budget_code)}")
        self.description_var = ttb.StringVar(value=self.__ACTIVITY.description)
        self.client_var = ttb.StringVar(value=self.__ACTIVITY.get_client()[0])
        self.addres_var = ttb.StringVar(value=self.__ACTIVITY.address)
        self.__startDate = ttb.StringVar(value=datetime.today().strftime('%d/%m/%Y'))
        self.__finalDate = ttb.StringVar(value=self.__ACTIVITY.final_date.strftime('%d/%m/%Y'))

        self.create_widgets()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)  
        self.grab_set()
        self.transient()
        self.focus()
        self.anchor('center')
        self.title('Detalles de Actividad')
        self.place_window_center()
    
        self.deiconify()
        

    def create_widgets(self):
        contentFrame = CTkFrame(self, fg_color='white',border_width=1,  border_color='#CFCFCF')
        contentFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=10, pady=10)

        self.__services_icon = resize_icon(Image.open(f"{IMG_PATH}/project.png"))

        titleFrame = CTkFrame(contentFrame, fg_color=GUI_COLORS['primary'])
        titleFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=8, pady=(8,0))
        ttb.Label(titleFrame, image=self.__services_icon, compound='left', text=' Detalles de la Actividad', font=(GUI_FONT, 14, 'bold'), foreground='white', background=GUI_COLORS['primary']).grid(row=0,column=0, padx=10, pady=10, sticky='nsew')


        self.mainContent = tk.Frame(contentFrame)
        self.mainContent.config(background=FGCOLOR)
        self.mainContent.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        self.mainContent.columnconfigure(0, weight=1)
        self.mainContent.rowconfigure(0, weight=1)


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


        creatbtnimg = Image.open(f"{IMG_PATH}/editn.png")
        self.creatbtnimg = ImageTk.PhotoImage(creatbtnimg.resize(resize_image(20, creatbtnimg.size)))
        creatbtnimgh = Image.open(f"{IMG_PATH}/edith.png")
        self.creatbtnimgh = ImageTk.PhotoImage(creatbtnimgh.resize(resize_image(20, creatbtnimgh.size)))
        creatbtnimgp = Image.open(f"{IMG_PATH}/editp.png")
        self.creatbtnimgp = ImageTk.PhotoImage(creatbtnimgp.resize(resize_image(20, creatbtnimgp.size)))

        self.createBTN = ButtonImage(buttonss_section_frame, command=self.__start_activity, image=self.creatbtnimg, img_h=self.creatbtnimgh, img_p=self.creatbtnimgp, style='flatw.light.TButton', text='INICIAR', compound='center',padding=0)
        self.createBTN.grid(row=0, column=2, sticky='nsew', pady=2, padx=(0,4))

        self.__form()
        
        

    def __form(self):
        mainInforFrame = tk.Frame(self.mainContent)
        mainInforFrame.config(background=FGCOLOR)
        mainInforFrame.grid(row=0, column=0, sticky='nsew', pady=(0,2))
        mainInforFrame.columnconfigure(1, weight=1)

        code_label = ttb.Label(mainInforFrame, 
                                      anchor='w', 
                                      text='Codigo', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        code_label.grid(row=0, column=0, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.codeEntry = ttb.Entry(mainInforFrame, 
                                       width=20, state='readonly',
                                       textvariable=self.code_var
                                      )
        self.codeEntry.grid(row=1, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=4, columnspan=1)


        client_label = ttb.Label(mainInforFrame, 
                                      anchor='w', 
                                      text='Cliente', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        client_label.grid(row=0, column=1, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.clientEntry = ttb.Entry(mainInforFrame, 
                                        state='readonly',
                                        textvariable=self.client_var
                                      )
        self.clientEntry.grid(row=1, column=1, sticky='nsew',pady=(2,0),padx=4, ipady=4, columnspan=1)



        
    

        moreInfoFrame = tk.Frame(mainInforFrame)
        moreInfoFrame.config(background=FGCOLOR)
        moreInfoFrame.grid(row=2, column=0, sticky='nsew', columnspan=2)
        moreInfoFrame.columnconfigure(0, weight=1)
     

        description_label = ttb.Label(moreInfoFrame, 
                                      anchor='w', 
                                      text='Descripcion', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        description_label.grid(row=0, column=0, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')


        self.descriptionEntry = ttb.Text(moreInfoFrame, height=1)
        self.descriptionEntry.grid(row=1, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=4)
        self.descriptionEntry.insert('1.0', self.description_var.get())
        self.descriptionEntry.config(state='disabled')
        self.descriptionEntry.config(background='#D3D6DF')

        adress_entry = ttb.Label(moreInfoFrame, 
                                      anchor='w', 
                                      text='Direccion', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        adress_entry.grid(row=2, column=0, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.addressEntry = ttb.Text(moreInfoFrame, height=1)
        self.addressEntry.grid(row=3, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=4)
        self.addressEntry.insert('1.0', self.addres_var.get())
        self.addressEntry.config(state='disabled')
        self.addressEntry.config(background='#D3D6DF')


        date_label = ttb.Label(mainInforFrame, 
                                      anchor='w', 
                                      text='Fecha de Inicio', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        date_label.grid(row=3, column=0, columnspan=2, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.start_dateEntry = ttb.Entry(mainInforFrame, state='readonly', textvariable=self.__startDate)
        self.start_dateEntry.grid(row=4, column=0, columnspan=2, sticky='nsew',pady=(2,0),padx=4, ipady=0,)


        date_label = ttb.Label(mainInforFrame, 
                                      anchor='w', 
                                      text='Fecha de Culminación', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        date_label.grid(row=5, column=0, columnspan=2, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.end_dateEntry = ttb.Entry(mainInforFrame, state='readonly', textvariable=self.__finalDate)
        self.end_dateEntry.grid(row=6, column=0, columnspan=2, sticky='nsew',pady=(2,0),padx=4, ipady=0,)


        equipmentFrame = tk.Frame(mainInforFrame)
        equipmentFrame.config(background=FGCOLOR)
        equipmentFrame.grid(row=7, column=0, sticky='nsew', pady=(12,2),columnspan=2)
        equipmentFrame.columnconfigure(0, weight=1)

        equipment_label = ttb.Label(equipmentFrame, 
                                      anchor='w', 
                                      text='Seleccionar Equipos', 
                                      bootstyle='dark', 
                                      background=FGCOLOR,
                                      font=('arial',14,'bold'))
        equipment_label.grid(row=0, column=0, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        addroundimg = Image.open(f"{IMG_PATH}/addround.png")
        self.addroundimg = ImageTk.PhotoImage(addroundimg.resize(resize_image(12, addroundimg.size)))
        addroundimgh = Image.open(f"{IMG_PATH}/addroundh.png")
        self.addroundimgh = ImageTk.PhotoImage(addroundimgh.resize(resize_image(12, addroundimgh.size)))
        addroundimgp = Image.open(f"{IMG_PATH}/addroundp.png")
        self.addroundimgp = ImageTk.PhotoImage(addroundimgp.resize(resize_image(12, addroundimgp.size)))

        self.addBTN = ButtonImage(equipmentFrame,  command=lambda:MachinerySelection(self, callback=self.__set_machinery,selectionMode=True, machinery_filter = 1), image=self.addroundimg, img_h=self.addroundimgh, img_p=self.addroundimgp, style='flatw.light.TButton', padding=0)
        self.addBTN.grid(row=0, column=1, sticky='nsew', pady=2, padx=(0,4))


        removeroundimg = Image.open(f"{IMG_PATH}/removeround.png")
        self.removeroundimg = ImageTk.PhotoImage(removeroundimg.resize(resize_image(12, removeroundimg.size)))
        removeroundimgh = Image.open(f"{IMG_PATH}/removeroundh.png")
        self.removeroundimgh = ImageTk.PhotoImage(removeroundimgh.resize(resize_image(12, removeroundimgh.size)))
        removeroundimgp = Image.open(f"{IMG_PATH}/removeroundp.png")
        self.removeroundimgp = ImageTk.PhotoImage(removeroundimgp.resize(resize_image(12, removeroundimgp.size)))

        self.removeBTN = ButtonImage(equipmentFrame, command=self.__remove_machinery,  image=self.removeroundimg, img_h=self.removeroundimgh, img_p=self.removeroundimgp, style='flatw.light.TButton', padding=0)
        self.removeBTN.grid(row=0, column=2, sticky='nsew', pady=2, padx=(0,4))

        grid_frame = tk.Frame(equipmentFrame,)
        grid_frame.config(background='#fff')
        grid_frame.grid(row=1, column=0, columnspan=3, padx=2, pady=(0,10), sticky='nsew')
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.rowconfigure(0, weight=1)

        columns = ('Codigo', 'Descripcion', 'Modelo')

        yscroll = ttb.Scrollbar(grid_frame, 
                                orient='vertical',
                                bootstyle="dark-round")
        yscroll.grid(row=0, column=1, padx=(1,0), pady=2,sticky='ns', rowspan=2)

        xscroll = ttb.Scrollbar(grid_frame, 
                                orient='horizontal',
                                bootstyle="dark-round")
        xscroll.grid(row=1, column=0, padx=1, pady=2,sticky='ew')

        self.machineryGridview = ttb.Treeview(grid_frame,columns=columns,show='headings', bootstyle='dark',
                                 height=4,  xscrollcommand=xscroll.set,
                                selectmode='extended', yscrollcommand=yscroll.set)
        self.machineryGridview.grid(row=0,column=0,padx=(0,2),pady=(2,2),sticky='nsew')

        yscroll.configure(command=self.machineryGridview.yview)
        xscroll.configure(command=self.machineryGridview.xview)

        self.machineryGridview.heading('Codigo',text='Codigo', anchor='w')
        self.machineryGridview.heading('Descripcion',text='Descripcion', anchor='w')
        self.machineryGridview.heading("Modelo", text='Modelo', anchor='w')
      

        self.machineryGridview.column(columns[0],width=150,stretch=False,anchor='w')
        self.machineryGridview.column(columns[1],width=300,stretch=True, minwidth=300,anchor='w')
        self.machineryGridview.column(columns[2],width=150,stretch=False,anchor='w')

    def __set_machinery(self, machinery):
        self.machineryGridview.insert("",
                text=1,
                index=ttb.END,
                values=(machinery.code, machinery.description, machinery.get_model()),
        )


    def __remove_machinery(self):
        selected = self.machineryGridview.focus()
        if selected:  
            ask = messagebox.askquestion('Confirmacion','Desea remover el equipo?', parent=self)
            if ask == 'yes':
                
                self.machineryGridview.delete(selected)
     
            
        



    def __start_activity(self):
        START_DATE = datetime.strptime(self.start_dateEntry.get(), '%d/%m/%Y')
        FINAL_DATE = datetime.strptime(self.end_dateEntry.get(), '%d/%m/%Y')

        if START_DATE < FINAL_DATE:

            self.__ACTIVITY.update_date(START_DATE,FINAL_DATE)

            for item in self.machineryGridview.get_children():
                data = self.machineryGridview.item(item, 'values')[0]
                machinery = Machinery.findOneMachinery(data)
                machinery.enable()
                self.__ACTIVITY.add_machinery(data)
            self.callback()
            self.destroy()
            messagebox.showinfo('Aviso','Actividad Iniciada Satisfactoriamente!')
            del self
        else:
            messagebox.showwarning("Fecha",'Existe discrepancias en las fechas seleccionadas.')




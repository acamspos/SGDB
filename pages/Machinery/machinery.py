import ttkbootstrap as ttb
from assets.globals import GUI_COLORS, IMG_PATH, GUI_FONT
from assets.utils import resize_icon, resize_image
from assets.globals import invoice_icon, budget_icon, project_icon, refresh_icon
from components.dcards import DashboardCard
from components.buttons import ButtonImage
from PIL import Image, ImageTk
from customtkinter import CTkFrame, CTkLabel
import tkinter as tk
from assets.styles.styles import SGDB_Style
from components.bcards import BCards
###### GRAPH LIBRARIES

from models.entitys.machinery import Machinery
from pages.Machinery.views.machinary_form import MachinaryForm
from tkinter import messagebox
import assets.globals as constGlobal

class MachineryPage(ttb.Frame):
    def __init__(self, master=None):
        SGDB_Style()
        super().__init__(master, height=50, width=50)
        PART_COLOR = GUI_COLORS['bg']
        PART2_COLOR = GUI_COLORS['warning']

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        ########## GUI ICONSr##########
        self.__dash_icon = Image.open(f'{IMG_PATH}/machinery_title.png')
        self.__dash_icon = ImageTk.PhotoImage(self.__dash_icon.resize(resize_image(10, self.__dash_icon.size)))
        self.__refresh_icon = resize_icon(refresh_icon)
        self.__bill_icon = resize_icon(invoice_icon)
        self.__budget_icon = resize_icon(budget_icon)
        self.__project_icon = resize_icon(project_icon)

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
                               text=' Maquinaria', 
                                padding='0 0',
                               background='#212946',
                               font=('arial',15, 'bold'), 
                               foreground='#fff')
        page_title.grid(row=0, column=0, sticky='nsew',padx=(80,0))

        reportBTN = Image.open(f"{IMG_PATH}/report.png")
        self.reportBTN = ImageTk.PhotoImage(reportBTN.resize(resize_image(25, reportBTN.size)))

        
        reporthBTN = Image.open(f"{IMG_PATH}/reporth.png")
        self.reporthBTN = ImageTk.PhotoImage(reporthBTN.resize(resize_image(25, reporthBTN.size)))

        ButtonImage(frame_title, image=self.reportBTN,style='flat.light.TButton', padding=0).grid(row=0, column=1, sticky='nsew', pady=2, padx=6)

        reportpBTN = Image.open(f"{IMG_PATH}/reportp.png")
        self.reportptBTN = ImageTk.PhotoImage(reportpBTN.resize(resize_image(25, reportpBTN.size)))

        ButtonImage(frame_title, image=self.reportBTN, img_h=self.reporthBTN, img_p=self.reportptBTN,style='flat.light.TButton', padding=0).grid(row=0, column=1, sticky='nsew', pady=2, padx=6)

        ttb.Separator(self, orient='horizontal',bootstyle='dark').grid(row=1, column=0, sticky='nsew',padx=20)

        ######### PAGE CONTENT #########
        self.numRecords = ttb.IntVar(value=0)

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

        ttb.Label(subtitle, text='Inicio/Equipos', background=PART2_COLOR, font=(GUI_FONT,9), foreground='#fff').grid(row=1, column=1, sticky='nsew', padx=(4,8), pady=(0,8))

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

        self.deleteBTN = ButtonImage(buttons_frame, command=self.__delete_machinery, image=self.deletebtnimg, img_h=self.deletebtnimgh, img_p=self.deletebtnimgp, style='#D9D9D9.TButton', padding=0)
        self.deleteBTN.grid(row=0, column=4, sticky='nsew', pady=2, padx=(0,8))


        self.SEARCHENTRY = ttb.Entry(buttons_frame, bootstyle='info', width=30)
        self.SEARCHENTRY.grid(row=0,column=5, ipady=2, padx=(0,8), sticky='e')
        self.SEARCHENTRY.bind('<Return>', lambda e: self.__findMachinery())
        
        searchbtnimg = Image.open(f"{IMG_PATH}/searchbtn.png")
        self.searchbtnimg = resize_icon(searchbtnimg, (50,50))

        searchbtnimgh = Image.open(f"{IMG_PATH}/searchbtnh.png")
        self.searchbtnimgh = resize_icon(searchbtnimgh, (50,50))

        searchbtnimgp = Image.open(f"{IMG_PATH}/searchbtnp.png")
        self.searchbtnimgp = resize_icon(searchbtnimgp, (50,50))

        ButtonImage(buttons_frame, image=self.searchbtnimg, img_h=self.searchbtnimgh, img_p=self.searchbtnimgp, command=self.__findMachinery, style='#D9D9D9.TButton', padding=0).grid(row=0, column=6, pady=2, padx=(0,0))

        grid_frame = tk.Frame(self.dashboard_content,)
        grid_frame.config(background='#D9D9D9')
        grid_frame.grid(row=3, column=0, columnspan=1, padx=10, pady=(0,10), sticky='nsew')
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.rowconfigure(0, weight=1)

        columns = ('code', 'description', 'brand','model','status')

        yscroll = ttb.Scrollbar(grid_frame, 
                                orient='vertical',
                                bootstyle="dark-round")
        yscroll.grid(row=0, column=1, padx=1, pady=2,sticky='ns', rowspan=2)

        xscroll = ttb.Scrollbar(grid_frame, 
                                orient='horizontal',
                                bootstyle="dark-round")
        xscroll.grid(row=1, column=0, padx=1, pady=2,sticky='ew')

        self.machineryGridView = ttb.Treeview(grid_frame,columns=columns,show='headings', style='cust.primary.Treeview',
                                 height=10, padding=0, xscrollcommand=xscroll.set,
                                selectmode='extended', yscrollcommand=yscroll.set)
        self.machineryGridView.grid(row=0,column=0,padx=2,pady=(2,2),sticky='nsew')

        yscroll.configure(command=self.machineryGridView.yview)
        xscroll.configure(command=self.machineryGridView.xview)

        self.machineryGridView.heading(columns[0],text='Codigo', anchor='w')
        self.machineryGridView.heading(columns[1],text='Descripcion', anchor='w')
        self.machineryGridView.heading(columns[2], text='Marca', anchor='w')
        self.machineryGridView.heading(columns[3], text='Modelo', anchor='w')
        self.machineryGridView.heading(columns[4], text='Status', anchor='w')
   
      

        self.machineryGridView.column(columns[0],width=150,stretch=False,anchor='w')
        self.machineryGridView.column(columns[1],width=300,stretch=True, minwidth=450,anchor='w')
        self.machineryGridView.column(columns[2],width=150,stretch=False,anchor='w')
        self.machineryGridView.column(columns[3],width=150,stretch=False,anchor='w')
        self.machineryGridView.column(columns[4],width=150,stretch=False,anchor='w')
        self.machineryGridView.bind('<<TreeviewSelect>>', lambda e: self.__enabled_view())

        

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

        ttb.Label(budgetsStateFrame, text='Equipos', font=(GUI_FONT,13,'bold'), 
                  foreground='#fff', background='#212946', anchor='w'
                ).grid(row=0, column=0, sticky='nsew', padx=20,pady=(15,5))
        
        self.r_i = resize_icon(Image.open(f'{IMG_PATH}/refresh_b.png'))
        self.r_i_h = resize_icon(Image.open(f'{IMG_PATH}/refresh_b_h.png'))

        refresh = ButtonImage(budgetsStateFrame, compound='left',  style='212946.TButton', 
                   padding=0, image=self.r_i,
                   img_h=self.r_i_h, img_p=self.r_i)
        refresh.grid(row=0, column=0, pady=(20,5), padx=20, sticky='ne')

        self.availableMachineryList = tk.Frame(budgetsStateFrame)
        self.availableMachineryList.grid(row=1, column=0, sticky='nsew', padx=20,pady=(10,10))
        self.availableMachineryList.columnconfigure(0, weight=1)
        self.availableMachineryList.config(background='#212946')

        

        ttb.Label(self.availableMachineryList, text='Descipcion',  background='#212946', font=(GUI_FONT,11,'bold'),foreground='white').grid(row=0, column=0, sticky='nsew')
        ttb.Label(self.availableMachineryList, text='Status',  background='#212946', font=(GUI_FONT,11,'bold'),foreground='white', anchor='center').grid(row=0, column=1, sticky='nsew')

        ttb.Separator(self.availableMachineryList, bootstyle='danger').grid(row=1, column=0, sticky='nsew', columnspan=2, pady=(0,8))

        self.machineryList = tk.Frame(self.availableMachineryList)
        self.machineryList.config(background='#212946')
        self.machineryList.grid(row=2, column=0, sticky='nsew', padx=2,pady=(0,10), columnspan=2)
        self.machineryList.columnconfigure(0, weight=1)
    
        self.bind("<Map>",lambda e: self.update_pages())

    def update_pages(self):
        self.__findMachinery()
        self.set_privileges()
      
    
    def set_privileges(self):
        if constGlobal.loggued_user.rol == 1:
            self.deleteBTN.grid(row=0, column=4, sticky='nsew', pady=2, padx=(0,8))
        else:
            self.deleteBTN.grid_forget()
    #################### METHODS #######################

    def __set_machinery_status_list(self):
        for wid in self.machineryList.winfo_children():
            wid.destroy()
        machinery = Machinery.getMachineryNotAvailable()
        if machinery:
            for index, machinery in enumerate(machinery):
                ttb.Label(self.machineryList, text=machinery['code'], anchor='w', foreground='#fff', background='#212946', font=(GUI_FONT,10,'bold')).grid(row=index*2, column=0, sticky='nsew', padx=(4,6), pady=(0,4))
                if int(machinery['status']) == 3:
                    ttb.Label(self.machineryList, text='No disponible', foreground=GUI_COLORS['danger'],
                            background='#212946', font=(GUI_FONT,10,'bold')).grid(row=index*2, column=1, padx=(0,6), pady=(0,4))
                else:
                    ttb.Label(self.machineryList, text="En Uso", foreground=GUI_COLORS['success'],
                            background='#212946', font=(GUI_FONT,10,'bold')).grid(row=index*2, column=1, padx=(0,6), pady=(0,4))
                ttb.Frame(self.machineryList, height=1, bootstyle='info').grid(row=index*2+1, column=0, padx=12, columnspan=2, sticky='nsew', pady=(0,10))




    def __delete_machinery(self):
        ask = messagebox.askquestion('Eliminar', 'Desea eliminar el registro del Equipo?', parent=self)
        if ask == 'yes':
            machinery = self.__get_selected_machinery()
            machinery.delete()
            del machinery
            messagebox.showinfo('Aviso','Equipo Eliminado satisfactoriamente.', parent=self)
            self.__findMachinery()

    def __open_create_form(self):
        ask = messagebox.askquestion('Registrar','Desea crear un nuevo Equipo?', parent=self)
        if ask == 'yes':
            waitwindow = MachinaryForm(self, window_type='create', title='Registrar Equipo',)
            waitwindow.wait_window()
            self.__findMachinery()


    def __open_edit_form(self):
            machinery = self.__get_selected_machinery()
            if machinery:
                ask = messagebox.askquestion('Modificar','Desea modificar el registro seleccionado?', parent=self)
                if ask == 'yes':
                    waitwindow = MachinaryForm(self, window_type='edit', title='Modificar Equipo', machinery=machinery)
                    waitwindow.wait_window()
                    self.__findMachinery()
            del machinery

    def __get_selected_machinery(self,) -> Machinery:
        selected = self.machineryGridView.focus()
        if selected:
            code = self.machineryGridView.item(selected, 'values')[0]
            return Machinery.findOneMachinery(code)


    def __open_view_form(self):
        machinery = self.__get_selected_machinery()
        if machinery:
            MachinaryForm(self, window_type='view', title='Detalles del Equipo', machinery=machinery)
        del machinery

    
    def __findMachinery(self):
        self.machineryGridView.delete(*self.machineryGridView.get_children())
        machinerys = Machinery.findAllMachinerys(name=self.SEARCHENTRY.get())
        
        if machinerys:
            for machinery in machinerys:
                mach = Machinery(**machinery)
                self.machineryGridView.insert("",
                                ttb.END,
                                values=(mach.code,mach.description,mach.get_brand(),mach.get_model(),mach.get_status()), tags='row')
        del machinerys
        self.numRecords.set(Machinery.countRecords())
        self.__set_machinery_status_list()


    def __enabled_view(self):
        if self.machineryGridView.selection()!= ():
            self.viewBTN.config(state='normal')
            self.editBTN.config(state='normal')
            self.deleteBTN.config(state='normal')
        else:
            self.viewBTN.config(state='disabled')
            self.editBTN.config(state='disabled')
            self.deleteBTN.config(state='disabled')

    
    




if __name__=="__main__":
    app = ttb.Window(themename='new')
  
    SGDB_Style()
    MachineryPage(app).pack()
    app.mainloop()
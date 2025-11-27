import ttkbootstrap as ttb


from assets.globals import GUI_COLORS, GUI_FONT, IMG_PATH

from pages.Extras.subtable import SubWindowsSelection

from datetime import datetime
from tkinter import messagebox
from assets.styles.styles import SGDB_Style
from customtkinter import CTkFrame
from PIL import Image, ImageTk
from components.buttons import ButtonImage
from assets.utils import resize_icon, resize_image
import tkinter as tk
from assets.db.db_connection import DB
from models.entitys.representative import Representative
from pages.clients.clients import ClientModule






windows_type = {
    'create':"Creacion",
    'edit':"Edicion",
    'view':'Vista'
}

class RepresentativeForm(ttb.Toplevel):
    def __init__(self, master=None, window_type = 'create', title = '', representative = None):
        super().__init__(master)
        self.focus()

        
        self.window_title = title
        self.window_type = window_type

        ######### MODAL WINDOW CONFIG #########
        
        



        self.__REPRESENTATIVE: Representative = representative

        ######### VARIABLES #########
        
        self.__documentId = ttb.StringVar()
        self.__name = ttb.StringVar()
        self.__lastname = ttb.StringVar()

        self.__companydRif = ttb.StringVar()
        self.__companydName = ttb.StringVar()

        self.__department = ttb.StringVar()

        self.__phone = ttb.StringVar()
        self.__email = ttb.StringVar()


      
    
        self.__createWidgets()

        if self.__REPRESENTATIVE:
            self.__set_representative_data()


        self.title(title)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.transient()
        self.grab_set()
        self.resizable(0,0)
        self.config(background="#D9D9D9")
        self.place_window_center()
        self.iconbitmap('SIGAG.ico')
   



    
    def __createWidgets(self):
        


        FGCOLOR = 'white'

        contentFrame = CTkFrame(self, fg_color='white',border_width=1,  border_color='#CFCFCF')
        contentFrame.grid(row = 1, column = 0, sticky = 'nsew', padx=10, pady=10)

        self.__representative_icon = resize_icon(Image.open(f"{IMG_PATH}/representative.png"), icon_size=(40,40))


        titleFrame = CTkFrame(contentFrame, fg_color=GUI_COLORS['primary'])
        titleFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=8, pady=(8,0))
        ttb.Label(titleFrame, image=self.__representative_icon, background=GUI_COLORS['primary'], ).grid(row=0, column=0, rowspan=2, sticky='nsew', padx=(8,4), pady=8)

        ttb.Label(titleFrame, text=self.window_title, background=GUI_COLORS['primary'], font=(GUI_FONT,13,'bold'), foreground='#fff').grid(row=0, column=1, sticky='nsew', padx=(4,8), pady=(14,0))

        ttb.Label(titleFrame, text=f'Inicio / Representantes / {windows_type[self.window_type]}', background=GUI_COLORS['primary'], font=(GUI_FONT,9), foreground='#fff').grid(row=1, column=1, sticky='nsew', padx=10, pady=(0,14))
        machinary_content_frame = tk.Frame(contentFrame)
        machinary_content_frame.config(background=FGCOLOR)
        machinary_content_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)


            ########### Description Section ###########

        mainDataFrame = tk.Frame(machinary_content_frame)
        mainDataFrame.config(background=FGCOLOR)
        mainDataFrame.grid(row=0, column=0, sticky='nsew', pady=(0,2),padx=4)
        mainDataFrame.columnconfigure(0, weight=1)
        mainDataFrame.columnconfigure(1, weight=1)
        mainDataFrame.columnconfigure(2, weight=1)

        documentId_label = ttb.Label(mainDataFrame, 
                                      anchor='w', 
                                      text='Documento de Identidad', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        documentId_label.grid(row=0, column=0, padx=(0,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.documentIdEntry = ttb.Entry(mainDataFrame,  width=25, textvariable=self.__documentId )
        self.documentIdEntry.grid(row=1, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=4, )
        

        name_label = ttb.Label(mainDataFrame, 
                                      anchor='w', 
                                      text='Nombre', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        name_label.grid(row=0, column=1, padx=(8,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.nameEntry = ttb.Entry(mainDataFrame,  width=25, textvariable=self.__name )
        self.nameEntry.grid(row=1, column=1, sticky='nsew',pady=(2,0),padx=(8,0), ipady=4, )


        lastname_label = ttb.Label(mainDataFrame, 
                                      anchor='w', 
                                      text='Apellido', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        lastname_label.grid(row=0, column=2, padx=(8,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.lastnameEntry = ttb.Entry(mainDataFrame, 
                                       width=25,
                                      textvariable=self.__lastname)
        self.lastnameEntry.grid(row=1, column=2, sticky='nsew',pady=(2,0),padx=(8,0), ipady=4, )


        companyDataFrame = tk.Frame(machinary_content_frame)
        companyDataFrame.config(background=FGCOLOR)
        companyDataFrame.grid(row=1, column=0, padx=4, sticky='nsew', pady=(2,10))
        companyDataFrame.columnconfigure(0, weight=1)
        companyDataFrame.columnconfigure(1, weight=1)

        company_label = ttb.Label(companyDataFrame, 
                                     anchor='w', 
                                     text='Empresa', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=('arial',11,'bold'))
        company_label.grid(row=0, column=0, padx=4, pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        
        company_frame = tk.Frame(companyDataFrame)
        company_frame.config(background=FGCOLOR)
        company_frame.grid(row=1, column=0, sticky='nsew' ,pady=(4,0), columnspan=2)
        company_frame.columnconfigure(3,weight=1)

        company_frame.anchor('w')
        
        ttb.Label(company_frame, text='RIF', font=(GUI_FONT,9,'bold'), background='#fff').grid(row=0, column=0, padx=(6,0))
        

        self.rifCompanyEntry = ttb.Entry(company_frame, 
                                     textvariable=self.__companydRif,
                                     width=20, state='readonly', justify='center'
                                     )
        self.rifCompanyEntry.grid(row=0, column=1, sticky='nsew',padx=5, ipady=4,)

        if self.window_type != 'view':

            self.Company_search_btn = ttb.Button(company_frame, 
                                            command=self.__open_company_selection,
                                            text='...',
                                            bootstyle='dark')
            self.Company_search_btn.grid(row=0, column=2, padx=(2), sticky='nsew', pady=1)

        self.nameCompanyEntry = ttb.Entry(company_frame, width=45,state='readonly',
                                     textvariable=self.__companydName,
                                     )
        self.nameCompanyEntry.grid(row=0, column=3, sticky='nsew',padx=5, ipady=4,)         

        department_label = ttb.Label(companyDataFrame, 
                                     anchor='w', 
                                     text='Departamento', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=('arial',11,'bold'))
        department_label.grid(row=2, column=0, padx=4, pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
             
        self.__departmentEntry = ttb.Entry(companyDataFrame, 
                                       width=45,
                                      textvariable=self.__department)
        self.__departmentEntry.grid(row=3, column=0, sticky='nsew',pady=(2,0),padx=(8,0), ipady=4, columnspan=2 )


        phone_label = ttb.Label(companyDataFrame, 
                                     anchor='w', 
                                     text='Telefono', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=('arial',11,'bold'))
        phone_label.grid(row=4, column=0, padx=4, pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
             
        self.__phoneEntry = ttb.Entry(companyDataFrame, 
                                       width=45,
                                      textvariable=self.__phone)
        self.__phoneEntry.grid(row=5, column=0, sticky='nsew',pady=(2,0),padx=(8,0), ipady=4, )


        email_label = ttb.Label(companyDataFrame, 
                                     anchor='w', 
                                     text='Correo', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=('arial',11,'bold'))
        email_label.grid(row=4, column=1, padx=4, pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
             
        self.__emailEntry = ttb.Entry(companyDataFrame, 
                                       width=45,
                                      textvariable=self.__email)
        self.__emailEntry.grid(row=5, column=1, sticky='nsew',pady=(2,0),padx=(8,0), ipady=4, )


        

        ttb.Separator(machinary_content_frame, bootstyle='light').grid(row=9, column=0, sticky='nsew', columnspan=2)


        buttonss_section_frame = tk.Frame(machinary_content_frame,)
        buttonss_section_frame.configure(background=FGCOLOR)
        buttonss_section_frame.grid(row=10, column=0, pady=(8,0), sticky='nsew', columnspan=2)
        buttonss_section_frame.anchor('e')



        closeimg = Image.open(f"{IMG_PATH}/closen.png")
        self.closeimg = ImageTk.PhotoImage(closeimg.resize(resize_image(20, closeimg.size)))
        closeimgh = Image.open(f"{IMG_PATH}/closeh.png")
        self.closeimgh = ImageTk.PhotoImage(closeimgh.resize(resize_image(20, closeimgh.size)))
        closeimgp = Image.open(f"{IMG_PATH}/closep.png")
        self.closeimgp = ImageTk.PhotoImage(closeimgp.resize(resize_image(20, closeimgp.size)))
        self.closeBTN = ButtonImage(buttonss_section_frame, image=self.closeimg, img_h=self.closeimgh, command=self.destroy, img_p=self.closeimgp, style='flatw.light.TButton', text='CERRAR', compound='center',padding=0)
        self.closeBTN.grid(row=0, column=0, sticky='nsew', pady=2, padx=(0,4))

        
        self.__form_fields =[self.documentIdEntry,self.nameEntry, self.lastnameEntry, self.__departmentEntry, self.__phoneEntry, self.__emailEntry]
        
        self.__form_variables = [self.__documentId, self.__name, self.__lastname,  self.__department, self.__email, self.__email, self.__companydRif ]


        if self.window_type == 'create':


            creatbtnimg = Image.open(f"{IMG_PATH}/registrar.png")
            self.creatbtnimg = ImageTk.PhotoImage(creatbtnimg.resize(resize_image(20, creatbtnimg.size)))
            creatbtnimgh = Image.open(f"{IMG_PATH}/registrarh.png")
            self.creatbtnimgh = ImageTk.PhotoImage(creatbtnimgh.resize(resize_image(20, creatbtnimgh.size)))
            creatbtnimgp = Image.open(f"{IMG_PATH}/registrarp.png")
            self.creatbtnimgp = ImageTk.PhotoImage(creatbtnimgp.resize(resize_image(20, creatbtnimgp.size)))

            self.createBTN = ButtonImage(buttonss_section_frame, command=self.createRepresentativeRecord, image=self.creatbtnimg, img_h=self.creatbtnimgh, img_p=self.creatbtnimgp, style='flatw.light.TButton', text='REGISTRAR', compound='center',padding=0)
            self.createBTN.grid(row=0, column=1, sticky='nsew', pady=2, padx=(0,4))

            self.__set_form_state()

        elif self.window_type == 'edit':
            editbtn = Image.open(f"{IMG_PATH}/editn.png")
            self.editbtn = ImageTk.PhotoImage(editbtn.resize(resize_image(20, editbtn.size)))
            editbtnh = Image.open(f"{IMG_PATH}/edith.png")
            self.editbtnh = ImageTk.PhotoImage(editbtnh.resize(resize_image(20, editbtnh.size)))
            editbtnp = Image.open(f"{IMG_PATH}/editp.png")
            self.editbtnp = ImageTk.PhotoImage(editbtnp.resize(resize_image(20, editbtnp.size)))

            self.editBTN = ButtonImage(buttonss_section_frame, command=self.editRepresentativeRecord, image=self.editbtn, img_h=self.editbtnh, img_p=self.editbtnp, style='flatw.light.TButton', text='MODIFICAR', compound='center',padding=0)
            self.editBTN.grid(row=0, column=2, sticky='nsew', pady=2, padx=(0,4))

            self.__set_form_state()
            self.documentIdEntry.configure(state='readonly')
        
        else:
            self.__set_form_state('readonly')
           


    def __set_form_state(self, state = 'normal'):
        for field in self.__form_fields:
            field.config(state=state,cursor='xterm')

    
    def __open_company_selection(self):
        select_window = ClientModule(self, callback = self.__set_company_info, selectionMode=True)
        self.wait_window(select_window)
        self.grab_set()
        self.transient()


    def __set_company_info(self, client):
        self.__companydRif.set(client.rif)
        self.__companydName.set(client.name)
          



    def representativeInstance(self):
        return Representative(
            id=self.__documentId.get(),
            name=self.__name.get(),
            lastname=self.__lastname.get(),
            company=self.__companydRif.get(),
            department=self.__department.get(),
            email=self.__email.get(),
            phone=self.__phone.get()
        )
    

    def __check_fields(self):
        return not '' in [value.get() for value in self.__form_variables]
    


    

    def createRepresentativeRecord(self):

        if self.__check_fields():
            if Representative.validate_id(self.__documentId.get()):
                ask = messagebox.askquestion('Crear','Crear nuevo Representante?', parent=self)
                if ask == 'yes':
                    newRepresentative = self.representativeInstance()
                    newRepresentative.create()
                    messagebox.showinfo('Aviso','Representante creado satisfactoriamente.', parent=self)
                    self.destroy()
            else:
                messagebox.showwarning('Aviso','El codigo ingresado ya se encuentra asociado a un registro.', parent=self)
        else:
            messagebox.showwarning('Aviso','Existen algunos campos invalidos o faltan por rellenar.', parent=self)


    def editRepresentativeRecord(self):
        if self.__check_fields():
            ask = messagebox.askquestion('Modificar','Modificar el Registro del Representante?', parent=self)
            if ask == 'yes':
                newRepresentative = self.representativeInstance()
                newRepresentative.update()
                messagebox.showinfo('Aviso','Registro modificado satisfactoriamente.', parent=self)
                self.destroy()
        else:
            messagebox.showwarning('Aviso','Existen algunos campos invalidos o faltan por rellenar.', parent=self)


    def __set_representative_data(self):
        self.__documentId.set(self.__REPRESENTATIVE.id)
        self.__name.set(self.__REPRESENTATIVE.name)
        self.__lastname.set(self.__REPRESENTATIVE.lastname)
        self.__companydRif.set(self.__REPRESENTATIVE.company)
        self.__companydName.set(self.__REPRESENTATIVE.get_company())
        self.__department.set(self.__REPRESENTATIVE.department)
        self.__phone.set(self.__REPRESENTATIVE.phone)
        self.__email.set(self.__REPRESENTATIVE.email)
        
    

    
 



# app = ttb.Window(themename='new')
# SGDB_Style()
# RepresentativeForm(window_type='edit', title='Modificar serviceo')
# app.mainloop()
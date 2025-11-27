import ttkbootstrap as ttb
from assets.globals import GUI_FONT, IMG_PATH
from assets.styles.styles import SGDB_Style
from customtkinter import CTkFrame
from PIL import Image, ImageTk
from components.buttons import ButtonImage
from assets.utils import resize_icon, resize_image
import tkinter as tk
from models.entitys.user import User
from tkinter import messagebox
from assets.db.db_connection import DB
from components.password_entry import PasswordEntry

roles = {row[1]:row[0] for row in DB.get_roles()}

class UserForm(ttb.Toplevel):
    def __init__(self, master=None, window_type = 'create', user=None, title = ''):
        super().__init__(master, toolwindow=True)
        self.focus()
        self.withdraw()
        self.window_title = title
        self.window_type = window_type

        ######### MODAL WINDOW CONFIG #########

        self.title(title)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.transient()
        self.grab_set()
        self.config(background="#D9D9D9")
       
        self.__UPDATE_PASSWORD = ttb.IntVar(value=0)
        if self.window_type == 'create':
            self.__UPDATE_PASSWORD.set(1)

        self.__USER: User = user

        ######### VARIABLES #########

        self.__id = ttb.StringVar()
        self.__username = ttb.StringVar()
        self.__name = ttb.StringVar()
        self.__lastname = ttb.StringVar()
        self.__email = ttb.StringVar()
        self.__phone = ttb.StringVar()
        self.__rol = ttb.IntVar()
        self.__rol_name = ttb.StringVar()

        self.__password = ttb.StringVar()
        self.__confirmPassword = ttb.StringVar()

        self.__createWidgets()

        if self.__USER:
            self.__set_client_info()
        self.place_window_center()
        self.deiconify()
        
    def __createWidgets(self):
        

        FGCOLOR = 'white'

        contentFrame = CTkFrame(self, fg_color='white',border_width=1,  border_color='#CFCFCF')
        contentFrame.grid(row = 1, column = 0, sticky = 'nsew', padx=10, pady=10)
        contentFrame.columnconfigure(0, weight=1)

        self.__products_icon = resize_icon(Image.open(f"{IMG_PATH}/users.png"))

        titleFrame = CTkFrame(contentFrame, fg_color='#212946')
        titleFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=8, pady=(8,0))
        titleFrame.columnconfigure(0, weight=1)
        
        ttb.Label(titleFrame, image=self.__products_icon, compound='left', text=f' {self.window_title}', font=(GUI_FONT, 14, 'bold'), foreground='white', background='#212946').grid(row=0,column=0, padx=10, pady=10, sticky='nsew')
       
        product_info_content = tk.Frame(contentFrame)
        product_info_content.config(background=FGCOLOR)
        product_info_content.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        product_info_content.columnconfigure(1, weight=1)
        product_info_content.columnconfigure(2, weight=1)

        mainInforFrame = tk.Frame(product_info_content)
        mainInforFrame.config(background=FGCOLOR)
        mainInforFrame.grid(row=0, column=0, sticky='nsew', columnspan=2)
        mainInforFrame.columnconfigure(1, weight=1)

        rif_label = ttb.Label(mainInforFrame, 
                                      anchor='w', 
                                      text='Documento de Identidad', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        rif_label.grid(row=0, column=0, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        self.rifEntry = ttb.Entry(mainInforFrame, textvariable=self.__id, width=30)
        self.rifEntry.grid(row=1, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=4, columnspan=1)

        usrnamelabel = ttb.Label(mainInforFrame, 
                                      anchor='w', 
                                      text='Nombre de Usuario', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        usrnamelabel.grid(row=0, column=1, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        self.usernameEntry = ttb.Entry(mainInforFrame, width=80, textvariable=self.__username)
        self.usernameEntry.grid(row=1, column=1, sticky='nsew',pady=(2,0),padx=4, ipady=4, columnspan=1)

        moreInfoFrame = tk.Frame(product_info_content)
        moreInfoFrame.config(background=FGCOLOR)
        moreInfoFrame.grid(row=2, column=0, sticky='nsew', columnspan=2, pady=(0,12))
        moreInfoFrame.columnconfigure(0, weight=1)
        moreInfoFrame.columnconfigure(1, weight=1)

        name_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Nombre', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=('arial',11,'bold'))
        name_label.grid(row=0, column=0, padx=(4,4), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        self.nameEntry = ttb.Entry(moreInfoFrame, textvariable=self.__name )
        self.nameEntry.grid(row=1, column=0, sticky='nsew',padx=(4,4), ipady=4,)


        phoneNumber_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Apellido', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=('arial',11,'bold'))
        phoneNumber_label.grid(row=0, column=1, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        self.lastnameEntry = ttb.Entry(moreInfoFrame, textvariable=self.__lastname)
        self.lastnameEntry.grid(row=1, column=1, sticky='nsew',padx=(4,0), ipady=4)


        website_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Correo', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=('arial',11,'bold'))
        website_label.grid(row=2, column=0, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew',)
        self.emailEntry = ttb.Entry(moreInfoFrame, textvariable=self.__email )
        self.emailEntry.grid(row=3, column=0, sticky='nsew',padx=(4,0), ipady=4,columnspan=2)

        email_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Telefono', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=('arial',11,'bold'))
        email_label.grid(row=4, column=0, padx=(4,4), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        self.phoneEntry = ttb.Entry(moreInfoFrame, textvariable=self.__phone )
        self.phoneEntry.grid(row=5, column=0, sticky='nsew',padx=(4,4), ipady=4,)


        rol_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Rol', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=('arial',11,'bold'))
        rol_label.grid(row=4, column=1, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        

        self.rolCombobox = ttb.Combobox(moreInfoFrame, values=list(roles.keys()), state='readonly', textvariable=self.__rol_name, style='selectionOnly.TCombobox')
        self.rolCombobox.grid(row=5, column=1, sticky='nsew',padx=(4,4),)
        self.rolCombobox.bind('<<ComboboxSelected>>', lambda e: self.__rol.set(roles[self.rolCombobox.get()]))
        self.rolCombobox.current(0)
        self.__rol.set(1)

        if self.window_type == 'edit':

            ttb.Separator(moreInfoFrame, bootstyle='light').grid(row=6, column=0, sticky='nsew', columnspan=2, pady=(8,4))

            
            updatepassword_label = ttb.Label(moreInfoFrame, 
                                        anchor='w', 
                                        text='Actualizar Contraseña', 
                                        bootstyle='danger',
                                        background=FGCOLOR ,
                                        font=('arial',11,'bold'))
            updatepassword_label.grid(row=7, column=0, padx=(4,0), pady=(2,5), ipadx=8, ipady=8, sticky='nsew')

            checkButton = ttb.Checkbutton(moreInfoFrame, text='Habilitar Campos de Contraseña', style='custom.success.TCheckbutton', onvalue=1, offvalue=0, variable=self.__UPDATE_PASSWORD, command=self.enabled_password_fields)
            checkButton.grid(row=7, column=1, padx=(4,0), pady=(2,5), ipadx=8, ipady=8, sticky='nsew')


        self.PASSWORD_FRAME = ttb.Frame(moreInfoFrame, style='white.TFrame')
        self.PASSWORD_FRAME.columnconfigure(0, weight=1)
        self.PASSWORD_FRAME.columnconfigure(1, weight=1)
        


        password_label = ttb.Label(self.PASSWORD_FRAME, 
                                     anchor='w', 
                                     text='Contraseña', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=('arial',11,'bold'))
        password_label.grid(row=0, column=0, padx=(4,4), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        self.passwordEntry = PasswordEntry(self.PASSWORD_FRAME,textvariable=self.__password)
        self.passwordEntry.grid(row=1, column=0, sticky='nsew',padx=(4,4), ipady=4,)


        passwordConfirm_label = ttb.Label(self.PASSWORD_FRAME, 
                                     anchor='w', 
                                     text='Confirmar Contraseña', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=('arial',11,'bold'))
        passwordConfirm_label.grid(row=0, column=1, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        self.passwordConfirmEntry = PasswordEntry(self.PASSWORD_FRAME, textvariable=self.__confirmPassword)
        self.passwordConfirmEntry.grid(row=1, column=1, sticky='nsew',padx=(4,0), ipady=4)


        ttb.Separator(product_info_content, bootstyle='light').grid(row=9, column=0, sticky='nsew', columnspan=2)


        buttonss_section_frame = tk.Frame(product_info_content,)
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

        if self.window_type == 'create':
            creatbtnimg = Image.open(f"{IMG_PATH}/registrar.png")
            self.creatbtnimg = ImageTk.PhotoImage(creatbtnimg.resize(resize_image(20, creatbtnimg.size)))
            creatbtnimgh = Image.open(f"{IMG_PATH}/registrarh.png")
            self.creatbtnimgh = ImageTk.PhotoImage(creatbtnimgh.resize(resize_image(20, creatbtnimgh.size)))
            creatbtnimgp = Image.open(f"{IMG_PATH}/registrarp.png")
            self.creatbtnimgp = ImageTk.PhotoImage(creatbtnimgp.resize(resize_image(20, creatbtnimgp.size)))

            self.createBTN = ButtonImage(buttonss_section_frame,  command=self.createUserRecord, image=self.creatbtnimg, img_h=self.creatbtnimgh, img_p=self.creatbtnimgp, style='flatw.light.TButton', text='REGISTRAR', compound='center',padding=0)
            self.createBTN.grid(row=0, column=1, sticky='nsew', pady=2, padx=(0,4))

            #self.__set_form_state()

        elif self.window_type == 'edit':
            editbtn = Image.open(f"{IMG_PATH}/editn.png")
            self.editbtn = ImageTk.PhotoImage(editbtn.resize(resize_image(20, editbtn.size)))
            editbtnh = Image.open(f"{IMG_PATH}/edith.png")
            self.editbtnh = ImageTk.PhotoImage(editbtnh.resize(resize_image(20, editbtnh.size)))
            editbtnp = Image.open(f"{IMG_PATH}/editp.png")
            self.editbtnp = ImageTk.PhotoImage(editbtnp.resize(resize_image(20, editbtnp.size)))

            self.editBTN = ButtonImage(buttonss_section_frame, command=self.editClientRecord, image=self.editbtn, img_h=self.editbtnh, img_p=self.editbtnp, style='flatw.light.TButton', text='MODIFICAR', compound='center',padding=0)
            self.editBTN.grid(row=0, column=2, sticky='nsew', pady=2, padx=(0,4))

            #self.__set_form_state()
            self.rifEntry.configure(state='readonly')
        
        self.FORM_FIELDS = [self.rifEntry, self.nameEntry, self.lastnameEntry, self.usernameEntry, self.emailEntry, self.phoneEntry,self.rolCombobox, self.passwordEntry, self.passwordConfirmEntry]
        self.FORM_DATA = [self.__id, self.__name, self.__lastname, self.__username, self.__email, self.__phone, self.__password, self.__confirmPassword, self.__rol_name, self.__rol]
        self.enabled_password_fields()

    def enabled_password_fields(self):
        
        if self.__UPDATE_PASSWORD.get() == 1:
            self.PASSWORD_FRAME.grid(row=8,column=0, columnspan=2, sticky='nsew')
        else:
            self.PASSWORD_FRAME.grid_forget()

        
            

    def userInstance(self):
        return User(ci = self.__id.get(),
                    name = self.__name.get(),
                    lastname = self.__lastname.get(),
                    username = self.__username.get(),
                    email = self.__email.get(),
                    phone = self.__phone.get(),
                    password = self.__password.get(),
                    rol = self.__rol.get())
    

    def __check_fields(self):
        empyt_fields = False
        field_func = lambda field: field.bind('<FocusIn>', lambda e: field.config(bootstyle='primary'))
        FIELDS = self.FORM_FIELDS
        if self.__UPDATE_PASSWORD.get() == 0:
            FIELDS = self.FORM_FIELDS[:-2]

        for field in FIELDS:
            if not field.get():
                field.config(bootstyle='danger')
                field_func(field)
                empyt_fields = True

        if empyt_fields:
            messagebox.showwarning('Fields',f"Existen campos por llenar", parent=self)
            return False
        
        if self.__password.get() != self.__confirmPassword.get() and self.__UPDATE_PASSWORD.get()==1:
            messagebox.showwarning('Contraseña', 'La Contraseña no coincide. Verificar.')
            return False
        
        return True
    

    def createUserRecord(self):
        if self.__check_fields():
            if User.validate_id(self.__id.get()):
                ask = messagebox.askquestion('Crear','Crear Registro de Usuario?', parent=self)
                if ask == 'yes':
                    newUser = self.userInstance()
                    print(newUser)
                    newUser.create()
                    messagebox.showinfo('Aviso','Registro creado satisfactoriamente.', parent=self)
                    self.destroy()
            else:
                messagebox.showwarning('Aviso','El RIF ingresado ya se encuentra asociado a un registro.', parent=self)
        else:
            messagebox.showwarning('Aviso','Existen algunos campos invalidos.', parent=self)


    def editClientRecord(self):
        if self.__check_fields():
            ask = messagebox.askquestion('Modificar','Modificar el Registro de Usuario?', parent=self)
            if ask == 'yes':
                newUser = self.userInstance()
                print(newUser)
           
                newUser.update(self.__UPDATE_PASSWORD.get())

                messagebox.showinfo('Aviso','Registro modificado satisfactoriamente.', parent=self)
                self.destroy()
        else:
            messagebox.showwarning('Aviso','Existen algunos campos invalidos.', parent=self)
        
    
    def __set_client_info(self):
        self.__id.set(self.__USER.ci)
        self.__name.set(self.__USER.name)
        self.__lastname.set(self.__USER.lastname)
        self.__username.set(self.__USER.username)
        self.__email.set(self.__USER.email)
        self.__phone.set(self.__USER.phone)
        self.__rol.set(self.__USER.rol)
        self.__rol_name.set(self.__USER.get_rol())



# app = ttb.Window(themename='new')
# SGDB_Style()
# UserForm(window_type='edit', title='Modificar Usuarios')
# app.mainloop()
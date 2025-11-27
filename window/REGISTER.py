import ttkbootstrap as ttb
from assets.globals import IMG_PATH, GUI_FONT
from assets.utils import resize_icon, resize_image
from PIL import Image
from tkinter import messagebox
from models.entitys.user import User

from components.password_entry import PasswordEntry
from components.buttons import ButtonImage

from PIL import ImageTk
roles = {
    'master':1,
    'gerente':2,
    'administrador':3
}

class Register(ttb.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        ####### CONFIG WINDOWS ######
        self.columnconfigure(0, weight=1)
 
        ####### REGISTER VARIABLES ########
        self.rol = ttb.IntVar()

        ####### CREATING FORM WIDGETS ########
        self.create_images()
        self.create_widgets()

        

    

    def create_widgets(self):

        form_div = ttb.Frame(self)
        form_div.grid(row=0, column=0, sticky='nsew', padx=30, pady=(5,5))
        form_div.columnconfigure(0, weight=1)
        form_div.anchor('center')

        ttb.Label(form_div, image=self.LOGIN_ICON, text=' REGISTRO', font=(GUI_FONT,16,'bold'), bootstyle='primary', anchor='center', compound='left').grid(row=0, column=0, padx=100, pady=(20,20), columnspan=2, sticky='nsew')


        ttb.Label(form_div, text='Nombre', font=(GUI_FONT, 12, 'bold'), foreground='#02474A').grid(row=1, column=0, sticky='nsew',pady=(5,0))
        self.username_entry = ttb.Entry(form_div, bootstyle='primary', width=30, name='nombre',)
        self.username_entry.grid(row=2, column=0, sticky='nsew', pady=(8,12),ipady=6,padx=(0,6))

        ttb.Label(form_div, text='Apellido', font=(GUI_FONT,12,'bold'),  foreground='#02474A').grid(row=1, column=1, sticky='nsew')
        self.userLastname_entry = ttb.Entry(form_div, bootstyle='primary', width=30, name='apellido')
        self.userLastname_entry.grid(row=2, column=1, sticky='nsew', pady=(8,12),ipady=6)

        ttb.Label(form_div, text='Email', font=(GUI_FONT,12,'bold'),  foreground='#02474A').grid(row=3, column=0, sticky='nsew')
        self.email_entry = ttb.Entry(form_div, bootstyle='primary', width=35, name='email')
        self.email_entry.grid(row=4, column=0, sticky='nsew', pady=(8,12),ipady=6, columnspan=2)

        ttb.Label(form_div, text='Contraseña', font=(GUI_FONT,12,'bold'),  foreground='#02474A').grid(row=5, column=0, sticky='nsew')
        self.password_entry = PasswordEntry(form_div, show='*', bootstyle='primary ', name='contraseña')
        self.password_entry.grid(row=6, column=0, sticky='nsew', pady=(8,12), ipady=6, columnspan=2,)


        ttb.Label(form_div, text='Confirmar Contraseña', font=(GUI_FONT,12,'bold'),  foreground='#02474A').grid(row=7, column=0, sticky='nsew')
        self.confirmPassword_entry = PasswordEntry(form_div, show='*', bootstyle='primary ', name='confirmacion de contraseña')
        self.confirmPassword_entry.grid(row=8, column=0, sticky='nsew', pady=(8,12), ipady=6, columnspan=2,)


        ttb.Label(form_div, text='Rol', font=(GUI_FONT,12,'bold'),  foreground='#02474A').grid(row=9, column=0, sticky='nsew')
        self.rol_combobox = ttb.Combobox(form_div, style='formsize.primary.TCombobox', name='rol', width=35, 
                                         values=('Master','Gerente','Administrador'), state='readonly', font=(GUI_FONT,11,'bold'))
        self.rol_combobox.grid(row=10, column=0, sticky='nsew', pady=(8,12), columnspan=2)
        self.rol_combobox.bind('<<ComboboxSelected>>', lambda e: self.rol.set(roles[self.rol_combobox.get().lower()]))

     

        log_in = ButtonImage(self, image=self.REGISTER_BTN,  compound='center',style='flat.light.TButton', 
                            padding=0, command=self.register, img_h=self.REGISTER_BTN_in, text='REGISTRAR',
                            img_p=self.REGISTER_BTN)        
        log_in.grid(row=1, column=0, pady=(20,5))
        

        #################### back button ###########################################
        close_btn = ButtonImage(self, compound='left',  style='flat.light.TButton', 
                   padding=0, image=self.CLOSE_I, command=self.destroy,
                   img_h=self.CLOSE_H_I, img_p=self.CLOSE_I)
        close_btn.grid(row=0, column=0, pady=10, padx=10, sticky='nw')

    
        self.FORM_FIELDS = [
            self.username_entry, self.userLastname_entry, self.password_entry,
            self.confirmPassword_entry, self.email_entry, self.rol_combobox
        ]

    
    def create_images(self):
        self.CLOSE_I = Image.open(f"{IMG_PATH}/back_btn.png")
        self.CLOSE_I = ImageTk.PhotoImage(self.CLOSE_I.resize(resize_image(10, self.CLOSE_I.size)))

        self.CLOSE_H_I = Image.open(f"{IMG_PATH}/back_btn_h.png")
        self.CLOSE_H_I = ImageTk.PhotoImage(self.CLOSE_H_I.resize(resize_image(10, self.CLOSE_H_I.size)))

        self.REGISTER_BTN = Image.open(f"{IMG_PATH}/log_in_butt.png")
        self.REGISTER_BTN = ImageTk.PhotoImage(self.REGISTER_BTN.resize(resize_image(25,self.REGISTER_BTN.size)))

        self.REGISTER_BTN_in = Image.open(f"{IMG_PATH}/log_in_butt_in.png")
        self.REGISTER_BTN_in = ImageTk.PhotoImage(self.REGISTER_BTN_in.resize(resize_image(25,self.REGISTER_BTN_in.size)))

        self.REGISTER_BTN_in = Image.open(f"{IMG_PATH}/log_in_butt_p.png")
        self.REGISTER_BTN_in = ImageTk.PhotoImage(self.REGISTER_BTN_in.resize(resize_image(25,self.REGISTER_BTN_in.size)))

        self.LOGIN_ICON = Image.open(f"{IMG_PATH}/login.png")
        self.LOGIN_ICON = resize_icon(self.LOGIN_ICON, (50,50))


        
    def register(self):
        empyt_fields = False
        field_func = lambda field: field.bind('<FocusIn>', lambda e: field.config(bootstyle='primary'))
        for field in self.FORM_FIELDS:
            if not field.get():
                field.config(bootstyle='danger')
                field_func(field)
                empyt_fields = True

        if empyt_fields:
            messagebox.showwarning('Fields',f"Existen campos por llenar", parent=self)

        else:
            if self.password_entry.get() != self.confirmPassword_entry.get():
                messagebox.showwarning('Contraseña', 'La Contraseña no coincide. Verificar.')
                return 
            
            new_user = User(
                id=0,
                name=self.username_entry.get(),
                lastname=self.userLastname_entry.get(),
                username=self.email_entry.get(),
                password=self.password_entry.get(),
                rol=self.rol.get()
            )


            new_user.create()
            messagebox.showinfo('Usuario', 'Usuario creado satisfactoriamente!')
            self.clean_data()
    
    def clean_data(self):
        for field in self.FORM_FIELDS:
            field.delete(0, ttb.END)    
        
        

import ttkbootstrap as ttb
from assets.globals import GUI_COLORS, IMG_PATH
from assets.utils import resize_icon, resize_image
from PIL import Image, ImageTk
from models.entitys.user import User, validate_user
from tkinter import messagebox
from window.REGISTER import Register
from components.buttons import ButtonImage
from components.password_entry import PasswordEntry
import assets.globals as constGlobal

class Login(ttb.Toplevel):
    def __init__(self, master, callback = None, *args, **kwargs):
        super().__init__(master, overrideredirect=False, *args, **kwargs)
        self.withdraw()
        self.callback = callback
        

        ######### WINDOW CONFIG ##########
        SYSTEM_WIDTH = self.winfo_screenwidth()
        SYSTEM_HEIGHT = self.winfo_screenheight()


        self.form_width = round(SYSTEM_WIDTH*0.70)
        self.form_height = round(SYSTEM_HEIGHT*0.70)


        pwidth = (SYSTEM_WIDTH-self.form_width)//2
        pheight = (SYSTEM_HEIGHT-self.form_height)//2


        self.geometry(str(self.form_width)+"x"+str(self.form_height)+"+"+str(pwidth)+"+"+str(pheight-60))
        
        self.minsize(width=self.form_width,height=self.form_height)

    
        self.protocol("WM_DELETE_WINDOW", self.master.quit)
        self.title('SGAG')
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1) 
        
        self.resizable(0,0)
        
        
        
        ######### WINDOW BACKGROUND ##########
        self.bg = Image.open(f'{IMG_PATH}/backoff.png')
        self.bg = ImageTk.PhotoImage(self.bg.resize(size=(round(self.form_width),round(self.form_height))))


        ttb.Label(self, image=self.bg, border=0).grid(row=0, column=0, sticky='nsew')


        ##### Form Creation #####
        self.create_form()
        self.place_window_center()
        self.iconbitmap('SIGAG.ico')

        self.deiconify()
        
        
        
    def create_form(self):

        ##### Form frame #####
        form = ttb.Frame(self,)
        form.grid(row=0, column=0, ipady=20,sticky="nsw")
        form.columnconfigure(0, weight=1)
    

        self.login_icon = Image.open(f"{IMG_PATH}/logo.png")
        self.login_icon = resize_icon(self.login_icon, (round(self.form_width*0.10),round(self.form_width*0.10)))

        ttb.Label(form, image=self.login_icon, text='LOGIN', font=('arial black',18,'bold'), bootstyle='primary', anchor='center', compound='top').grid(row=0, column=0, pady=(50,30), sticky='nsew')

        self.SHOW_PASS = Image.open(f"{IMG_PATH}/show.png")
        self.SHOW_PASS = resize_icon(self.SHOW_PASS, (35,35))

        self.HIDE_PASS = Image.open(f"{IMG_PATH}/hide.png")
        self.HIDE_PASS = resize_icon(self.HIDE_PASS, (35,35))

        self.SHOW_H_PASS = Image.open(f"{IMG_PATH}/show_h.png")
        self.SHOW_H_PASS = resize_icon(self.SHOW_H_PASS, (35,35))

        self.HIDE_H_PASS = Image.open(f"{IMG_PATH}/hide_h.png")
        self.HIDE_H_PASS = resize_icon(self.HIDE_H_PASS, (35,35))


        form_div = ttb.Frame(form)
        form_div.grid(row=1, column=0, sticky='nsew', padx=30, pady=(10,10))
        form_div.columnconfigure(0, weight=1)


        ttb.Label(form_div, text='Nombre de Usuario', font=('',12,'bold'), foreground=GUI_COLORS['primary']).grid(row=0, column=0, sticky='nsew')

        self.email_entry = ttb.Entry(form_div, bootstyle='primary', width=55)
        self.email_entry.grid(row=1, column=0, sticky='nsew', pady=(8,6),ipady=6, columnspan=2)
        self.email_entry.bind("<FocusIn>", lambda e: self.alert_email.config(text=''))
        self.alert_email = ttb.Label(form_div, text='', bootstyle='danger', anchor='center')
        self.alert_email.grid(row=2, column=0, columnspan=2, sticky='n', pady=(0,6))

        ttb.Label(form_div, text='Contraseña', font=('',12,'bold'), foreground=GUI_COLORS['primary']).grid(row=3, column=0, sticky='nsew')


        self.password_entry = PasswordEntry(form_div, show='*', bootstyle='primary ')
        self.password_entry.grid(row=4, column=0, sticky='nsew', pady=(8,6), ipady=6, columnspan=2,)
        self.password_entry.bind("<FocusIn>", lambda e: self.alert_password.config(text=''))
        self.password_entry.bind("<Return>", lambda e: self.log_in())

        self.alert_password = ttb.Label(form_div, text='', bootstyle='danger', anchor='center')
        self.alert_password.grid(row=5, column=0, columnspan=2, sticky='n', pady=(0,6))


       

        self.butt = Image.open(f"{IMG_PATH}/log_in_butt.png")
        self.butt = ImageTk.PhotoImage(self.butt.resize(resize_image(25,self.butt.size)))

        self.butt_in = Image.open(f"{IMG_PATH}/log_in_butt_in.png")
        self.butt_in = ImageTk.PhotoImage(self.butt_in.resize(resize_image(25,self.butt_in.size)))

        self.butt_p = Image.open(f"{IMG_PATH}/log_in_butt_p.png")
        self.butt_p = ImageTk.PhotoImage(self.butt_p.resize(resize_image(25,self.butt_p.size)))

        log_in = ButtonImage(form, image=self.butt, img_h=self.butt_in, compound='center', text='INGRESAR',
                    img_p=self.butt_p, style='flat.light.TButton',padding=0,
                    command=self.log_in)
        log_in.grid(row=2, column=0, pady=(5,10),padx=20)


     

    def register_form(self):
        Register(self).grid(row=0, column=0, sticky='nsw')

      
    def log_in(self):

        user_try = User(username=self.email_entry.get(), password=self.password_entry.get())
        user = validate_user(user_try)
        if user:
            if user.password:
                messagebox.showinfo('SG SYSTEM','Bienvenido', parent=self)
                self.destroy()
                if self.callback:
                    constGlobal.loggued_user = user
                    self.callback(user)
            else:
                self.alert_password.config(text='Contraseña Incorrecta')
        else:
            self.alert_email.config(text='Email no registrado')
        

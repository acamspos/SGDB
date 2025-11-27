import ttkbootstrap as ttb
from assets.globals import GUI_COLORS, IMG_PATH, GUI_FONT
from assets.utils import resize_icon, resize_image
from assets.globals import invoice_icon, budget_icon, project_icon, refresh_icon
from components.buttons import ButtonImage
from PIL import Image, ImageTk
from customtkinter import CTkFrame
import tkinter as tk
from assets.styles.styles import SGDB_Style
from components.bcards import BCards
###### GRAPH LIBRARIES

from pages.users.userForm import UserForm
from tkinter import messagebox
from models.entitys.user import User
from assets.db.db_connection import DB

class UsersPage(ttb.Frame):
    def __init__(self, master=None):
        SGDB_Style()
        super().__init__(master, height=50, width=50)
        PART_COLOR = GUI_COLORS['bg']
        PART2_COLOR = GUI_COLORS['primary']

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        ########## GUI ICONSr##########
        self.__dash_icon = Image.open(f'{IMG_PATH}/usertitle.png')
        self.__dash_icon = ImageTk.PhotoImage(self.__dash_icon.resize(resize_image(10, self.__dash_icon.size)))



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
                               text=' Usuarios', 
                                padding='0 0',
                               background='#212946',
                               font=('arial',15, 'bold'), 
                               foreground='#fff')
        page_title.grid(row=0, column=0, sticky='nsew',padx=(80,0))

       

        ttb.Separator(self, orient='horizontal',bootstyle='dark').grid(row=1, column=0, sticky='nsew',padx=20)

      
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

        ttb.Label(subtitle, text='Gestion de Usuarios', background=PART2_COLOR, font=(GUI_FONT,13,'bold'), foreground='#fff').grid(row=0, column=1, sticky='nsew', padx=(4,8), pady=(8,0))

        ttb.Label(subtitle, text='Inicio/Usuarios', background=PART2_COLOR, font=(GUI_FONT,9), foreground='#fff').grid(row=1, column=1, sticky='nsew', padx=(4,8), pady=(0,8))

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


        editbtnimg = Image.open(f"{IMG_PATH}/editbtn.png")
        self.editbtnimg = resize_icon(editbtnimg,(50,50))

        editbtnimgh = Image.open(f"{IMG_PATH}/editbtnh.png")
        self.editbtnimgh = resize_icon(editbtnimgh, (50,50))

        editbtnimgp = Image.open(f"{IMG_PATH}/editbtnp.png")
        self.editbtnimgp = resize_icon(editbtnimgp, (50,50))

        self.editBTN = ButtonImage(buttons_frame, image=self.editbtnimg, img_h=self.editbtnimgh, img_p=self.editbtnimgp, style='#D9D9D9.TButton', padding=0, state='disabled', command=self.__open_edit_form)
        self.editBTN.grid(row=0, column=3, sticky='nsew', pady=2, padx=(0,8))


        deletebtnimg = Image.open(f"{IMG_PATH}/deletebtn.png")
        self.deletebtnimg = resize_icon(deletebtnimg, (50,50))

        deletebtnimgh = Image.open(f"{IMG_PATH}/deletebtnh.png")
        self.deletebtnimgh = resize_icon(deletebtnimgh, (50,50))

        deletebtnimgp = Image.open(f"{IMG_PATH}/deletebtnp.png")
        self.deletebtnimgp = resize_icon(deletebtnimgp, (50,50))

        self.deleteBTN = ButtonImage(buttons_frame, image=self.deletebtnimg, img_h=self.deletebtnimgh, command=self.__delete_service, img_p=self.deletebtnimgp, style='#D9D9D9.TButton', padding=0, state='disabled')
        self.deleteBTN.grid(row=0, column=4, sticky='nsew', pady=2, padx=(0,8))


        self.SEARCHENTRY = ttb.Entry(buttons_frame, bootstyle='info', width=30)
        self.SEARCHENTRY.grid(row=0,column=5, ipady=2, padx=(0,8), sticky='e')
        self.SEARCHENTRY.bind('<Return>', lambda e: self.__findUsers())
        
        searchbtnimg = Image.open(f"{IMG_PATH}/searchbtn.png")
        self.searchbtnimg = resize_icon(searchbtnimg, (50,50))

        searchbtnimgh = Image.open(f"{IMG_PATH}/searchbtnh.png")
        self.searchbtnimgh = resize_icon(searchbtnimgh, (50,50))

        searchbtnimgp = Image.open(f"{IMG_PATH}/searchbtnp.png")
        self.searchbtnimgp = resize_icon(searchbtnimgp, (50,50))

        ButtonImage(buttons_frame, image=self.searchbtnimg, img_h=self.searchbtnimgh, command=self.__findUsers, img_p=self.searchbtnimgp, style='#D9D9D9.TButton', padding=0).grid(row=0, column=6, pady=2, padx=(0,0))

        grid_frame = tk.Frame(self.dashboard_content,)
        grid_frame.config(background='#D9D9D9')
        grid_frame.grid(row=3, column=0, columnspan=1, padx=10, pady=(0,10), sticky='nsew')
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.rowconfigure(0, weight=1)

        columns = ('id', 'username', 'ci','name','lastname','tlf','email','rol')

        yscroll = ttb.Scrollbar(grid_frame, 
                                orient='vertical',
                                bootstyle="dark-round")
        yscroll.grid(row=0, column=1, padx=1, pady=2,sticky='ns', rowspan=2)

        xscroll = ttb.Scrollbar(grid_frame, 
                                orient='horizontal',
                                bootstyle="dark-round")
        xscroll.grid(row=1, column=0, padx=1, pady=2,sticky='ew')

        self.userGridview = ttb.Treeview(grid_frame,columns=columns,show='headings', style='cust.primary.Treeview',
                                 height=10, padding=0, xscrollcommand=xscroll.set,
                                selectmode='extended', yscrollcommand=yscroll.set)
        self.userGridview.grid(row=0,column=0,padx=2,pady=(2,2),sticky='nsew')

        yscroll.configure(command=self.userGridview.yview)
        xscroll.configure(command=self.userGridview.xview)

        self.userGridview.heading(columns[0],text='Id', anchor='center')
        self.userGridview.heading(columns[1],text='Usuario', anchor='center')
        self.userGridview.heading(columns[2],text='Cedula', anchor='center')
        self.userGridview.heading(columns[3],text='Nombre', anchor='center')
        self.userGridview.heading(columns[4], text='Apellido', anchor='center')
        self.userGridview.heading(columns[5], text='Telefono', anchor='center')
        self.userGridview.heading(columns[6],text='Email', anchor='center')
        self.userGridview.heading(columns[7],text='Rol', anchor='center')
      

        self.userGridview.column(columns[0],width=80,stretch=False,anchor='center')
        self.userGridview.column(columns[1],width=200,stretch=True,anchor='center')
        self.userGridview.column(columns[2],width=140,stretch=False,anchor='center')
        self.userGridview.column(columns[3],width=200,stretch=False,anchor='center')
        self.userGridview.column(columns[4],width=200,stretch=False,anchor='center')
        self.userGridview.column(columns[5],width=160,stretch=False,anchor='center')
        self.userGridview.column(columns[6],width=300,stretch=False,anchor='center')
        self.userGridview.column(columns[7],width=160,stretch=False,anchor='center')

        self.userGridview.bind('<<TreeviewSelect>>', lambda e: self.__enabled_view())

        ####### AMOUNT RECORD WIDGET #########

        self.bind('<Map>', lambda e:self.__findUsers())

        
    def __delete_service(self):
        ask = messagebox.askquestion('Eliminar', 'Desea eliminar el usuario del sistema?', parent=self)
        if ask == 'yes':
            service = self.__get_user_selected()
            service.delete()
            del service
            messagebox.showinfo('Aviso','Servicio Eliminado satisfactoriamente.', parent=self)
            self.__findUsers()

    def __open_create_form(self):
        ask = messagebox.askquestion('Registrar','Desea crear un nuevo Servicio?', parent=self)
        if ask == 'yes':
            waitwindow = UserForm(self, window_type='create', title='Registrar Usuario',)
            waitwindow.wait_window()
            self.__findUsers()


    def __open_edit_form(self):
            user = self.__get_user_selected()
            if user:
                ask = messagebox.askquestion('Modificar','Desea modificar el registro seleccionado?', parent=self)
                if ask == 'yes':
                    waitwindow = UserForm(self, window_type='edit', title='Modificar Usuario', user=user)
                    waitwindow.wait_window()
                    self.__findUsers()
            del user

    def __get_user_selected(self,) -> User:
        selected = self.userGridview.focus()
        if selected:
            ci = self.userGridview.item(selected, 'values')[2]
            return User.findOneUser(ci)


    

    
    def __findUsers(self):
        self.userGridview.delete(*self.userGridview.get_children())
        users = User.findAllUsers(username=self.SEARCHENTRY.get())
        for user in users:
            user = User(**user)
           
            self.userGridview.insert("",
                            ttb.END,
                            values=(user.id, user.username, user.ci, user.name, user.lastname, user.phone, user.email, user.get_rol()), tags='row')
        del users
 


    def __enabled_view(self):
        if self.userGridview.selection()!= ():
    
            self.editBTN.config(state='normal')
            self.deleteBTN.config(state='normal')
        else:
           
            self.editBTN.config(state='disabled')
            self.deleteBTN.config(state='disabled')



if __name__=="__main__":
    app = ttb.Window(themename='new')
  
    SGDB_Style()
    UsersPage(app).pack()
    app.mainloop()
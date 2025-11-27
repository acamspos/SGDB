import ttkbootstrap as ttb
from assets.globals import GUI_COLORS, IMG_PATH, GUI_FONT
from assets.utils import resize_icon, resize_image
from PIL import Image, ImageTk
from customtkinter import CTkFrame
import tkinter as tk

from components.buttons import ButtonImage
from assets.styles.styles import SGDB_Style

# Configuración
from assets.db.db_connection import DB
from pages.representative.views.representativeForm import RepresentativeForm

from models.entitys.representative import Representative

from tkinter import messagebox

class RepresentativeModule(ttb.Toplevel):
    def __init__(self, master=None, callback=None, selectionMode = False, filter_company = None):
        PART_COLOR = GUI_COLORS['bg']
        PART2_COLOR = GUI_COLORS['primary']

        super().__init__(master)
        
        ############# CONFIGURACION VENTANA #############
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.geometry('1200x850')
        ############## ESTILOS PERSONALIZADOS ##############
        self.transient()
        self.grab_set()
        self.config(background="#D9D9D9")
        self.focus()
        ########### VARIABLES DE PAGINACION ############
        self.callback = callback
        self.filter_company = filter_company

        ####################### ELEMENTOS DE LA INTERFAZ GRAFICA #######################

        ###### TSECCION DEL TITULO:

        

        ######### SECCION DE CONTENIDO:
    

        self.CONTENT_FRAME = CTkFrame(self,fg_color='#fff')
        self.CONTENT_FRAME.grid(row=0, column=0, sticky='nsew',padx=10, pady=10, )
        self.CONTENT_FRAME.columnconfigure(0, weight=1)
        self.CONTENT_FRAME.rowconfigure(3, weight=1)

        subtitle = CTkFrame(self.CONTENT_FRAME, corner_radius=6, fg_color=PART2_COLOR)
        subtitle.grid(row=0, column=0, sticky='nsew', padx=10, pady=(10,2))

        self.micon = resize_icon(Image.open(f'{IMG_PATH}/representative.png'),(45,45))

        ttb.Label(subtitle, image=self.micon, background=PART2_COLOR, ).grid(row=0, column=0, rowspan=2, sticky='nsew', padx=(8), pady=8)

        ttb.Label(subtitle, text='Gestion de Representantes', background=PART2_COLOR, anchor='sw', font=(GUI_FONT,13,'bold'), foreground='#fff').grid(row=0, column=1, sticky='nsew', padx=(4,8), pady=(8,0))

        ttb.Label(subtitle, text='Inicio / Representantes', background=PART2_COLOR, anchor='nw', font=(GUI_FONT,9), foreground='#fff').grid(row=1, column=1, sticky='nsew', padx=(4,8), pady=(0,8))


     
        ttb.Frame(self.CONTENT_FRAME, bootstyle='primary').grid(row=1, column=0, sticky='nsew', padx=10, pady=5)

        buttons_frame = tk.Frame(self.CONTENT_FRAME, background='red')
        buttons_frame.config(background='#fff')
        buttons_frame.grid(row=2, column=0, sticky='nsew', padx=10)
        buttons_frame.columnconfigure(6, weight=1)


        creatbtnimg = Image.open(f"{IMG_PATH}/create.png")
        self.creatbtnimg = resize_icon(creatbtnimg, (50,50))

        creatbtnimgh = Image.open(f"{IMG_PATH}/createh.png")
        self.creatbtnimgh = resize_icon(creatbtnimgh, (50,50))

        creatbtnimgp = Image.open(f"{IMG_PATH}/createp.png")
        self.creatbtnimgp = resize_icon(creatbtnimgp, (50,50))

        ButtonImage(buttons_frame, image=self.creatbtnimg, img_h=self.creatbtnimgh, img_p=self.creatbtnimgp,  style='flatw.light.TButton', padding=0, command=self.__open_create_form).grid(row=0, column=0, sticky='', pady=2, padx=(0,8))


        ttb.Separator(buttons_frame, orient='vertical',bootstyle='dark').grid(row=0, column=1, sticky='ew', padx=(0,8))

        if not selectionMode:

            viewbtnimg = Image.open(f"{IMG_PATH}/view.png")
            self.viewbtnimg = resize_icon(viewbtnimg, (50,50))

            viewbtnimgh = Image.open(f"{IMG_PATH}/viewh.png")
            self.viewbtnimgh = resize_icon(viewbtnimgh, (50,50))

            viewbtnimgp = Image.open(f"{IMG_PATH}/viewp.png")
            self.viewbtnimgp = resize_icon(viewbtnimgp, (50,50))
            self.viewBTN = ButtonImage(buttons_frame, state='disabled', image=self.viewbtnimg, img_h=self.viewbtnimgh,  img_p=self.viewbtnimgp, style='flatw.light.TButton', padding=0, command=self.__open_view_form)
            self.viewBTN.grid(row=0, column=2, sticky='', pady=2, padx=(0,8))


            editbtnimg = Image.open(f"{IMG_PATH}/editbtn.png")
            self.editbtnimg = resize_icon(editbtnimg,(50,50))

            editbtnimgh = Image.open(f"{IMG_PATH}/editbtnh.png")
            self.editbtnimgh = resize_icon(editbtnimgh, (50,50))

            editbtnimgp = Image.open(f"{IMG_PATH}/editbtnp.png")
            self.editbtnimgp = resize_icon(editbtnimgp, (50,50))

            self.editBTN = ButtonImage(buttons_frame, command=self.__open_edit_form,state='disabled', image=self.editbtnimg, img_h=self.editbtnimgh, img_p=self.editbtnimgp, style='flatw.light.TButton', padding=0, )
            self.editBTN.grid(row=0, column=3, sticky='nsew', pady=2, padx=(0,8))


            deleteBTNimg = Image.open(f"{IMG_PATH}/deleteBTN.png")
            self.deleteBTNimg = resize_icon(deleteBTNimg, (50,50))

            deleteBTNimgh = Image.open(f"{IMG_PATH}/deleteBTNh.png")
            self.deleteBTNimgh = resize_icon(deleteBTNimgh, (50,50))

            deleteBTNimgp = Image.open(f"{IMG_PATH}/deleteBTNp.png")
            self.deleteBTNimgp = resize_icon(deleteBTNimgp, (50,50))

            self.deleteBTN = ButtonImage(buttons_frame, state='disabled', command=self.__deleteRepresentative, image=self.deleteBTNimg, img_h=self.deleteBTNimgh, img_p=self.deleteBTNimgp, style='flatw.light.TButton', padding=0)
            self.deleteBTN.grid(row=0, column=4, sticky='', pady=2, padx=(0,8))


        ttb.Separator(buttons_frame, orient='vertical',bootstyle='dark').grid(row=0, column=5, sticky='ew', padx=(0,8))


        
        self.searchEntry = ttb.Entry(buttons_frame,width=30)
        self.searchEntry.grid(row=0, column=6, ipady=3, sticky='e', padx=(0,6))
        self.searchEntry.bind()



        searchbtnimg = Image.open(f"{IMG_PATH}/searchbtn.png")
        self.searchbtnimg = resize_icon(searchbtnimg, (50,50))

        searchbtnimgh = Image.open(f"{IMG_PATH}/searchbtnh.png")
        self.searchbtnimgh = resize_icon(searchbtnimgh, (50,50))

        searchbtnimgp = Image.open(f"{IMG_PATH}/searchbtnp.png")
        self.searchbtnimgp = resize_icon(searchbtnimgp, (50,50))

        ButtonImage(buttons_frame, command=self.__findRepresentatives, image=self.searchbtnimg, img_h=self.searchbtnimgh, img_p=self.searchbtnimgp, style='flatw.light.TButton', padding=0).grid(row=0, column=7, pady=2, padx=(10,0))

        grid_frame = tk.Frame(self.CONTENT_FRAME,)
        grid_frame.config(background='#fff')
        grid_frame.grid(row=3, column=0, columnspan=1, padx=10, pady=(0,10), sticky='nsew')
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.rowconfigure(0, weight=1)

        columns = ('id','name','lastname','company','department','phone','email', )
        yscroll = ttb.Scrollbar(grid_frame, 
                                orient='vertical',
                                bootstyle="dark-round")
        yscroll.grid(row=0, column=1, padx=1, pady=2,sticky='ns', rowspan=2)

        xscroll = ttb.Scrollbar(grid_frame, 
                                orient='horizontal',
                                bootstyle="dark-round")
        xscroll.grid(row=1, column=0, padx=1, pady=2,sticky='ew')

        self.representativeGridView = ttb.Treeview(grid_frame,columns=columns,show='headings', style='cust.primary.Treeview',
                                 height=14, padding=0, xscrollcommand=xscroll.set,
                                selectmode='extended', yscrollcommand=yscroll.set)
        self.representativeGridView.grid(row=0,column=0,padx=2,pady=(2,2),sticky='nsew')

        yscroll.configure(command=self.representativeGridView.yview)
        xscroll.configure(command=self.representativeGridView.xview)

        self.representativeGridView.heading("#0")
        self.representativeGridView.heading(columns[0], anchor='w', text='C.I.')
        self.representativeGridView.heading(columns[1], anchor='w', text='Nombre')
        self.representativeGridView.heading(columns[2], anchor='w', text='Apellido')
        self.representativeGridView.heading(columns[3], anchor='w', text='Empresa')
        self.representativeGridView.heading(columns[4], anchor='w', text='Departamento')
        self.representativeGridView.heading(columns[5], anchor='w', text='Telefono')
        self.representativeGridView.heading(columns[6], anchor='w', text='Correo')


        self.representativeGridView.column('#0', width=0)
        self.representativeGridView.column(columns[0], width=150, stretch=False, anchor='center')
        self.representativeGridView.column(columns[1], width=200, stretch=False, anchor='w')
        self.representativeGridView.column(columns[2], width=200, stretch=False, anchor='w')
        self.representativeGridView.column(columns[3], width=400, stretch=False, anchor='w')
        self.representativeGridView.column(columns[4], width=200, stretch=False, anchor='w')
        self.representativeGridView.column(columns[5], width=200, stretch=False, anchor='w')
        self.representativeGridView.column(columns[6], width=200, stretch=False, anchor='w')

        self.representativeGridView.tag_configure('row', background='#E7E6E6')



       
        if selectionMode:
            self.representativeGridView.bind('<Double-1>', lambda e: self.__select_Representative())

        else:
            self.representativeGridView.bind('<<TreeviewSelect>>', lambda e: self.__enabled_view())
        
        self.__findRepresentatives()
        self.place_window_center()

    def __select_Representative(self):
        representative = self.__get_selected_representative()
        if representative:
            self.destroy()
            if self.callback:
                self.callback(representative)
            
        del representative


    def __enabled_view(self):
        if self.representativeGridView.selection()!= ():
            self.viewBTN.config(state='normal')
            self.editBTN.config(state='normal')
            self.deleteBTN.config(state='normal')
        else:
            self.viewBTN.config(state='disabled')
            self.editBTN.config(state='disabled')
            self.deleteBTN.config(state='disabled')




    def __findRepresentatives(self):
        self.representativeGridView.delete(*self.representativeGridView.get_children())
        representatives = Representative.findAllRepresentative(name=self.searchEntry.get(), filter_company= self.filter_company)
        for representative in representatives:
            self.representativeGridView.insert("",
                            ttb.END,
                            values=(representative[0], representative[1],representative[2],representative[3],representative[4],representative[5],representative[6]), tags='row')
        del representatives
   

    def __deleteRepresentative(self):
        ask = messagebox.askquestion('Eliminar', 'Desea eliminar el registro del representante?', parent=self)
        if ask == 'yes':
            representative = self.__get_selected_representative()

            if representative.check_records():
                representative.delete()
                del representative
                messagebox.showinfo('Aviso','Representante Eliminado satisfactoriamente.', parent=self)
                self.__findRepresentatives()
            else:
                messagebox.showinfo('Aviso','El Representante no puede ser Eliminado. Se encuentra vinculado a documentos.', parent=self)
           

    def __open_create_form(self):
        ask = messagebox.askquestion('Registrar','Desea crear un nuevo registro?', parent=self)
        if ask == 'yes':
            waitwindow = RepresentativeForm(self, window_type='create', title='Registrar Representante')
            waitwindow.wait_window()
            self.__findRepresentatives()


    def __open_edit_form(self):
            representative = self.__get_selected_representative()
            if representative:
                ask = messagebox.askquestion('Modificar','Desea modificar el registro seleccionado?', parent=self)
                if ask == 'yes':
                    waitwindow = RepresentativeForm(self, window_type='edit', title='Modificar Proveedor', representative=representative)
                    waitwindow.wait_window()
                    self.__findRepresentatives()
            del representative

    def __get_selected_representative(self,):
        selected = self.representativeGridView.focus()

        if selected:
            idR = self.representativeGridView.item(selected, 'values')[0]
            representative = Representative.findOneRepresentative(idR)
            return representative


    def __open_view_form(self):
        representative = self.__get_selected_representative()
        if representative:
            RepresentativeForm(self, window_type='view', title='Detalles del Representante', representative=representative)
        del representative
            
            


if __name__=="__main__":
    app = ttb.Window(themename='new')
  
    SGDB_Style()
    RepresentativeModule(app)
    app.mainloop()
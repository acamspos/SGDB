import ttkbootstrap as ttb
from assets.globals import GUI_COLORS, GUI_FONT, IMG_PATH
from customtkinter import CTkFrame
from assets.styles.styles import SGDB_Style
from PIL import Image
from assets.utils import resize_icon
from components.buttons import ButtonImage
from models.entitys.provider import Provider
from pages.providers.views.providerForm import ProviderForm
from pages.providers.views.providerViewForm import ProviderView
from tkinter import messagebox


class ProviderModule(ttb.Toplevel):
    def __init__(self, master=None, callback=None, selectionMode = False):
        

        super().__init__(master)
        self.focus()
      
        self.transient()
        self.grab_set()
        self.config(background="#D9D9D9")
        SYSTEM_WIDTH = self.winfo_screenwidth()
        SYSTEM_HEIGHT = self.winfo_screenheight()

        pwidth = (SYSTEM_WIDTH-1200)//2
        pheight = (SYSTEM_HEIGHT-800)//2

        self.geometry(str(1200)+"x"+str(800)+"+"+str(pwidth)+"+"+str(pheight-60))
        self.minsize(width=1200,height=800)
        self.title('Proveedores')
        

        ############# CONFIGURACION VENTANA #############
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        ############## ESTILOS PERSONALIZADOS ##############
        
        ########### VARIABLES DE PAGINACION ############
        self.selectionMode = selectionMode
        self.callback = callback    
        self.create_widgets()

    def create_widgets(self):
        PART_COLOR = GUI_COLORS['bg']
        PART2_COLOR = GUI_COLORS['danger']

        self.CONTENT_FRAME = CTkFrame(self,fg_color='#fff')
        self.CONTENT_FRAME.grid(row=0, column=0, sticky='nsew',padx=10, pady=10, )
        self.CONTENT_FRAME.columnconfigure(0, weight=1)
        self.CONTENT_FRAME.rowconfigure(3, weight=1)

        subtitle = CTkFrame(self.CONTENT_FRAME, corner_radius=6, fg_color=PART2_COLOR)
        subtitle.grid(row=0, column=0, sticky='nsew', padx=10, pady=(10,2))

        self.micon = resize_icon(Image.open(f'{IMG_PATH}/management.png'),(45,45))

        ttb.Label(subtitle, image=self.micon, background=PART2_COLOR, ).grid(row=0, column=0, rowspan=2, sticky='nsew', padx=(8), pady=8)

        ttb.Label(subtitle, text='Gestion de Proveedores', background=PART2_COLOR, font=(GUI_FONT,13,'bold'), foreground='#fff').grid(row=0, column=1, sticky='nsew', padx=(4,8), pady=(8,0))

        ttb.Label(subtitle, text='Inicio/Compras', background=PART2_COLOR, font=(GUI_FONT,9), foreground='#fff').grid(row=1, column=1, sticky='nsew', padx=(4,8), pady=(0,8))


     
        ttb.Frame(self.CONTENT_FRAME, bootstyle='primary').grid(row=1, column=0, sticky='nsew', padx=10, pady=5)

        buttons_frame = ttb.Frame(self.CONTENT_FRAME, style='white.TFrame')

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

        if not self.selectionMode:

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

            self.deleteBTN = ButtonImage(buttons_frame, state='disabled', command=self.__deleteProvider, image=self.deleteBTNimg, img_h=self.deleteBTNimgh, img_p=self.deleteBTNimgp, style='flatw.light.TButton', padding=0)
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

        ButtonImage(buttons_frame, command=self.__findProviders, image=self.searchbtnimg, img_h=self.searchbtnimgh, img_p=self.searchbtnimgp, style='flatw.light.TButton', padding=0).grid(row=0, column=7, pady=2, padx=(10,0))

        grid_frame = ttb.Frame(self.CONTENT_FRAME, style='white.TFrame')

        grid_frame.grid(row=3, column=0, columnspan=1, padx=10, pady=(0,10), sticky='nsew')
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.rowconfigure(0, weight=1)

        columns = ('id','rif','name','tlf','address','email', )
        yscroll = ttb.Scrollbar(grid_frame, 
                                orient='vertical',
                                bootstyle="dark-round")
        yscroll.grid(row=0, column=1, padx=1, pady=2,sticky='ns', rowspan=2)

        xscroll = ttb.Scrollbar(grid_frame, 
                                orient='horizontal',
                                bootstyle="dark-round")
        xscroll.grid(row=1, column=0, padx=1, pady=2,sticky='ew')

        self.providerGridView = ttb.Treeview(grid_frame,columns=columns,show='headings', style='cust.primary.Treeview',
                                 height=14, padding=0, xscrollcommand=xscroll.set,
                                selectmode='extended', yscrollcommand=yscroll.set)
        self.providerGridView.grid(row=0,column=0,padx=2,pady=(2,2),sticky='nsew')

        yscroll.configure(command=self.providerGridView.yview)
        xscroll.configure(command=self.providerGridView.xview)

        self.providerGridView.heading("#0")
        self.providerGridView.heading(columns[0], anchor='w', text='ID')
        self.providerGridView.heading(columns[1], anchor='w', text='Rif')
        self.providerGridView.heading(columns[2], anchor='w', text='Nombre de Empresa / Proveedor')
        self.providerGridView.heading(columns[3], anchor='w', text='Telefono')
        self.providerGridView.heading(columns[4], anchor='w', text='Direccion')
        self.providerGridView.heading(columns[5], anchor='w', text='Email')

        self.providerGridView.column('#0', width=0)
        self.providerGridView.column(columns[0], width=80, stretch=False, anchor='center')
        self.providerGridView.column(columns[1], width=150, stretch=False, anchor='center')
        self.providerGridView.column(columns[2], width=300, stretch=False, anchor='w')
        self.providerGridView.column(columns[3], width=200, stretch=False, anchor='w')
        self.providerGridView.column(columns[4], width=400, stretch=False, anchor='w')
        self.providerGridView.column(columns[5], width=200, stretch=False, anchor='w')

        self.providerGridView.tag_configure('row', background='#E7E6E6')
        self.__findProviders()


       
        if self.selectionMode:
            self.providerGridView.bind('<Double-1>', lambda e: self.__select_provider())

        else:
            self.providerGridView.bind('<<TreeviewSelect>>', lambda e: self.__enabled_view())
 
    def __select_provider(self):
        provider = self.__get_selected_provieder()
        if provider:
            self.destroy()
            self.callback(provider)
        del provider


    def __enabled_view(self):
        if self.providerGridView.selection()!= ():
            self.viewBTN.config(state='normal')
            self.editBTN.config(state='normal')
            self.deleteBTN.config(state='normal')
        else:
            self.viewBTN.config(state='disabled')
            self.editBTN.config(state='disabled')
            self.deleteBTN.config(state='disabled')




    def __findProviders(self):
        self.providerGridView.delete(*self.providerGridView.get_children())
        providers = Provider.findAllProvider(name=self.searchEntry.get())
        for provider in providers:
            prov = Provider(**provider)

            self.providerGridView.insert("",
                            ttb.END,
                            values=(prov.id,prov.rif, prov.name, prov.phone, prov.address,prov.email), tags='row')
            
            del prov

    def __deleteProvider(self):
        ask = messagebox.askquestion('Eliminar', 'Desea eliminar el registro del proveedor?', parent=self)
        if ask == 'yes':
            provider = self.__get_selected_provieder()
        
            if provider.check_records():
                provider.delete()
                del provider
                messagebox.showinfo('Aviso','Proveedor Eliminado satisfactoriamente.', parent=self)
                self.__findProviders()
            else:
                messagebox.showinfo('Aviso','El Proveedor no puede ser Eliminado. Se encuentra vinculado a documentos.', parent=self)

    def __open_create_form(self):
        ask = messagebox.askquestion('Registrar','Desea crear un nuevo registro?', parent=self)
        if ask == 'yes':
            waitwindow = ProviderForm(self, window_type='create', title='Registrar Proveedor')
            waitwindow.wait_window()
            self.__findProviders()


    def __open_edit_form(self):
            provider = self.__get_selected_provieder()
            if provider:
                ask = messagebox.askquestion('Modificar','Desea modificar el registro seleccionado?', parent=self)
                if ask == 'yes':
                    waitwindow = ProviderForm(self, window_type='edit', title='Modificar Proveedor', provider=provider)
                    waitwindow.wait_window()
                    self.__findProviders()
            del provider

    def __get_selected_provieder(self,):
        selected = self.providerGridView.focus()

        if selected:
            idP = self.providerGridView.item(selected, 'values')[0]
            provider = Provider.findOneProvider(idP)
            return provider


    def __open_view_form(self):
        provider = self.__get_selected_provieder()

        if provider:
            ProviderView(self, window_type='view', title='Detalles del Proveedor', provider=provider)

        del provider

    
            


if __name__=="__main__":
    app = ttb.Window(themename='new')
  
    SGDB_Style()
    ProviderModule(app)
    app.mainloop()
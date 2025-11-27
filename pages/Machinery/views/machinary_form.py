import ttkbootstrap as ttb


from assets.globals import GUI_COLORS, GUI_FONT, IMG_PATH

from pages.Extras.subtable import SubWindowsSelection
from tkinter import messagebox
from customtkinter import CTkFrame
from PIL import Image, ImageTk
from components.buttons import ButtonImage
from assets.utils import resize_icon, resize_image
import tkinter as tk
from assets.db.db_connection import DB
from models.entitys.machinery import Machinery
from assets.globals import on_validate_length, on_combobox_change, validateFloat



class MachinaryForm(ttb.Toplevel):
    def __init__(self, master=None, window_type = 'create', title = '', machinery = None):
        super().__init__(master)
        
        self.withdraw()
        self.window_title = title
        self.window_type = window_type



        self.__MACHINERY: Machinery = machinery

        ######### VARIABLES #########
        self.__code = ttb.StringVar()
        self.__cost = ttb.StringVar()
        self.__cost.trace_add('write', self.__cost_calculation)

        self.__cost_exchange = ttb.StringVar(value=0.0)

        self.__description = ttb.StringVar()

        self.__brandId = ttb.IntVar()
        self.__brandName = ttb.StringVar()

        self.__modelId = ttb.IntVar()
        self.__modelName = ttb.StringVar()

        self.__state = ttb.IntVar()
        self.__stateName = ttb.StringVar()

        self.provider_var = ttb.IntVar()
        self.provider_var_description = ttb.StringVar()

        self.__currency = ttb.IntVar()
        self.__currencyName = ttb.StringVar()
        self.__currencyValue = ttb.StringVar()
        self.currency_value_var = ttb.DoubleVar()
      
    
        self.__createWidgets()

        if self.__MACHINERY:
            self.__set_machinery_data()

        self.title(title)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.transient()
        self.grab_set()
        self.focus()
        self.config(background="#D9D9D9")
        self.place_window_center()
        self.iconbitmap('SIGAG.ico')
        self.deiconify()


    def __cost_calculation(self, v=None, i=None, m=None):
        currency_value = float(self.__currencyValue.get())
        if currency_value == 0:
            currency_value = 1


        cost = self.__cost.get()
        if not cost:
            cost = 0
        else:
            cost = float(cost)
        self.__cost_exchange.set(cost*currency_value)



    
    def __createWidgets(self):
        


        FGCOLOR = 'white'

        contentFrame = CTkFrame(self, fg_color='white',border_width=1,  border_color='#CFCFCF')
        contentFrame.grid(row = 1, column = 0, sticky = 'nsew', padx=10, pady=10)

        self.__services_icon = resize_icon(Image.open(f"{IMG_PATH}/service.png"))


        titleFrame = CTkFrame(contentFrame, fg_color=GUI_COLORS['warning'])
        titleFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=8, pady=(8,0))
        ttb.Label(titleFrame, image=self.__services_icon, compound='left', text=f' {self.window_title}', font=(GUI_FONT, 14, 'bold'), foreground='white', background=GUI_COLORS['warning']).grid(row=0,column=0, padx=10, pady=10, sticky='nsew')


        machinary_content_frame = tk.Frame(contentFrame)
        machinary_content_frame.config(background=FGCOLOR)
        machinary_content_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)


            ########### Description Section ###########

        mainInforFrame = tk.Frame(machinary_content_frame)
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

        self.codeEntry = ttb.Entry(mainInforFrame,  width=30, textvariable=self.__code,validate='key',validatecommand=(self.register(lambda e: on_validate_length(e,lenght=20)), '%P'))
        self.codeEntry.grid(row=1, column=0, sticky='nsew',pady=(2,0),padx=4, ipady=4, )


        description_label = ttb.Label(mainInforFrame, 
                                      anchor='w', 
                                      text='Descripcion', 
                                      bootstyle='primary', 
                                      background=FGCOLOR,
                                      font=('arial',11,'bold'))
        description_label.grid(row=0, column=1, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')

        self.descriptionEntry = ttb.Entry(mainInforFrame, 
                                       width=100,validate='key',validatecommand=(self.register(lambda e: on_validate_length(e,lenght=200)), '%P'),
                                      textvariable=self.__description)
        self.descriptionEntry.grid(row=1, column=1, sticky='nsew',pady=(2,0),padx=4, ipady=4, )


        moreInfoFrame = tk.Frame(machinary_content_frame)
        moreInfoFrame.config(background=FGCOLOR)
        moreInfoFrame.grid(row=1, column=0, sticky='nsew', pady=(0,10))
        moreInfoFrame.columnconfigure(0, weight=1)
        moreInfoFrame.columnconfigure(1, weight=1)

        brand_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Marca', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=('arial',11,'bold'))
        brand_label.grid(row=0, column=0, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        
        brand_frame = tk.Frame(moreInfoFrame)
        brand_frame.config(background=FGCOLOR)
        brand_frame.grid(row=1, column=0, sticky='nsew' ,pady=(4,0),padx=(4,10),)
        brand_frame.columnconfigure(1,weight=1)

        brand_frame.anchor('w')
        
        d_number_frame = CTkFrame(brand_frame, 
                                   width=35, 
                                   height=30, 
                                   fg_color=GUI_COLORS['light'], 
                                   )
        d_number_frame.grid(row=0, column=0, sticky='nsw')
        d_number_frame.anchor('center')
        d_number_frame.grid_propagate(0)

        ttb.Label(d_number_frame, textvariable=self.__brandId, bootstyle='light inverse').grid(row=0, column=0, sticky='nsew')


        self.brandEntry = ttb.Entry(brand_frame, state='readonly', textvariable=self.__brandName,)
        self.brandEntry.grid(row=0, column=1, sticky='nsew',padx=(4,0), ipady=4,)
        
        if not self.window_type == 'view':
            
            self.brand_search_btn = ttb.Button(brand_frame, 
                                            command=lambda:self.__open_selection_modal('Marcas','brand', self.__set_brand_info),
                                            text='...',
                                            bootstyle='dark')
            self.brand_search_btn.grid(row=0, column=2, padx=2, sticky='nsew', pady=1)              
     
        model_label = ttb.Label(moreInfoFrame, 
                                     anchor='w', 
                                     text='Modelo', 
                                     bootstyle='primary',
                                     background=FGCOLOR ,
                                     font=('arial',11,'bold'))
        model_label.grid(row=0, column=1, padx=(4,0), pady=(2,0), ipadx=8, ipady=8, sticky='nsew')
        
        model_frame = tk.Frame(moreInfoFrame)
        model_frame.config(background=FGCOLOR)
        model_frame.grid(row=1, column=1, sticky='nsew' ,pady=(4,0),padx=(4,10),)
        model_frame.columnconfigure(1,weight=1)

        model_frame.anchor('w')
        
        d_number_frame = CTkFrame(model_frame, 
                                   width=35, 
                                   height=30, 
                                   fg_color=GUI_COLORS['light'], 
                                   )
        d_number_frame.grid(row=0, column=0, sticky='nsw')
        d_number_frame.anchor('center')
        d_number_frame.grid_propagate(0)

        ttb.Label(d_number_frame, bootstyle='light inverse', textvariable=self.__modelId).grid(row=0, column=0, sticky='nsew')


        self.modelEntry = ttb.Entry(model_frame, 
                                    textvariable=self.__modelName, state='readonly'
                                     )
        self.modelEntry.grid(row=0, column=1, sticky='nsew',padx=(4,0), ipady=4,)

        if not self.window_type == 'view':
        
            self.model_search_btn = ttb.Button(model_frame, 
                                            command=lambda:self.__open_selection_modal('Modelos','model', self.__set_model_info),
                                            text='...',
                                            bootstyle='dark')
            self.model_search_btn.grid(row=0, column=2, padx=(2), sticky='nsew', pady=1)



        cost_section_frame = tk.Frame(machinary_content_frame,)
        cost_section_frame.config(background=FGCOLOR)
        cost_section_frame.grid(row=2, column=0,  pady=(4,0), ipadx=8, ipady=8, sticky='nsew')

        CURRENCY =  DB.getCurrencyList()
        CURRENCY_DICT = {row[1]:row[0] for row in CURRENCY}
        CURRENCY_DICT_VALUE = {row[0]:row[2] for row in CURRENCY}
        del CURRENCY
   

            ###### Currency Section ######
        currency_label = ttb.Label(cost_section_frame, 
                                   anchor='w', 
                                   text='Moneda', 
                                   background=FGCOLOR,
                                   font=('arial',11,'bold'))
        currency_label.grid(row=0, column=0, padx=(4,0), pady=(2,0), ipadx=8, sticky='nsew')


        def set_exchange_rate(var,index,mode):
            value = CURRENCY_DICT_VALUE[self.__currency.get()]
            if value == 1:
                value = 0.0
            self.__currencyValue.set(value)
         
     
        
        self.currencyCombobox = ttb.Combobox(cost_section_frame, values=list(CURRENCY_DICT.keys()), state='readonly', style='selectionOnly.TCombobox', textvariable=self.__currencyName, width=30)
        self.currencyCombobox.grid(row=1, column=0, padx=(4,10), pady=(2,0), sticky='nsew')
        self.currencyCombobox.bind("<<ComboboxSelected>>", lambda e: on_combobox_change(e,self.__currency, CURRENCY_DICT, self.currencyCombobox))
        self.currencyCombobox.current(1)
        self.__currency.trace_add('write', set_exchange_rate)
        self.__currency.set(2)


        exchangeFrame = CTkFrame(cost_section_frame, fg_color=GUI_COLORS['info'], corner_radius=3)
        exchangeFrame.grid(row=2, column=0, padx=(4,10), pady=(8,0), sticky='nsew')
        exchangeFrame.anchor('center')


        ttb.Label(exchangeFrame, text='Tasa de Canbio', font=(GUI_FONT,11,'bold'), background=GUI_COLORS['info'], foreground='white').grid(row=0, column=0, padx=5,pady=(5,0), sticky='nsew')
        ttb.Label(exchangeFrame, textvariable=self.__currencyValue, anchor='center', width=8, font=(GUI_FONT,11), background=GUI_COLORS['info'], foreground='white').grid(row=1, column=0, padx=5,pady=(2,5), sticky='nsew')


        cost_label = ttb.Label(cost_section_frame, 
                               anchor='w', 
                               text='Costo Factura', 
                               background=FGCOLOR, 
                               font=('arial',11,'bold'))
        cost_label.grid(row=0, column=1, padx=(4,0), pady=(2,0), ipadx=8, sticky='nsew')



        self.costEntry = ttb.Entry(cost_section_frame, width=30, textvariable=self.__cost,justify='center',
                                    validate="key",validatecommand=(self.register(validateFloat), "%P"))
        self.costEntry.grid(row=1,column=1, padx=(4,10), sticky='nsew', ipady=4,)

        costexchangeFrame = CTkFrame(cost_section_frame, fg_color=GUI_COLORS['light'], corner_radius=3)
        costexchangeFrame.grid(row=2, column=1, padx=(4,10), pady=(8,0), sticky='nsew')
        costexchangeFrame.anchor('center')


        ttb.Label(costexchangeFrame, text='Costo al Cambio', font=(GUI_FONT,11,'bold'), background=GUI_COLORS['light'], foreground=GUI_COLORS['dark']).grid(row=0, column=0, columnspan=2,padx=5,pady=(5,0))
        ttb.Label(costexchangeFrame, textvariable=self.__cost_exchange, anchor='center', width=12, font=(GUI_FONT,11), background=GUI_COLORS['light'], foreground=GUI_COLORS['dark']).grid(row=1, column=0, padx=(5,0),pady=(2,5))
        ttb.Label(costexchangeFrame, text='Bs.', anchor='center', font=(GUI_FONT,11,'bold'), background=GUI_COLORS['light'], foreground=GUI_COLORS['dark']).grid(row=1, column=1, padx=(0,5),pady=(2,5))



        STATE =  DB.getStateMachineryList()
        STATE_DICT = {row[1]:row[0] for row in STATE}
        del STATE
   

            ###### state Section ######
        state_label = ttb.Label(cost_section_frame, 
                                   anchor='w', 
                                   text='Status', 
                                   background=FGCOLOR,
                                   font=('arial',11,'bold'))
        state_label.grid(row=0, column=2, padx=(4,0), pady=(2,0), ipadx=8, sticky='nsew')


  
     
        
        self.stateCombobox = ttb.Combobox(cost_section_frame, values=list(STATE_DICT.keys()), state='readonly', style='selectionOnly.TCombobox', textvariable=self.__stateName, width=30)
        self.stateCombobox.grid(row=1, column=2, padx=(4,10), pady=(2,0), sticky='nsew')
        self.stateCombobox.bind("<<ComboboxSelected>>", lambda e: on_combobox_change(e,self.__state, STATE_DICT, self.stateCombobox))
        self.stateCombobox.current(1)
        self.__state.set(2)


        

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

        
        self.__form_fields =[self.codeEntry, self.descriptionEntry, self.costEntry]
        
        self.__form_variables = [self.__cost, self.__description,  self.__brandId, self.__modelId]


        if self.window_type == 'create':


            creatbtnimg = Image.open(f"{IMG_PATH}/registrar.png")
            self.creatbtnimg = ImageTk.PhotoImage(creatbtnimg.resize(resize_image(20, creatbtnimg.size)))
            creatbtnimgh = Image.open(f"{IMG_PATH}/registrarh.png")
            self.creatbtnimgh = ImageTk.PhotoImage(creatbtnimgh.resize(resize_image(20, creatbtnimgh.size)))
            creatbtnimgp = Image.open(f"{IMG_PATH}/registrarp.png")
            self.creatbtnimgp = ImageTk.PhotoImage(creatbtnimgp.resize(resize_image(20, creatbtnimgp.size)))

            self.createBTN = ButtonImage(buttonss_section_frame, command=self.createMachineryRecord, image=self.creatbtnimg, img_h=self.creatbtnimgh, img_p=self.creatbtnimgp, style='flatw.light.TButton', text='REGISTRAR', compound='center',padding=0)
            self.createBTN.grid(row=0, column=1, sticky='nsew', pady=2, padx=(0,4))

            self.__set_form_state()

        elif self.window_type == 'edit':
            editbtn = Image.open(f"{IMG_PATH}/editn.png")
            self.editbtn = ImageTk.PhotoImage(editbtn.resize(resize_image(20, editbtn.size)))
            editbtnh = Image.open(f"{IMG_PATH}/edith.png")
            self.editbtnh = ImageTk.PhotoImage(editbtnh.resize(resize_image(20, editbtnh.size)))
            editbtnp = Image.open(f"{IMG_PATH}/editp.png")
            self.editbtnp = ImageTk.PhotoImage(editbtnp.resize(resize_image(20, editbtnp.size)))

            self.editBTN = ButtonImage(buttonss_section_frame, command=self.editMachineryRecord, image=self.editbtn, img_h=self.editbtnh, img_p=self.editbtnp, style='flatw.light.TButton', text='MODIFICAR', compound='center',padding=0)
            self.editBTN.grid(row=0, column=2, sticky='nsew', pady=2, padx=(0,4))

            self.__set_form_state()
            self.codeEntry.configure(state='readonly')
        
        else:
            self.__set_form_state('readonly')
            self.currencyCombobox.config(state='disabled')
            self.stateCombobox.config(state='disabled')



    def __set_form_state(self, state = 'normal'):

        for field in self.__form_fields:
            field.config(state=state,cursor='xterm')
          



    def machineryInstance(self):
        return Machinery(
            code=self.__code.get(),
            description=self.__description.get(),
            brand=self.__brandId.get(),
            model=self.__modelId.get(),
            currency=self.__currency.get(),
            status=self.__state.get(),
            cost=self.__cost.get()
        )
    

    def __check_fields(self):
        return not '' in [value.get() for value in self.__form_variables]
    

    def __field_num_entrys(self):
        if not self.__cost.get():
            self.__cost.set(0)
    

    def createMachineryRecord(self):

        if self.__check_fields():
            if Machinery.validate_code(self.__code.get()):
                ask = messagebox.askquestion('Crear','Crear nuevo Equipo?', parent=self)
                if ask == 'yes':
                    self.__field_num_entrys()
                    newMachinery = self.machineryInstance()
                    newMachinery.create()
                    messagebox.showinfo('Aviso','Equipo creado satisfactoriamente.', parent=self)
                    self.destroy()
            else:
                messagebox.showwarning('Aviso','El codigo ingresado ya se encuentra asociado a un registro.', parent=self)
        else:
            messagebox.showwarning('Aviso','Existen algunos campos invalidos o faltan por rellenar.', parent=self)


    def editMachineryRecord(self):
        if self.__check_fields():
            ask = messagebox.askquestion('Modificar','Modificar el Registro del Equipo?', parent=self)
            if ask == 'yes':
                self.__field_num_entrys()
                newMachinery = self.machineryInstance()
                newMachinery.update()
                messagebox.showinfo('Aviso','Registro modificado satisfactoriamente.', parent=self)
                self.destroy()
        else:
            messagebox.showwarning('Aviso','Existen algunos campos invalidos o faltan por rellenar.', parent=self)


    def __set_machinery_data(self):
        self.__code.set(self.__MACHINERY.code)
        self.__description.set(self.__MACHINERY.description)
        
        self.__currency.set(self.__MACHINERY.currency)
        self.__currencyName.set(self.__MACHINERY.get_currency())
        self.__brandId.set(self.__MACHINERY.brand)
        self.__brandName.set(self.__MACHINERY.get_brand())
        self.__modelId.set(self.__MACHINERY.model)
        self.__modelName.set(self.__MACHINERY.get_model())
        self.__cost.set(self.__MACHINERY.cost)
        self.__state.set(self.__MACHINERY.status)
        self.__stateName.set(self.__MACHINERY.get_status())

    
    def __open_selection_modal(self, title, table, callback = None):
        select_window = SubWindowsSelection(window_title=title, database_table=table, callback = callback)
        self.wait_window(select_window)
        self.grab_set()
        self.transient()
    
 



    def __set_brand_info(self, id, description):
        self.__brandId.set(id)
        self.__brandName.set(description)

    def __set_model_info(self, id, provider_name):
        self.__modelId.set(id)
        self.__modelName.set(provider_name)



# app = ttb.Window(themename='new')
# SGDB_Style()
# MachinaryForm(window_type='edit', title='Modificar serviceo')
# app.mainloop()
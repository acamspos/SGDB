import ttkbootstrap as ttb
from assets.globals import GUI_COLORS, IMG_PATH, GUI_FONT, indicator_icon
from assets.utils import resize_icon
from components.buttons import ButtonImage
from PIL import Image
from customtkinter import CTkFrame
import tkinter as tk
from assets.styles.styles import SGDB_Style

###### GRAPH LIBRARIES
from assets.globals import on_validate_length
from tkinter import messagebox
from assets.db.db_connection import DB

class SubWindowsSelection(ttb.Toplevel):
    def __init__(self, master=None, window_title = None, database_table = None, callback = None, *args, **kwargs):
        SGDB_Style()
        super().__init__(master, height=50, width=50)
        PART_COLOR = GUI_COLORS['bg']
        PART2_COLOR = GUI_COLORS['primary']
        self.config(background='#D9D9D9')
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.minsize(width=620, height=60)
        self.transient()
        self.focus()
        self.grab_set()
        self.window_title = window_title
        self.callback = callback

        self.database_table = database_table

        self.edit_mode = False
        self.selection_mode = True
        self.id_var = ttb.StringVar()
        
        ######### GUI ICONS #########

        self.__indicator_icon = resize_icon(indicator_icon, icon_size=(15,15))


        #### Grid Container ######
        self.MAIN_FRAME = CTkFrame(self,fg_color='#fff')
        self.MAIN_FRAME.grid(row=0, column=0, sticky='nsew',padx=10, pady=10, rowspan=2)
        self.MAIN_FRAME.columnconfigure(0, weight=1)
        self.MAIN_FRAME.rowconfigure(4, weight=1)

        subtitle = CTkFrame(self.MAIN_FRAME, corner_radius=6, fg_color=PART2_COLOR)
        subtitle.grid(row=0, column=0, sticky='nsew', padx=10, pady=(10,2))

        self.micon = resize_icon(Image.open(f'{IMG_PATH}/management.png'),(40,40))

        ttb.Label(subtitle, image=self.micon, background=PART2_COLOR, ).grid(row=0, column=0, sticky='nsew', padx=(8), pady=8)

        ttb.Label(subtitle, text=window_title, background=PART2_COLOR, font=(GUI_FONT,16,'bold'), foreground='#fff').grid(row=0, column=1, sticky='nsew', padx=(4,8), pady=(8,8))

        ttb.Frame(self.MAIN_FRAME, bootstyle='primary').grid(row=1, column=0, sticky='nsew', padx=10, pady=5)

        buttons_frame = tk.Frame(self.MAIN_FRAME, background='red')
        buttons_frame.config(background='#fff')
        buttons_frame.grid(row=1, column=0, sticky='nsew', padx=10)
        buttons_frame.columnconfigure(7, weight=1)


        creatbtnimg = Image.open(f"{IMG_PATH}/create.png")
        self.creatbtnimg = resize_icon(creatbtnimg, (50,50))

        creatbtnimgh = Image.open(f"{IMG_PATH}/createh.png")
        self.creatbtnimgh = resize_icon(creatbtnimgh, (50,50))

        creatbtnimgp = Image.open(f"{IMG_PATH}/createp.png")
        self.creatbtnimgp = resize_icon(creatbtnimgp, (50,50))

        self.createBTN = ButtonImage(buttons_frame, image=self.creatbtnimg, img_h=self.creatbtnimgh, img_p=self.creatbtnimgp, command=self.create_record, style='flatw.light.TButton', padding=0)
        self.createBTN.grid(row=0, column=0, sticky='', pady=2, padx=(0,8))


        ttb.Separator(buttons_frame, orient='vertical',bootstyle='dark').grid(row=0, column=1, sticky='ew', padx=(0,8))


        editbtnimg = Image.open(f"{IMG_PATH}/editbtn.png")
        self.editbtnimg = resize_icon(editbtnimg,(50,50))

        editbtnimgh = Image.open(f"{IMG_PATH}/editbtnh.png")
        self.editbtnimgh = resize_icon(editbtnimgh, (50,50))

        editbtnimgp = Image.open(f"{IMG_PATH}/editbtnp.png")
        self.editbtnimgp = resize_icon(editbtnimgp, (50,50))

        self.editBTN = ButtonImage(buttons_frame, image=self.editbtnimg, img_h=self.editbtnimgh, img_p=self.editbtnimgp, style='flatw.light.TButton', padding=0, state='disabled', command=self.edit_record)
        self.editBTN.grid(row=0, column=2, sticky='', pady=2, padx=(0,8))


        deletebtnimg = Image.open(f"{IMG_PATH}/deletebtn.png")
        self.deletebtnimg = resize_icon(deletebtnimg, (50,50))

        deletebtnimgh = Image.open(f"{IMG_PATH}/deletebtnh.png")
        self.deletebtnimgh = resize_icon(deletebtnimgh, (50,50))

        deletebtnimgp = Image.open(f"{IMG_PATH}/deletebtnp.png")
        self.deletebtnimgp = resize_icon(deletebtnimgp, (50,50))

        self.deleteBTN = ButtonImage(buttons_frame, image=self.deletebtnimg, img_h=self.deletebtnimgh, command=self.delete_record, img_p=self.deletebtnimgp, style='flatw.light.TButton', padding=0, state='disabled')
        
        self.deleteBTN.grid(row=0, column=3, sticky='', pady=2, padx=(0,8))


        ttb.Separator(buttons_frame, orient='vertical',bootstyle='dark').grid(row=0, column=4, sticky='ew', padx=(0,8))

        ttb.Separator(buttons_frame, orient='vertical').grid(row=0, column=5, padx=4, pady=6, sticky='nsew')

        cancelBTN = Image.open(f"{IMG_PATH}/cancel.png")
        self.cancelBTN = resize_icon(cancelBTN, (50,50))
        
        cancelhBTN = Image.open(f"{IMG_PATH}/cancelh.png")
        self.cancelhBTN = resize_icon(cancelhBTN, (50,50))

        cancelpBTN = Image.open(f"{IMG_PATH}/cancelp.png")
        self.cancelpBTN = resize_icon(cancelpBTN, (50,50))


        self.cancel_btn = ButtonImage(buttons_frame, 
                                     image=self.cancelBTN,
                                  
                                   img_h=self.cancelhBTN,
                                   img_p=self.cancelpBTN, 
                                   padding=0,
                                   state='disabled',
                                    style='flatw.light.TButton',
                                     command=self.cancel_process
                                     )
        self.cancel_btn.grid(row=0, column=6, padx=(2,5), pady=5, sticky='')


        saveBTN = Image.open(f"{IMG_PATH}/save.png")
        self.saveBTN = resize_icon(saveBTN, (50,50))
        
        savehBTN = Image.open(f"{IMG_PATH}/saveh.png")
        self.savehBTN = resize_icon(savehBTN, (50,50))


        savepBTN = Image.open(f"{IMG_PATH}/savep.png")
        self.saveptBTN = resize_icon(savepBTN, (50,50))

        
     

        self.save_btn = ButtonImage(buttons_frame, 
                                   image=self.saveBTN,
                                  
                                   img_h=self.savehBTN,
                                   img_p=self.saveptBTN, 
                                   padding=0,
                                   state='disabled',
                                   style='flatw.light.TButton',
                                   command=self.save_record)
        self.save_btn.grid(row=0, column=7, padx=(2,10), pady=2, sticky='')


        self.SEARCHENTRY = ttb.Entry(buttons_frame, bootstyle='info', width=30,validate='key',validatecommand=(self.register(lambda e: on_validate_length(e,lenght=100)), '%P'))
        self.SEARCHENTRY.grid(row=0,column=8, ipady=2, padx=(0,8), sticky='e')
        self.SEARCHENTRY.bind('<Return>', lambda e: self.find_records())
        
        searchbtnimg = Image.open(f"{IMG_PATH}/searchbtn.png")
        self.searchbtnimg = resize_icon(searchbtnimg, (50,50))

        searchbtnimgh = Image.open(f"{IMG_PATH}/searchbtnh.png")
        self.searchbtnimgh = resize_icon(searchbtnimgh, (50,50))

        searchbtnimgp = Image.open(f"{IMG_PATH}/searchbtnp.png")
        self.searchbtnimgp = resize_icon(searchbtnimgp, (50,50))

        self.searchBTN = ButtonImage(buttons_frame, image=self.searchbtnimg, img_h=self.searchbtnimgh, command=self.find_records, img_p=self.searchbtnimgp, style='flatw.light.TButton', padding=0)
        self.searchBTN.grid(row=0, column=9, pady=2, padx=(0,0))


        self.new_record_frame = tk.Frame(self.MAIN_FRAME,  border=6,)
        self.new_record_frame.config(background='#fff')
        self.new_record_frame.columnconfigure(3, weight=1)

        ttb.Label(self.new_record_frame, text='Codigo', background='#fff', font=('arial',11,'bold')).grid(row=0, column=0, padx=4)

        self.code_entry = ttb.Entry(self.new_record_frame, width=10, bootstyle='primary', textvariable=self.id_var, state='readonly')
        self.code_entry.grid(row=0, column=1, sticky='nsew', padx=4)

        ttb.Label(self.new_record_frame, text='Descripcion', background='#fff', font=('arial',11,'bold')).grid(row=0, column=2, padx=4)

        self.description_entry = ttb.Entry(self.new_record_frame, bootstyle='primary',validate='key',validatecommand=(self.register(lambda e: on_validate_length(e,lenght=100)), '%P'))
        self.description_entry.grid(row=0, column=3, sticky='nsew', padx=4)

        grid_frame = tk.Frame(self.MAIN_FRAME,)
        grid_frame.config(background='#fff')
        grid_frame.grid(row=4, column=0, columnspan=1, padx=10, pady=(0,10), sticky='nsew')
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.rowconfigure(0, weight=1)


        columns = ('Codigo','Descripcion')

        yscroll = ttb.Scrollbar(grid_frame, 
                                orient='vertical',
                                bootstyle="dark-round")
        yscroll.grid(row=0, column=1, sticky='ns',rowspan=2)

    
        self.dataGrid = ttb.Treeview(grid_frame,
                                columns=columns,
                                bootstyle='dark', 
                                height=10)
        self.dataGrid.grid(row=0,column=0, sticky='nsew')

        self.dataGrid.bind('<<TreeviewSelect>>', lambda e: self.select_item())
        self.dataGrid.bind('<Double-1>', lambda e: self.select_info())

        self.dataGrid.heading('#0')
        self.dataGrid.heading('Codigo',text='Codigo', anchor='w')
        self.dataGrid.heading("Descripcion", text='Descripcion', anchor='w')

        
        self.dataGrid.column('#0', width=50, stretch=False,anchor='w')
        self.dataGrid.column(columns[0],width=120,stretch=False,anchor='w')
        self.dataGrid.column(columns[1],width=200,stretch=True,anchor='w')

        self.find_records()

        self.row_selected = None


    def select_item(self):
        if not self.row_selected is None and self.row_selected != self.dataGrid.focus():
            self.dataGrid.item(self.row_selected, image='')

        self.row_selected = self.dataGrid.focus()
        
        if self.row_selected:   
            self.dataGrid.item(self.row_selected, image=self.__indicator_icon)
            self.editBTN.config(state='normal')
            self.deleteBTN.config(state='normal')
        else:
            self.editBTN.config(state='disabled')
            self.deleteBTN.config(state='disabled')

    def display_record(self):
        self.buttons_state('disabled')
        self.dataGrid.config(selectmode='none')
        self.new_record_frame.grid(row=2, column=0, sticky='nsew', padx=4,pady=4)
        self.selection_mode = False

        # self.code_entry.insert(0, len(data[self.window_title])+1)
    def create_record(self):
        self.display_record()
        self.id_var.set(DB.get_next_id_subtable(self.database_table)[0])
    

    def cancel_process(self):
        if messagebox.askquestion('Confirmacion','Desea cancelar este proceso?', parent=self)  == 'yes':
            self.close_record()
        self.dataGrid.config(selectmode='browse')

    def close_record(self):
       
        self.buttons_state()
        self.id_var.set(None)
        self.description_entry.delete(0, ttb.END)
        self.new_record_frame.grid_forget()
        self.edit_mode = False
        self.selection_mode = True
        
    
    def save_record(self):
        ask = messagebox.askquestion('Confirmacion','Desea guardar los datos?', parent=self)
        if ask == 'yes':
            if not self.edit_mode:
                DB.subTable_insert(self.database_table, self.description_entry.get())
            else:
                DB.subTable_Update(self.database_table,self.description_entry.get(),self.id_var.get())
            messagebox.showinfo('Almacenamiento', 'Datos almacenados exitosamente.', parent=self)
            self.find_records()
            self.close_record()
        self.dataGrid.config(selectmode='browse')


    def buttons_state(self, state = 'normal',):
        states: list = ['normal','disabled']
        if state == 'disabled':
            states.reverse()
        self.save_btn.config(state=states[1])
        self.cancel_btn.config(state=states[1])
        self.createBTN.config(state=states[0])
        self.SEARCHENTRY.config(state=states[0])
        self.searchBTN.config(state=states[0])

        if state == 'normal' and not self.dataGrid.focus():
            states.reverse()
        self.deleteBTN.config(state=states[0])
        self.editBTN.config(state=states[0])

    def edit_record(self):
            if messagebox.askquestion('Actualizar','Desea modificar el registro seleccionado?', parent=self) == 'yes':
                self.edit_mode = True
                self.display_record()
                data = self.dataGrid.item(self.dataGrid.focus(), 'values')
                self.id_var.set(data[0])
                self.description_entry.insert(0, data[1])

    def delete_record(self):
        ask = messagebox.askokcancel('Eliminar','Desea Eliminar este registro?',parent=self)
        if ask:
            focus = self.dataGrid.focus()
            item = self.dataGrid.item(focus, 'values')[0]
            DB.subTable_delete(self.database_table, item)
            messagebox.showinfo('Almacenamiento','El registro se ha eliminado satisfactoriamente!', parent=self)
            self.find_records()

    def delete_info(self):
        self.callback('','')
        self.destroy()

    def select_info(self):
        row = self.dataGrid.focus()
        if row and self.selection_mode:
            info_selected = self.dataGrid.item(row, 'values')
            self.callback(info_selected[0], info_selected[1])
            self.destroy()
    
    def find_records(self):
        self.row_selected = None
        self.dataGrid.delete(*self.dataGrid.get_children())
        records = DB.subTable_find(self.database_table, self.SEARCHENTRY.get())
        if records:
            for record in records:
                self.dataGrid.insert("",ttb.END,values=(record['id'],record['description']),)

      

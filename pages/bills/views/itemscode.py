import ttkbootstrap as ttb
from assets.globals import GUI_COLORS, IMG_PATH, GUI_FONT
from assets.utils import resize_image, resize_icon
from PIL import Image, ImageTk
from tkinter import messagebox
import tkinter as tk
from components.buttons import ButtoLabel, ButtonImage
from ttkbootstrap.scrolled import ScrolledFrame
from models.entitys.activity import Activity
from customtkinter import CTkFrame #767171
from assets.db.db_connection import DB
from assets.styles.styles import SGDB_Style
from tkinter import ttk
from datetime import datetime
from models.entitys.bills import Item, Bill
FGCOLOR = 'white'

def tiene_duplicados(lista):
    return len(lista) != len(set(lista))


class ItemsCodePosition(ttb.Toplevel):
    def __init__(self, master=None, bill = None, *args, **kwargs):
        super().__init__(master,background='red')
        SGDB_Style()
        
        # SYSTEM_WIDTH = self.winfo_screenwidth()
        # SYSTEM_HEIGHT = self.winfo_screenheight()

        # pwidth = (SYSTEM_WIDTH-671)//2
        # pheight = (SYSTEM_HEIGHT-507)//2

        # self.geometry(str(671)+"x"+str(507)+"+"+str(pwidth)+"+"+str(pheight-60))
        self.minsize(width=920,height=507)
        self.title('Documentos de Aceptacion')
        self.success_code = False
        self.config(background='#D0CECE')
        self.withdraw()
        self.focus()

        self.transient()
        
        self.anchor('center')
        
  
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)  
        self.grab_set()

       
        self.__BILL: Bill = bill
        
        ### VARS ####


      
      
        self.create_widgets()


        self.deiconify()

    def create_widgets(self):


        contentFrame = CTkFrame(self, fg_color='white',border_width=1,  border_color='#CFCFCF')
        contentFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=10, pady=10)
        contentFrame.columnconfigure(0, weight=1)
        contentFrame.rowconfigure(1, weight=1)        

        self.__services_icon = resize_icon(Image.open(f"{IMG_PATH}/task_icon.png"))


        titleFrame = CTkFrame(contentFrame, fg_color=GUI_COLORS['primary'])
        titleFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=8, pady=(8,0))
        ttb.Label(titleFrame, image=self.__services_icon, compound='left', text=' Codigos de Documentos de Aceptacion', font=(GUI_FONT, 14, 'bold'), foreground='white', background=GUI_COLORS['primary']).grid(row=0,column=0, padx=10, pady=10, sticky='nsew')


        self.mainContent = tk.Frame(contentFrame)
        self.mainContent.config(background=FGCOLOR)
        self.mainContent.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        self.mainContent.columnconfigure(0, weight=1)
        self.mainContent.rowconfigure(0, weight=1)


            ########### Description Section ###########

        
        ttb.Separator(self.mainContent, bootstyle='light').grid(row=2, column=0, sticky='nsew', columnspan=2)


        buttonss_section_frame = tk.Frame(self.mainContent,)
        buttonss_section_frame.configure(background=FGCOLOR)
        buttonss_section_frame.grid(row=3, column=0, pady=(8,8), sticky='nsew', columnspan=2)
        buttonss_section_frame.anchor('e')



        closeimg = Image.open(f"{IMG_PATH}/closen.png")
        self.closeimg = ImageTk.PhotoImage(closeimg.resize(resize_image(20, closeimg.size)))
        closeimgh = Image.open(f"{IMG_PATH}/closeh.png")
        self.closeimgh = ImageTk.PhotoImage(closeimgh.resize(resize_image(20, closeimgh.size)))
        closeimgp = Image.open(f"{IMG_PATH}/closep.png")
        self.closeimgp = ImageTk.PhotoImage(closeimgp.resize(resize_image(20, closeimgp.size)))
        self.closeBTN = ButtonImage(buttonss_section_frame, image=self.closeimg, img_h=self.closeimgh, command=self.destroy, img_p=self.closeimgp, style='flatw.light.TButton', text='CERRAR', compound='center',padding=0)
        self.closeBTN.grid(row=0, column=0, sticky='nsew', pady=2, padx=(0,4))



        processimg = Image.open(f"{IMG_PATH}/registrar.png")
        self.processimg = ImageTk.PhotoImage(processimg.resize(resize_image(20, processimg.size)))
        processimgh = Image.open(f"{IMG_PATH}/registrarh.png")
        self.processimgh = ImageTk.PhotoImage(processimgh.resize(resize_image(20, processimgh.size)))
        processimgp = Image.open(f"{IMG_PATH}/registrarp.png")
        self.processimgp = ImageTk.PhotoImage(processimgp.resize(resize_image(20, processimgp.size)))

        self.processBTN = ButtonImage(buttonss_section_frame, command=self.process_activity, image=self.processimg, img_h=self.processimgh, img_p=self.processimgp, style='flatw.light.TButton', text='PROCESAR', compound='center',padding=0)
        self.processBTN.grid(row=0, column=2, sticky='nsew', pady=2, padx=(0,4))

        self.create_othersWidgets()
        self.__set_tasks()

    def create_othersWidgets(self):
            
        task_list_frame = tk.Frame(master=self.mainContent, width=800, height=600)
        task_list_frame.configure(background='#fff')
        task_list_frame.grid(row=0, column=0, padx=10, pady=(5,10), sticky='nsew')
        task_list_frame.columnconfigure(0, weight=1)
        task_list_frame.rowconfigure(4, weight=1)

        
        self.scroll_frame_content = ScrolledFrame(task_list_frame, style='white.TFrame', bootstyle='round dark')
        self.scroll_frame_content.grid(row=4, column=0, sticky='nsew', padx=4)
      
        self.scroll_frame_content.columnconfigure(1, weight=3)
        self.scroll_frame_content.columnconfigure(2, weight=1)
    

        ttb.Label(self.scroll_frame_content, background='#fff', justify='center', text=f'Posicion', font=('arial',11,'bold'),).grid(row=0, column=0, sticky='nsew')

        ttb.Label(self.scroll_frame_content, background='#fff', justify='center', text=f'Descripcion', font=('arial',11,'bold'),).grid(row=0, column=1, sticky='nsew')

        ttb.Label(self.scroll_frame_content, background='#fff', justify='center', text=f'Cantidad', font=('arial',11,'bold'),).grid(row=0, column=2, sticky='')

        ttb.Label(self.scroll_frame_content, background='#fff', justify='center', text=f'Codigo', anchor='center', font=('arial',11,'bold'),).grid(row=0, column=3, sticky='nsew',padx=(0,18))

        ttb.Separator(self.scroll_frame_content, bootstyle='dark').grid(row=1, column=0, columnspan=4, pady=(10,10), padx=(0,18),sticky='nsew')
 
        self.data_update = []
        self.codesvar = []
        self.checkboxes = []

    def change_task_state(self,index, idT):
            DB.update_task(idT=idT,state=self.codesvar[index].get())
            self.check_activit_progress()

    
    def check_activit_progress(self):
            if 0 not in [x.get() for x in self.codesvar]:
                self.processBTN.config(state='normal')
            else:
                self.processBTN.config(state='disabled')

    def process_activity(self):

        if tiene_duplicados([row[0].get() for row in self.data_update]):
            messagebox.showwarning('Posiciones','Existen posiciones duplicadas!', parent=self)
        else:
            ask = messagebox.askquestion(title='Confirmacion', message='Desea Procesar los Codigos?', parent=self)
            if ask == 'yes':
                data = [(row[0].get() if row[0].get() else None,row[1].get()  if row[1].get() else None,row[2],row[3]) for row in self.data_update]
                Item.set_documentCode(data)
                self.destroy()
                self.success_code = True

    def __set_tasks(self):
        tasks = Item.findAllItems(self.__BILL.code)
        if tasks:
            for index, task in enumerate(tasks):
                item = Item(**task)
                #ttb.Label(self.cont, text=f'Task #{index+1}', font=('arial',11,'bold'), foreground=GUI_COLORS['danger'], padding=5, ).grid(row=index*2+2, column=0, sticky='nsew',padx=5,pady=5)
                positionvar = ttb.StringVar()
                entryposition = ttk.Entry(self.scroll_frame_content, textvariable=positionvar)
                entryposition.grid(row=index*2+2, column=0, sticky='', padx=(0,26))


                ttb.Label(self.scroll_frame_content, background='#fff', text=f'{item.itemDescription}',width=30, font=('arial',11),).grid(row=index*2+2, column=1, sticky='nsew')

                ttb.Label(self.scroll_frame_content, background='#fff', justify='center', text=f'{item.quantity}', font=('arial',11),).grid(row=index*2+2, column=2, sticky='')

                codevar = ttb.StringVar()# Variable para almacenar el estado del checkbox (1 para marcado, 0 para desmarcado)
                
          


                entrycode = ttk.Entry(self.scroll_frame_content, textvariable=codevar)
                
                # Agregar la variable a la lista de self.codesvar y el entrycode a la lista de entrycodes
        
                self.codesvar.append(codevar)
                self.checkboxes.append(entrycode)
                
                self.data_update.append([positionvar,codevar,item.itemId,self.__BILL.code])

                entrycode.grid(row=index*2+2, column=3, sticky='', padx=(0,26))

                ttb.Separator(self.scroll_frame_content, bootstyle='light').grid(row=index*2+3, column=0, columnspan=4, padx=(0,18),pady=(10,15),sticky='nsew')


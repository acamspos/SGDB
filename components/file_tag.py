import tkinter as tk
import ttkbootstrap as ttb
from assets.globals import close_icon
from assets.utils import resize_icon
from components.buttons import IconButton

class FileTag(ttb.Frame):
    def __init__(self, master = None, bg='#EAEAEA', path:str = '', file_name:str = '',  display:str = 'column', callback = None):
        super().__init__(master)
        self.style = ttb.Style()
        self.style.configure('tagfile.TFrame', background=bg)
        self.configure(style='tagfile.TFrame')
        self.anchor('center')
        self.columnconfigure(0, weight=1)

        self.path = path
        self.callback = callback
        
        dataFrame = ttb.Frame(self, style='tagfile.TFrame')
        dataFrame.grid(row=0, column=0, padx=(4,12), sticky='nsew')
        dataFrame.anchor('w')

        file_name_label = ttb.Label(dataFrame, text=file_name, justify='center', anchor='w', font=('arial',10, 'bold'), 
                                    bootstyle='primary', background=bg)
        file_name_label.grid(row=0, column=0, sticky='nsew', pady=0, padx=(0,2))

        file_size_label = ttb.Label(dataFrame, text='(13 K)', justify='center', anchor='w', font=('arial',10, 'bold'), )
        file_size_label.grid(row=0, column=1, sticky='nsew', pady=0, )
        file_size_label.config( background=bg)


        self.__close_icon = resize_icon(close_icon, icon_size=(26,26))
        IconButton(self, image=self.__close_icon, bg=bg, command=lambda:self.delete_command()).grid(row=0, column=1, sticky='nsew', padx=6, pady=6)

    def delete_command(self):
        if self.callback:
            self.callback(self.path)
        self.destroy()

class EmailTag(ttb.Frame):
    def __init__(self, master = None, bg='#EAEAEA', email:str = '', user_name:str = '',  display:str = 'column', callback = None):
        super().__init__(master)
        self.style = ttb.Style()
        self.style.configure('tagfile.TFrame', background=bg)
        self.configure(style='tagfile.TFrame')
        self.anchor('center')
        self.columnconfigure(0, weight=1)

        self.email = email
        self.callback = callback
        
        dataFrame = ttb.Frame(self, style='tagfile.TFrame')
        dataFrame.grid(row=0, column=0, padx=(4,12), sticky='nsew')
        dataFrame.anchor('w')

        file_name_label = ttb.Label(dataFrame, text=f"{user_name} ({self.email})", justify='center', anchor='w', font=('arial',10, 'bold'), 
                                    bootstyle='primary', background=bg)
        file_name_label.grid(row=0, column=0, sticky='nsew', pady=0, padx=(0,2))

        self.__close_icon = resize_icon(close_icon, icon_size=(22,22))
        IconButton(self, image=self.__close_icon, bg=bg, command=lambda:self.delete_command()).grid(row=0, column=1, sticky='nsew', padx=6, pady=6)

    def delete_command(self):
        if self.callback:
            self.callback(self.email)
        self.destroy()
    
                

# app = ttb.Window()
# app.columnconfigure(0, weight=1)
# FileTag(file_name='Facturas 225.pdf').grid(row=0, column=0, padx=6, pady=6, sticky='nsew')
# app.mainloop()

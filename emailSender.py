import ttkbootstrap as ttb
import re

from ttkbootstrap.scrolled import ScrolledFrame
from components.file_tag import FileTag, EmailTag
from assets.globals import GUI_COLORS, GUI_FONT, IMG_PATH

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from email.mime.base import MIMEBase
from email import encoders
from pages.clients.clients import ClientModule
from pages.providers.providers import ProviderModule
from pages.representative.representative import RepresentativeModule
from customtkinter import CTkFrame
from PIL import Image, ImageTk
from components.buttons import ButtonImage
from assets.utils import resize_icon, resize_image
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
FGCOLOR = 'white'

pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
class EmailSender(ttb.Toplevel):
    def __init__(self, master=None, user = [], subject = '', callback = None, file = ''):
        super().__init__(master)
        self.withdraw()
        self.focus()

        
        
        self.window_title = 'Gestor de Correos'
        ######### MODAL WINDOW CONFIG #########

        self.title('Gestor de Correos')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.transient()
        self.grab_set()
        self.config(background="#fff")
       

        self.callback = callback
        self.from_addr = ttb.StringVar(value='camposagustinrc@gmail.com')
        self.to_addr = ttb.StringVar()
        self.subject = ttb.StringVar(value=subject)
        self.content = ttb.StringVar()
        self.files = []
        self.emails = []

        

        self.__createWidgets()

        

        self.place_window_center()
        self.iconbitmap('SIGAG.ico')
        self.deiconify()
        if user != []:
            for us in user:
                self.add_user(us[0],us[1])
        if file:
            self.unpload_file(file)

    
    def __createWidgets(self):
        


        

        contentFrame = CTkFrame(self, fg_color='white',border_width=1,  border_color='#CFCFCF')
        contentFrame.grid(row = 1, column = 0, sticky = 'nsew', padx=10, pady=10)
        contentFrame.columnconfigure(0, weight=1)


        self.__products_icon = resize_icon(Image.open(f"{IMG_PATH}/email.png"), )


        titleFrame = CTkFrame(contentFrame, fg_color='#212946')
        titleFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=8, pady=(8,0))
        titleFrame.columnconfigure(0, weight=1)
        
        ttb.Label(titleFrame, image=self.__products_icon, compound='left', text=f' {self.window_title}', font=(GUI_FONT, 14, 'bold'), foreground='white', background='#212946').grid(row=0,column=0, padx=10, pady=10, sticky='nsew')

        
        ttb.Separator(contentFrame, bootstyle='light').grid(row=1, column=0, sticky='nsew', columnspan=2, padx=10,pady=(8,0))
       

        self.MAIN_FRAME = tk.Frame(contentFrame)
        self.MAIN_FRAME.config(background=FGCOLOR)
        self.MAIN_FRAME.grid(row=2, column=0, sticky='nsew', padx=10, pady=(15,20))
        self.MAIN_FRAME.columnconfigure(0, weight=1)


        ttb.Separator(contentFrame, bootstyle='light').grid(row=3, column=0, sticky='nsew', columnspan=2, padx=10)


        buttonss_section_frame = tk.Frame(contentFrame,)
        buttonss_section_frame.configure(background=FGCOLOR)
        buttonss_section_frame.grid(row=4, column=0, pady=(8,8), padx=10, sticky='nsew', columnspan=2)
        buttonss_section_frame.anchor('e')
 

        closeimg = Image.open(f"{IMG_PATH}/closen.png")
        self.closeimg = ImageTk.PhotoImage(closeimg.resize(resize_image(20, closeimg.size)))
        closeimgh = Image.open(f"{IMG_PATH}/closeh.png")
        self.closeimgh = ImageTk.PhotoImage(closeimgh.resize(resize_image(20, closeimgh.size)))
        closeimgp = Image.open(f"{IMG_PATH}/closep.png")
        self.closeimgp = ImageTk.PhotoImage(closeimgp.resize(resize_image(20, closeimgp.size)))
        self.closeBTN = ButtonImage(buttonss_section_frame, image=self.closeimg, img_h=self.closeimgh, command=self.destroy, img_p=self.closeimgp, style='flatw.light.TButton', text='CERRAR', compound='center',padding=0)
        self.closeBTN.grid(row=0, column=0, sticky='nsew', pady=2, padx=(0,8))



        findFileimg = Image.open(f"{IMG_PATH}/findfile.png")
        self.findFileimg = ImageTk.PhotoImage(findFileimg.resize(resize_image(20, findFileimg.size)))
        findFileimgh = Image.open(f"{IMG_PATH}/findfileh.png")
        self.findFileimgh = ImageTk.PhotoImage(findFileimgh.resize(resize_image(20, findFileimgh.size)))
        findFileimgp = Image.open(f"{IMG_PATH}/findfilep.png")
        self.findFileimgp = ImageTk.PhotoImage(findFileimgp.resize(resize_image(20, findFileimgp.size)))

        self.findFileBTN = ButtonImage(buttonss_section_frame,   image=self.findFileimg, img_h=self.findFileimgh, 
                                       img_p=self.findFileimgp, style='flatw.light.TButton', padding=0,
                                       command=self.add_file)
        self.findFileBTN.grid(row=0, column=1, sticky='nsew', pady=2, padx=(0,4))



        boldimg = Image.open(f"{IMG_PATH}/bold.png")
        self.boldimg = ImageTk.PhotoImage(boldimg.resize(resize_image(20, boldimg.size)))
        boldimgh = Image.open(f"{IMG_PATH}/boldh.png")
        self.boldimgh = ImageTk.PhotoImage(boldimgh.resize(resize_image(20, boldimgh.size)))
        boldimgp = Image.open(f"{IMG_PATH}/boldp.png")
        self.boldimgp = ImageTk.PhotoImage(boldimgp.resize(resize_image(20, boldimgp.size)))

        self.boldBTN = ButtonImage(buttonss_section_frame,   image=self.boldimg, img_h=self.boldimgh, img_p=self.boldimgp, 
                                   style='flatw.light.TButton', padding=0, command=self.add_style)
        self.boldBTN.grid(row=0, column=2, sticky='nsew', pady=2, padx=(0,4))




        sendBTNimg = Image.open(f"{IMG_PATH}/editn.png")
        self.sendBTNimg = ImageTk.PhotoImage(sendBTNimg.resize(resize_image(20, sendBTNimg.size)))
        sendBTNimgh = Image.open(f"{IMG_PATH}/edith.png")
        self.sendBTNimgh = ImageTk.PhotoImage(sendBTNimgh.resize(resize_image(20, sendBTNimgh.size)))
        sendBTNimgp = Image.open(f"{IMG_PATH}/editp.png")
        self.sendBTNimgp = ImageTk.PhotoImage(sendBTNimgp.resize(resize_image(20, sendBTNimgp.size)))

        self.createBTN = ButtonImage(buttonss_section_frame,   image=self.sendBTNimg, img_h=self.sendBTNimgh, 
                                     img_p=self.sendBTNimgp, style='flatw.light.TButton', text='ENVIAR', 
                                     compound='center',padding=0, command=self.send_email)
        self.createBTN.grid(row=0, column=3, sticky='nsew', pady=2, padx=(4,4))

        
        

        self.mainPage()


    def mainPage(self):
        send_email_frame = ttb.Frame(self.MAIN_FRAME,style='white.TFrame',)
        send_email_frame.grid(row=0, column=0, sticky='nsew')
        send_email_frame.columnconfigure(0, weight=1)

      
        ttb.Label(send_email_frame, text='Correos', font=(GUI_FONT,11,'bold'),background='#fff').grid(row=0, column=0, padx=5, pady=5, sticky='nsew')


        emailsFrame = ttb.Frame(send_email_frame, style='white.TFrame')
        emailsFrame.grid(row=1, column=0, sticky='nswe')
        emailsFrame.columnconfigure(0, weight=1)

        self.send_to_entry = ttb.Entry(emailsFrame, width=60, )
        self.send_to_entry.grid(row=0, column=0, sticky='nswe', ipady=5,pady=2)
        self.send_to_entry.bind('<Return>', lambda e: self.add_user(email=self.to_addr.get(), user_name= 'Gust'))


        addimg = Image.open(f"{IMG_PATH}/create.png")
        self.addimg = ImageTk.PhotoImage(addimg.resize(resize_image(16, addimg.size)))
        addimgh = Image.open(f"{IMG_PATH}/createh.png")
        self.addimgh = ImageTk.PhotoImage(addimgh.resize(resize_image(16, addimgh.size)))
        addimgp = Image.open(f"{IMG_PATH}/createp.png")
        self.addimgp = ImageTk.PhotoImage(addimgp.resize(resize_image(16, addimgp.size)))

        self.addBTN = ButtonImage(emailsFrame,  image=self.addimg, img_h=self.addimgh, img_p=self.addimgp, 
                                  style='flatw.light.TButton', padding=0, command=lambda:self.add_user(email=self.send_to_entry.get()))
        self.addBTN.grid(row=0, column=1, sticky='', padx=(4,1))




        findimg = Image.open(f"{IMG_PATH}/searchbtn.png")
        self.findimg = ImageTk.PhotoImage(findimg.resize(resize_image(16, findimg.size)))
        findimgh = Image.open(f"{IMG_PATH}/searchbtnh.png")
        self.findimgh = ImageTk.PhotoImage(findimgh.resize(resize_image(16, findimgh.size)))
        findimgp = Image.open(f"{IMG_PATH}/searchbtnp.png")
        self.findimgp = ImageTk.PhotoImage(findimgp.resize(resize_image(16, findimgp.size)))

        self.findBTN = ButtonImage(emailsFrame,   image=self.findimg, img_h=self.findimgh, img_p=self.findimgp, style='flatw.light.TButton', padding=0, command=self.select_company_type)
        self.findBTN.grid(row=0, column=2, sticky='', padx=(0,0))




        self.email_list_frame = ScrolledFrame(send_email_frame, autohide=False, height=80, style='white.TFrame', bootstyle='round dark')
        self.email_list_frame.grid(row=2, column=0, sticky='nsew',pady=2,padx=2)




        ttb.Label(send_email_frame, 
                  text='Asunto', 
                    background='#fff',
                  font=(GUI_FONT,11,'bold')
        ).grid(row=3, column=0, padx=4, pady=(0,0), ipadx=8, ipady=4, sticky='nsew')
        
        subject_entry = ttb.Entry(send_email_frame, width=80)
        subject_entry.grid(row=4, column=0, sticky='nsew',pady=(2,0),padx=4,ipady=6)

            ### EMAIL BODY ###
        ttb.Label(send_email_frame, 
                  text='Mensaje', 
                   background='#fff',
                  font=(GUI_FONT,11,'bold')
        ).grid(row=5, column=0, padx=4, pady=(4,0), ipadx=8, ipady=8, sticky='nsew')

        self.contentText = ttb.Text(send_email_frame, height=6)
        self.contentText.config(highlightbackground=GUI_COLORS['info'],highlightcolor=GUI_COLORS['info'])
        self.contentText.grid(row=6, column=0, sticky='nsew',pady=(4,0),padx=4)


        filesFrame = ttb.Frame(send_email_frame, style='white.TFrame')
        filesFrame.grid(row=7, column=0,padx=4, sticky='nsew',pady=(4,0))
        filesFrame.columnconfigure(0, weight=1)

        ttb.Label(filesFrame, 
                  text='Files', 
                  background='#fff',
                  font=(GUI_FONT,11,'bold')
        ).grid(row=0, column=0, padx=1, pady=1, ipadx=8, ipady=4, sticky='nsew')
        
        self.file_list_frame = ScrolledFrame(filesFrame, autohide=False, height=80, style='white.TFrame', bootstyle='dark round')
        self.file_list_frame.grid(row=1, column=0, sticky='nsew',pady=2,padx=2)
        self.file_list_frame.columnconfigure(0, weight=1)



        # if user != {}:
        #     self.to_addr.set(user['email'])
        #     self.add_user(email=user['email'], user_name= user['name'])



    def add_user(self, email:str, user_name = ''):
        user_email = email.replace(" ",'')

        if not re.match(pattern, user_email):
            messagebox.showwarning('Email', 'La dirección ingresada es invalida.\n Por favor, verifique e intente nuevamente.',parent=self)
        else:
            emailtag = EmailTag(self.email_list_frame, email=user_email, user_name=user_name, callback=self.delete_emails_callback)
            emailtag.pack(fill='both', expand=True, padx=(4,18), pady=2)
            self.emails.append(user_email)
            self.to_addr.set('')

    def add_file(self):
        self.get_html_format()
        file = askopenfilename(parent=self)
        if file:
            self.unpload_file(file)

    def unpload_file(self, file):
        file_tag = FileTag(self.file_list_frame,
                    path = file,
                    file_name=file.replace('\\','/').split('/')[-1],
                    callback = self.delete_callback
        )
        file_tag.pack(fill='both', expand=True, padx=(4,18), pady=2)
        self.files.append(file.replace('\\','/'))

    def delete_callback(self, file):
        self.files.remove(file)
    
    def delete_emails_callback(self, email):
        self.emails.remove(email)
        
    def add_style(self,):
        if self.contentText.tag_ranges("sel"):
            start = self.contentText.index(ttb.SEL_FIRST).split('.')[1]
            final = self.contentText.index(ttb.SEL_LAST).split('.')[1]
            self.contentText.tag_config("bold",font=('arial',10, 'bold'))
            text = self.contentText.tag_nextrange("bold",f"1.{int(start)}", f"1.{int(final)}")   
            for index in range(int(start), int(final)):
                if "bold" in self.contentText.tag_names(f"1.{index}"):
                    self.contentText.tag_remove('bold',f"1.{int(index)}", f"1.{int(index+1)}")
                else: 
                    self.contentText.tag_add("bold",f"1.{int(index)}", f"1.{int(index+1)}")
                

    def get_html_format(self):
        text = self.contentText.get('1.0', ttb.END)
        bold = False
        add_lenght=0
        for index in range(0, len(text)):
            if "bold" in self.contentText.tag_names(f"1.{index}") and bold == False:
                text = text[:index+add_lenght] + '<strong>' + text[index+add_lenght:]
                bold = True
                add_lenght += len('<strong>')
            elif not "bold" in self.contentText.tag_names(f"1.{index}") and bold: 
                text = text[:index + add_lenght] + '</strong>' + text[index + add_lenght:]
                add_lenght += len('</strong>')
                bold = False
    
        return text
       
    def send_email(self):
        if len(self.emails) > 0:
            if messagebox.askokcancel('Email','Desea enviar este correo electronico?', parent=self):    
                msg = MIMEMultipart()
                msg['From'] = self.from_addr.get()
                msg['To'] = self.to_addr.get()
                msg['Subject'] = self.subject.get()
                body = MIMEText(self.get_html_format(), 'html','utf-8')
    
                msg.attach(body)
                for file in self.files:
                 
                    with open(file, 'rb') as f:
                        attpac = MIMEBase('application', 'octet-stream')
                        attpac.set_payload((f).read())
                        encoders.encode_base64(attpac)
                        attpac.add_header('Content-disposition', 'attatchment', filename=('utf-8', '', file.replace('\\','/').split('/')[-1]))
                        #('Content-Disposition', 'attachment; filename= '+file.replace('\\','/').split('/')[-1])
                    msg.attach(attpac)
                text = msg.as_string()
                with smtplib.SMTP(port=587,host="smtp.gmail.com") as connection:
                    connection.starttls()
                    connection.login(user=self.from_addr.get(),password='fjnj octc lxao keyo')
                    connection.sendmail(self.from_addr.get(), self.emails, text)
                if self.callback:
                    self.callback()
                messagebox.showinfo('Email', 'Mensaje enviado satisfactoriamente.', parent=self)
                self.destroy()
        else:
            messagebox.showwarning('Email', 'Debe Ingresar una dirección de correo electronico.', parent=self)


    def select_company_type(self):

        def set_email(company):
            self.add_user(email=company.email, user_name=company.name)

        def set_representative(repre):
            self.add_user(email=repre.email, user_name=f"{repre.name} {repre.lastname}")

        def open_window(rol=''):
      
            window.destroy()
            if rol == 'prov':
                aux_window = ProviderModule(self, callback=set_email,selectionMode=True)
            elif rol=='client':
                aux_window = ClientModule(self, callback=set_email,selectionMode=True)
            else:
                aux_window = RepresentativeModule(self, callback=set_representative,selectionMode=True)
            

        window = ttb.Toplevel(title='Orden de Compraa', toolwindow=True)
        window.withdraw()
        window.resizable(0,0)
        window.focus()
        window.grab_set()
        auxFrame = CTkFrame(window, fg_color='white')
        auxFrame.grid(row=0, column=0, padx=10, pady=10)




        clientimg = Image.open(f"{IMG_PATH}/greenButton.png")
        self.clientimg = ImageTk.PhotoImage(clientimg.resize(resize_image(19, clientimg.size)))
        clientimgh = Image.open(f"{IMG_PATH}/greenButtonh.png")
        self.clientimgh = ImageTk.PhotoImage(clientimgh.resize(resize_image(19, clientimgh.size)))
        clientimgp = Image.open(f"{IMG_PATH}/greenButtonp.png")
        self.clientimgp = ImageTk.PhotoImage(clientimgp.resize(resize_image(19, clientimgp.size)))

        self.clientBTN = ButtonImage(auxFrame,  command=lambda:open_window('client'), compound='center', text='Cliente',image=self.clientimg, img_h=self.clientimgh, img_p=self.clientimgp, style='flatw.light.TButton', padding=0)
        self.clientBTN.grid(row=0, column=0, sticky='', pady=(0,8), padx=(4))


        providerimg = Image.open(f"{IMG_PATH}/redButton.png")
        self.providerimg = ImageTk.PhotoImage(providerimg.resize(resize_image(19, providerimg.size)))
        providerimgh = Image.open(f"{IMG_PATH}/redButtonh.png")
        self.providerimgh = ImageTk.PhotoImage(providerimgh.resize(resize_image(19, providerimgh.size)))
        providerimgp = Image.open(f"{IMG_PATH}/redButtonp.png")
        self.providerimgp = ImageTk.PhotoImage(providerimgp.resize(resize_image(19, providerimgp.size)))

        self.providerButton = ButtonImage(auxFrame,  command=lambda:open_window('prov'), compound='center', text='Proveedor',image=self.providerimg, img_h=self.providerimgh, img_p=self.providerimgp, style='flatw.light.TButton', padding=0)
        self.providerButton.grid(row=0, column=1, sticky='', pady=(0,8), padx=(4))

        repreimg = Image.open(f"{IMG_PATH}/repreButton.png")
        self.repreimg = ImageTk.PhotoImage(repreimg.resize(resize_image(19, repreimg.size)))
        repreimgh = Image.open(f"{IMG_PATH}/repreButtonh.png")
        self.repreimgh = ImageTk.PhotoImage(repreimgh.resize(resize_image(19, repreimgh.size)))
        repreimgp = Image.open(f"{IMG_PATH}/repreButtonp.png")
        self.repreimgp = ImageTk.PhotoImage(repreimgp.resize(resize_image(19, repreimgp.size)))

        self.repreButton = ButtonImage(auxFrame,  command=lambda:open_window(), compound='center', text='Representante',image=self.repreimg, img_h=self.repreimgh, img_p=self.repreimgp, style='flatw.light.TButton', padding=0)
        self.repreButton.grid(row=0, column=2, sticky='', pady=(0,8), padx=(4))


        window.place_window_center()
        window.deiconify()




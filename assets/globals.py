from ttkbootstrap.themes.standard import STANDARD_THEMES
from datetime import datetime
from pathlib import Path
from models.entitys.user import User

######### GUI GLOBAL VARIABLES #########

W_WIDTH = 1600
W_HEIGHT = 900
SYSTEM_WIDTH = 0
SYSTEM_HEIGHT = 0
DISPLAY_PAGE = None
SET_BUTTON = None
loggued_user: User = None


########### PATH OPTIONS VARIABLES ###########
IMG_PATH = Path(__file__).parent / 'img'
GRAPH_PATH = Path(__file__).parent.parent / "matplotlib_style/pitayasmoothie-dark.mplstyle"

############### FONT STYLE ###############

GUI_FONT = 'segoi ui'

##############################################

pages_dict = {}
pages_dash_access = []


######### GUI COLORS #########

STANDARD_THEMES['new'] = {
        "type": "light",
        "colors": {
            "primary": "#06283D",
            "secondary": "#1363DF",
            "success": "#3fb618",
            "info": "#394867",
            "warning": "#EC7524",
            "danger": "#e74c3c",
            "light": "#D3D6DF",
            "dark": "#373A3C",
            "bg": "#F2F2F2",
            "fg": "#373a3c",
            "selectbg": "#7e8081",
            "selectfg": "#ffffff",
            "border": "#ced4da",
            "inputfg": "#373a3c",
            "inputbg": "#fdfdfe",
            "active": "#efefef",
        },
}

GUI_COLORS = STANDARD_THEMES['new']['colors']


########## ICONOS #########
from PIL import Image, ImageTk

menu_icon = Image.open(f'{IMG_PATH}/menu-bar.png')

add_icon = Image.open(f'{IMG_PATH}/add-folder.png')

delete_icon = Image.open(f'{IMG_PATH}/delete-folder.png')

trash_icon = Image.open(f'{IMG_PATH}/bin.png')

process_icon = Image.open(f'{IMG_PATH}/process.png')

refresh_icon = Image.open(f'{IMG_PATH}/refresh.png')

home_icon = Image.open(f'{IMG_PATH}/home.png')

statistics_icon = Image.open(f'{IMG_PATH}/statistics.png')

invoice_icon = Image.open(f'{IMG_PATH}/invoice.png')

refresh_icon = Image.open(f'{IMG_PATH}/refresh.png')

budget_icon = Image.open(f'{IMG_PATH}/budget.png')

dashboard_icon = Image.open(f'{IMG_PATH}/dashboard.png') ####

project_icon = Image.open(f'{IMG_PATH}/project.png')

search_icon = Image.open(f'{IMG_PATH}/search.png')

edit_icon = Image.open(f'{IMG_PATH}/edit.png')

project_icon = Image.open(f'{IMG_PATH}/project.png')

plus_icon = Image.open(f'{IMG_PATH}/add-button.png')

minus_icon = Image.open(f'{IMG_PATH}/minus.png')

order_icon = Image.open(f'{IMG_PATH}/checklist.png')

save_icon = Image.open(f'{IMG_PATH}/diskette.png')

email_icon = Image.open(f'{IMG_PATH}/email.png')

printer_icon = Image.open(f'{IMG_PATH}/printer.png')

filter_icon = Image.open(f'{IMG_PATH}/filter.png')

addDocument_icon = Image.open(f'{IMG_PATH}/add-document.png')

addDocument2_icon = Image.open(f'{IMG_PATH}/paper-clip.png')

close_icon = Image.open(f'{IMG_PATH}/close.png')

bold_icon = Image.open(f'{IMG_PATH}/bold-button.png')

arrow_icon = Image.open(f'{IMG_PATH}/arrow1.png')

arrow_close_icon = Image.open(f'{IMG_PATH}/arrow2.png')

inventory_icon = Image.open(f'{IMG_PATH}/inventory.png')

products_icon = Image.open(f'{IMG_PATH}/products.png')

services_icon = Image.open(f'{IMG_PATH}/customer-service.png')

machinery_icon = Image.open(f'{IMG_PATH}/production.png')

cancel_icon = Image.open(f'{IMG_PATH}/contract.png')


company_icon = Image.open(f'{IMG_PATH}/company.png')

code_icon = Image.open(f'{IMG_PATH}/code.png')

representative_icon = Image.open(f'{IMG_PATH}/representative.png')

description_icon = Image.open(f'{IMG_PATH}/document.png')

address_icon = Image.open(f'{IMG_PATH}/address.png')

next_page_icon = Image.open(f'{IMG_PATH}/next.png')

logo_system_icon = Image.open(f'{IMG_PATH}/logo.png')

calendar_icon = Image.open(f'{IMG_PATH}/calendar.png')

delete_all_icon = Image.open(f'{IMG_PATH}/equal.png')

exchange_sp_icon = Image.open(f'{IMG_PATH}/exchange.png')

log_out_icon = Image.open(f'{IMG_PATH}/log-out.png')

currency_icon = Image.open(f'{IMG_PATH}/currency.png')

checked_icon = Image.open(f'{IMG_PATH}/checked.png')

export_icon = Image.open(f'{IMG_PATH}/export.png')

new_record_icon = Image.open(f'{IMG_PATH}/folder.png')

eraser_icon = Image.open(f'{IMG_PATH}/eraser.png')

indicator_icon = Image.open(f'{IMG_PATH}/proximo.png')

decrease_profit_icon = Image.open(f'{IMG_PATH}/ddollar.png')

increase_profit_icon = Image.open(f'{IMG_PATH}/idollar.png')

email_black_icon = Image.open(f'{IMG_PATH}/email_black.png')

phone_icon = Image.open(f'{IMG_PATH}/phone.png')

link_icon = Image.open(f'{IMG_PATH}/link.png')

notes_icon = Image.open(f'{IMG_PATH}/notes.png')

calendar_2_icon = Image.open(f'{IMG_PATH}/calendar_2.png')

wallet_icon = Image.open(f'{IMG_PATH}/wallet.png')

search_form_icon = Image.open(f'{IMG_PATH}/search_form.png')

view_document_icon = Image.open(f'{IMG_PATH}/view-document.png')

money_icon = Image.open(f'{IMG_PATH}/money.png')

unchecked_icon = Image.open(f'{IMG_PATH}/unchecked.png')

checkbox_icon = Image.open(f'{IMG_PATH}/checkbox.png')

company_color_icon = Image.open(f'{IMG_PATH}/companyc.png')

department_color_icon = Image.open(f'{IMG_PATH}/dept.png')

user_color_icon = Image.open(f'{IMG_PATH}/user.png')

id_color_icon = Image.open(f'{IMG_PATH}/id.png')

validate_icon = Image.open(f'{IMG_PATH}/validate.png')

delivery_icon = Image.open(f'{IMG_PATH}/delivery.png')

black_currency_icon = Image.open(f"{IMG_PATH}/black_currency.png")



def on_validate_length(P, lenght = 20):
    return len(P) <= lenght  

import re

def check_email_format(cadena):
    patron_correo = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
    if re.match(patron_correo, cadena):
        return True
    else:
        return False

def limitar_longitud(widget, limit ):
    contenido = widget.get("1.0", "end-1c")
    if len(contenido) > limit:
        nuevo_contenido = contenido[:limit]
        widget.delete("1.0", "end")
        widget.insert("1.0", nuevo_contenido)


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def on_combobox_change(event, var, dictionary, combobox):
    ID = dictionary[combobox.get()]
    var.set(ID)


def validate_number(x) -> bool:
    """Validates that the input is a number"""
    if x.isdigit():
        return True
    elif x == "":
        return True
    else:
        return False

def validateInput(text):
        if text in '0123456789.' or isfloat(text):
            return True
        return False

def validateFloat(text):
    if isfloat(text) or text=='':
        return True
    return False

def check_float_value(var=None, moder=None, indexr=None, value=None):
    if not isfloat(value.get()):
        value.set(value.get()[:-1])

    

def checkDATE(var):
    try:
        datetime.strptime(var.get(),'%d/%m/%Y')
        return True
    except ValueError:
        var.set(datetime.today().strftime('%d/%m/%Y'))

import socket


def check_internet_connection():
    try:
        # Intenta conectar con un servidor de Google (puedes cambiar la dirección si prefieres otro)
        socket.create_connection(("www.google.com", 80), timeout=5)
        return True
    except OSError:
        return False

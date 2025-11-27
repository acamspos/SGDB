from pydantic import BaseModel
from assets.db.db_connection import DB
from tkinter import messagebox
from mysql.connector import Error


class Task(BaseModel):
    
    id: int
    activity_id: int
    item_type: int
    item_code: str
    amount: int
    complete: bool

    def get_type(self):
        if self.item_type == 1:
            return 'Ejecucion de Servicio'
        else:
            return 'Entrega de Suministros'
 
    

    def get_description(self):
        try:
            DB.DB.connect()
            aux = DB.DB.cursor(buffered=True,)
            if self.item_type == 1:
                label = 'name'
                table = 'services'
            else:
                label = 'description'
                table = 'products'
            sql = f"""SELECT {label} FROM {table} WHERE code=%s"""
            aux.execute(sql, (self.item_code,))
            description = aux.fetchone()[0]
            aux.close()
            return description
        except Error as ex:
                messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            DB.DB.close()
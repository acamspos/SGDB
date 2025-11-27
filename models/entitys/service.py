
from pydantic import BaseModel
from typing import Optional
from assets.db.db_connection import DB
from tkinter import messagebox
from mysql.connector import Error

class Service(BaseModel):
    code: Optional[str] = ''
    name: str
    description: str
    warranty: str | None
    currency: int = 0
    price1: float = 0
    price2: float = 0
    price3: float = 0
    
    def openDecorator(func):
        def nueva_funcion(self):
            try:
                DB.DB.connect()
                data = func(self)
         
                if data:
                    return data
            except Error as ex:
                messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
            finally:
                DB.DB.close()
            
        return nueva_funcion
 
    def create(self):
        dict_data = self.model_dump()
        schema = tuple(dict_data.keys())
        data = list(dict_data.values())
        DB.createServiceDB(schema=schema, data=data)

    def update(self):
        dict_data = self.model_dump()
        schema = tuple(dict_data.keys())[1:]
        data = list(dict_data.values())[1:]
        data.append(self.code)
        sentence = ''
        for key in schema:
            sentence+=f"{key}=%s,"
        sentence = sentence[:-1]
        DB.updateServiceDB(fields=sentence, data=data)

    @openDecorator
    def get_currency(self):
        aux = DB.DB.cursor(buffered=True)
        sql = 'SELECT description FROM currency WHERE id=%s'
        aux.execute(sql, (self.currency,))
        currencyD = aux.fetchone()[0]
        return currencyD
    
    def delete(self):
        DB.deleteOneServiceDB(self.code)
        del self
    
    @classmethod
    def findOneService(self, code):
        data = DB.findOneServiceDB(code)
        return Service(**data)
    

    @classmethod
    def findAllServices(self, name=''):
        data = DB.findAllServicesDB(name)
        return data
    
    @classmethod
    def findAllServicesNative(self, name=''):
        data = DB.findAllServicesNativeDB(name)
        return data
    
    
    @classmethod
    def validate_code(self, code):
        check = DB.checkServiceCodeDB(code)
        return check != None
    
    @classmethod
    def countRecords(self):
        return DB.countServiceRecords()
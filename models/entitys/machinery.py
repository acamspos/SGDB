from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from assets.db.db_connection import DB
from tkinter import messagebox
from mysql.connector import Error

class Machinery(BaseModel):
    code: Optional[str] = ''
    description: str
    brand: int = 0
    model: int = 0
    status: int = 1
    currency: int = 0
    cost: float = 0
    
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
        DB.createMachineryDB(schema=schema, data=data)

    def update(self):
        dict_data = self.model_dump()
        schema = tuple(dict_data.keys())[1:]
        data = list(dict_data.values())[1:]
        data.append(self.code)
        sentence = ''
        for key in schema:
            sentence+=f"{key}=%s,"
        sentence = sentence[:-1]
        DB.updateMachineryDB(fields=sentence, data=data)



    def use(self):
        DB.changeMachineryStateDB(self.code,2)


    def enable(self):
        DB.changeMachineryStateDB(self.code,1)

    @openDecorator
    def get_currency(self):
        aux = DB.DB.cursor(buffered=True)
        sql = 'SELECT description FROM currency WHERE id=%s'
        aux.execute(sql, (self.currency,))
        currencyD = aux.fetchone()[0]
        return currencyD
    
    @openDecorator
    def get_brand(self):
        aux = DB.DB.cursor(buffered=True)
        sql = 'SELECT description FROM brand WHERE id=%s'
        aux.execute(sql, (self.brand,))
        brandD = aux.fetchone()[0]
        return brandD
    
    @openDecorator
    def get_model(self):
        aux = DB.DB.cursor(buffered=True)
        sql = 'SELECT description FROM model WHERE id=%s'
        aux.execute(sql, (self.model,))
        modelD = aux.fetchone()[0]
        return modelD
    
    @openDecorator
    def get_status(self):
        aux = DB.DB.cursor(buffered=True)
        sql = 'SELECT description FROM machinery_state WHERE id=%s'
        aux.execute(sql, (self.status,))
        statusD = aux.fetchone()[0]
        return statusD
    
    def delete(self):
        DB.deleteOneMachineryDB(self.code)
        del self
    
    @classmethod
    def findOneMachinery(self, code):
        data = DB.findOneMachineryDB(code)
        return Machinery(**data)
    

    @classmethod
    def findAllMachinerys(self, name='',mach_filter=None):
        data = DB.findAllMachinerysDB(search_value=name, machiery_filter=mach_filter)
        return data
    
    @classmethod
    def validate_code(self, code):
        check = DB.checkMachineryCodeDB(code)
        return check == None
    
    @classmethod
    def countRecords(self):
        return DB.countMachineryRecords()
    
    @classmethod
    def getMachineryNotAvailable(self, ):
        return DB.getMachineryNotAvailableDB()
    
    
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
department = {1:'Producto',2:'Servicio'}

from assets.db.db_connection import DB
from tkinter import messagebox
from mysql.connector import Error

class Product(BaseModel):
    code: Optional[str] = ''
    description: str
    department: int = 0
    brand: int = 0
    provider: int = 0
    currency: int = 0
    measurement: int = 0
    cost: float = 0
    directcost: float = 0
    indirectcost: float = 0
    tax: int = 0
    price_1: float = 0
    price_2: float = 0
    price_3: float = 0
    profit_1: float = 0
    profit_2: float = 0
    profit_3: float = 0
    stock: int = 0
    stock_1: int = 0
    stock_2: int = 0
    stock_3: int = 0
    stock_4: int = 0

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
        DB.createProductDB(schema=schema, data=data)

    def update(self):
        dict_data = self.model_dump()
        schema = tuple(dict_data.keys())[1:]
        data = list(dict_data.values())[1:]
        data.append(self.code)
        sentence = ''
        for key in schema:
            sentence+=f"{key}=%s,"
        sentence = sentence[:-1]
        DB.updateProductDB(fields=sentence, data=data)

    def reduce_existence(self, amount):
        if amount <= self.stock:
            self.stock -= int(amount)
            DB.reduceExistenceProductDB(amount, self.code)
            return True
        return False

    def return_existence(self, amount):
        self.stock += int(amount)
        DB.addExistenceProductDB(amount, self.code)
        return True
    
    @openDecorator
    def get_department(self):
        aux = DB.DB.cursor(buffered=True)
        sql = 'SELECT description FROM department WHERE id=%s'
        aux.execute(sql, (self.department,))
        dep_descript = aux.fetchone()[0]
        return dep_descript
    
    @openDecorator
    def get_brand(self):
        aux = DB.DB.cursor(buffered=True)
        sql = 'SELECT description FROM brand WHERE id=%s'
        aux.execute(sql, (self.brand,))
        brandD = aux.fetchone()[0]
        return brandD
    
    @openDecorator
    def get_provider(self):
        aux = DB.DB.cursor(buffered=True)
        sql = 'SELECT name FROM providers WHERE id=%s'
        aux.execute(sql, (self.provider,))
        providerD = aux.fetchone()[0]
        return providerD
    
    @openDecorator
    def get_tax(self):
        aux = DB.DB.cursor(buffered=True)
        sql = 'SELECT description FROM tax WHERE id=%s'
        aux.execute(sql, (self.tax,))
        taxD = aux.fetchone()[0]
        return taxD
    
    @openDecorator
    def get_currency(self):
        aux = DB.DB.cursor(buffered=True)
        sql = 'SELECT description FROM currency WHERE id=%s'
        aux.execute(sql, (self.currency,))
        currencyD = aux.fetchone()[0]
        return currencyD
    

    @openDecorator
    def get_measurement(self):
        aux = DB.DB.cursor(buffered=True)
        sql = 'SELECT description FROM measurement WHERE id=%s'
        aux.execute(sql, (self.measurement,))
        measureD = aux.fetchone()[0]
        return measureD
    

    def delete(self):
        DB.deleteOneProductDB(self.code)
        del self
    
    @classmethod
    def findOneProduct(self, code):
        data = DB.findOneProductDB(code)
        return Product(**data)
    

    @classmethod
    def findAllProduct(self, name=''):
        data = DB.findAllProductsDB(name)#findAllProductsNativeDB
        return data
    

    @classmethod
    def findAllProductNative(self, name='', field='code',operator='LIKE'):
        data = DB.findAllProductsNativeDB(name, field, operator)#findAllProductsNativeDB
        return data

    @classmethod
    def validate_code(self, code):
        check = DB.checkProductCodeDB(code)
        return check != None
   

    @classmethod
    def getProductsOutOfStock(self, ):
        return DB.getProductsOutOfStockDB()
    
    
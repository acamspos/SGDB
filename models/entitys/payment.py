from pydantic import BaseModel
from typing import Optional
from assets.db.db_connection import DB
from datetime import datetime
from tkinter import messagebox
from mysql.connector import Error

class Payment(BaseModel):
    paymentDate: str | datetime
    reference: str
    document: str
    company: str
    paymentType: str
    documentType: str = 'VENTA'
    currency: int
    amount: float
    amountUSD: float
    exchange_rate: float
    description: str

    
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

    @classmethod
    def creatAll(self, data):
        schema = tuple(Payment.model_fields.keys())
     
        return DB.createPaymentRecord(schema=schema, data=data)

    @openDecorator
    def get_currency(self):
        aux = DB.DB.cursor(buffered=True)
        sql = 'SELECT description FROM currency WHERE id=%s'
        aux.execute(sql, (self.currency,))
        currencyD = aux.fetchone()[0]
        return currencyD
    
    @openDecorator
    def get_currency_icon(self):
        aux = DB.DB.cursor(buffered=True)
        sql = 'SELECT icon FROM currency WHERE id=%s'
        aux.execute(sql, (self.currency,))
        currencyD = aux.fetchone()[0]
        return currencyD
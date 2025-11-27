from pydantic import BaseModel
from typing import Optional
from assets.db.db_connection import DB
from datetime import datetime
from tkinter import messagebox
from mysql.connector import Error

class PurchaseDocument(BaseModel):
   
    code: str = ''
    provider: str
    control: str = ""
    documentCondition: str
    currency: int
    dateOfIssue: datetime
    expirationDate: datetime
    registrationDate: datetime
    total: float
    totalUSD: float
    debtUSD: float = 0
    totalPaidUSD: float = 0
    exchangeRate: float = 0
    payment_status: int = 1
    documentState: int
    purchaseType: int
    description: str = None

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

    def check_dates(self):
        if self.dateOfIssue >= self.expirationDate:
            self.documentState = 2

    def findItems(self):
        return DB.find_purchase_items(code=self.code)
    

    @classmethod
    def findPurchasesByProvider(self, providerRif:str = None, unpaid=False):
        return DB.findPurchasesByProviderDB(providerRif=providerRif,unpaid=unpaid)
        
    

    @classmethod
    def findAll(self, date = None, datefilter = None):
        return DB.findAllPurchasesDB(date=date, datefilter=datefilter)
    
    
    @classmethod
    def findOnePurchase(self, code, rif):
        data = DB.findOnePurchaseDB(code, rif)
        return PurchaseDocument(**data)

    def create(self, items):
        self.check_dates()
        dict_data = self.model_dump()
        schema = tuple(dict_data.keys())
        data = list(dict_data.values())
        DB.createPurchaseDB(schema=schema, data=data)
        DB.insert_purchase_items(items)
    
   

    def delete(self,):
        DB.deleteOnePurchase(self.code)
        del self

    
    @openDecorator
    def get_company(self):
        aux = DB.DB.cursor(buffered=True)
        sql = 'SELECT name FROM providers WHERE rif=%s'
        aux.execute(sql, (self.provider,))
        company = aux.fetchone()[0]
        return company
    
    @openDecorator
    def get_documentState(self):
        aux = DB.DB.cursor(buffered=True)
        sql = 'SELECT description FROM documentstate WHERE id=%s'
        aux.execute(sql, (self.documentState,))
        currencyD = aux.fetchone()[0]
        return currencyD
    
    @openDecorator
    def get_documentStatus(self):
        aux = DB.DB.cursor(buffered=True)
        sql = 'SELECT description FROM paymentstatus WHERE id=%s'
        aux.execute(sql, (self.payment_status,))
        currencyD = aux.fetchone()[0]
        return currencyD
    
    @openDecorator
    def get_purchaseType(self):
        aux = DB.DB.cursor(buffered=True)
        sql = 'SELECT description FROM billtype WHERE id=%s'
        aux.execute(sql, (self.purchaseType,))
        currencyD = aux.fetchone()[0]
        return currencyD

    
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
    
    @classmethod
    def update_document_states(self):
        return DB.updatePurchasesToExpire()
    
    @classmethod
    def get_document_to_expirate(self):
        return [PurchaseDocument(**doc) for doc in DB.findPurchasesToExpira()]


class PurchaseItem(BaseModel):
    purchaseCode: str
    product: str
    description: str
    presentation: str
    tax: int
    cost: float
    price1: float
    price2: float
    price3: float
    profit1: float
    profit2: float
    profit3: float
    stock: int
    stock1: int
    stock2: int
    stock3: int
    stock4: int
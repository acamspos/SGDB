from pydantic import BaseModel
from typing import Optional
from assets.db.db_connection import DB
from datetime import datetime, timedelta
from models.entitys.activity import Activity
import pathlib
from win32com import client
import openpyxl
from openpyxl.drawing.image import Image
from tkinter import messagebox
from datetime import datetime
from openpyxl.styles import NamedStyle, Font, Alignment, Border, Side
from mysql.connector import Error
import os
class Budget(BaseModel):
   
    code: int
    description: str
    client: str = ""
    address: str
    representative: str
    creationDate: datetime | str
    deliveryDays: int | str
    validationDays: int | str
    currency: int
    state: int = 1
    sub_total: float = 0
    iva: float = 0
    total_amount: float = 0
    exchange_rate: float
    editable: bool = True
    processed: bool = False
    purchaseOrder: str | None = None
    type: int = 1
    processingDate: datetime | None = None
    finishDate: datetime | None = None
    creationUser: int | None = None
    processingUser: int | None = None
    deleted: bool = False

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

    def setPurchaseOrder(self, purchasesOrder):
        DB.updateBudgetDB(fields='purchaseOrder=%s', data=(purchasesOrder,self.code))



    def create(self, items):
        dict_data = self.model_dump()
        schema = tuple(dict_data.keys())[1:]
        data = list(dict_data.values())[1:]
        
        code = DB.createBudgetDB(schema=schema, data=data)

        Item.create_list(items, code)

    def update(self, items):
        Item.deleteItems(self.code)
        dict_data = self.model_dump()
        schema = tuple(dict_data.keys())[1:]
        data = list(dict_data.values())[1:]
        data.append(self.code)
        sentence = ''
        for key in schema:
            sentence+=f"{key}=%s,"
        sentence = sentence[:-1]
        DB.updateBudgetDB(fields=sentence, data=data)
        Item.create_list(items, self.code)


    @classmethod
    def reject_by_time(self):
        COTZ = DB.rejectBudgetByTimeDB()
        return COTZ
    
    def process(self, user):
        DB.updateBudgetDB(fields='state=%s,editable=False,processingDate=%s,processingUser=%s', data=(2,datetime.today().strftime('%Y-%m-%d'),user,self.code))

    def approve(self, user):
        DB.updateBudgetDB(fields='state=%s,processed=True,editable=False,finishDate=%s,processingUser=%s', data=(3,datetime.today().strftime('%Y-%m-%d'),user,self.code))
        date = datetime.today()
        Activity(type=self.type,stage=1 if self.deliveryDays >0 else 2,budget_code=self.code, start_date=datetime.today().strftime('%Y-%m-%d') if self.deliveryDays==0 else None ,final_date=(date+timedelta(days=self.deliveryDays)).strftime('%Y-%m-%d'),
                 complete=False, address=self.address, client=self.client,description=self.description).create()

    
    def reject(self, user):
        DB.updateBudgetDB(fields='state=%s,processed=True,editable=False,finishDate=%s,processingUser=%s', data=(4,datetime.today().strftime('%Y-%m-%d'),user,self.code,))
       

    def delete(self):
        if self.processed:
            return False
        else:
            Item.deleteItems(self.code)
            DB.deleteOneBudgetDB(self.code)
            del self
            return True
    
    @classmethod
    def findOneBudget(self, code):
        data = DB.findOneBudgetDB(code)
        return Budget(**data)
    

    @classmethod
    def findAllBudgets(self, value='',condition_field = 'b.code', codition_operator = 'LIKE', filter_status = None):
        data = DB.findAllBudgetsDB(value, condition_field, codition_operator, filter_status)
        return data
    
    @classmethod
    def validate_code(self, code):
        check = DB.checkBudgetCodeDB(code)
      
        return check == None
    

    @classmethod
    def getProductsOutOfStock(self, ):
        return DB.getProductsOutOfStockDB()
    
    @classmethod
    def getNextBudgetCode(self):
        return DB.getNextBudgetCode2()
    

    def findItems(self) -> list:
        records = Item.findAllItems(self.code)
        return [Item(**data) for data in records]
    

    @openDecorator
    def get_company(self):
        aux = DB.DB.cursor(buffered=True)
        sql = 'SELECT name FROM clients WHERE rif=%s'
        aux.execute(sql, (self.client,))
        company = aux.fetchone()[0]
        return company
    
    @openDecorator
    def get_company_email(self):
        aux = DB.DB.cursor(buffered=True)
        sql = 'SELECT email FROM clients WHERE rif=%s'
        aux.execute(sql, (self.client,))
        company = aux.fetchone()[0]
        return company

    @openDecorator
    def get_representative(self):
        aux = DB.DB.cursor(buffered=True)
        sql = 'SELECT name,lastname FROM representative WHERE id=%s'
        aux.execute(sql, (self.representative,))
        repre = aux.fetchone()
        return f"{repre[0]} {repre[1]}"

    @openDecorator
    def get_representative_email(self):
        aux = DB.DB.cursor(buffered=True)
        sql = 'SELECT email FROM representative WHERE id=%s'
        aux.execute(sql, (self.representative,))
        repre = aux.fetchone()
        return repre[0]
    

    def collect_data_for_email(self):
        return [[self.get_company_email(),self.get_company()],[self.get_representative_email(),self.get_representative()]]
    
    @openDecorator
    def get_currency(self):
        aux = DB.DB.cursor(buffered=True)
        sql = 'SELECT description FROM currency WHERE id=%s'
        aux.execute(sql, (self.currency,))
        currencyD = aux.fetchone()[0]
        return currencyD
    
    @openDecorator
    def get_type(self):
        aux = DB.DB.cursor(buffered=True)
        sql = 'SELECT type FROM record_type WHERE id=%s'
        aux.execute(sql, (self.type,))
        typeD = aux.fetchone()[0]
        return typeD
    
    @classmethod
    def countEditableBudgets(self):
        return DB.countBudgetsByState(1)
    
    @classmethod
    def countProcessBudgets(self):
        return DB.countBudgetsByState(2)
    

    @classmethod
    def countApproveBudgets(self):
        return DB.countBudgetsByState(3)
    

    @classmethod
    def countRejectBudgets(self):
        return DB.countBudgetsByState(4)
    
    
    @classmethod
    @openDecorator
    def countBudgets(self):
        aux = DB.DB.cursor(buffered=True)
        month = datetime.today().month
        year = datetime.today().year
        sql = f"""
        SELECT 
            DATE(creationDate) AS fecha,
            COUNT(*) AS cantidad_registros
        FROM 
            budgets
        WHERE 
            MONTH(creationDate) = {month} AND YEAR(creationDate) = {year}
        GROUP BY 
            DATE(creationDate);"""
        aux.execute(sql,)
        currencyD = aux.fetchall()
        return currencyD
    

    def create_pdf(self, path_to_save, parent=None):
        template =  str(pathlib.Path(__file__).parent.parent.parent) + "\\templates\\template.xlsx"
        template_file = openpyxl.load_workbook(template)
        sheet = template_file['template']
        sheet = template_file.active

        nueva = sheet
        nueva.title = f'COTIZACIÓN {self.code}'
            
        # imag = Image('C:/Users/Agustin Campos/Desktop/SGDB/assets/img/abielcaj91Logo.png')
        # nueva.add_image(imag, 'C1')

        nueva['B15'] = "Cotización " +'0'*(6-len(str(self.code)))+str(self.code)
        nueva['K3'] = '15 de Agosto de 2023'
        nueva['D7'] = self.get_company()
        nueva['D9'] = self.representative
        nueva['D11'] = self.address
        nueva['D13'] = self.description

        items = [Item(**ite) for ite in Item.findAllItems(self.code)]
        index = 0
        for index, item in enumerate(items):
            nueva[f'B{17+index}'] = index+1
            nueva[f'C{17+index}'] = item.itemDescription
            nueva[f'F{17+index}'] = item.quantity
            nueva[f'G{17+index}'] = ''
            nueva[f'H{17+index}'] = self.deliveryDays
            nueva[f'I{17+index}'] = self.validationDays
            nueva[f'J{17+index}'] = self.get_currency()
            nueva[f'K{17+index}'] = item.price
            nueva[f'L{17+index}'] = item.total_price
        
        nueva[f'C{index+17+2}'] = "NOTA: ENTREGA EN BASE MATURIN ESTADO MONAGAS"
        output_template =  str(pathlib.Path(__file__).parent.parent.parent) + "\\templates\\budgets.xlsx"
        template_file.save(output_template)
        template_file.close()


        try:
            code = '0'*(7-len(str(self.code)))+str(self.code)
            path = str(path_to_save).replace('/','\\') + f'\\COT_{code}.pdf'

            excel = client.Dispatch("Excel.Application")

            sheets = excel.Workbooks.Open(output_template)
            work_sheets = sheets.Worksheets[0]
            # Converting into PDF File
            work_sheets.ExportAsFixedFormat(0, path)
        except:
            excel.quit()
            return None
        finally:
            sheets.Close()
            excel.quit()
           
            os.remove("C:\\Users\\Agustin Campos\\Desktop\\SGDB\\templates\\budgets.xlsx")
            messagebox.showinfo('Cotización','PDF generado exitosamente.', parent=parent)
            return(path)

     
    


class Item(BaseModel):
   
    code: int
    itemType: int
    itemId: str
    itemDescription: str
    cost: float
    quantity: int
    price: float
    total_price: float
    totalUSD: float
    currency: int
    date: datetime | str

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
        DB.createItemBudgetDB(schema=schema, data=data)

    @openDecorator
    def get_type(self):
        aux = DB.DB.cursor(buffered=True)
        sql = 'SELECT description FROM itemType WHERE id=%s'
        aux.execute(sql, (self.itemType,))
        typeD = aux.fetchone()[0]
        return typeD

    @classmethod
    def create_list(self, items, budget_code):
        for item in items:
            item['code'] = budget_code
            Item(**item).create()


    @classmethod
    def findAllItems(self, budget_code):
        data = DB.findABudgetitemsDB(budget_code)
        return data
    
    @classmethod
    def deleteItems(self, budget_code):
        DB.deleteAllItemsByBudget(budget_code)

    @classmethod
    def normalQuantity(self, budget_code, itemId):
        data = DB.returnQuantityOneItemsDB(budget_code,itemId)
        return data
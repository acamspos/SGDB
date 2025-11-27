from pydantic import BaseModel
from assets.db.db_connection import DB
from tkinter import messagebox
from mysql.connector import Error

class Representative(BaseModel):
    id: str = ''
    name: str = ''
    lastname: str = ''
    company: str
    department: str
    email: str = ''
    phone: str = ''

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
    
    def check_records(self):
        if DB.checkRepresentativeRecordsDB(self.id) < 0:
            return True
        return False


    def create(self):
        dict_data = self.model_dump()
        schema = tuple(dict_data.keys())
        data = list(dict_data.values())
        DB.createRepresentativeDB(schema=schema, data=data)

    def update(self):
        dict_data = self.model_dump()
        schema = tuple(dict_data.keys())[1:]
        data = list(dict_data.values())[1:]
        data.append(self.id)
        sentence = ''
        for key in schema:
            sentence+=f"{key}=%s,"
        sentence = sentence[:-1]
        DB.updateRepresentativeDB(fields=sentence, data=data)

    @openDecorator
    def get_company(self):
        aux = DB.DB.cursor(buffered=True)
        sql = 'SELECT name FROM clients WHERE rif=%s'
        aux.execute(sql, (self.company,))
        company = aux.fetchone()[0]
        return company
    
    @classmethod
    def findOneRepresentative(self, idR):
        data = DB.findOneRepresentativeDB(idR)
        return Representative(**data)


    @classmethod
    def findAllRepresentative(self, name='', filter_company=None):
        data = DB.findAllRepresentativesByNameDB(name, filter_company)
        return data
    

    @classmethod
    def validate_id(self, rif):
        check = DB.checkRepresentativeIdCodeDB(rif)
        return check == None
    
    
    def delete(self,):
        DB.deleteOneRepresentativeDB(self.id)
        del self

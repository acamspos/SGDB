from pydantic import BaseModel
from typing import Optional
from assets.db.db_connection import DB

class Client(BaseModel):
    rif: str = ''
    name: str = ''
    address: str = ''
    email: str = ''
    phone: str = ''
    website: str = ''


    

    def create(self):
        dict_data = self.model_dump()
        schema = tuple(dict_data.keys())
        data = list(dict_data.values())
        DB.createClientDB(schema=schema, data=data)


    def update(self):
        dict_data = self.model_dump()
        schema = tuple(dict_data.keys())[2:]
        data = list(dict_data.values())[2:]
        data.append(self.rif)
        
        sentence = ''
        for key in schema:
            sentence+=f"{key}=%s,"
        sentence = sentence[:-1]

        DB.updateClientDB(fields=sentence, data=data)

    def check_records(self):
        if DB.checkClientRecordsDB(self.rif) < 0:
            return True
        return False
    
    @classmethod
    def findOneClient(self, rif):
        data = DB.findOneClientDB(rif)
        return Client(**data)
    

    @classmethod
    def findAllClient(self, name=''):
        data = DB.findAllClientsByNameDB(name)
        return data
    
    @classmethod
    def validate_rif(self, rif):
        check = DB.checkClientRifCode(rif)
        return check == None
    
    
    def delete(self,):
        DB.deleteOneClient(self.rif)
        del self

    def get_debit_documents(self):
        return DB.findBillsByClientDB(self.rif, unpaid=True)
    

    def get_all_documents(self):
        return DB.findBillsByClientDB(self.rif)
    
    def get_payments_records(self, bill = None):
        return DB.findClientPayments(self.rif, bill)
    
    
    def get_total_debt(self):
        return DB.get_client_balance('totalUSD',self.rif)
    

    def get_actual_debt(self):
        return DB.get_client_balance('debtUSD', self.rif)
    
    def get_total_paid(self):
        return DB.get_client_balance('totalPaidUSD', self.rif)
    
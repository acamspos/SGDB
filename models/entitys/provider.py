from pydantic import BaseModel
from typing import Optional
from assets.db.db_connection import DB

class Provider(BaseModel):
    id: Optional[int] = 0
    rif: str = ''
    name: str = ''
    address: str = ''
    email: str = ''
    phone: str = ''
    website: str = ''



    def create(self):
        dict_data = self.model_dump()
        schema = tuple(dict_data.keys())[1:]
        data = list(dict_data.values())[1:]
        DB.createProviderDB(schema=schema, data=data)


    def update(self):
        dict_data = self.model_dump()
        schema = tuple(dict_data.keys())[2:]
        data = list(dict_data.values())[2:]
        data.append(self.rif)
        
        sentence = ''
        for key in schema:
            sentence+=f"{key}=%s,"
        sentence = sentence[:-1]

        DB.updateProviderDB(fields=sentence, data=data)


    def check_records(self):
        if DB.checkProvidersRecordsDB(self.rif) < 0:
            return True
        return False


    @classmethod
    def findOneProvider(self, id):
        data = DB.findOneProviderDB(id)
        return Provider(**data)
    

    @classmethod
    def findAllProvider(self, name=''):
        data = DB.findAllProvidersByNameDB(name)
        return data
    
    @classmethod
    def validate_rif(self, rif):
        check = DB.checkProviderRifCode(rif)
        return check == None
    
    
    def delete(self,):
        DB.deleteOneProvider(self.rif)
        del self

    def get_total_debt(self):
        return DB.get_provider_balance('totalUSD',self.rif)
    

    def get_actual_debt(self):
        return DB.get_provider_balance('debtUSD', self.rif)
    
    def get_total_paid(self):
        return DB.get_provider_balance('totalPaidUSD', self.rif)
    
    def get_all_documents(self):
        return DB.findPurchasesByProviderDB(self.rif)
    
    def get_debit_documents(self):
        return DB.findPurchasesByProviderDB(self.rif, unpaid=True)
    
    def get_payments_records(self, purchase = None):
        return DB.findProviderPayments(self.rif, purchase)

from pydantic import BaseModel
from typing import Optional
import bcrypt
from assets.db.db_connection import DB
from tkinter import messagebox
from mysql.connector import Error

class User(BaseModel):
    id: Optional[int] = None
    ci: str = None
    name: str = None
    lastname: str = None
    username: str = None
    email: str = None
    phone: str = None
    password: str | bool = None
    rol: int = None
#crypt.checkpw(user.password.encode(),row[2].encode())
    def hash_password(self):
        hashed = bcrypt.hashpw(self.password.encode(), bcrypt.gensalt())
        return hashed

    def create(self):
        dict_data = self.model_dump()
        dict_data['password'] = self.hash_password()
        schema = tuple(dict_data.keys())[1:]
        data = list(dict_data.values())[1:]

        DB.createUserDb(schema=schema, data=data)

    @classmethod
    def validate_id(self, idu):
        check = DB.checkUserIDDB(idu)

        return check == None

    
    def update(self, update_password:bool):
      
        dict_data = self.model_dump()
        
        if update_password == False:
            del dict_data['password']
        else:
            dict_data['password'] = self.hash_password()
        schema = tuple(dict_data.keys())[2:]
        data = list(dict_data.values())[2:]
        data.append(self.ci)
        sentence = ''
        for key in schema:
            sentence+=f"{key}=%s,"
        sentence = sentence[:-1]
        DB.updateUserDb(fields=sentence, data=data)

    
    def update_password(self, password):
        passw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        DB.updateUserPasswordDb(password=passw, ci=self.ci)

    
    @classmethod
    def findOneUser(self, ci):
        data = DB.findOneUser(ci)
        return User(**data)
    
    def get_rol(self):
        try:
            DB.DB.connect()
            aux = DB.DB.cursor(buffered=True)
            sql = 'SELECT description FROM rol WHERE id=%s'
            aux.execute(sql, (self.rol,))
            typeD = aux.fetchone()[0]
            return typeD
        except Error as ex:
                messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            DB.DB.close()
    
    @classmethod
    def findAllUsers(self, username=''):
        data = DB.findAllUsers(search_value=username)
        return data

   
def validate_user(user: User):
    try:
        DB.DB.connect()
        aux = DB.DB.cursor(buffered=True, dictionary=True)

        sql = "SELECT * FROM users where username = BINARY  '{}'".format(user.username)

        aux.execute(sql)
        row = aux.fetchone()

        if row:
            db_user = User(**row)
            db_user.password = bcrypt.checkpw(user.password.encode(),db_user.password.encode())
            return db_user
        else:
            return None
    except Error as ex:
                messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
    finally:
            DB.DB.close()
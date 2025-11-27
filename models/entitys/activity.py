from pydantic import BaseModel
from typing import Optional
from assets.db.db_connection import DB
from datetime import datetime, timedelta
from tkinter import messagebox
from mysql.connector import Error


class Activity(BaseModel):
    
    id: int=0
    type: int
    stage: int = 1
    budget_code: int
    description: str
    client: str
    address: str
    start_date: datetime | str | None = None
    final_date: datetime | str | None = None
    complete: bool

    @classmethod
    def get_avtivity_to_end(self):
        return DB.activityToExpireDB()

    @classmethod
    def findOneActivity(self,id):
       
        data = DB.findOneActivityDB(id)
        return Activity(**data)
    
    def update(self):
        self.__init__(**DB.get_activity(self.id))

    def get_activity_description(self):
        try:
            DB.DB.connect()
            aux = DB.DB.cursor(buffered=True,)
            sql = f"""SELECT description FROM activity WHERE code=%s"""
            aux.execute(sql, (self.budget_code,))
            tasks = aux.fetchone()[0]
            aux.close()
            return tasks
        except Error as ex:
                messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            DB.DB.close()


    def get_client(self): #rif_company
        try:
            DB.DB.connect()
            aux = DB.DB.cursor(buffered=True,)
            sql = f"""SELECT c.name FROM activity a 
            INNER JOIN clients c ON c.rif=a.client
            WHERE a.id=%s"""
            aux.execute(sql, (self.id,))
            tasks = aux.fetchone()
            aux.close()
            return tasks
        except Error as ex:
                messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            DB.DB.close()

    @classmethod
    def lastFive(self):
        try:
            DB.DB.connect()
            aux = DB.DB.cursor(buffered=True, dictionary=True)
            sql = f"""SELECT * FROM activity ORDER BY id DESC LIMIT 5"""
            aux.execute(sql,)
            currencyD = aux.fetchall()
            
            return currencyD
        except Error as ex:
                messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            DB.DB.close()

   
    
    def get_purchaseOrder(self):
        try:
            DB.DB.connect()
            aux = DB.DB.cursor(buffered=True,)
            sql = f"""SELECT purchaseOrder FROM budgets WHERE code=%s"""
            aux.execute(sql, (self.budget_code,))
            tasks = aux.fetchone()[0]
            aux.close()
            return tasks
        except Error as ex:
                messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            DB.DB.close()

    def get_totals(self):
        try:
            DB.DB.connect()
            aux = DB.DB.cursor(buffered=True,)
            sql = f"""SELECT currency, sub_total, iva, total_amount FROM budgets WHERE code=%s"""
            aux.execute(sql, (self.budget_code,))
            tasks = aux.fetchone()
            aux.close()
            return tasks
        except Error as ex:
                messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            DB.DB.close()

    def get_currency(self, id):
        try:
            DB.DB.connect()
            aux = DB.DB.cursor(buffered=True)
            sql = f"""SELECT description FROM currency WHERE id=%s"""
            aux.execute(sql, (id,))
            description = aux.fetchone()[0]
            aux.close()
            return description
        except Error as ex:
                messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            DB.DB.close()

    def get_machinery(self):
        try:
            DB.DB.connect()
            aux = DB.DB.cursor(buffered=True, dictionary=True)
            sql = f"""SELECT ma.machinery FROM activity a
            INNER JOIN machinery_activity ma ON ma.activity_id=a.id
            WHERE a.id=%s"""
            aux.execute(sql,(self.id,))
            codes = aux.fetchall()
            if len(codes) > 0:
                sql2 = f"""SELECT * FROM machinery WHERE code in ({('%s,'*(len(codes)))[:-1]})"""
                aux.execute(sql2, [code['machinery'] for code in codes])
                machinery = aux.fetchall()
                aux.close()
                return machinery
            return None
        except Error as ex:
                messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            DB.DB.close()
    
    def get_tasks(self):
        try:
            DB.DB.connect()
            aux = DB.DB.cursor(buffered=True, dictionary=True)
            sql = f"""SELECT * FROM task WHERE activity_id=%s"""
            aux.execute(sql, (self.id,))
            tasks = aux.fetchall()
            aux.close()
            return tasks
        except Error as ex:
                messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            DB.DB.close()
        
    def complete_all_tasks(self):
        try:
            DB.DB.connect()
            aux = DB.DB.cursor(buffered=True, dictionary=True)
            sql = f"""UPDATE task SET complete = 1 WHERE activity_id=%s"""
            aux.execute(sql, (self.id,))
            tasks = aux.fetchall()
            aux.close()
            return tasks
        except Error as ex:
                messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            DB.DB.close()

    def get_num_tasks(self):
        try:
            DB.DB.connect()
            aux = DB.DB.cursor(buffered=True)
            sql_task = f"""SELECT COUNT(*) AS tasks FROM task WHERE activity_id=%s"""
            aux.execute(sql_task, (self.id,))
            data = aux.fetchone()[0]
            aux.close()
            return data
        except Error as ex:
                messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            DB.DB.close()
    
    def get_num_tasks_complete(self):
        try:
            DB.DB.connect()
            aux = DB.DB.cursor(buffered=True)
            sql_complete_task = f"""SELECT COUNT(*) FROM task WHERE activity_id=%s AND complete=true"""
            aux.execute(sql_complete_task, (self.id,))
            data = aux.fetchone()[0]
            aux.close()
            return data
        except Error as ex:
                messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            DB.DB.close()

        
    def create(self):
        dict_data = self.model_dump()
        schema = tuple(dict_data.keys())[1:]
        data = list(dict_data.values())[1:]
        DB.createActivityDB(schema=schema, data=data)
       

    def get_type(self):
        try:
            DB.DB.connect()
            aux = DB.DB.cursor(buffered=True)
            sql = f"""SELECT type FROM activity_type WHERE id=%s"""
            aux.execute(sql, (self.type,))
            description = aux.fetchone()[0]
            aux.close()
            return description
        except Error as ex:
                messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            DB.DB.close()
        
    def get_stage(self):
        try:
            DB.DB.connect()
            aux = DB.DB.cursor(buffered=True)
            sql = f"""SELECT stage FROM stage WHERE id=%s"""
            aux.execute(sql, (self.stage,))
            description = aux.fetchone()[0]
            aux.close()
            return description
        except Error as ex:
                messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            DB.DB.close()
        
    def extend_activity(self, days):
        try:
            DB.DB.connect()
            new_final_date = self.final_date + timedelta(days=days)
            aux = DB.DB.cursor(buffered=True)
            sql = 'UPDATE activity SET final_date=%s WHERE id=%s'
            aux.execute(sql, (new_final_date,self.id))
            self.final_date = new_final_date
            DB.DB.commit()
            aux.close()
        except Error as ex:
                messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            DB.DB.close()

    @classmethod
    def activities_to_complete(self):
        activities = DB.find_activities_to_expire(date=datetime.today())
        return activities

    def add_machinery(self, data):
        try:
            DB.DB.connect()
            aux = DB.DB.cursor(buffered=True)
            sql = 'INSERT INTO machinery_activity (activity_id,machinery) VALUES (%s,%s)'
            aux.execute(sql, (self.id,data))
            DB.DB.commit()
            aux.close()
        except Error as ex:
                messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            DB.DB.close()

    def update_machinery_state(self, ):
        try:
            DB.DB.connect()
            aux = DB.DB.cursor(buffered=True)
            sql = 'UPDATE  machinery_activity SET complete = 1 WHERE activity_id=%s'
            aux.execute(sql, (self.id,))
            DB.DB.commit()

            sql = 'SELECT machinery FROM machinery_activity WHERE activity_id=%s'
            aux.execute(sql, (self.id,))
            codes = aux.fetchall()

            for code in codes:
                DB.update_machinery_state(code[0],1)
            aux.close()
        except Error as ex:
                messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            DB.DB.close()

    def complete_activity(self):
        self.complete_all_tasks()
        self.update_machinery_state()
        self.update_stage(3)

    
    def update_stage(self, stage):
        try:
            DB.DB.connect()
            aux = DB.DB.cursor(buffered=True)
            sql = 'UPDATE activity SET stage=%s WHERE id=%s'
            aux.execute(sql, (stage,self.id))
            self.stage = stage
            DB.DB.commit()
            aux.close()
        except Error as ex:
                messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            DB.DB.close()

    def update_process(self,):
        try:
            DB.DB.connect()
            aux = DB.DB.cursor(buffered=True)
            sql = 'UPDATE activity SET complete=1 WHERE id=%s'
            aux.execute(sql, (self.id,))
            DB.DB.commit()
            aux.close()
        except Error as ex:
                messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            DB.DB.close()

    
    def update_date(self,start, end):
        try:
            DB.DB.connect()
            aux = DB.DB.cursor(buffered=True)
            sql = 'UPDATE activity SET start_date=%s, final_date=%s WHERE id=%s'
            aux.execute(sql, (start,end,self.id))
            DB.DB.commit()
            aux.close()
        except Error as ex:
                messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            DB.DB.close()

    
    @classmethod
    def countProgramada(self):
        return DB.countaActivityByState(1)
    
    @classmethod
    def countProcess(self):
        return DB.countaActivityByState(2)
    

    @classmethod
    def countCompleted(self):
        return DB.countaActivityByState(3)
    

    @classmethod
    def countCancelded(self):
        return DB.countaActivityByState(4)
    

    
    

#Activity(type=1,stage=2,title='gustrc-23',description='ESTO ES UNA NUEVA PRUEBA DEL SISTEMA CON LA BASE DE DATOS',budget_code='000124',client=1,address=1,start_date=datetime.today()).create()
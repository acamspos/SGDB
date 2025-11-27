import mysql.connector as mysql
from mysql.connector import Error
from tkinter import messagebox
import dotenv
import os
from datetime import datetime, timedelta
dotenv.load_dotenv()
from tkinter import messagebox

class Database:
    ######## Inicializar Conexion ########
    def __init__(self):
        try:
            
            self.DB = mysql.connect(
                user = 'root',
                password = os.getenv('DB_PASSWORD'),
                host = 'localhost',
                db = os.getenv('DB_NAME'),
            )
        except Error as ex:
            messagebox.showerror('BASE DE DATOS', f'Error al establecer la conexion con la Base de datos.')

        finally:
            self.DB.close()
    def restore_db(self, backup_file_path):
        
        try:
            self.DB.connect()
            if self.DB.is_connected():
                cursor = self.DB.cursor()

                with open(backup_file_path, 'r') as sql_file:
                    sql_script = sql_file.read()

                cursor.execute(sql_script)

        except Error as err:
            messagebox.showerror('Error',f"Error: {err}")
        finally:
            # Cerrar la conexión
            if self.DB.is_connected():
                cursor.close()
                self.DB.close()
            if not self.DB.is_connected():
                self.DB.connect()

    ###############################################################
    ############# FUNCIONES DE TABLAS AUXILIARES - DB #############
    ###############################################################

    def getStateMachineryList(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT * FROM machinery_state"""
            aux.execute(sql)
            data = aux.fetchall()
            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
    
        finally:
            self.DB.close()

    def getCurrencyList(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT * FROM currency"""
            aux.execute(sql)
            data = aux.fetchall()
            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def getBudgetsTypeList(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT * FROM record_type"""
            aux.execute(sql)
            data = aux.fetchall()
            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def getTaxList(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT * FROM tax"""
            aux.execute(sql)
            data = aux.fetchall()

            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    
    def getMeasurementList(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT * FROM measurement"""
            aux.execute(sql)
            data = aux.fetchall()

            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    ##########################################################
    ############# FUNCIONES DE ACTIVIDADES - DB #############
    ##########################################################


   
    def createActivityDB(self, schema, data):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""INSERT INTO activity {str(schema).replace("'",'')} VALUES ({str(len(schema)*'%s,')[:-1]})"""
            aux.execute(sql, data)
            self.DB.commit()
            aux.close()

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    ##########################################################
    ############# FUNCIONES DE FACTURAS - DB #############
    ##########################################################

    def getNextBillCode(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT AUTO_INCREMENT
            FROM information_schema.TABLES
            WHERE TABLE_SCHEMA = '{os.getenv('DB_NAME')}'
            AND TABLE_NAME = 'bills'"""
            aux.execute(sql)
            info = aux.fetchone()
            aux.close()
            return info
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
   
        finally:
            self.DB.close()
    def createBillDB(self, schema, data):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""INSERT INTO bills {str(schema).replace("'",'')} VALUES ({str(len(schema)*'%s,')[:-1]})"""
          
            aux.execute(sql, data)
            self.DB.commit()
            bill_id = aux.lastrowid
            aux.close()
            return bill_id

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
    
        finally:
            self.DB.close()

    def deleteOneBillDB(self, code):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""DELETE FROM bills WHERE code=%s"""
            sql1 = f"""DELETE FROM paymentRecords WHERE document=%s and documentType='VENTA'"""
            sql2 = f"""DELETE FROM itemsBills WHERE code=%s"""
            for sentence in [sql2,sql1,sql]:
                aux.execute(sentence, (code,))
                self.DB.commit()
            aux.close()
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def rejectBill(self, code, user):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""UPDATE bills SET documentState=4, processingUser=%s WHERE code=%s"""
            aux.execute(sql, (user,code))
            self.DB.commit()
            aux.close()
        except Error as ex:
            messagebox.showerror('Error',f"Ha ocurrido un error: {ex}")

        finally:
            self.DB.close()
    def updateRejectBill(self, code):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""UPDATE bills SET reused=1 WHERE code=%s"""
            aux.execute(sql, (code,))
            self.DB.commit()
            aux.close()
        except Error as ex:
            messagebox.showerror('Error',f"Ha ocurrido un error: {ex}")

        finally:
            self.DB.close()
    def updateBillDB(self, fields, data):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""UPDATE bills SET {fields} WHERE code=%s"""

            aux.execute(sql, data)
            self.DB.commit()
            aux.close()

        except Error as ex:
            messagebox.showerror('Error',f"Ha ocurrido un error: {ex}")

        finally:
            self.DB.close()

    def findAllBillsDB(self, search_value, condition_field, codition_operator, filter_status):
        try:
            self.DB.connect() 
            data = []
            aux = self.DB.cursor(buffered=True, )
            sql = f"""SELECT b.code,ps.description,cr.description, b.total_amount,ds.description,b.description,c.name,b.creationDate, b.expirationDate, b.exchange_rate, cu.username, pu.username, b.documentState FROM bills b
             INNER JOIN clients c ON c.rif = client
             INNER JOIN paymentStatus ps ON ps.id = b.payment_status
             INNER JOIN currency cr ON cr.id = b.currency
             INNER JOIN documentState ds ON ds.id = b.documentState
             INNER JOIN users cu ON cu.id = b.creationUser
             LEFT JOIN users pu ON pu.id = b.processingUser
             WHERE {condition_field} {codition_operator} %s"""
            data.append(f'%{search_value}%')
            if filter_status:
                sql += ' AND b.state=%s'
                data.append(filter_status)
            aux.execute(sql, data)
            data = aux.fetchall()
            aux.close()
       
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def findRejectBillsDB(self):
        try:
            self.DB.connect() 
            data = []
            aux = self.DB.cursor(buffered=True,dictionary=True)
            sql = f"""SELECT *FROM bills  WHERE documentState = 4 and reused=0"""
            aux.execute(sql,)
            data = aux.fetchall()
            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    
    def findOneBillDB(self, search_value):
        try:
            self.DB.connect() 
            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = f"""SELECT * FROM bills WHERE code =  %s"""
        
            aux.execute(sql, (search_value,))
            data = aux.fetchone()
            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def findBillsByClientDB(self, clientID, date:list = None, condition = None, status = None, dateField = 'creationDate', unpaid = False):
        try:
            self.DB.connect()  
            data = []
            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = """SELECT * FROM bills WHERE client = %s"""
            data.append(clientID)
  
            if date != None:
                sql += f" AND {dateField} BETWEEN %s AND %s"
                data.extend(date)
  
            if status:
                sql += 'AND payment_status = %s'
                data.append(status)
      
            if unpaid:
                sql += " AND debtUSD > 0"
                
            aux.execute(sql, data)
            bills = aux.fetchall()
            aux.close()
            return bills
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    
    def getCurrencyValues(self, currency_id = 2):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT amount FROM currency WHERE id=%s"""
            aux.execute(sql,(currency_id,))
            data = aux.fetchone()
            aux.close()
            return data[0]

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
    ######################
    #   finally:
    # self.DB.close()####################################
    ############# FUNCIONES DE COTIZACIONES - DB #############
    ##########################################################
    def getNextBillCode2(self):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = """SELECT code
                FROM bills
                ORDER BY code DESC
                LIMIT 1;"""
            aux.execute(sql)
            info = aux.fetchone()
            if not info:
                info = 0
            else:
                info = info[0]

            aux.close()
            return info +1
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
   
        finally:
            self.DB.close()


    def getNextBudgetCode2(self):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = """SELECT code
                FROM budgets
                ORDER BY code DESC
                LIMIT 1;"""
            aux.execute(sql)
            info = aux.fetchone()
            if not info:
                info = 0
            else:
                info = info[0]

            aux.close()
            return info +1
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
   
        finally:
            self.DB.close()
    def getNextBudgetCode(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT *
            FROM information_schema.TABLES
            WHERE TABLE_SCHEMA = '{os.getenv('DB_NAME')}'
            AND TABLE_NAME = 'budgets'"""
            aux.execute(sql)
            info = aux.fetchone()
            aux.close()

            return info
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
   
        finally:
            self.DB.close()
    def createBudgetDB(self, schema, data):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""INSERT INTO budgets {str(schema).replace("'",'')} VALUES ({str(len(schema)*'%s,')[:-1]})"""
            aux.execute(sql, data)
            self.DB.commit()
            ID = aux.lastrowid
            aux.close()
            return ID
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
        #SELECT LAST_INSERT_ID()
    def budgetCodeInserted(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT LAST_INSERT_ID()"""
            aux.execute(sql)
            code = aux.fetchone()
            aux.close()
            return code
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def idBudgcex(self):
        aux = self.DB.cursor(buffered=True)
        sql = """SELECT AUTO_INCREMENT
        FROM information_schema.TABLES
        WHERE TABLE_SCHEMA = 'sg_db'
        AND TABLE_NAME = 'budgets';"""
        aux.execute(sql)
        code = aux.fetchone()
        aux.close()
        return code

    def updateBudgetDB(self, fields, data):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""UPDATE budgets SET {fields} WHERE code=%s"""
            aux.execute(sql, data)
            self.DB.commit()
            aux.close()

        except Error as ex:
            messagebox.showerror('Error',f"Ha ocurrido un error: {ex}")

        finally:
            self.DB.close()
    
    def rejectBudgetByTimeDB(self):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql_COTZ = """SELECT code, DATE_ADD(processingDate, INTERVAL validationDays DAY) FROM budgets  
                WHERE state=2 AND DATE_ADD(processingDate, INTERVAL validationDays DAY) <= %s"""
            aux.execute(sql_COTZ, (datetime.today().strftime('%Y-%m-%d'),))
            COTZ = aux.fetchall()
            
            sql = f"""UPDATE budgets 
                SET state = 4 
                WHERE DATE_ADD(processingDate, INTERVAL validationDays DAY) <= %s AND state=2 """
            
            aux.execute(sql, (datetime.today().strftime('%Y-%m-%d'),))
            self.DB.commit()
            aux.close()
            if COTZ == None:
                return 0
            return COTZ
        except Error as ex:
            messagebox.showerror('Error',f"Ha ocurrido un error: {ex}")

        finally:
            self.DB.close()

    def checkBudgetCodeDB(self, code):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT * FROM budgets WHERE code=%s"""
            aux.execute(sql, (code,))
            data = aux.fetchone()
            aux.close()
            return data
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def findOneBudgetDB(self, search_value=''):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = f"""SELECT * FROM budgets WHERE code=%s"""
            aux.execute(sql, (search_value,))
            data = aux.fetchone()
            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    
    

    def deleteOneBudgetDB(self, rif):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""DELETE FROM budgets WHERE code=%s"""
            aux.execute(sql, (rif,))
            self.DB.commit()
            aux.close()
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
    
        finally:
            self.DB.close()
  

    ##################################################################
    ############# FUNCIONES DE ITEMS - COTIZACIONES - DB #############
    ##################################################################

   
    def createItemBudgetDB(self, schema, data):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""INSERT INTO itemsBudgets {str(schema).replace("'",'')} VALUES ({str(len(schema)*'%s,')[:-1]})"""
            aux.execute(sql, data)
            self.DB.commit()
            aux.close()

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def findABudgetitemsDB(self, Budget_code):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = f"""SELECT * FROM itemsBudgets WHERE code = %s"""
            aux.execute(sql, (Budget_code,))
            data = aux.fetchall()
            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def createItemBillsDB(self, schema, data):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""INSERT INTO itemsBills {str(schema).replace("'",'')} VALUES ({str(len(schema)*'%s,')[:-1]})"""
            aux.execute(sql, data)
            self.DB.commit()
            aux.close()

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def findABillsitemsDB(self, Bills_code):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = f"""SELECT * FROM itemsBills WHERE code = %s"""
            aux.execute(sql, (Bills_code,))
            data = aux.fetchall()
            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    

    def returnQuantityOneItemsDB(self, bill_code, itemId):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT quantity FROM itemsBudgets WHERE code = %s and itemId = %s"""

            aux.execute(sql, (bill_code,itemId))
            data = aux.fetchone()
            aux.close()
            if not data:
                data = 0
            else:
                data = data[0]
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    
    def returnQuantityOneItemsBillDB(self, bill_code, itemId):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT quantity FROM itemsbills WHERE code = %s and itemId = %s"""

            aux.execute(sql, (bill_code,itemId))
            data = aux.fetchone()
            aux.close()
            if not data:
                data = 0
            else:
                data = data[0]
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()


            
    
    def findAllBudgetsDB(self, search_value, condition_field, codition_operator, filter_status):
        try:
            self.DB.connect() 
            data = []
            aux = self.DB.cursor(buffered=True, )
            sql = f"""SELECT b.code,b.description,s.description,bt.type,c.name,b.address,b.representative,b.creationDate,cr.description,b.sub_total,b.iva,b.total_amount,cu.username,pu.username FROM budgets b
             INNER JOIN clients c ON c.rif = client
             INNER JOIN representative r ON r.id = representative
             INNER JOIN currency cr ON cr.id = currency
             INNER JOIN status s ON s.id = state
             INNER JOIN record_type bt ON bt.id = b.type
             INNER JOIN users cu ON cu.id = b.creationUser
             LEFT JOIN users pu ON pu.id = b.processingUser
             WHERE {condition_field} {codition_operator} %s"""
            data.append(f'%{search_value}%')
            if filter_status:
                sql += ' AND b.state=%s'
                data.append(filter_status)
            aux.execute(sql, data)
            data = aux.fetchall()
            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def countBudgetsByState(self, state):
        try:
            self.DB.connect() 
     
            aux = self.DB.cursor(buffered=True, )
            sql = f"""SELECT COUNT(*) FROM budgets WHERE state = %s"""
          
            aux.execute(sql, (state,))
            data = aux.fetchone()
            aux.close()
            return data[0]

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
    
        finally:
            self.DB.close()
    

    def deleteAllItemsByBudget(self, budget_code):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""DELETE FROM itemsBudgets WHERE code=%s"""
            aux.execute(sql, (budget_code,))
            self.DB.commit()
            aux.close()
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    
    ############# FUNCIONES DE USUARIOS - DB #############


    #######################################################
    ############# FUNCIONES DE SERVICIOS - DB #############
    #######################################################

    def createServiceDB(self, schema, data):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""INSERT INTO services {str(schema).replace("'",'')} VALUES ({str(len(schema)*'%s,')[:-1]})"""
            aux.execute(sql, data)
            self.DB.commit()
            aux.close()

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def updateServiceDB(self, fields, data):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""UPDATE services SET {fields} WHERE code=%s"""
            aux.execute(sql, data)
            self.DB.commit()
            aux.close()

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def findOneServiceDB(self, code):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = f"""SELECT * FROM services WHERE code=%s"""
            aux.execute(sql, (code,))
            data = aux.fetchone()
            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def findAllServicesDB(self, search_value = '', condition_field = 'name', codition_operator = 'LIKE'):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True, )
            sql = f"""SELECT code,name,s.description,c.description,warranty FROM services s
             INNER JOIN currency c ON c.id = currency
             WHERE {condition_field} {codition_operator} %s"""
            aux.execute(sql, (f'%{search_value}%',))
            data = aux.fetchall()
            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def findAllServicesNativeDB(self, search_value = '',):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = f"""SELECT * FROM services
             WHERE name LIKE %s"""
            aux.execute(sql, (f'%{search_value}%',))
            data = aux.fetchall()
            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
        
    def deleteOneServiceDB(self, code):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""DELETE FROM services WHERE code=%s"""
            aux.execute(sql, (code,))
            self.DB.commit()
            aux.close()
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    
    def checkServiceCodeDB(self, code):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT * FROM services WHERE code=%s"""
            aux.execute(sql, (code,))
            data = aux.fetchone()
            aux.close()
            return data
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def countServiceRecords(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT COUNT(*) FROM services"""
            aux.execute(sql)
            data = aux.fetchone()
            aux.close()
            return data[0]

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()




    #######################################################
    ############# FUNCIONES DE MAQUINARIA - DB #############
    #######################################################

    def createMachineryDB(self, schema, data):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""INSERT INTO machinery {str(schema).replace("'",'')} VALUES ({str(len(schema)*'%s,')[:-1]})"""
            aux.execute(sql, data)
            self.DB.commit()
            aux.close()

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def updateMachineryDB(self, fields, data):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""UPDATE machinery SET {fields} WHERE code=%s"""
            aux.execute(sql, data)
            self.DB.commit()
            aux.close()

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def changeMachineryStateDB(self,code, state):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""UPDATE machinery SET status=%s WHERE code=%s"""
            aux.execute(sql, (state,code))
            self.DB.commit()
            aux.close()

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def findOneMachineryDB(self, code):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = f"""SELECT * FROM machinery WHERE code=%s"""
            aux.execute(sql, (code,))
            data = aux.fetchone()
            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def findAllMachinerysDB(self, search_value = '', condition_field = 'description', codition_operator = 'LIKE', machiery_filter = None):
        try:
            self.DB.connect()
            data = []
            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = f"""SELECT code,description, brand, model, status FROM machinery
             WHERE {condition_field} {codition_operator} %s"""
            data.append(f'%{search_value}%')
            if machiery_filter:
                sql+=' AND status = %s'
                data.append(machiery_filter)
            
            aux.execute(sql, data)
            data = aux.fetchall()
            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        
        finally:
            self.DB.close()

    def deleteOneMachineryDB(self, code):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""DELETE FROM machinery WHERE code=%s"""
            aux.execute(sql, (code,))
            self.DB.commit()
            aux.close()
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    
    def checkMachineryCodeDB(self, code):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT * FROM machinery WHERE code=%s"""
            aux.execute(sql, (code,))
            data = aux.fetchone()
            aux.close()
            return data
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def countMachineryRecords(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT COUNT(*) FROM machinery"""
            aux.execute(sql)
            data = aux.fetchone()
            aux.close()
            return data[0]

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def getMachineryNotAvailableDB(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = f"""SELECT code, status FROM machinery WHERE status=2 or status=3"""
            aux.execute(sql)
            data = aux.fetchall()
            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()





    #######################################################
    ############# FUNCIONES DE PRODUCTOS - DB #############
    #######################################################

    def findAllProductsDB(self, search_value = '', condition_field = 'code', codition_operator = 'LIKE'):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True, )
            sql = f"""SELECT code,pd.description,b.description,d.description,p.name,m.description,c.description FROM products pd
             INNER JOIN brand b ON b.id = brand
             INNER JOIN department d ON d.id = department
             INNER JOIN providers p ON p.id = provider
             INNER JOIN measurement m ON m.id = measurement
             INNER JOIN currency c ON c.id = currency
             WHERE {condition_field} {codition_operator} %s"""
            aux.execute(sql, (f'%{search_value}%',))
            data = aux.fetchall()
            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def findAllProductsNativeDB(self, search_value = '',condition_field = 'code', codition_operator = 'LIKE'):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = f"""SELECT * FROM products 
             WHERE {condition_field} {codition_operator} %s"""
            aux.execute(sql, (f'%{search_value}%',))
            data = aux.fetchall()
            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
    
        finally:
            self.DB.close()


    def findOneProductDB(self, search_value=''):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = f"""SELECT * FROM products WHERE code=%s"""
            aux.execute(sql, (search_value,))
            data = aux.fetchone()
            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def createProductDB(self, schema, data):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""INSERT INTO products {str(schema).replace("'",'')} VALUES ({str(len(schema)*'%s,')[:-1]})"""
            aux.execute(sql, data)
            self.DB.commit()
            aux.close()

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def updateProductDB(self, fields, data):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""UPDATE products SET {fields} WHERE code=%s"""
            aux.execute(sql, data)
            self.DB.commit()
            aux.close()

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def reduceExistenceProductDB(self, amount, code):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = """UPDATE products SET stock=stock-%s WHERE code=%s"""
            aux.execute(sql, (amount, code))
            self.DB.commit()
            aux.close()

        except:
            pass
        finally:
            self.DB.close()

    def addExistenceProductDB(self, amount, code):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = """UPDATE products SET stock=stock+%s WHERE code=%s"""
            aux.execute(sql, (amount, code))
            self.DB.commit()
            aux.close()

        except:
            pass
        finally:
            self.DB.close()

    def checkProductCodeDB(self, code):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT * FROM products WHERE code=%s"""
            aux.execute(sql, (code,))
            data = aux.fetchone()
            aux.close()
            return data
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def deleteOneProductDB(self, rif):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""DELETE FROM products WHERE code=%s"""
            aux.execute(sql, (rif,))
            self.DB.commit()
            aux.close()
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
    
        finally:
            self.DB.close()
    def getProductsOutOfStockDB(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = f"""SELECT code, stock FROM products WHERE stock<=5"""
            aux.execute(sql)
            data = aux.fetchall()
            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def countProductRecords(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT COUNT(*) FROM products"""
            aux.execute(sql)
            data = aux.fetchone()
            aux.close()
            return data[0]

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    #########################################################
    ########### FUNCIONES DE REPRESENTANTES - DB ############
    #########################################################

    def createRepresentativeDB(self, schema, data):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""INSERT INTO representative {str(schema).replace("'",'')} VALUES ({str(len(schema)*'%s,')[:-1]})"""
            aux.execute(sql, data)
            self.DB.commit()
            aux.close()
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def updateRepresentativeDB(self, fields, data):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""UPDATE representative SET {fields} WHERE id=%s"""
            
            aux.execute(sql,data)
            self.DB.commit()
            aux.close()
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    
    def findOneRepresentativeDB(self, idP):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = f"""SELECT * FROM representative WHERE id = %s"""
            aux.execute(sql, (idP,))
            data = aux.fetchone()
            aux.close()
            return data
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def findAllRepresentativesByNameDB(self, name = '', filter_company = None):
        try:
            self.DB.connect()
            data = []
            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT r.id,r.name,lastname,c.name,department,r.phone,r.email FROM representative r
            INNER JOIN clients c ON c.rif = company
            WHERE lastname LIKE %s"""
            data.append(f'%{name}%')
            if filter_company:
                sql +=" AND company = %s"
                data.append(filter_company)
            aux.execute(sql, data)
            data = aux.fetchall()
            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def deleteOneRepresentativeDB(self, Id):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""DELETE FROM representative WHERE id=%s"""
            aux.execute(sql, (Id,))
            self.DB.commit()
            aux.close()
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def checkRepresentativeIdCodeDB(self, Id):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT * FROM representative WHERE id=%s"""
            aux.execute(sql, (Id,))
            data = aux.fetchone()
            aux.close()
            return data
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()


    

    #########################################################
    ############# FUNCIONES DE CLIENTES - DB #############
    #########################################################

    def createClientDB(self, schema, data):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)

            sql = f"""INSERT INTO clients {str(schema).replace("'",'')} VALUES ({str(len(schema)*'%s,')[:-1]})"""
            
            aux.execute(sql, data)
            self.DB.commit()
            aux.close()
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def updateClientDB(self, fields, data):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""UPDATE clients SET {fields} WHERE rif=%s"""
            
            aux.execute(sql,data)
            self.DB.commit()
            aux.close()
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    
    def findOneClientDB(self, idP):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = f"""SELECT * FROM clients WHERE rif = %s"""
            aux.execute(sql, (idP,))
            data = aux.fetchone()
            aux.close()
            return data
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def findAllClientsByNameDB(self, name = ''):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = f"""SELECT * FROM clients WHERE name LIKE  %s"""
            aux.execute(sql, (f'%{name}%',))
            data = aux.fetchall()
            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def deleteOneClient(self, rif):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""DELETE FROM clients WHERE rif=%s"""
            aux.execute(sql, (rif,))
            self.DB.commit()
            aux.close()
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def checkClientRifCode(self, rif):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT * FROM clients WHERE rif=%s"""
            aux.execute(sql, (rif,))
            data = aux.fetchone()
            aux.close()
            return data
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    
    #########################################################
    ############# FUNCIONES DE PROVEEDORES - DB #############
    #########################################################

    def createProviderDB(self, schema, data):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)

            sql = f"""INSERT INTO providers {str(schema).replace("'",'')} VALUES ({str(len(schema)*'%s,')[:-1]})"""
            
            aux.execute(sql, data)
            self.DB.commit()
            aux.close()
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def updateProviderDB(self, fields, data):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""UPDATE providers SET {fields} WHERE rif=%s"""
            
            aux.execute(sql,data)
            self.DB.commit()
            aux.close()
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    
    def findOneProviderDB(self, idP):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = f"""SELECT * FROM providers WHERE id = %s"""
            aux.execute(sql, (idP,))
            data = aux.fetchone()
            aux.close()
            return data
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def findAllProvidersByNameDB(self, name = ''):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = f"""SELECT * FROM providers WHERE name LIKE  %s"""
            aux.execute(sql, (f'%{name}%',))
            data = aux.fetchall()
            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def deleteOneProvider(self, rif):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""DELETE FROM providers WHERE rif=%s"""
            aux.execute(sql, (rif,))
            self.DB.commit()
            aux.close()
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def checkProviderRifCode(self, rif):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT * FROM providers WHERE rif=%s"""
            aux.execute(sql, (rif,))
            data = aux.fetchone()
            aux.close()
            return data
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()



    ##########################################################
    ############# FUNCIONES DE ACTIVIDADES - DB #############
    #########################################################
            
    def activityToExpireDB(self):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql_COTZ = """SELECT id, budget_code FROM activity  
                WHERE stage<=2 AND DATE_ADD(final_date, INTERVAL -1 DAY) = %s"""
            aux.execute(sql_COTZ, (datetime.today().strftime('%Y-%m-%d'),))
            COTZ = aux.fetchall()
            
            

            aux.close()
            return COTZ
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def findOneActivityDB(self,activityId):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = f"""SELECT * FROM activity WHERE id=%s"""
            aux.execute(sql, (activityId,))
            data = aux.fetchone()
            aux.close()
            return data
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def countaActivityByState(self, state):
        try:
            self.DB.connect() 
     
            aux = self.DB.cursor(buffered=True, )
            sql = f"""SELECT COUNT(*) FROM activity WHERE stage = %s"""
          
            aux.execute(sql, (state,))
            data = aux.fetchone()
            aux.close()
            return data[0]

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    #################################################################
    ############# FUNCIONES DE REGISTRO DE COMPRAS - DB #############
    #################################################################

    def findAllPurchasesDB(self, date = None, dateField = 'registrationDate',datefilter=None):
        try:
            self.DB.connect()  
            data = []
            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = """SELECT * FROM purchases"""
            if date != None:
                if datefilter==None:
                    sql += f" WHERE {dateField} = %s"
                    data.append(date)
                elif datefilter=='MONTH':
                    sql += f" WHERE MONTH({dateField}) = %s AND YEAR({dateField})=%s"
                    data.extend([date, datetime.today().year])
                elif datefilter=='YEAR':
                    sql += f" WHERE YEAR({dateField}) = %s"
                    data.append(date)
                else:
                    sql += f" WHERE {dateField} BETWEEN %s AND %s"
                    data.extend(date)

            aux.execute(sql, data)
            purchases = aux.fetchall()
            aux.close()
            return purchases
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()


    def findPurchasesByProviderDB(self, providerId, date:list = None, condition = None, status = None, dateField = 'registrationDate', unpaid = False):
        try:
            self.DB.connect()  
            data = []
            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = """SELECT * FROM purchases WHERE provider = %s"""
            data.append(providerId)
  
            if date != None:
                sql += f" AND {dateField} BETWEEN %s AND %s"
                data.extend(date)
  
            if status:
                sql += 'AND payment_status = %s'
                data.append(status)
      
            if condition:
                sql += 'AND condition = %s'
                data.append(condition)
            if unpaid:
                sql += " AND debtUSD > 0"
                
            aux.execute(sql, data)
            purchases = aux.fetchall()
            aux.close()
            return purchases
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()



    def createPurchaseDB(self, schema, data):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""INSERT INTO purchases {str(schema).replace("'",'')} VALUES ({str(len(schema)*'%s,')[:-1]})"""
            aux.execute(sql, data)
            self.DB.commit()
            aux.close()

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def findProviderPayments(self, providerRif=None,billCode=None):
        try:
            self.DB.connect()  
            data = []
            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = """SELECT * FROM paymentRecords WHERE company = %s and documentType = 'COMPRA'"""
            data.append(providerRif)
  
            if billCode:
                sql += f" AND document = %s"
                data.append(billCode)

            aux.execute(sql, data)
            purchases = aux.fetchall()
            aux.close()
            return purchases
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()


    def findOnePurchaseDB(self, code, rif):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = f"""SELECT * FROM purchases WHERE code=%s and provider=%s"""
            aux.execute(sql, (code,rif))
            data = aux.fetchone()
            
            aux.close()
            return data
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def find_currency_usd(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT amount FROM currency WHERE id=2"""
            aux.execute(sql)
            data = aux.fetchone()[0]
            
            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def insert_purchase_items(self, items):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""INSERT INTO purchases_products (purchaseCode,product_code,description,tax,currency,presentation,cost,price1,
            price2,price3,profit1,profit2,profit3,quantity,quantity1,quantity2,quantity3,quantity4,totalStock,totalcost,totalcostdocumentcurrency) 
            VALUES ({('%s,'*21)[:-1]})"""
            aux.executemany(sql,items)
            self.DB.commit()
            aux.close()
      

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def find_purchase_items(self, code):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT pp.purchaseCode, pp.product_code, pp.description, t.description, c.description, m.description,
            pp.cost, pp.price1, pp.price2, pp.price3, pp.profit1, pp.profit2, pp.profit3, pp.quantity, pp.quantity1, pp.quantity2,
            pp.quantity3, pp.quantity4, pp.totalStock, pp.totalcost, pp.totalcostdocumentcurrency FROM purchases_products pp
            INNER JOIN tax t ON t.id = pp.tax
            INNER JOIN currency c ON c.id = pp.currency
            INNER JOIN measurement m ON m.id = pp.presentation
            WHERE purchaseCode = %s"""
            aux.execute(sql,(code,))
            items = aux.fetchall()
            aux.close()
            return items

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    
    def get_provider_balance(self, field, provider_rif):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)

            sql = f"""SELECT
                        SUM(
                        d.{field}
                        ) AS total_deuda_en_currency_deseada
                    FROM
                        purchases d
                    LEFT JOIN
                        currency cBS ON cBS.id = 1
                    LEFT JOIN
                        currency cUSD ON cUSD.id = 2
                    WHERE d.provider = %s
                    """
            aux.execute(sql, (provider_rif,))
            data = aux.fetchone()[0]
            aux.close()
            if not data:
                return 0
            return round(data,2)
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    

    def get_client_balance(self, field, client_rif):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)

            sql = f"""SELECT
                        SUM(d.{field})
                    FROM
                        bills d
                    LEFT JOIN
                        currency cBS ON cBS.id = 1
                    LEFT JOIN
                        currency cUSD ON cUSD.id = 2
                    WHERE d.client = %s
                    """
            aux.execute(sql, (client_rif,))
            data = aux.fetchone()[0]
            aux.close()
            if not data:
                return 0
            return round(data,2)
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    ############## ACTIVITIES ##############

    def get_activity(self, id):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = f"""SELECT * FROM activity where id=%s"""
            aux.execute(sql,(id,))
            data = aux.fetchone()
           
            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def find_activities(self, search_value='', state = ''):
        try:
            self.DB.connect()
            data = [f'%{search_value}%',]
            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = f"""SELECT * FROM activity WHERE budget_code LIKE %s AND complete=0"""
            if state:
                sql += ' AND stage = %s'
                data.append(state)
            aux.execute(sql, data)
            data = aux.fetchall()
            
            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def find_activities_to_expire(self, date = datetime.today() + timedelta(days=1)):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True, dictionary=True)
            final_date = date
            sql = f"""SELECT * FROM activity WHERE complete=0 AND final_date=%s AND stage>1"""
            aux.execute(sql, (final_date,))
            data = aux.fetchall()
            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()


    def update_task(self, idT, state):
        try:
            self.DB.connect()
            
            aux = self.DB.cursor(buffered=True)
            sql = f"""UPDATE task SET complete=%s WHERE id=%s"""
            aux.execute(sql,(state,idT))
            self.DB.commit()
            aux.close()
            
            
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        
        finally:
            self.DB.close()

    def update_machinery_state(self, idT, state):
        try:
            self.DB.connect()
            
            aux = self.DB.cursor(buffered=True)
            sql = f"""UPDATE machinery SET status=%s WHERE code=%s"""
            aux.execute(sql,(state,idT))
            self.DB.commit()
            aux.close()
            
            
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
            
        finally:
            self.DB.close()
    ##################################################################
    ############# FUNCIONES DE DEPARTMENTO Y MARCAS - DB #############
    ##################################################################

    def subTable_insert(self, table, data):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"INSERT INTO {table} (description) VALUES (%s)"
            info = (data,)
            aux.execute(sql,info)
            self.DB.commit()
            aux.close()

        except:
            pass
        finally:
            self.DB.close()


    def get_next_id_subtable(self, table):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT AUTO_INCREMENT
                    FROM INFORMATION_SCHEMA.TABLES
                    WHERE TABLE_NAME = '{table}'"""
            aux.execute(sql)
            data = aux.fetchone()

            aux.close()
            return data
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            self.DB.close()


    
    def subTable_find(self, table, data):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = f"""SELECT * FROM {table} WHERE description LIKE %s ORDER BY id ASC"""

            info = ( f'%{data}%',)
            aux.execute(sql, info)
            data = aux.fetchall()
            aux.close()

            return data
            
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def subTable_Update(self, table, value, id):
        try:
            self.DB.connect()
            
            aux = self.DB.cursor(buffered=True)
            sql = f"""UPDATE {table} SET description=%s WHERE id=%s"""
            aux.execute(sql,(value,id))
            self.DB.commit()
            aux.close()
            
            
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
            
        finally:
             self.DB.close()

    def subTable_delete(self, table, id):
        try:
            self.DB.connect()
            
            aux = self.DB.cursor(buffered=True)
            sql = f"""DELETE FROM {table} WHERE id=%s"""
            aux.execute(sql,(id,))
            self.DB.commit()
            aux.close()
            
            
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def createPaymentRecord(self, schema, data):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""INSERT INTO paymentRecords {str(schema).replace("'",'')} VALUES ({str(len(schema)*'%s,')[:-1]})"""

            aux.executemany(sql, data)
            self.DB.commit()
            aux.close()
            return True

        except Error as ex:
            messagebox.showerror('Error',f"Error: {ex}")
            return False
        finally:
            self.DB.close()

        
    def findClientPayments(self, clientRIF=None,billCode=None):
        try:
            self.DB.connect()  
            data = []
            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = """SELECT * FROM paymentRecords WHERE company = %s and documentType = 'VENTA'"""
            data.append(clientRIF)
  
            if billCode:
                sql += f" AND document = %s"
                data.append(billCode)

            aux.execute(sql, data)
            purchases = aux.fetchall()
            aux.close()
            return purchases
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    
    def findPayments(self, billCode):
        try:
            self.DB.connect()  
            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = """SELECT * FROM paymentRecords WHERE document = %s and documentType='VENTA'"""


            aux.execute(sql, (billCode,))
            payments = aux.fetchall()
            aux.close()
            return payments
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def getBillTypeList(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT * FROM billType"""
            aux.execute(sql)
            data = aux.fetchall()
            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
    
        finally:
            self.DB.close()
    ###################### statistic ##########################
            
    def growthRateDB(self, initial_date=None, final_date=None):
        try:
            self.DB.connect()
            if not final_date:
                date = datetime.today()
                final_date = datetime.today()
                initial_date = datetime(year=date.year,month=date.month,day=1) - timedelta(days=1)
                
        

            aux = self.DB.cursor(buffered=True)
            sql1 = f"""SELECT SUM(totalUSD) FROM bills WHERE YEAR(creationDate) = {initial_date.year} AND MONTH(creationDate) = {initial_date.month} AND documentState<>4"""
            aux.execute(sql1)
            ventaspasadas = aux.fetchone()[0]

            sql2 = f"""SELECT SUM(totalUSD) FROM bills WHERE YEAR(creationDate) = {final_date.year} AND MONTH(creationDate) = {final_date.month} AND documentState<>4"""
            aux.execute(sql2)
            ventasactuales = aux.fetchone()[0]


            if ventasactuales and ventaspasadas and ventaspasadas > 0:
                return round(((ventasactuales-ventaspasadas)/ventaspasadas)*100,2)
            else:
                return 0
            

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    
    def UtilityRateDB(self, initial_date=None, final_date=None):
        try:
            self.DB.connect()
           

            aux = self.DB.cursor(buffered=True)
            sql1 = f"""SELECT SUM(quantity*cost) FROM itemsBills"""
            aux.execute(sql1)
            costo = aux.fetchone()[0]

            sql2 = f"""SELECT SUM(totalUSD) FROM itemsBills"""
            aux.execute(sql2)
            ingresos = aux.fetchone()[0]

    

            if costo and costo > 0:
                return round(((ingresos-costo)/ingresos)*100,2)
            else:
                return 0
            

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def totalGainDB(self):
        try:
            self.DB.connect()
           

            aux = self.DB.cursor(buffered=True)
            sql1 = f"""SELECT SUM(totalpaidUSD) FROM bills WHERE documentState<>4"""
            aux.execute(sql1)
            cobrado = aux.fetchone()[0]
            if not cobrado:
                cobrado = 0

            sql2 = f"""SELECT SUM(totalUSD) FROM bills WHERE documentState<>4"""
            aux.execute(sql2)
            total = aux.fetchone()[0]

            if total and total > 0:
                return [round(cobrado,2), round(total,2)]
            else:
                return [0,1]
            

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def totalSpentDB(self):
        try:
            self.DB.connect()
           

            aux = self.DB.cursor(buffered=True)
            sql1 = f"""SELECT SUM(totalpaidUSD) FROM purchases"""
            aux.execute(sql1)
            pagado = aux.fetchone()[0]
            if not pagado:
                pagado = 0

            sql2 = f"""SELECT SUM(totalUSD) FROM purchases"""
            aux.execute(sql2)
            total = aux.fetchone()[0]



            if total and  total > 0:
                return [round(pagado,2), round(total,2)]
        
            return [0,1]
            

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    
    def get_sales_flow(self,startDate, endDate):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)

            sql = """SELECT
                        YEAR(creationDate) AS year,
                        MONTH(creationDate) AS month,
                        ROUND(SUM(totalUSD),2) AS cantidad_total
                    FROM
                        bills
                    WHERE
                        creationDate BETWEEN %s AND %s AND documentState<>4
                    GROUP BY YEAR(creationDate), MONTH(creationDate)
                    ORDER BY year, month"""
            aux.execute(sql,(startDate, endDate))
            data = aux.fetchall()
            aux.close()
            return data
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            self.DB.close()
    
    def get_income_expenses(self,startDate, endDate):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)

            sql = """SELECT
                        YEAR(creationDate) AS year,
                        MONTH(creationDate) AS month,
                        ROUND(SUM(totalUSD),2) AS cantidad_total
                    FROM
                        bills 
                    WHERE 
                        creationDate BETWEEN %s AND %s AND documentState<>4
                    GROUP BY YEAR(creationDate), MONTH(creationDate)
                    ORDER BY year, month"""
            aux.execute(sql,(startDate, endDate))
            data = aux.fetchall()

            sql2 = """SELECT
                        YEAR(dateOfIssue) AS year,
                        MONTH(dateOfIssue) AS month,
                        ROUND(SUM(totalUSD),2) AS cantidad_total
                    FROM
                        purchases
                    WHERE dateOfIssue BETWEEN %s AND %s 
                    GROUP BY YEAR(dateOfIssue), MONTH(dateOfIssue)
                    ORDER BY year, month"""
            aux.execute(sql2,(startDate, endDate))
            data2 = aux.fetchall()

            aux.close()

            return [data, data2]
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            self.DB.close()
    #########################################

    def total_bill_DB(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)

            sql2 = f"""SELECT SUM(totalUSD) FROM bills WHERE documentState<>4"""
            aux.execute(sql2)
            total = aux.fetchone()[0]


            if total and total > 0:
                return total
            else:
                return 0
            

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def total_Purchases_DB(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)

            sql2 = f"""SELECT SUM(totalUSD) FROM purchases"""
            aux.execute(sql2)
            total = aux.fetchone()[0]


            if total and total > 0:
                return total
            else:
                return 0
            

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def total_budgets_DB(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)

            sql2 = f"""SELECT COUNT(*) FROM budgets WHERE processed = 1"""
            aux.execute(sql2)
            total = aux.fetchone()[0]


            if total and total > 0:
                return total
            else:
                return 0
            

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
            
        finally:
            self.DB.close()
            
    def total_activity_DB(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)

            sql2 = f"""SELECT COUNT(*) FROM activity"""
            aux.execute(sql2)
            total = aux.fetchone()[0]


            if total and total > 0:
                return total
            else:
                return 0
            

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    
    def approve_ratio_DB(self):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)

            sql_processed = f"""SELECT COUNT(*) FROM budgets WHERE processed = 1"""
            aux.execute(sql_processed)
            processed = aux.fetchone()[0]


            sql_approve = f"""SELECT COUNT(*) FROM budgets WHERE state = 3"""
            aux.execute(sql_approve)
            approve = aux.fetchone()[0]

            if processed and processed>0:
                return round((approve/processed)*100,2)
            return 0
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            self.DB.close()
    
    def count_total_bills_DB(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)

            sql2 = f"""SELECT COUNT(*) FROM bills"""
            aux.execute(sql2)
            total = aux.fetchone()[0]


            if total and total > 0:
                return total
            else:
                return 0
            

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    
    def inventory_cost_DB(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)

            sql2 = f"""SELECT
            SUM(CASE WHEN p.currency=2 THEN (stock+stock_1+stock_2+stock_3+stock_4)*cost
                ELSE (stock+stock_1+stock_2+stock_3+stock_4)*cost/tc.amount END) AS total_cost
            FROM
                products p
            INNER JOIN currency tc ON tc.id=2"""
            aux.execute(sql2)
            total = aux.fetchone()[0]


            if total and total > 0:
                return round(total,2)
            else:
                return 0
            

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def total_services_complete_DB(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)

            sql2 = f"""SELECT
            COUNT(*)
            FROM
            task 
            WHERE item_type=1 AND complete=1"""
            aux.execute(sql2)
            total = aux.fetchone()[0]


            if total and total > 0:
                return total
            else:
                return 0
            

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    
    def top_10_products_DB(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)

            sql2 = f"""SELECT products.code, products.description, SUM(itemsbills.quantity) as total_vendido
                    FROM products
                    JOIN itemsbills ON products.code = itemsbills.itemId
                    GROUP BY products.code, products.description
                    ORDER BY total_vendido DESC LIMIT 10"""
            aux.execute(sql2)
            products = aux.fetchall()


            return products

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def get_products_vs_services(self,startDate, endDate):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)

            sql = """SELECT
                        YEAR(ITB.date) AS year,
                        MONTH(ITB.date) AS month,
                        SUM(ITB.totalUSD) AS cantidad_total
                    FROM
                        itemsBills ITB
                    INNER JOIN bills b ON b.code = ITB.code
                    WHERE
                        ITB.date BETWEEN %s AND %s AND ITB.itemType = 1 AND b.documentState<>4
                    GROUP BY YEAR(ITB.date), MONTH(ITB.date)
                    ORDER BY year, month"""
            aux.execute(sql,(startDate, endDate))
            services = aux.fetchall()

            sql1 = """SELECT
                        YEAR(ITB.date) AS year,
                        MONTH(ITB.date) AS month,
                        SUM(ITB.totalUSD) AS cantidad_total
                    FROM
                        itemsBills ITB
                    INNER JOIN bills b ON b.code = ITB.code
                    WHERE
                        ITB.date BETWEEN %s AND %s AND ITB.itemType = 2 AND b.documentState<>4
                    GROUP BY YEAR(ITB.date), MONTH(ITB.date)
                    ORDER BY year, month"""
            aux.execute(sql1,(startDate, endDate))
            products = aux.fetchall()

            aux.close()
            return [products, services]
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            self.DB.close()
    



    def get_total_machinery(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)

            sql2 = f"""SELECT
            COUNT(*)
            FROM
            machinery"""
            aux.execute(sql2)
            total = aux.fetchone()[0]


            if total and total > 0:
                return total
            else:
                return 0
            

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def get_total_products(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)

            sql2 = f"""SELECT
            COUNT(*)
            FROM
            products"""
            aux.execute(sql2)
            total = aux.fetchone()[0]


            if total and total > 0:
                return total
            else:
                return 0
            

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    
    def get_total_services(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)

            sql2 = f"""SELECT
            COUNT(*)
            FROM
            services"""
            aux.execute(sql2)
            total = aux.fetchone()[0]


            if total and total > 0:
                return total
            else:
                return 0
            

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def get_total_clients(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)

            sql2 = f"""SELECT
            COUNT(*)
            FROM
            machinery"""
            aux.execute(sql2)
            total = aux.fetchone()[0]


            if total and total > 0:
                return total
            else:
                return 0
            

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
    
        finally:
            self.DB.close()
    def get_total_providers(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)

            sql2 = f"""SELECT
            COUNT(*)
            FROM
            providers"""
            aux.execute(sql2)
            total = aux.fetchone()[0]


            if total and total > 0:
                return total
            else:
                return 0
            

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def get_activity_completed(self):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)

            sql = """SELECT
                        COUNT(*)
                    FROM
                        activity"""
            aux.execute(sql,)
            all_ac = aux.fetchone()[0]

            sql1 = """SELECT
                        COUNT(*)
                    FROM
                        activity
                    WHERE stage=3"""
            aux.execute(sql1,)
            ac_c =aux.fetchone()[0]
            if not ac_c:
                ac_c = 0

            aux.close()
    
            if all_ac and all_ac>0:
                return [ac_c, all_ac]
            
            return [0,0]
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            self.DB.close()
    
    def get_task_completed(self):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)

            sql = """SELECT
                        COUNT(*)
                    FROM
                        task"""
            aux.execute(sql,)
            all_ac = aux.fetchone()[0]

            sql1 = """SELECT
                        COUNT(*)
                    FROM
                        task
                    WHERE complete=1"""
            aux.execute(sql1,)
            ac_c = aux.fetchone()[0]
            if not ac_c:
                ac_c = 0

            aux.close()
        
            if all_ac and all_ac>0:
                return [ac_c, all_ac]
            
            return [0,0]
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            self.DB.close()


    def total_COBRAR_VS_FACTURADO_DB(self):
        try:
            self.DB.connect()
           

            aux = self.DB.cursor(buffered=True)
            sql1 = f"""SELECT SUM(totalpaidUSD) FROM bills WHERE documentState<>4"""
            aux.execute(sql1)
            cobrado = aux.fetchone()[0]

            sql2 = f"""SELECT SUM(debtUSD) FROM bills WHERE documentState<>4"""
            aux.execute(sql2)
            faltante = aux.fetchone()[0]

            return [cobrado,faltante]
        

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def total_aprobado_vs_rechazada_DB(self):
        try:
            self.DB.connect()
           

            aux = self.DB.cursor(buffered=True)
            sql1 = f"""SELECT COUNT(*) FROM budgets WHERE state=3"""
            aux.execute(sql1)
            approve = aux.fetchone()[0]

            sql2 = f"""SELECT  COUNT(*) FROM budgets WHERE state=4"""
            aux.execute(sql2)
            rejected = aux.fetchone()[0]

            return [approve, rejected]
        

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def createUserDb(self, schema,data):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""INSERT INTO users  {str(schema).replace("'",'')} VALUES ({str(len(schema)*'%s,')[:-1]})"""
            aux.execute(sql,data)
            self.DB.commit()
            aux.close()
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            self.DB.close()


    def updateUserDb(self, fields,data):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""UPDATE users SET {fields} WHERE ci=%s"""
            aux.execute(sql,data)
            self.DB.commit()
            aux.close()
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            self.DB.close()

    
    def updateUserPasswordDb(self, password,ci):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""UPDATE users SET password=%s WHERE ci=%s"""
            aux.execute(sql,(password,ci))
            self.DB.commit()
            aux.close()
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            self.DB.close()


    def findAllUsers(self, search_value):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = f"""SELECT * FROM users WHERE username LIKE %s"""
            aux.execute(sql,(f'%{search_value}%',))
            
            users = aux.fetchall()
            aux.close()
            return users
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            self.DB.close()
    

    def findOneUser(self, ci):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = f"""SELECT * FROM users WHERE ci=%s"""
            aux.execute(sql,(ci,))
            
            users = aux.fetchone()
            aux.close()
            return users
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")
        finally:
            self.DB.close()

    def get_roles(self):
        try:
            self.DB.connect()

            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT * FROM rol"""
            aux.execute(sql)
            data = aux.fetchall()
            aux.close()
            return data

        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def checkUserIDDB(self, ci):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT * FROM users WHERE ci=%s"""
            aux.execute(sql, (ci,))
            data = aux.fetchone()
            aux.close()
            return data
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def findPurchasesToExpira(self, date = datetime.today()+timedelta(days=1)):
        try:
            self.DB.connect()  
            
            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = """SELECT * FROM purchases WHERE expirationDate = %s and documentState = 1"""
            aux.execute(sql, (date.strftime("%Y-%m-%d"),))
            purchases = aux.fetchall()
            aux.close()
            return purchases
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def updatePurchasesToExpire(self,):
        try:
            self.DB.connect()  
            aux = self.DB.cursor(buffered=True)
            sql = """SELECT code,provider FROM purchases WHERE expirationDate<=%s and documentState= 1"""
            aux.execute(sql, (datetime.today().strftime('%Y-%m-%d'),))
            purchases = aux.fetchall()

            sql = """UPDATE purchases SET documentState=2 WHERE code= %s AND provider=%s"""
            aux.executemany(sql,purchases)
            aux.close()
            self.DB.commit()
            return purchases
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    
    def findBillsToExpira(self, date = datetime.today()+timedelta(days=1)):
        try:
            self.DB.connect()  
            
            aux = self.DB.cursor(buffered=True, dictionary=True)
            sql = """SELECT * FROM bills WHERE expirationDate = %s and documentState = 1"""
            aux.execute(sql, (date.strftime("%Y-%m-%d"),))
            bills = aux.fetchall()
            aux.close()
            return bills
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def updateBillsToExpire(self,):
        try:
            self.DB.connect()  
            aux = self.DB.cursor(buffered=True)
            sql = """SELECT code,client FROM bills WHERE expirationDate<=%s and documentState= 1"""
            aux.execute(sql, (datetime.today().strftime('%Y-%m-%d'),))
            bills = aux.fetchall()

            sql = """UPDATE bills SET documentState=2 WHERE code= %s AND client=%s"""
            aux.executemany(sql,bills)
            aux.close()
            self.DB.commit()
            return bills
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    def deleteOnePurchase(self, code):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            SQLITEMS = f"""DELETE FROM purchases_products WHERE code=%s"""
            SQLPAYMENTS = f"""DELETE FROM paymentRecords WHERE code=%s AND documentType='COMPRA'"""
            sql = f"""DELETE FROM purchases WHERE code=%s"""
            for row in [SQLITEMS, SQLPAYMENTS, sql]:
                aux.execute(row, (code,))
                self.DB.commit()
            aux.close()
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()

    def select_currency(self):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT amount FROM currency WHERE id=2"""
            aux.execute(sql)
            amount = aux.fetchone()[0]
            aux.close()
            return amount
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error en la base de datos: {ex}")

        finally:
            self.DB.close()
    
    def update_exchange_value(self, amount):
        try:
            self.DB.connect()
            aux = self.DB.cursor(buffered=True)
            sql = f"""UPDATE currency SET amount=%s WHERE id=2"""
            aux.execute(sql,(amount,))
            self.DB.commit()
            aux.close()
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error al actualizar la tasa de cambio: {ex}")

        finally:
            self.DB.close()

    
    def checkClientRecordsDB(self, PROVIDERRIF):
        try:
            self.DB.connect()
            records = 0
            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT COUNT(*) FROM budgets WHERE client=%s"""
            sql2 = f"""SELECT COUNT(*) FROM bills WHERE client=%s"""
            for sentence in [sql,sql2]:
                aux.execute(sentence, (PROVIDERRIF,))
                data = aux.fetchone()
                if data:
                    records += int(data[0])
            aux.close()
     
            return records
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error al actualizar la tasa de cambio: {ex}")
        finally:
            self.DB.close()



    def checkRepresentativeRecordsDB(self, REPRESENTATIVCI):
        try:
            self.DB.connect()
            records = 0
            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT COUNT(*) FROM budgets WHERE representative=%s"""
            aux.execute(sql, (REPRESENTATIVCI,))
            data = aux.fetchone()
            if data:
                records += int(data[0])
            aux.close()
         
            return records
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error al actualizar la tasa de cambio: {ex}")
        finally:
            self.DB.close()

    
    def checkProvidersRecordsDB(self, PROVIDERRIF):
        try:
            self.DB.connect()
            records = 0
            aux = self.DB.cursor(buffered=True)
            sql = f"""SELECT COUNT(*) FROM purchases WHERE provider=%s"""
        
            aux.execute(sql, (PROVIDERRIF,))
            data = aux.fetchone()
            if data:
                records += int(data[0])
            aux.close()
          
            return records
        except Error as ex:
            messagebox.showerror('Error', f"Ha ocurrido un error al actualizar la tasa de cambio: {ex}")
        finally:
            self.DB.close()


import sqlite3
from contextlib import closing
from dataProcessing import *

DATABASE = sqlite3.Connection

def connectDb() -> sqlite3.Connection:
    return sqlite3.connect("customerDb.db")

def createTable(db : DATABASE) -> None:
    query = '''CREATE TABLE IF NOT EXISTS customer (
                    ID VARCHAR(6),
                    name VARCHAR(20) NOT NULL,
                    phone_no VARCHAR(10),
                    PAN_no VARCHAR(10),
                    pincode VARCHAR(6),
                    PRIMARY KEY(ID)
                )'''
    
    with closing(db.cursor()) as c:
        c.execute(query)
    db.commit()

def generateID(db : DATABASE) -> str:
        '''
        returns next ID to be inserted in table
        '''
        query = '''SELECT COUNT(ID) from customer'''
        with closing(db.cursor()) as c:
            c.execute(query)
            rows = c.fetchone()[0]
        rows += 1        
        if rows <= 9:
            return "C-000" + str(rows)
        elif rows <= 99:
            return "C-00" + str(rows)
        elif rows <= 999:
            return "C-0" + str(rows)
        return "C-" + str(rows)

def insertValuesIntoDb(db : DATABASE, data : dict) -> str:
    if data["name"] == "":
        return "insert name"
    
    if not validPhoneNumber(data["phone_no"]):
        return "invalid phone number" 
    
    if not validPIN(data["pincode"]):
        return "invalid pin code"
    
    data["PAN"] = standarisePAN(data["PAN"])
    
    if not validPAN(data["PAN"]):
        return "invalid PAN no."
    
    ID = generateID(db)

    query = '''INSERT INTO customer VALUES (?, ?, ?, ?, ?)'''

    with closing(db.cursor()) as c:
        c.execute(query, (ID, data["name"], data["phone_no"], data["PAN"], data["pincode"]))
    db.commit()

    return "values inserted"

def updateValuesInDb(db : DATABASE, data : dict) -> str:

    if data["name"] == "":
        return "insert name"

    if not validPhoneNumber(data["phone_no"]):
        return "invalid phone number" 
    
    if not validPIN(data["pincode"]):
        return "invalid pin code"
    
    data["PAN"] = standarisePAN(data["PAN"])
    
    if not validPAN(data["PAN"]):
        return "invalid PAN no."
    
    def IDExists() -> bool:
        query = '''SELECT * FROM customer WHERE ID = ?'''

        with closing(db.cursor()) as c:
            c.execute(query, (data["ID"],))
            exists = True if not c.fetchone() == None else False
        return exists

    if not IDExists():
        return "invalid ID"

    query = '''UPDATE customer SET name = ?, phone_no = ?, PAN_no = ?, pincode = ? WHERE ID = ?'''

    with closing(db.cursor()) as c:
        c.execute(query, (data["name"], data["phone_no"], data["PAN"], data["pincode"], data["ID"]))
    db.commit()

    return "values updates"

def returnCustomerData(db : DATABASE, inputStr : str, checkID : bool) -> list:
    
    if checkID:
        query = f'''SELECT * FROM customer where ID like "{inputStr}%"'''
    else:
        query = f'''SELECT * FROM customer where name like "{inputStr}%"'''
    
    with closing(db.cursor()) as c:
        c.execute(query)
        data = c.fetchall()

    return data

def deleteCustomer(db : DATABASE , id : str) -> str:
    query = '''SELECT * FROM customer WHERE ID = ?'''
    with closing(db.cursor()) as c:
        c.execute(query, (id,))
        exists = True if c.fetchone() != None else False
    if not exists:
        return "Customer does not exist"

    query = '''DELETE FROM customer WHERE ID = ?'''
    with closing(db.cursor()) as c:
        c.execute(query, (id,))
    db.commit()
    return "customer removed successfully"


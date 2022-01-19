import sqlite3
import os
import pandas as pd

#making sure the DB file is always new. Only thinking behind doing this is not to over populate the table each time we run it hence 
# reducing the internal load calls.
if os.path.exists('RootDB.db'):
    os.remove('RootDB.db')
#establishing connection with new db file.
con = sqlite3.Connection("RootDB.db")
cur= con.cursor()
# Query to create table
cur.execute('''CREATE TABLE Products (
    Product_id varchar NOT NULL PRIMARY KEY,
    P_name varchar(30),
    P_price varchar(19),
    P_condition varchar(10),
    P_quant varchar(19),
    Description varchar(300))
    ''')

#Populating table with dummy data.
cur.execute(''' Insert into Products values('101','Office Chair',300,
'New', '5','Voted as most preferred chair for long hours of sitting with customizable lumbar and neck support')''')

cur.execute(''' Insert into Products values('102','High resolution curved monitor - 42 inches',400,
'New', '2','42 inches of 1080p liquid display monitor suitable for watching movies and office work with voice assisstant')''')

cur.execute(''' Insert into Products values('103','Face creme',99,'New', '10','Best suited for dry skin, use after face wash.')''')

# print("Db Created")
#Crud- main methods : Each method establishes a new connection with exisitng db to keep the db thread calls count to 1. 
# avoids from db to get locked or parallel access.  
def sql_query(query):
    try:
        with sqlite3.connect("RootDB.db") as con:
            cur = con.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            return ("Success",rows)
    except Exception as ex:
        return ("Failure",ex)

def sql_edit_insert(query,var):
    try:
        with sqlite3.connect("RootDB.db") as con:
            cur = con.cursor()
            cur.execute(query,var)
            con.commit()
            return 'Success'
    except Exception as ex:
        return ex

def sql_delete(query,var):
    try:
        with sqlite3.connect("RootDB.db") as con:
            cur = con.cursor()
            cur.execute(query,var)
            con.commit()
            return 'Success'
    except Exception as ex:
        return ex
#sub routin for DB Update
def sql_query2(query,var):
    try:
        with sqlite3.connect("RootDB.db") as con:
            cur = con.cursor()
            cur.execute(query,var)
            rows = cur.fetchall()
            return ('Success',rows)
    except Exception as ex : return ('Failure',ex)

#Converting db to csv file with headers.
def tocsv():
    try:
        conn = sqlite3.connect("RootDB.db", isolation_level=None,
                            detect_types=sqlite3.PARSE_COLNAMES)
        db_df = pd.read_sql_query("SELECT * FROM Products", conn)
        db_df.to_csv('Products.csv', index=False)
        return "Success. Please check root folder for .csv file"
    except Exception as ex:
        return ex

con.commit() # helps ending the session with db 
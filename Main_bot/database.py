import sqlite3


db = sqlite3.connect("database.db")
cursor = db.cursor()

hui = []

def db_start():
    list_objects = {}
    info = cursor.execute("SELECT * FROM istoki_info").fetchone()
    length = len(cursor.execute("SELECT * FROM istoki").fetchone())
    
    list_objects[info[4]] = info[:6]
    list_objects[info[4] + "_count"] = length
     
    info = cursor.execute("SELECT * FROM seafront_info").fetchone()
    length = len(cursor.execute("SELECT * FROM seafront").fetchone())
    
    list_objects[info[4]] = info[:6]
    list_objects[info[4] + "_count"] = length
    
    info = cursor.execute("SELECT * FROM work_info").fetchone()
    length = len(cursor.execute("SELECT * FROM work").fetchone())
    
    list_objects[info[4]] = info[:6]
    list_objects[info[4] + "_count"] = length
    
    return list_objects
    

def return_passwords(item):
    pass_list = []

    passwords = cursor.execute(f"SELECT * FROM {item}").fetchone()
    passwords = tuple([i for i in passwords])


    access_points = cursor.execute(f'PRAGMA table_info({item})').fetchall()  
    access_points = tuple([i[1] for i in access_points])
    
   
    for i in range(len(access_points)):
        pass_list.append((access_points[i], passwords[i]))

    return pass_list


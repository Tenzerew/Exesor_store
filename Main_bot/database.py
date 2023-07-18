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


def add_location(location, network, password):
    try:
        cursor.execute(f"CREATE TABLE {location}({network} TEXT)")
        cursor.execute(f"INSERT INTO {location} VALUES(?) ", (password,))
        db.commit()
    except:
        return "Такая локация уже существует."


def add_passwords(location, keys_passwords):
    try:
        keys_passwords = eval(keys_passwords)
    
        keys = keys_passwords.keys()
    except Exception:
        return "Неправильный ввод словаря"
    try:
        for i in keys:
            cursor.execute(f"""ALTER TABLE {location}\n
                        ADD {i} TEXT;
                        """)
    except sqlite3.OperationalError:
        return "Такие точки уже существуют"
    

    keys_list = []
    values_list = []
    for i, j in keys_passwords.items():
        keys_list.append(i)
        values_list.append(j)
    try:
        for i in range(len(keys_list)):
            cursor.execute(f"UPDATE {location} SET '{keys_list[i]}' = '{values_list[i]}';")
        db.commit()
    except sqlite3.OperationalError:
        return "Такие пароли уже существуют"


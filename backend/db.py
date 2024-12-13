from sqlite3 import connect
from werkzeug.security import check_password_hash, generate_password_hash

DB_NAME = "database.db"

def execute_query(query, many = False):
    conn = connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    cur = conn.execute(query)
    res = cur.fetchall() if many else cur.fetchone()
    conn.commit()
    conn.close()
    print("res: ", res)
    return res

def execute_update(query):
    conn = connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute(query)
    conn.commit()
    conn.close()

def insert_otp(token, otp):
    query = f"insert into otp_requests values('{token}', {otp})"
    execute_update(query)

def validate_otp(token, received_otp):
    original_otp = execute_query(f"select otp from otp_requests where token = '{token}'")
    if not original_otp:
        return False
    original_otp = original_otp[0]
    execute_update(f"delete from otp_requests where token = '{token}'")
    return original_otp == received_otp

def create_student(info, key):
    password_hash = generate_password_hash(info['password'])
    query = f"insert into student values ('{info['email']}', '{password_hash}', '{key}', '{info['name']}')"
    execute_update(query)

def create_faculty(info, key):
    password_hash = generate_password_hash(info['password'])
    query = f"insert into faculty values ('{info['email']}', '{password_hash}', '{key}', '{info['name']}', 0)"
    execute_update(query)

def select_key(email, password, login_type):
    row = execute_query(f"select * from {login_type} where email = '{email}'")
    if not row:
        return None
    if check_password_hash(row[1], password):
        return row[2]
    else:
        return None

def validate_authorization(token):
    if not (token.startswith("Bearer") and "@" in token):
        return None 
    user_type, key = token[7:].split("@")
    query = f"select * from {user_type} where key = '{key}'"
    if execute_query(query) == None:
        return None
    return user_type, key
    
def select_faculty_status():
    query = "select name, email, incampus from faculty"
    return execute_query(query, True)

def update_faculty_status(key, incampus):
    query = f"update faculty set incampus = {incampus} where key = '{key}'"
    execute_update(query)

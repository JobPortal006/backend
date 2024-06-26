from django.db import connection
import bcrypt
from datetime import datetime
from data import message

con = connection.cursor()

# Check email and password is registered or not from Signup table
# Encode the password value 
# Update the loggedin_time in the signup table
def login(email, password):
    sql_select = "SELECT * FROM signup WHERE email=%s"
    sql_update = "UPDATE signup SET loggedin_time=%s WHERE email=%s"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    value_select = (email,)
    try:
        # Assuming con is your database connection
        con.execute(sql_select, value_select)
        user = con.fetchone()  # Fetch the result after executing the SELECT query
        if user:
            hashed_password_from_db = user[4]  # Assuming 'Fourth' is the third column
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password_from_db.encode('utf-8')):
                value_update = (current_time, email)
                con.execute(sql_update, value_update)
                # rows_affected = con.rowcount
                # insert=message.rowcount(rows_affected) 
                return True
            else: 
                return False
        else: 
            return False
    except Exception as e:
        print(f"Error during login: {e}")
        if str(e) == "(2006, 'Server has gone away')":
            message.serverReload()
        if str(e) == "(2013, 'Lost connection to server during query')":
            message.serverReload()
        if str(e) == "Invalid salt":
            message.serverReload()
        if str(e) == "(2013, 'Lost connection to MySQL server during query')":
            message.serverReload()
        return False

# Check mobile is already registered in table or not
def loginWithOTP(mobile_number):
    check_sql = "SELECT * FROM signup WHERE mobile_number = %s"
    query = con.execute(check_sql, [mobile_number])
    if query:
        return True
    else:
        return False
    
def email_check(email):
    con = connection.cursor() 
    sql = "SELECT * FROM signup WHERE email = %s"
    con.execute(sql, [email])
    user = con.fetchone()
    con.close()
    return True if user else False
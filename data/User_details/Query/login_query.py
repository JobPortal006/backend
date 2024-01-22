from django.db import connection
import bcrypt
from datetime import datetime

con = connection.cursor()

# Check email and password is registered or not from Signup table
# Encode the password value 
def login(email, password):
    sql_select = "SELECT * FROM signup WHERE email=%s"
    sql_update = "UPDATE signup SET loggedinTime=%s WHERE email=%s"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    value_select = (email,)
    con.execute(sql_select, value_select)
    user = con.fetchone()#Get the user details here

    if user:
        hashed_password = user[3].encode('utf-8')  # Assuming 'Fourth' is the third column
        print(hashed_password)  # Print the hashed password

        if bcrypt.checkpw(password.encode('utf-8'), hashed_password): # Check the password value in table
            # Update the loggedin_time in the signup table
            value_update = (current_time, email)
            con.execute(sql_update, value_update)
            return True
        else:
            return False
    else:
        return False

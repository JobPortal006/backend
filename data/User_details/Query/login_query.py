from django.db import connection
import bcrypt
from datetime import datetime

con = connection.cursor()

# Check email and password is registered or not from Signup table
# Encode the password value 
# def login(email, password):
#     sql_select = "SELECT * FROM signup WHERE email=%s"
#     sql_update = "UPDATE signup SET loggedinTime=%s WHERE email=%s"
#     current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
#     value_select = (email,)
#     con.execute(sql_select, value_select)
    
#     user = con.fetchone()  # Fetch the result after executing the SELECT query
#     print(user)
#     if user:
#         hashed_password = user[3].encode('utf-8')  # Assuming 'Fourth' is the third column
#         print("Password is", hashed_password)  # Print the hashed password

#         if bcrypt.checkpw(password.encode('utf-8'), hashed_password): # Check the password value in table
#             # Update the loggedin_time in the signup table
#             value_update = (current_time, email)
#             con.execute(sql_update, value_update)
#             return True
#         else: 
#             return False
#     else: 
#         return False


def login(email, password):
    sql_select = "SELECT * FROM signup WHERE email=%s"
    sql_update = "UPDATE signup SET loggedin_time=%s WHERE email=%s"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    value_select = (email,)

    try:
        # Assuming con is your database connection
        con.execute(sql_select, value_select)
        user = con.fetchone()

        if user:
            hashed_password_from_db = user[4]  # Assuming 'Fourth' is the third column

            # Check if the hashed password is in the correct format
            if '$2b$' not in hashed_password_from_db:
                raise ValueError("Invalid hashed password format")

            if bcrypt.checkpw(password.encode('utf-8'), hashed_password_from_db.encode('utf-8')):
                # Update the loggedin_time in the signup table
                value_update = (current_time, email)
                con.execute(sql_update, value_update)
                return True
            else: 
                return False
        else:
            return False
    except Exception as e:
        # Handle exceptions (print or log the error)
        print(f"Error during login: {e}")
        return False

    
def loginWithOTP(mobile_number) :
  check_sql = "SELECT * FROM signup WHERE mobile_number = %s"
  query=con.execute(check_sql,[mobile_number])
  return query

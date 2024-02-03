from django.db import connection
import bcrypt
from data.User_details import message

con = connection.cursor()

def demo():
  assert 1==1

# Check email is already registered in the table or not
def email_check(email) :
  check_sql = "SELECT * FROM signup WHERE email = %s"
  query=con.execute(check_sql,[email])
  rows_affected = con.rowcount
  insert=message.rowcount(rows_affected) 
  if query:
    return True,insert
  else:
    return False

# Insert the signup data into signup table
# Store the password as hashed format
def signup_query(email,mobile_number,password,signup_by):
  try:
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    sql = "INSERT INTO signup(email,mobile_number,password,signup_by) VALUES(%s,%s,%s,%s)"
    value = (email,mobile_number,hashed_password.decode('utf-8'),signup_by)
    con.execute(sql,value)
    rows_affected = con.rowcount
    insert=message.rowcount(rows_affected) 
    return True,insert
  except Exception as e:
    print(f"Error during Signup: {e}")
    return False


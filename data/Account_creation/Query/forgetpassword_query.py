from django.db import connection
import bcrypt
from data import message

con = connection.cursor()  

#Update the password from signup table
#Password is inserted in hash format
def update_password(password,email):
  hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
  sql="UPDATE signup SET password=%s WHERE email=%s"
  value=(hashed_password.decode('utf-8'), email)
  con.execute(sql,value) 
  rows_affected = con.rowcount
  insert=message.rowcount(rows_affected) 
  return True,insert

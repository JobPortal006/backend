from django.db import connection
import bcrypt

con = connection.cursor()

#Update the password from signup table
#Password is inserted in hash format
def update_password(password,email):
  hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
  sql="UPDATE signup SET password=%s WHERE email=%s"
  value=(hashed_password.decode('utf-8'), email)
  con.execute(sql,value) 
  return True

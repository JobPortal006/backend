from django.db import connection
import bcrypt

con = connection.cursor()

#Check email is already registered in the table or not
def email_check(email) :
  check_sql = "SELECT * FROM signup WHERE email = %s"
  query=con.execute(check_sql,[email])
  return query

#Insert the data into signup table
def signup_query(email,mobile_number,password,signup_by):
  hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
  sql = "INSERT INTO signup(email,mobile_number,password,signup_by) VALUES(%s,%s,%s,%s)"
  value = (email,mobile_number,hashed_password.decode('utf-8'),signup_by)
  con.execute(sql,value)
  return True


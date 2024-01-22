from django.db import connection

con = connection.cursor()

#Check email is already registered in the table or not
def email_check(email) :
  check_sql = "SELECT * FROM signup WHERE email = %s"
  query=con.execute(check_sql,[email])
  return query

#Update the password from signup table
def update_password(password,email):
      sql="UPDATE signup SET password=%s WHERE email=%s"
      value=(password, email)
      print(value)
      con.execute(sql,value) 
      return True
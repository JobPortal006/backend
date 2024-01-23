from django.db import connection

con = connection.cursor()

def mobileNumber(mobile_number) :
  check_sql = "SELECT * FROM signup WHERE mobile_number = %s"
  con.execute(check_sql,[mobile_number])
  user = con.fetchone()
  print(user)
  id = user[0] 
  return id


def personal_details(user_id,registered_by,first_name,last_name,date_of_birth,mobile_number,gender,profile_picture):
  sql = "INSERT INTO personal_details (user_id,registered_by,first_name,last_name,date_of_birth,mobile_number,gender,profile_picture) VALUES (%s, %s, %s, %s, %s, %s)"
  values = (user_id,registered_by,first_name,last_name,date_of_birth,mobile_number,gender,profile_picture)
  print(values)
  con.execute(sql, values)
  return True
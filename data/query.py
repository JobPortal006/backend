from django.db import connection

con = connection.cursor()

def email_check(email) :
  check_sql = "SELECT * FROM signup_page WHERE email = %s"
  query=con.execute(check_sql,[email])
  return query

def myquery(first_name,last_name,mobile,password,confirm_password,email):
      sql = "INSERT INTO signup_page(first_name,last_name,mobile,password,confirm_password,email) VALUES(%s,%s,%s,%s,%s,%s)"
      value = (first_name,last_name,mobile,password,confirm_password,email)
      print(value)
      con.execute(sql,value)
      return True

def select(email,password):
      sql="SELECT * FROM signup_page WHERE email=%s AND password=%s"
      value=(email, password)
      con.execute(sql,value)
      user = con.fetchone()
      print(user)
      if user:
          return True
      else:
          return False

def password(password,cpassword,email):
      sql="UPDATE signup_page SET password=%s, confirm_password=%s WHERE email=%s"
      value=(password, cpassword, email)
      print(value)
      con.execute(sql,value) 
      return True

def user_account(firstName, lastName, email, address, mobileNumber, gender, experience, percentage10, educationType,percentage12, diplomaPercentage, 
                 department, college_name,batchYear, companyName, role, position, relocate,profilePicture, resume):
      sql = "INSERT INTO user_account (firstName, lastName, email,address, mobileNumber, gender, experience, percentage10, educationType,percentage12, diplomaPercentage, department, collegeName,batchYear, companyName, role, position, relocate,profilePicture, resume) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
      values = ( firstName, lastName, email,address, mobileNumber, gender, experience, percentage10, educationType, percentage12, diplomaPercentage, department, college_name,
            batchYear, companyName, role, position, relocate,profilePicture, resume)
      con.execute(sql, values)
      return True

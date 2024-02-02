from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
    
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db import connection
# from data.User_details.Query import signup_query
from data import views
from data.User_details import message
# from data.User_details.signup import send_signup_email

con = connection.cursor()

# Insert the data into signup table
# Data will store both User and Recruiter on same table
# Password is inserted in hash format
# Check email is already registered in table or not 
# Once registered - Send mail to registered email as (Signup Successfully message)
@csrf_exempt
def signup1(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            email = data.get('email')
            mobile_number = data.get('mobile_number')
            password = data.get('password')
            signup_by = data.get('signup_by')
            print(email,mobile_number,signup_by)
            email_check = views.email_check(email) 
            if email_check:
                return message.error('emailError')
            else:
                views.signup_query(email,mobile_number,password,signup_by)
                # send_signup_email(email)
                return message.success('Signup')
        else:
            return message.error('Error')
    except Exception: 
        return message.serverErrorResponse()

@csrf_exempt   
def send_signup_email(email):
    subject = 'Sign up Successfully'
    message_html = render_to_string('email.html')
    message_plain = strip_tags(message_html)
    from_email = 'brochill547@gmail.com'
    recipient_list = [email]
    send_mail(subject, message_plain, from_email, recipient_list, html_message=message_html)

import bcrypt

con = connection.cursor()

# Check email is already registered in the table or not
def email_check(email) :
  check_sql = "SELECT * FROM signup WHERE email = %s"
  query=con.execute(check_sql,[email])
  return query

# Insert the signup data into signup table
# Store the password as hashed format
def signup_query(email,mobile_number,password,signup_by):
  try:
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    sql = "INSERT INTO signup(email,mobile_number,password,signup_by) VALUES(%s,%s,%s,%s)"
    value = (email,mobile_number,hashed_password.decode('utf-8'),signup_by)
    con.execute(sql,value)
    print(value,'1===========')
    return True
  except Exception as e:
    print(f"Error during Signup: {e}")
    return False


@csrf_exempt
def post_job(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            jobDescription = data.get('jobDescription') 
            jobTitle = data.get('jobTitle')
            employmentType = data.get('employmentType')
            keySkills = data.get('keySkills')
            experience = data.get('experience')
            salary = data.get('salary')
            location = data.get('location')
            noOfVacancies = data.get('noOfVacancies')
            qualificationType = data.get('qualificationType')

            if (
                jobDescription and jobTitle and employmentType and keySkills and
                experience and salary and location and noOfVacancies and qualificationType
            ):
                # query.post_job(
                #     jobDescription, jobTitle, employmentType, keySkills,
                #     experience, salary, location, noOfVacancies, qualificationType
                # )
                subject = 'Post a Job'
                message_html = render_to_string('account.html')
                message_plain = strip_tags(message_html)
                from_email = 'brochill547@gmail.com'
                # recipient_list = [email]
                # send_mail(subject, message_plain, from_email, recipient_list, html_message=message_html)
                return True
            else:
                return False
    except Exception as e:
        return(f' error{e}')  
 
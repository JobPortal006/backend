from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db import connection
from data.Account_creation.Query import signup_query,login_query
from data.Account_creation import message

con = connection.cursor()

# Insert the data into signup table
# Data will store both User and Recruiter on same table
# Password is inserted in hash format
# Check email is already registered in table or not 
# Once registered - Send mail to registered email as (Signup Successfully message)
@csrf_exempt
def signup(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            email = data.get('email')
            mobile_number = data.get('mobile_number')
            password = data.get('password')  
            signup_by = data.get('signup_by') 
            print(email,mobile_number,signup_by)
            data_check = message.data_check(email,mobile_number,password,signup_by) 
            if data_check:
                email_exists = signup_query.email_check(email)
                mobile_exists = login_query.loginWithOTP(mobile_number)
                if email_exists:  
                    return message.response('Error','emailError')
                elif mobile_exists:
                    return message.response('Error','mobileError')
                else:
                    signup_query.signup_query(email,mobile_number,password,signup_by)
                    send_signup_email(email)
                    return message.response('Success','Signup')
            else:
                return message.response('Error','InputError')
        else:
            return message.response('Error','Error')
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

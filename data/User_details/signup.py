from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from data import response
from django.db import connection
from data.User_details.Query import signup_query
from data.User_details import message

con = connection.cursor()

# Insert the data into signup table
# Data will store both User and Recruiter on same table
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
            print(email,password,mobile_number,signup_by)
            email_check = signup_query.email_check(email) 
            if email_check:
                error=message.emailError()
                return message.errorResponse(error)
            else:
                signup_query.signup_query(email,mobile_number,password,signup_by)
                subject = 'Sign up Successfully'
                message_html = render_to_string('email.html')
                message_plain = strip_tags(message_html)
                from_email = 'brochill547@gmail.com'
                recipient_list = [email]
                send_mail(subject, message_plain, from_email, recipient_list, html_message=message_html)
                success=message.Signup()
                return message.handleSuccess(success)
        else:
            error=message.Error()
            return message.errorResponse(error)
    except Exception:
        return message.serverErrorResponse()
    

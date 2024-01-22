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

#Insert the data into signup table
#Once registerd - Send mail to registered email (Signup Successfully message)
@csrf_exempt
def signup(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            email = data.get('email')
            mobileNumber = data.get('mobileNumber')
            password = data.get('password')
            signupBy = data.get('signupBy')
            print(email,password,mobileNumber,signupBy)
            email_check = signup_query.email_check(email) 
            if email_check:
                error=message.emailError()
                return response.errorResponse(error)
            else:
                signup_query.signup_query(email,mobileNumber,password,signupBy)
                subject = 'Sign up Successfully'
                message_html = render_to_string('email.html')
                message_plain = strip_tags(message_html)
                from_email = 'brochill547@gmail.com'
                recipient_list = [email]
                send_mail(subject, message_plain, from_email, recipient_list, html_message=message_html)
                success=message.Signup()
                return response.handleSuccess(success)
        else:
            error=message.Error()
            return response.errorResponse(error)
    except Exception:
        return response.serverErrorResponse()
    

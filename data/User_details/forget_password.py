from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from data import response
from data.User_details import message
from data.User_details.Query import forgetpassword_query

orgemail = ""
@csrf_exempt
def forgetpassword(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            email = data.get('email')
            global orgemail
            orgemail=email
            print(orgemail)
            email_check = forgetpassword_query.email_check(email)
            if email_check:
              subject = 'Email Verification'
              message_html = render_to_string('verify_email.html')
              message_plain = strip_tags(message_html)
              from_email = 'brochill547@gmail.com'
              recipient_list = [email]
              send_mail(subject, message_plain, from_email, recipient_list, html_message=message_html)
              success=message.emailSent()
              return response.handleSuccess(success)
            else :
              error=message.emailSentError()
              return response.errorResponse(error)
        else:
          error=message.Error()
          return response.errorResponse(error)
    except Exception:
        return response.serverErrorResponse()
   
    
@csrf_exempt
def updatepassword(request):
    try :
      if request.method == 'POST':
        data = json.loads(request.body)
        password = data.get('password')
        email = orgemail 
        print(f"Email retrieved from session: {email}") 
        email_check = forgetpassword_query.email_check(email)
        if email_check:
          forgetpassword_query.update_password(password,email)
          success=message.passwordUpdate()
          return response.handleSuccess(success)
        else :
          error=message.emailSentError()
          return response.errorResponse(error)
    except Exception:
      return response.serverErrorResponse()

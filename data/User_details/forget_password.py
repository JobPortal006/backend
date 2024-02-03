from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from data.User_details import message
from data.User_details.Query import signup_query,forgetpassword_query

orgemail = ""
# Check email is registered or not in Signup table
# Sent mail to registered email for change password
@csrf_exempt
def forgetpassword(request):
  try: 
    if request.method == 'POST':
      data = json.loads(request.body)
      email = data.get('email')
      global orgemail
      orgemail=email
      print(orgemail)
      email_check,data = signup_query.email_check(email)
      if email_check:
        subject = 'Email Verification' 
        message_html = render_to_string('verify_email.html')
        message_plain = strip_tags(message_html)
        from_email = 'brochill547@gmail.com'
        recipient_list = [email]
        send_mail(subject, message_plain, from_email, recipient_list, html_message=message_html)
        return message.success('emailSent',data)
      else :
        return message.error('emailSentError')  
    else:
      return message.error('Error')
  except Exception:
      return message.serverErrorResponse()   
   
# Update password in signup Table and inserted in hash format
@csrf_exempt
def updatepassword(request):
    try :
      if request.method == 'POST':  
        data = json.loads(request.body)
        password = data.get('password')
        email = orgemail 
        print(f"Email retrieved from session: {email}") 
        password_update,data = forgetpassword_query.update_password(password,email)
        if password_update: 
          return message.success('passwordUpdate',data)
        else :
          return message.error('passwordUpdateError')
    except Exception:
      return message.serverErrorResponse()
 
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from data import message
from data.Account_creation.Query import signup_query,forgetpassword_query

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
      email_check = signup_query.email_check(email)
      if email_check:
        subject = 'Email Verification' 
        message_html = render_to_string('verify_email.html')
        message_plain = strip_tags(message_html)
        from_email = 'brochill547@gmail.com'
        recipient_list = [email]
        send_mail(subject, message_plain, from_email, recipient_list, html_message=message_html)
        return message.response('Success','emailSent')
      else :
        return message.response('Error','emailSentError')  
    else:
      return message.response('Error','Error')
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
        password_update = forgetpassword_query.update_password(password,email)
        if password_update: 
          return message.response('Success','passwordUpdate')
        else :
          return message.response('Error','passwordUpdateError')
    except Exception:
      return message.serverErrorResponse()
 
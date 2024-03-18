from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db import connection
from data.Account_creation.Query import login_query
from data import message
from data.Account_creation.Query import create_account_user_query
from django.http import JsonResponse
# import jwt
import datetime
import secrets
from data.token import create_token

con = connection.cursor()
# secret_key = secrets.token_hex(32)
# Check email and password is registered or not in Signup table
# Create a token for each email and send token to response
# Once logged in, update the loggedin time in table
@csrf_exempt
def login(request):
    try:
      if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        print(email)
        # Use your login_query function to validate credentials
        user = login_query.login(email, password)
        # secret_key = "12345"
        # payload = {
        #   'email': email,
        #   'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Token time set
        # }

        if user:
          # token = jwt.encode(payload, secret_key, algorithm='HS256')
          # print(token, "<- Token")
          # # Token Decode
          # decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
          # print(decoded_token.get('email'),"Original values")
          token = create_token(email)
          success_message = message.Login()
          # Get user_id using email in signup table
          user_id, registered_by , email= create_account_user_query.email_check(email)
          print(user_id, registered_by, email)
          response_data = {
            'response': success_message,  
            'token': token,  # Include the token in the response
            # 'candidate_id': user_id,
            'registered_by': registered_by
          }
          return message.handleSuccess(response_data)
        else:
          return message.response('Error','loginError')
      else:
        return message.response('Error','Error')
    except Exception as e:
      print(f"Exception: {str(e)}")
      return message.serverErrorResponse()

# Check mobile number is already registered or not in signup table 
@csrf_exempt
def loginWithOTP(request):
    try :
      if request.method == 'POST':
        data = json.loads(request.body)
        mobile_number = data.get('mobile_number')
        print(mobile_number)
        val = login_query.loginWithOTP(mobile_number)
        if val:
          return message.response('Success','loginWithOTP')
        else:
          return message.response('Error','loginWithOTPError')
      else:
        return message.response('Error','Error')
    except Exception:
       return message.serverErrorResponse()
    
@csrf_exempt 
def user_email_checks(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        print(email)
        email= login_query.email_check(email)
        if email:
          return message.response('Success','Signup')
        else:
          return message.response('Error','loginError')
    except Exception as e:
      return JsonResponse(str(e),safe=False)
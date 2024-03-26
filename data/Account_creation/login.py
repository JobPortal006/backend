from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connection
from data.Account_creation.Query import login_query
from data import message
from data.Account_creation.Query import create_account_user_query
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
      if user:
        token = create_token(email)
        success_message = message.Login()
        # Get user_id using email in signup table
        user_id, registered_by , email= create_account_user_query.email_check(email)
        print(user_id, registered_by, email)
        response_data = {
          'response': success_message,  
          'token': token,  # Include the token in the response
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
      user_id, registered_by, email = create_account_user_query.mobile_number(mobile_number)
      if val:
        token = create_token(email)
        success_message = message.Login()
        # Get user_id using email in signup table
        user_id, registered_by , email= create_account_user_query.email_check(email)
        print(user_id, registered_by, email)
        response_data = {
          'response': success_message,  
          'token': token,  # Include the token in the response
          'registered_by': registered_by
        }
        return message.handleSuccess(response_data)
      else:
        return message.response('Error','loginWithOTPError')
    else:
      return message.response('Error','Error')
  except Exception as e:
    return message.tryExceptError(str(e))
    
@csrf_exempt 
def user_email_checks(request):
  try:
    data = json.loads(request.body)
    email = data.get('email')
    print(email)
    email_check= login_query.email_check(email)
    if email_check:
      token = create_token(email)
      success_message = message.Login()
      user_id, registered_by , email= create_account_user_query.email_check(email)
      response_data = {
        'response': success_message,  
        'token': token,
        'registered_by': registered_by
      }
      return message.handleSuccess(response_data)
    else:
      return message.response('Error','emailSentError')
  except Exception as e:
    return message.tryExceptError(str(e))
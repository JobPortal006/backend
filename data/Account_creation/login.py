from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db import connection
from data.Account_creation.Query import login_query
from data import message
from data.Account_creation.Query import create_account_user_query

con = connection.cursor()

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
          try:
            user = User.objects.get(email=email)
          except User.DoesNotExist:
            # If user doesn't exist, create a new user
            user = User.objects.create_user(username=email, email=email, password=password)
          # Generate or retrieve the token for the user
          token, created = Token.objects.get_or_create(user=user)
          success_message = message.Login()
          # Get user_id using email in signup table
          user_id, registered_by , email= create_account_user_query.email_check(email)
          print(user_id, registered_by, email)
          response_data = {
            'message': success_message,
            'token': token.key,  # Include the token in the response
            'candidate_id': user_id,
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
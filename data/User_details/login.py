from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from data import response
from django.db import connection
from data.User_details.Query import login_query
from data.User_details import message

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
        print(email, password)
        # Use your login_query function to validate credentials
        user = login_query.login(email, password)
        if user:
          # Ensure 'user' is an instance of the User model
          if not isinstance(user, User):
            # Attempt to retrieve the User instance based on the provided email
            try:
              user = User.objects.get(email=email)
            except User.DoesNotExist:
              # If user doesn't exist, create a new user
              user = User.objects.create_user(username=email, email=email, password=password)
          # Generate or retrieve the token for the user
          token, created = Token.objects.get_or_create(user=user)
          success_message = message.Login()
          response_data = {
              'message': success_message,
              'token': token.key  # Include the token in the response
          }
          return message.handleSuccess(response_data)
        else:
            error_message = message.loginError()
            return message.errorResponse(error_message)
      else:
          error_message = message.Error()
          return message.errorResponse(error_message)
    except Exception as e:
      print(f"Exception: {str(e)}")
      return message.serverErrorResponse()

#Check mobile number is already registered or not in signup table 
@csrf_exempt
def loginWithOTP(request):
    try :
      if request.method == 'POST':
        data = json.loads(request.body)
        mobile_number = data.get('mobile_number')
        print(mobile_number)
        val = login_query.loginWithOTP(mobile_number)
        if val:
          success=message.loginWithOTP()
          return message.handleSuccess(success)
        else:
          error=message.loginWithOTPError()
          return message.errorResponse(error) 
      else:
        error=message.Error()
        return message.errorResponse(error)
    except Exception:
       return message.serverErrorResponse()
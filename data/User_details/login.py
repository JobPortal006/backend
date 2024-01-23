from django.views.decorators.csrf import csrf_exempt
import json
from data import response
from django.db import connection
from data.User_details.Query import login_query
from data.User_details import message

con = connection.cursor()

# Check email and password is registered or not from Signup table
# Once logged in, update the time in table
@csrf_exempt
def login(request):
    try :
      if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        print(email,password)
        val = login_query.login(email,password)
        if val:
          success=message.Login()
          return message.handleSuccess(success)
        else:
          error=message.loginError()
          return message.errorResponse(error)
      else:
        error=message.Error()
        return message.errorResponse(error)
    except Exception:
       return message.serverErrorResponse()

#Check mobile number is already registered or not in signup table 
@csrf_exempt
def loginWithOTP(request):
    try :
      if request.method == 'POST':
        data = json.loads(request.body)
        mobile_number = data.get('mobile_number')
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
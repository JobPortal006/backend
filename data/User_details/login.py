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
        val = login_query.login(email,password)
        if val:
          success=message.Login()
          return response.handleSuccess(success)
        else:
          error=message.loginError()
          return response.errorResponse(error)
      else:
        error=message.Error()
        return response.errorResponse(error)
    except Exception:
       return response.serverErrorResponse()
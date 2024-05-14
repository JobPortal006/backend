from django.views.decorators.csrf import csrf_exempt
import json
from data import message
from data.token import decode_token
from data.Job.post_job import retry_database_operation
from data.Account_creation.Query import create_account_employeer_query, create_account_user_query

# Check email is registered or not in Signup table
# Sent mail to registered email for change password
@csrf_exempt
@retry_database_operation
def user_account_creation_check(request):
  try: 
    if request.method == 'POST':
      data = json.loads(request.body)
      token = data.get('result_token')
      if token is not None:
        user_id, registered_by, email = decode_token(token)
        print(user_id, registered_by, email,'user_account_creation_check-->')  
        if user_id is not None:
          userid_check = create_account_user_query.userid_check(user_id)
          print(userid_check,'user_account_creation_check-->userid_check')
          if userid_check:
            return message.response('Success','accountCreationCheck')
          else:
            return message.response('Error','UserIdError')
        else:
          return message.tokenError('Error','tokenError')
      else:
        return message.response('Error','InputError')
    else:
      return message.response('Error','Error')
  except Exception as e:
    return message.tryExceptError(str(e)) 
  
@csrf_exempt
@retry_database_operation
def employeer_account_creation_check(request): 
  try: 
    if request.method == 'POST':
      data = json.loads(request.body)
      token = data.get('result_token')
      employee_id, registered_by, email = decode_token(token)
      print(employee_id, registered_by, email) 
      if employee_id is not None:
        userid_check = create_account_employeer_query.userid_check(employee_id)
        print(userid_check)
        if userid_check:
          return message.response('Success','accountCreationCheck')
        else:
          return message.response('Error','UserIdError')
      else:
        return message.tokenError('Error','tokenError')
    else:
      return message.response('Error','Error')
  except Exception as e:
    return message.tryExceptError(str(e)) 
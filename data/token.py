import jwt
import datetime
from data.Account_creation.Query import create_account_user_query
from jwt.exceptions import ExpiredSignatureError
import json
from django.views.decorators.csrf import csrf_exempt
from data import message

secret_key = "12345"

def decode_token(token):
    try:
        # Token Decode
        decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
        # print(decoded_token, "Original values")
        user_id = decoded_token.get('user_id')
        registered_by = decoded_token.get('registered_by')
        email = decoded_token.get('email')
        return user_id, registered_by, email
    except ExpiredSignatureError:
        print("Token expired")
        return None, None, None
    except Exception as e:
        print(f"Exception: {str(e)}")
        return None, None, None
    
def create_token(email):
  user_id, registered_by , email= create_account_user_query.email_check(email)
  if user_id is not None:
    exp_time = datetime.datetime.utcnow() + datetime.timedelta(days=1)

    # Convert the datetime object to a UNIX timestamp
    exp_timestamp = int(exp_time.timestamp())
    payload = {
      'user_id': user_id,
      'email':email,
      'registered_by':registered_by,
      'exp': exp_timestamp
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token  
  else:
     return None

@csrf_exempt
def token_expired(request):
  try:
    data = json.loads(request.body)
    token = data.get('token')
    print(token)
    decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
    user_id=decoded_token.get('user_id')
    if user_id is not None:
    # return JsonResponse(decoded_token)  # Return decoded token if not expired
      return message.response('Success','token') 
    else:
      return message.tokenError('Error','tokenError')
  except ExpiredSignatureError:
    return message.tokenError('Error','tokenError') 
  except Exception as e:
    print(str(e))
    return message.tryExceptError(str(e))
  
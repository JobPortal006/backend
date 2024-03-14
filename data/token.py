import jwt
import datetime
import secrets
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from data.Account_creation.Query import create_account_user_query

secret_key = "12345"

def decode_token(token):
  try:
    # Token Decode
    decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
    # print(decoded_token,"Original values")
    user_id=decoded_token.get('user_id')
    registered_by = decoded_token.get('registered_by')
    email = decoded_token.get('email')
    return user_id,registered_by,email
  except Exception as e:
    print(f"Exception: {str(e)}")
    return JsonResponse("Internal Error",safe=False)
    
def create_token(email):
  user_id, registered_by , email= create_account_user_query.email_check(email)
  payload = {
    'user_id': user_id,
    'email':email,
    'registered_by':registered_by,
    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Token time set
  }
  token = jwt.encode(payload, secret_key, algorithm='HS256')
  # print(token, "<- Token")
  return token
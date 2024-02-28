from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connection
from data.Account_creation import message
from django.http import JsonResponse
from data.Job.Query import apply_job_query

@csrf_exempt
def apply_job(request):
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        print(user_id)
        # if user_id != None:
        email, mobile_number, resume = apply_job_query.get_user_details(user_id)
        
        print(email,mobile_number, resume)
        return message.response('Success','deletePostJob')
    except Exception as e:
        return message.tryExceptError(str(e))
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connection
from data.Account_creation import message
from django.http import JsonResponse
from data.Job.Query import apply_job_query

@csrf_exempt
def fetch_apply_job(request):
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        print(user_id)

        result = apply_job_query.get_user_details(user_id)
        return JsonResponse(result)  # Return the dictionary directly as JsonResponse

    except Exception as e:
        return message.tryExceptError(str(e)) 
    
@csrf_exempt
def apply_job(request):
    try:
        data=json.loads(request.body)
        user_id=data.get('user_id')
        job_id = data.get('job_id')
        company_id = data.get('company_id')
        resume = data.get('resume')
        resume_id = apply_job_query.resume_id(resume)
        result = apply_job_query.insert_apply_job(user_id,job_id,company_id,resume_id)
    except Exception as e:
        return message.tryExceptError(str(e))
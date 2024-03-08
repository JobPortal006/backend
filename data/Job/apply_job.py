from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connection
from data import message
from django.http import JsonResponse
from data.Job.Query import apply_job_query
con = connection.cursor()

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

@csrf_exempt
def apply_jobs(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            job_id = data.get('job_id')
            user_id = data.get('user_id')
            current_ctc = data.get('current_ctc')
            expected_ctc = data.get('expected_ctc')   
            total_experience  = data.get('total_experience')  
            notice_period  = data.get('notice_period')      
            
            check_val = message.check(job_id,user_id,current_ctc,expected_ctc,total_experience,notice_period)
            
            if check_val == True:
                user_exp = apply_job_query.user_expectation_table(job_id,user_id,current_ctc,expected_ctc,total_experience,notice_period)
                final_result = json.dumps(user_exp)
                rs = json.loads(final_result)
                return JsonResponse(rs,safe=False)
            else:
                return JsonResponse("Invalid Datas",safe=False)
            
        except Exception as e:
            return JsonResponse(str(e),safe=False)     
    else:
        return JsonResponse("Method Incorrect",safe=False )
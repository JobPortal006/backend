from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connection
from data import message
from django.http import JsonResponse
from data.Job.Query import apply_job_query
from data.Account_creation.User_account.Query import update_user_account_query
from data.message import create_session

con = connection.cursor()

@csrf_exempt
def fetch_apply_job(request):
    try:
        data = json.loads(request.body)
        post_data = data.get('postdata', {})
        user_id = post_data.get('user_id')
        job_id = post_data.get('job_id')
        print(user_id,job_id)

        result = apply_job_query.get_user_details(user_id,job_id)
        return JsonResponse(result)  # Return the dictionary directly as JsonResponse

    except Exception as e:
        return message.tryExceptError(str(e)) 
    
# @csrf_exempt
# def apply_job(request):
#     try:
#         data=json.loads(request.body)
#         user_id=data.get('user_id')
#         job_id = data.get('job_id')
#         company_id = data.get('company_id')
#         resume = data.get('resume')
#         resume_id = apply_job_query.resume_id(resume)
#         result = apply_job_query.insert_apply_job(user_id,job_id,company_id,resume_id)
#     except Exception as e:
#         return message.tryExceptError(str(e))

@csrf_exempt
def apply_jobs(request):
    try:
        job_id = request.POST.get('job_id')
        user_id = request.POST.get('user_id')
        additional_queries = request.POST.get('additional_queries')
        current_ctc = request.POST.get('current_ctc')
        expected_ctc = request.POST.get('expected_ctc')
        total_experience = request.POST.get('total_experience')
        notice_period = request.POST.get('notice_period')
        print(user_id,job_id,additional_queries)
        print(current_ctc)
        print(expected_ctc)
        print(total_experience)
        print(notice_period)
        # data = json.loads(request.body)
        # job_id = data.get('job_id')
        # user_id = data.get('user_id') 
        # additional_queries  = data.get('additional_queries')  
        # current_ctc = data.get('current_ctc')
        # expected_ctc = data.get('expected_ctc')   
        # total_experience  = data.get('total_experience')  
        # notice_period  = data.get('notice_period')    
        # resume_path  = data.get('resume_path')

        resume_file = request.FILES.get('resume_path')
        print(resume_file,'resume_file----------')
        if resume_file is not None:
            print('if-------')
            resume_name = resume_file.name
            resume_file = resume_file.read() 
            print(resume_name, 'resume_name------------')
        else:
            print("else-------")
            resume_path = request.POST.get('resume_path')  
            print(resume_path, 'resume_path-------')  
        session = create_session()
        check_val = message.check(job_id,user_id)
        if check_val:
            existing_resume_key = update_user_account_query.get_resume_path(session,user_id)
            if resume_file is not None:
                print('if conditiong working fine------->1')
                resume_key = update_user_account_query.upload_resume_file(resume_file, resume_name, user_id, existing_resume_key)
            else:
                resume_key = resume_path  
            resume_id = apply_job_query.get_resume_id(resume_key,user_id)
            apply_job_result = apply_job_query.apply_job_table(job_id,user_id,resume_id)
            print(apply_job_result,'apply_job_result')
            if apply_job_result:
                if additional_queries == "Yes":
                    user_exp = apply_job_query.additional_queries_table(job_id,user_id,current_ctc,expected_ctc,total_experience,notice_period)
                    return message.response('Success','applyJob')
                else:
                    return message.response('Error','applyJobError')
            else:
                return message.response('Error','applyJobError')
        else:
            return message.response('Error','InputError')
    except Exception as e:
        print(f"The Error is: {str(e)}")
        return message.tryExceptError(str(e))    
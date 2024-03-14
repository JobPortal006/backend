from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connection
from data import message
from django.http import JsonResponse
from data.Job.Query import apply_job_query
from data.Account_creation.User_account.Query import update_user_account_query
from data.message import create_session
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from data.token import decode_token

con = connection.cursor()

@csrf_exempt
def fetch_apply_job(request):
    try:
        data = json.loads(request.body)
        post_data = data.get('postdata', {})
        # user_id = post_data.get('user_id')
        token = post_data.get('token')
        print(token)
        user_id,registered_by,email = decode_token(token)
        print(user_id, registered_by,email) 
        job_id = post_data.get('job_id')
        print(user_id,job_id)

        result = apply_job_query.get_user_details(user_id,job_id)
        if result is not None:
            return JsonResponse(result)  # Return the dictionary directly as JsonResponse
        else:
            return message.response('Error','companyError')

    except Exception as e:
        return message.tryExceptError(str(e)) 

@csrf_exempt
def apply_jobs(request):
    try:
        job_id = request.POST.get('job_id')
        token = request.POST.get('token')
        user_id,registered_by,email = decode_token(token)
        print(user_id, registered_by,email) 
        additional_queries = request.POST.get('additional_queries')
        current_ctc = request.POST.get('current_ctc')
        expected_ctc = request.POST.get('expected_ctc')
        total_experience = request.POST.get('total_experience')
        notice_period = request.POST.get('notice_period')
    
        resume_file = request.FILES.get('resume_path')
        if resume_file is not None:
            resume_name = resume_file.name
            resume_file = resume_file.read() 
        else:
            resume_path = request.POST.get('resume_path')  
        session = create_session()
        check_val = message.check(job_id,user_id)
        user_email = apply_job_query.user_email(user_id)
        company_email = apply_job_query.company_email(job_id)
        if check_val:
            existing_resume_key = update_user_account_query.get_resume_path(session,user_id)
            if resume_file is not None:
                resume_key = update_user_account_query.upload_resume_file(resume_file, resume_name, user_id, existing_resume_key)
            else:
                resume_key = resume_path  
            resume_id = apply_job_query.get_resume_id(resume_key,user_id)
            apply_job_result = apply_job_query.apply_job_table(job_id,user_id,resume_id)
            print(apply_job_result,'apply_job_result')
            if apply_job_result:
                if additional_queries == "Yes":
                    apply_job_query.additional_queries_table(job_id,user_id,current_ctc,expected_ctc,total_experience,notice_period)
                    send_email(user_email)
                    send_email(company_email)
                    return message.response('Success','applyJob')
                else:
                    return message.response('Error','applyJobError')
            else:
                return message.response('Error','userApplyJobError')
        else:
            return message.response('Error','InputError')
    except Exception as e:
        print(f"The Error is: {str(e)}")
        return message.tryExceptError(str(e))

job_response = ""

# Get all job_post data using user_id and send response through API
@csrf_exempt
def view_apply_jobs(request):
    try:
        data = json.loads(request.body)
        token = data.get('token')
        user_id,registered_by,email = decode_token(token)
        print(user_id, registered_by,email)
        all_results = []  
        if user_id is not None:
            processed_job_ids = set() # Using set() method store all job_id here, it will not repeat the duplicate job_id
            job_result=apply_job_query.view_apply_jobs(user_id,processed_job_ids) 
            if job_result is not None:# Check if search_result is not None before converting to a dictionary
                job_result_dict = json.loads(job_result) # Convert search_result to a Python dictionary
                all_results.append(job_result_dict) # Append results for each skill to the list
            else:
                return message.response1('Error', 'searchJobError', data={}) 
            global job_response
            job_response
        else:
            return message.response('Error','InputError')
        if job_result is not None:
            return message.response1('Success', 'searchJob', all_results)
        else:
            return message.response1('Error', 'searchJobError', data={})  
    except Exception as e:
        print(f"The Error is: {str(e)}")
        return message.tryExceptError(str(e))

# Send job_post reponse here
@csrf_exempt
def get_view_apply_jobs(request):
    try:
        url_response=job_response
        # print(url_response)
        if url_response is not None and url_response != '':
            return message.response1('Success', 'getJobDetails', url_response)
        else:
            return message.response1('Error', 'searchJobError', data={})  
    except Exception as e:
        print(f"The Error is: {str(e)}")
        return message.tryExceptError(str(e))
   
@csrf_exempt   
def send_email(email):
    subject = 'Job Applied Successfully'
    message_html = render_to_string('email.html')
    message_plain = strip_tags(message_html)
    from_email = 'brochill547@gmail.com'
    recipient_list = [email]
    send_mail(subject, message_plain, from_email, recipient_list, html_message=message_html)
from django.views.decorators.csrf import csrf_exempt
import json
from data import message
from data.token import decode_token
from data.Job.Query import job_details_query
job_response = ""
user_job_apply_result = ""
# Get all job details data using job_id and send response through API
@csrf_exempt
def job_details(request):
    try:
        data = json.loads(request.body)
        post_data = data.get('selectedJob', {})
        job_id = post_data.get('id')
        if job_id is None:
            job_id = post_data.get('job_post_id')
        print(job_id)
        token = data.get('token')
        user_id,registered_by,email = decode_token(token)
        print(user_id, registered_by,email)
        # if user_id is not None:
        valuesCheck = message.check(job_id)
        all_results = []  
        if valuesCheck:
            processed_job_ids = set() # Using set() method store all job_id here, it will not repeat the duplicate job_id
            job_result=job_details_query.job_result(job_id,user_id,processed_job_ids) # Get the job data here
            user_job_apply = False
            if user_id is not None:
                user_job_apply=job_details_query.check_user_id(user_id, job_id)# Check user is already apply for the job or not
            print(user_job_apply,'user_job_apply')
            if job_result is not None:# Check if search_result is not None before converting to a dictionary
                job_result_dict = json.loads(job_result) # Convert search_result to a Python dictionary
                all_results.append(job_result_dict) # Append results for each skill to the list
            else:
                return message.response1('Error', 'searchJobError', data={})
            global job_response,user_job_apply_result
            job_response=all_results
            user_job_apply_result=user_job_apply
            if user_job_apply and user_id is not None:
                return message.response1('Success', 'userApplyJob', all_results)
            elif job_result is not None:
                return message.response1('Success', 'userApplyJobResult', all_results)
            else:
                return message.response1('Error', 'searchJobError', data={})
        else:
            return message.response('Error','InputError')  
        # else:
        #     return message.tokenError('Error','tokenError')
    except Exception as e:
        print(f"The Error is: {str(e)}")
        return message.tryExceptError(str(e))

# Send job details reponse here
@csrf_exempt
def get_job_details(request):
    try:
        url_response=job_response
        user_job_apply=user_job_apply_result
        if user_job_apply:
            return message.response1('Success', 'userApplyJob', url_response)
        elif url_response is not None and url_response != '':
            return message.response1('Success', 'userApplyJobResult', url_response)
        else:
            return message.response1('Error', 'searchJobError', data={})  
    except Exception as e:
        print(f"The Error is: {str(e)}")
        return message.tryExceptError(str(e))
from django.views.decorators.csrf import csrf_exempt
import json
from data.Account_creation import message
from data.Job.Query import employer_post_jobs_query
job_response = ""

# Get all job_post data using employee_id and send response through API
@csrf_exempt
def employer_post_jobs(request):
    try:
        data = json.loads(request.body)
        employee_id = data.get('employee_id')
        # employee_id=5
        print(employee_id,'id----------')
        # valuesCheck = message.check(employee_id)
        all_results = []  
        if employee_id is not None:
            processed_job_ids = set() # Using set() method store all job_id here, it will not repeat the duplicate job_id
            job_result=employer_post_jobs_query.employer_post_jobs(employee_id,processed_job_ids) 
            # print(job_result,'1----------1')
            if job_result is not None:# Check if search_result is not None before converting to a dictionary
                job_result_dict = json.loads(job_result) # Convert search_result to a Python dictionary
                all_results.append(job_result_dict) # Append results for each skill to the list
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
        return message.serverErrorResponse()

# Send job_post reponse here
@csrf_exempt
def employer_post_jobs_view(request):
    try:
        url_response=job_response
        # print(url_response)
        if url_response is not None and url_response != '':
            return message.response1('Success', 'getJobDetails', url_response)
        else:
            return message.response1('Error', 'searchJobError', data={})  
    except Exception as e:
        print(f"The Error is: {str(e)}")
        return message.serverErrorResponse()
   

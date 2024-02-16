from django.views.decorators.csrf import csrf_exempt
import json
from data.Account_creation import message
from data.Job.Query import employer_post_jobs_query
job_response = ""
@csrf_exempt
def employer_post_jobs(request):
    try:
        data = json.loads(request.body)
        employee_id = data.get('employee_id')
        print(employee_id,'id----------')
        valuesCheck = message.check(employee_id)
        all_results = []  
        if valuesCheck:
            processed_job_ids = set()
            job_result=employer_post_jobs_query.employer_post_jobs(employee_id,processed_job_ids)
            print(job_result)
                # Check if search_result is not None before converting to a dictionary
            if job_result is not None:
                # Convert search_result to a Python dictionary
                job_result_dict = json.loads(job_result)
                # Append results for each skill to the list
                all_results.append(job_result_dict)
            global job_response
            job_response=all_results
            # Combine results for all skills and return
        if job_result is not None:
            return message.response1('Success', 'searchJob', all_results)
        else:
            return message.response1('Error', 'searchJobError', data={})  
    except Exception as e:
        print(f"The Error is: {str(e)}")
        return message.serverErrorResponse()

@csrf_exempt
def employer_post_jobs_view(request):
    try:
        url_response=job_response
        print(url_response)
        if url_response is not None and url_response != '':
            return message.response1('Success', 'getJobDetails', url_response)
        else:
            return message.response1('Error', 'searchJobError', data={})  
    except Exception as e:
        print(f"The Error is: {str(e)}")
        return message.serverErrorResponse()
   

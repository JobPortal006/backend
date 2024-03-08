from django.views.decorators.csrf import csrf_exempt
import json
from data import message
from data.Job.Query import job_details_query
job_response = ""

# Get all job details data using job_id and send response through API
@csrf_exempt
def job_details(request):
    try:
        data = json.loads(request.body)
        job_id = data.get('id')
        print(job_id)
        valuesCheck = message.check(job_id)
        all_results = []  
        if valuesCheck:
            processed_job_ids = set() # Using set() method store all job_id here, it will not repeat the duplicate job_id
            job_result=job_details_query.job_result(job_id,processed_job_ids) # Get the job data here
            # print(job_result)
            if job_result is not None:# Check if search_result is not None before converting to a dictionary
                job_result_dict = json.loads(job_result) # Convert search_result to a Python dictionary
                all_results.append(job_result_dict) # Append results for each skill to the list
            global job_response
            job_response=all_results
        if job_result is not None:
            return message.response1('Success', 'searchJob', all_results)
        else:
            return message.response1('Error', 'searchJobError', data={})  
    except Exception as e:
        print(f"The Error is: {str(e)}")
        return message.tryExceptError(str(e))

# Send job details reponse here
@csrf_exempt
def get_job_details(request):
    try:
        url_response=job_response
        if url_response is not None and url_response != '':
            return message.response1('Success', 'getJobDetails', url_response)
        else:
            return message.response1('Error', 'searchJobError', data={})  
    except Exception as e:
        print(f"The Error is: {str(e)}")
        return message.tryExceptError(str(e))
from django.views.decorators.csrf import csrf_exempt
import json
from data import message
from data.Job.Query import search_jobs_query
from data.Job import search_jobs
from sqlalchemy import and_
from data.Account_creation.Tables.table import EmployeeTypes
job_response = ""

# Search the job details data in database
# Send a response as JSON format 
# Date as converted into this format(Data/Month/Year)
# Skills are sent as a response in an array
@csrf_exempt
def job_details_by_employeeType(request):
    try:
        data = json.loads(request.body)
        employee_type = data.get('employee_type')
        print(employee_type)
        set_data_id = set()
        jobs = []
        if employee_type is not None:
            conditions = and_(EmployeeTypes.employee_type == employee_type)
            result = search_jobs_query.execute_query(conditions)
        jobs=search_jobs.job_response_details(result,set_data_id)
        global job_response
        job_response = jobs
        if jobs:
           return message.response1('Success','searchJob',jobs)
        else:
            return message.response1('Error','searchJobError',data={})
    except Exception as e:
        print(str(e))
        return message.tryExceptError(str(e))

# Get API for job details by employee type
@csrf_exempt
def job_details_by_employeeType_view(request):    
    try:
        url_response = job_response
        if url_response:
            return message.response1('Success', 'getJobDetails', url_response)
        else:
            return message.response1('Error', 'searchJobError', data={})
    except Exception as e:
        print(f"The Error is: {str(e)}")
        return message.tryExceptError(str(e))
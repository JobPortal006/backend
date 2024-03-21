from django.views.decorators.csrf import csrf_exempt
import json
from data import message
from data.Job.Query import search_jobs_query
from data.Job import json_response
from sqlalchemy import and_
from data.Job import search_jobs
from data.Account_creation.Tables.table import CompanyDetails
from data.Job import job_details_by_employeeType

# job_response = ""

# Search the job details data in database
# Send a response as JSON format 
# Date as converted into this format(Data/Month/Year)
# Skills are sent as a response in an array
@csrf_exempt
def job_details_by_companyName(request):
    try:
        data = json.loads(request.body)
        company_name = data.get('company_name')
        # company_call_fun
        global company_fun_call
        company_fun_call = 'company'
        search_jobs.search_fun_call = None
        job_details_by_employeeType.employee_call_fun = None
        print(company_name)
        set_data_id = set()
        jobs = []
        if company_name is not None:
            conditions = and_(CompanyDetails.company_name == company_name)
            result = search_jobs_query.execute_query(conditions)
        jobs=json_response.job_response_details(result,set_data_id)
        global job_response
        job_response = jobs
        if jobs: 
           return message.response1('Success', 'getJobDetails', jobs)
        else:
            return message.response1('Error','searchJobError',data={})
    except Exception as e:
        print(str(e))
        return message.tryExceptError(str(e))
    
def company_name_response():
    global job_response
    url_response = job_response
    return url_response

# Get API for job details by company name
@csrf_exempt
def job_details_by_companyName_view(request):
    try:
        url_response = job_response
        if url_response:
            return message.response1('Success', 'getJobDetails', url_response)
        else:
            return message.response1('Error', 'searchJobError', data={})
    except Exception as e:
        print(f"The Error is: {str(e)}")
        return message.tryExceptError(str(e))
    
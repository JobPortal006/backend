from django.views.decorators.csrf import csrf_exempt
import json
from data import message
from data.Job import search_jobs
from data.Job import job_details_by_employeeType
from data.Job import job_details_by_companyName
jobs = ""
@csrf_exempt
def job_filter(request):
    if request.method == 'POST':
        try:  
            data = json.loads(request.body)
            print(data)
            experience_value = data.get('experience')
            location_value = data.get('location')
            employee_type_value = data.get('employee_type')
            job_role_value = data.get('job_role')
            salary_range_value = data.get('salary_range')
            salary_range_value = ''.join(salary_range_value.split())
            jobs = search_jobs.job_response
            if jobs is None or jobs == '':
                jobs = job_search_result()
                print(jobs,'filter job_search_result-------')
            if jobs is None or jobs == '':
                jobs = job_company_name_result()
                print(jobs,'filter job_company_name_result-------')
            if jobs is None or jobs == '':
                jobs = job_employee_type_result()
                print(jobs,'filter job_employee_type_result--------')
            condition = ""
            def where_condition(data,location_value, dyanamic_value, condition):
                key_value = None
                for key, value in data.items():
                    if value == location_value:
                        key_value = key
                        break
                if dyanamic_value and key_value:
                    if condition:
                        condition += f" and '{dyanamic_value}' in job['{key_value}']"
                    else:
                        condition = f"'{dyanamic_value}' in job['{key_value}']"
                return condition
            if experience_value:
                for i in experience_value:
                    if i:
                        condition = where_condition(data,experience_value,i,condition)
            if location_value:
                    for i in location_value:
                         if i:
                              condition = where_condition(data,location_value,i,condition)             
            if employee_type_value:
                    condition = where_condition(data,employee_type_value,employee_type_value,condition)     
            if job_role_value:
                    for i in job_role_value:
                         if i:
                              condition = where_condition(data,job_role_value,i,condition)
            if salary_range_value: 
                condition = where_condition(data,salary_range_value,salary_range_value,condition)
            print("Where condition----->",condition)
            job_result = [job for job in jobs if eval(condition)]
            if not job_result:
                conditions = condition.split(" and ")
                new_val = " or ".join(conditions)
                job_result = [job for job in jobs if eval(new_val)]
            global job_response
            job_response=job_result
            if not job_result:
                return message.response('Error', 'searchJobError')
            return message.response1('Success', 'getJobDetails', job_result)
        except Exception as e:
            return message.tryExceptError(str(e))
    else:
        return message.response('Error', 'Error')
    
def job_search_result():
    return jobs

def job_company_name_result():
    jobs = job_details_by_companyName.job_response
    return jobs

def job_employee_type_result():
    jobs = job_details_by_employeeType.job_response
    return jobs
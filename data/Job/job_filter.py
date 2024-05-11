from django.views.decorators.csrf import csrf_exempt
import json
from data import message
from django.http import JsonResponse
from data.Job import search_jobs
from data.Job import job_details_by_companyName 
from data.Job import job_details_by_employeeType
job_response = ""
jobs = ""
@csrf_exempt
def job_filter(request):
    if request.method == 'POST':
        try:  
            data = json.loads(request.body)
            print(data) 

            global jobs
            experience_value = data.get('experience')
            location_value = data.get('location')
            employee_type_value = data.get('employee_type')
            job_role_value = data.get('job_role')
            salary_range_value = data.get('salary_range')
            

            if search_jobs.search_fun_call == 'search':
                jobs = search_jobs.job_response
                search_jobs.search_fun_call = None
                # job_details_by_companyName.company_fun_call  = None
                # job_details_by_employeeType.employee_call_fun = None
                # job_details_by_employeeType.employee_call_fun = None 
                # if jobs == '':
            if job_details_by_companyName.company_fun_call == 'company': 
                jobs = job_details_by_companyName.job_response
                job_details_by_companyName.company_fun_call = None
                # search_jobs.search_fun_call = None
                # job_details_by_employeeType.employee_call_fun = None
                # job_details_by_employeeType.employee_call_fun = None
            # print(job_details_by_employeeType.employee_call_fun ," 3----------------")   
            if job_details_by_employeeType.employee_call_fun == 'employee':
                jobs = job_details_by_employeeType.job_response
                job_details_by_companyName.company_fun_call = None
                # search_jobs.search_fun_call = None
                # job_details_by_employeeType.employee_call_fun = None

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
            global job_response,filter_result
            job_response=job_result
            # jobs = job_response
            print(job_result,'job_result-------')
            filter_result =other_function()
            if not job_result:
                return message.response('Error', 'searchJobError')
            return message.response1('Success', 'getJobDetails', job_result)
        except Exception as e:
            return message.tryExceptError(str(e))
    else:
        return message.response('Error', 'Error') 

def other_function():
    job_result=filter_result
    return job_result

@csrf_exempt
def filter_result(request):
    try:
        url_response = job_response
        # url_response=other_function()
        print(url_response,'----------')
        if url_response:
            return message.response1('Success', 'getJobDetails', url_response)
        else:
            return message.response1('Error', 'searchJobError', data={})
    except Exception as e:
        print(f"The Error is: {str(e)}")
        return message.tryExceptError(str(e))
    

# @csrf_exempt
# def filter_result(request):
#     try:
#         if request.method == 'POST':  # Ensure it's a POST request
#             data = json.loads(request.body)
#             print(data)
#             if data:
#                 return JsonResponse(data, safe=False)
#             else:
#                 return JsonResponse({'error': 'No data provided'}, status=400)
#         else:
#             return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
#     except json.JSONDecodeError as e:
#         return JsonResponse({'error': 'Invalid JSON format: {}'.format(str(e))}, status=400)
#     except Exception as e:
#         # Log the exception or handle it as required
#         return JsonResponse({'error': str(e)}, status=500)
   
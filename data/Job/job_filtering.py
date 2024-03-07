from django.views.decorators.csrf import csrf_exempt
import json
from data.Account_creation import message
from django.http import JsonResponse
from data.Job import search_jobs
job_response = ""
@csrf_exempt
def result_filter(request):
    if request.method == 'POST':
        
        try:  
            data = json.loads(request.body)
            print(data)
            experience_value = data.get('experience')
            location_value = data.get('location')
            employee_type_value = data.get('employee_type')
            job_role_value = data.get('job_role')
            salary_range_value = data.get('salary_range')
            jobs = search_jobs.job_response
            if jobs is None:
                jobs = job_filter_result()
            where_cons = ""
            
            def where_condition(data,location_value, dyanamic_value, where_cons):
                key_value = None
                for key, value in data.items():
                    if value == location_value:
                        key_value = key
                        break
                
                if dyanamic_value and key_value:
                    if where_cons:
                        where_cons += f" and  job['{key_value}'] == '{dyanamic_value}'"
                    else:
                        where_cons = f"job['{key_value}'] == '{dyanamic_value}'"

                return where_cons
            
            if experience_value:
                for i in experience_value:
                    if i:
                        where_cons = where_condition(data,experience_value,i,where_cons)
            
            if location_value:
                    for i in location_value:
                         if i:
                              where_cons = where_condition(data,location_value,i,where_cons)
                              
            if employee_type_value:
                    where_cons = where_condition(data,employee_type_value,employee_type_value,where_cons)     
            
            if job_role_value:
                    for i in job_role_value:
                         if i:
                              where_cons = where_condition(data,job_role_value,i,where_cons)
               
            if salary_range_value: 
                where_cons = where_condition(data,salary_range_value,salary_range_value,where_cons)
             
            print("WHERE_CON",where_cons)
           
            
            job_result = [job for job in jobs if eval(where_cons)]
            print(job_result," --------- ")
            if not job_result:
                conditions = where_cons.split(" and ")
                new_val = " or ".join(conditions)
                print("OR ",new_val)
                job_result = [job for job in jobs if eval(new_val)]
            global job_response
            job_response=job_result
            # print(" -------",job_result)
            if not job_result:
                # return JsonResponse("No Found Jobs",safe=False)
                return message.response('Error', 'searchJobError')
            return message.response1('Success', 'getJobDetails', job_result)
        
        except Exception as e:
            return message.tryExceptError(str(e))
        
    else:
        return JsonResponse("Method Failed",safe=False)
    
def job_filter_result():
    return job_response
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connection
from data.Account_creation import message
from django.http import JsonResponse
from data.Job.Query import job_filtering_query 

@csrf_exempt
def filter(request):
     if request.method == 'POST':
          try: 
               data = json.loads(request.body)
               
               experience_value = data.get('experience')
               location_value = data.get('location')
               employee_type_value = data.get('employee_type')
               job_role_value = data.get('job_role')
               salary_range_value = data.get('salary_range')
               
               global select_jobs
               and_op = 'AND'
               
               where_cons = ""
               
               filter_valyes =[]
               print("list ............... 1",filter_valyes)  
               for i in experience_value:
                    if i:
                         where_cons = job_filtering_query.where_condition(data,experience_value,and_op,filter_valyes,where_cons)
                         filter_valyes.append(i) 
               
               
               for i in location_value:
                    if i:
                         where_cons = job_filtering_query.where_condition(data,location_value,and_op,filter_valyes,where_cons)
                         filter_valyes.append(i) 
               
               if employee_type_value:
                    where_cons = job_filtering_query.where_condition(data,employee_type_value,and_op,filter_valyes,where_cons)
                    filter_valyes.append(employee_type_value)
                    
               
               for i in job_role_value:
                    if i:
                         where_cons = job_filtering_query.where_condition(data,job_role_value,and_op,filter_valyes,where_cons)
                         filter_valyes.append(i) 
               
               if salary_range_value: 
                    where_cons = job_filtering_query.where_condition(data,salary_range_value,and_op,filter_valyes,where_cons)
                    filter_valyes.append(salary_range_value)
                     
               #    filter_valyes_flat = [item for sublist in filter_valyes for item in sublist]
               single_list = [elem for sublist in filter_valyes for elem in (sublist if isinstance(sublist, list) else [sublist])]
               results = job_filtering_query.execute_join_jobPost(where_cons,single_list)
               jobs = job_filtering_query.result_fun(results)
               
               # global select_jobs 
               select_jobs = results
               
               if jobs:
                    json_data = json.loads(jobs.content)
                    return JsonResponse(json_data,safe=False)
               else: 
                    conditions = where_cons.split(" AND ")
                    new_val = " OR ".join(conditions)
                    print(new_val,"1111111111")
                    results = job_filtering_query.execute_join_jobPost(new_val,single_list)
                    jobs = job_filtering_query.result_fun(results)
                    json_data = json.loads(jobs.content)
                    select_jobs = results
                    
                    return JsonResponse(json_data,safe=False)
           
          
          except Exception as e:
               return JsonResponse({'error': str(e)}, status=500)
     else:
          return JsonResponse("Incorrect Method ",safe=False)
@csrf_exempt
def filter_select_jobs(request):
     if request.method == "GET":
          try:
               # print("----- ",select_jobs)
               if select_jobs:
                    
                    jobs = job_filtering_query.result_fun(select_jobs)
                    json_data = json.loads(jobs.content)
                    # print("Jobs : ",json_data)
                    return JsonResponse(json_data,safe=False)  
               else:
                    print("HIIIII") 
                    return JsonResponse("EMPTY",safe=False)  
                    
                     
          except Exception as e:
               return JsonResponse({'error': str(e)}, status=500)
     else:
          return JsonResponse("Incorrect Method ",safe=False)

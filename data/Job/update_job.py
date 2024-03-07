from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connection
from data.Account_creation import message
from django.http import JsonResponse
from data.Job.Query import update_job_query 

con = connection.cursor()

@csrf_exempt
def update_jobs(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            job_id = data.get('id')
            job_title = data.get('job_title')
            job_description = data.get('job_description')
            employee_type = data.get('employee_type')   
            job_role  = data.get('job_role')  
            location  = data.get('location')            
            skill_set = data.get('skills')            
            qualification = data.get('qualification')
            experience    = data.get('experience')
            salary_range  = data.get('salary_range')
            no_of_vacancies = data.get('no_of_vacancies') 
            company_name = data.get('company_name'),
            created_data = data.get('created_at')
            # id = data.get('id')
            global select_updatePostjob
            print(data)
            
            valuesCheck = message.check(job_id,job_title,job_description,employee_type,job_role,location,qualification,experience,salary_range,no_of_vacancies,company_name)
                
            if valuesCheck:
                employee_id =  update_job_query.getId_companyDetails(job_id)
            else:
                return JsonResponse("Invalid Datas ",safe=False)
           
           
            if job_id:
                check = update_job_query.jobPost_updateQuery( job_title, job_description, qualification, experience, salary_range, no_of_vacancies, job_id)
                update_job_query.update_skillSet(skill_set,job_id)
                update_job_query.location_eType_jRole(location,employee_type,job_role,job_id)
                
                # ID to fetch JOB-POST details
                
                where_con ="j.id = %s"
                
                job_id=(job_id,)
                
                results = update_job_query.execute_join_jobPost(where_con,job_id)
                if results:
                    jobs = update_job_query.result_fun(results)
                    select_updatePostjob = jobs
                    json_data = json.loads(jobs.content)
                    
                    return JsonResponse(json_data,safe=False)
                else:
                    return message.response('Success','updatePostJob')
                        
            return JsonResponse("Updated Successfully",safe=False)
        except Exception as e:
            return message.tryExceptError(str(e))
    else:
        return message.response('Error','UpdateJobPost_Method')
    

@csrf_exempt     
def select_updateJob(request):
     if request.method == 'GET':
          try:
               json_data = json.loads(select_updatePostjob.content)
               print(json_data)
               return JsonResponse(json_data,safe=False)
          except:
               return JsonResponse("FRailed",safe=False)
     else:
          return JsonResponse("Incorrect Method Type - Use GET",safe=False)
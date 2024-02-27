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
            job_title = data.get('job_title')
            job_description = data.get('job_description')
            employee_type = data.get('employee_type')   
            job_role  = data.get('job_role')  
            location  = data.get('location')            
            skill_set = data.get('skill_set')            
            qualification = data.get('qualification')
            experience    = data.get('experience')
            salary_range  = data.get('salary_range')
            no_of_vacancies = data.get('no_of_vacancies') 
            company_name = data.get('company_name')
            print(data)
            
            
            valuesCheck = message.check(job_title,job_description,employee_type,job_role,location,skill_set,qualification,experience,salary_range,no_of_vacancies,company_name)
            # Checkind Company Datails Table input company name get employee id
            if valuesCheck:
                employee_id =  update_job_query.getId_companyDetails(company_name)
            else:
                return JsonResponse("Invalid Company Name",safe=False)
            # Checking Post job Table  input employee_id get post_job ID   
            if employee_id:
                postJob_id = update_job_query.id_jobPost(employee_id)
            else:                       
                return JsonResponse("Invalid job Posting",safe=False)
            
            if postJob_id:
                check = update_job_query.jobPost_updateQuery( job_title, job_description, qualification, experience, salary_range, no_of_vacancies, postJob_id)
                
                update_job_query.update_skillSet(skill_set,employee_id,postJob_id)
                update_job_query.location_eType_jRole(location,employee_type,job_role,employee_id)
                
                # ID to fetch JOB-POST details
                
                where_con ="j.id = %s"
                
                postJob_id=(postJob_id,)
                
                results = update_job_query.execute_join_jobPost(where_con,postJob_id)
                if results:
                    jobs = update_job_query.result_fun(results)
                    json_data = json.loads(jobs.content)
                    return JsonResponse(json_data,safe=False)
                else:
                    return message.response('Success','updatePostJob')
        except Exception as e:
            return message.tryExceptError(str(e))
    else:
        return message.response('Error','UpdateJobPost_Method')
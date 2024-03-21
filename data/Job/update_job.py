from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connection
from data import message
from django.http import JsonResponse
from data.Job.Query import update_job_query,search_jobs_query
from sqlalchemy import and_
from data.Account_creation.Tables.table import JobPost
from data.Job import json_response

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
            print(data)
            set_data_id = set()
            valuesCheck = message.check(job_id,job_title,job_description,employee_type,job_role,location,qualification,experience,salary_range,no_of_vacancies,company_name)
            if valuesCheck:
                employee_id =  update_job_query.getId_companyDetails(job_id)
            else:
                return JsonResponse("Invalid Datas ",safe=False)
            if job_id:
                table_name= "location"
                field_name ="location"
                mappind_table="location_mapping"
                mappind_id="location_id"
                update_job_query.update_maping_tables(location,job_id,table_name,field_name,mappind_table,mappind_id)
                
                table_name= "qualification"
                field_name ="qualification"
                mappind_table="qualification_mapping"
                mappind_id="qualification_id"
                update_job_query.update_maping_tables(qualification,job_id,table_name,field_name,mappind_table,mappind_id)
                
                table_name= "skill_sets"
                field_name ="skill_set"
                mappind_table="skill_set_mapping"
                mappind_id="skill_id"
                update_job_query.update_maping_tables(skill_set,job_id,table_name,field_name,mappind_table,mappind_id)
                update_job_query.jobPost_updateQuery( job_title, job_description, qualification, experience, salary_range, no_of_vacancies,job_id)

                set_data_id = set()
                conditions = and_(JobPost.id == job_id)
                result = search_jobs_query.execute_query(conditions)
                json_data = json_response.job_response_details(result,set_data_id)
                if json_data:
                    return message.response1('Success', 'getJobDetails', json_data)
                else:
                    return message.response('Success','updateData')
            # return JsonResponse("Updated Successfully",safe=False)
        except Exception as e:
            return message.tryExceptError(str(e))
    else:
        return message.response('Error','UpdateJobPost_Method')
    

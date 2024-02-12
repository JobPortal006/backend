from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connection
from data.Account_creation import message
from django.http import JsonResponse
from data.Job.Query import post_job_insert_query 

con = connection.cursor()

@csrf_exempt
def post_jobs(request):
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
        valuesCheck = message.check(job_title,job_description,employee_type,job_role,location,skill_set,qualification,experience,salary_range,no_of_vacancies)
        print(valuesCheck)
        if valuesCheck:
            employee_id = post_job_insert_query.employee_id(company_name)
            company_id = post_job_insert_query.company_id(company_name)
            if employee_id and company_id:
                employee_type_id = post_job_insert_query.employee_type_id(employee_type)
                if employee_type_id == None:
                    post_job_insert_query.employee_type_insert(employee_type)
                    employee_type_id = post_job_insert_query.employee_type_id(employee_type)
                job_role_id = post_job_insert_query.job_role_id(job_role)
                if job_role_id == None:
                    post_job_insert_query.job_role_insert(job_role)
                    job_role_id = post_job_insert_query.job_role_id(job_role)
                location_id = post_job_insert_query.location_id(location)
                if location_id == None:
                    post_job_insert_query.location_insert(location)
                    location_id = post_job_insert_query.location_id(location)
                resul_postJob =post_job_insert_query.jobPost_insertQuery(employee_id, company_id, job_title, job_description,qualification,experience, salary_range, no_of_vacancies,employee_type_id,job_role_id,location_id)
                job_id = post_job_insert_query.get_id(job_title)
                for skill in skill_set:
                    print(skill)
                    skill_id = post_job_insert_query.skill_set(skill)
                    post_job_insert_query.skill_set_insert(employee_id,skill_id,job_id,company_id)
                if resul_postJob == True:
                    return message.response('Success','postJob')
                else:
                    return message.response('Error','postJobError') 
            else:
                return message.response('Error','companyError') 
        else:
            return message.response('Error','InputError')
    except Exception as e:
        print(f"Tha Error is : ",{str(e)})

@csrf_exempt
def locations(request):
    
   con.execute("select location from locations")
   
   rows = con.fetchall()
   locations_list = [{'location': row[0]} for row in rows]    
   json_result = json.dumps(locations_list)
   json_data = json.loads(json_result)
   print(json_data)

   print(json_data)
    
   return JsonResponse(json_data,safe=False)
    
    
@csrf_exempt
def experience(request):
    
   con.execute("select experience from job_post")
   
   rows = con.fetchall()
   locations_list = [{'experience': row[0]} for row in rows]    
   json_result = json.dumps(locations_list)
   json_data = json.loads(json_result)
   print(json_data)

   print(json_data)
    
   return JsonResponse(json_data,safe=False)    

@csrf_exempt
def employment_type(request):
    
   con.execute("select employee_type from employees_types")
   
   rows = con.fetchall()
   locations_list = [{'employee_type': row[0]} for row in rows]    
   json_result = json.dumps(locations_list)
   json_data = json.loads(json_result)
   print(json_data)

   print(json_data)
    
   return JsonResponse(json_data,safe=False)  

@csrf_exempt
def skill_set(request):
    try:
        # Execute the first query to get skill_set
        con.execute("SELECT skill_set FROM skill_sets")
        skill_rows = con.fetchall()
        skill_list = [{'skill_set': row[0]} for row in skill_rows]

        # Execute the second query to get job_title
        con.execute("SELECT job_title FROM job_post")
        job_rows = con.fetchall()
        job_title_list = [{'job_title': row[0]} for row in job_rows]
        combined_list = skill_list + job_title_list
        json_result = json.dumps(combined_list)
        json_data = json.loads(json_result)
        print(json_data)
        return JsonResponse(json_data, safe=False)

    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'error': 'An error occurred.'}, status=500)
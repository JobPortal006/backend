from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connection
from data.Account_creation import message
from django.http import JsonResponse
from data.Job.Query import post_job_insert_query 

con = connection.cursor()

# Insert the data into required tables
# Check the data is empty value or not
# Get employee_id using email in Signup Table
# Once account is created - Send mail to registered email as (Account Created Successfully message)
@csrf_exempt
def post_jobs(request):
    try:
        data = json.loads(request.body)
        job_title = data.get('job_title')
        job_description = data.get('job_description')
        employee_type = data.get('employee_type')   
        job_role = data.get('job_role')  
        location = data.get('location')            
        skill_set = data.get('skill_set')            
        qualification = data.get('qualification')
        experience = data.get('experience')
        salary_range = data.get('salary_range')  
        no_of_vacancies = data.get('no_of_vacancies') 
        company_name = data.get('company_name')
        email= data.get('email')
        print(data)
        print(email)
        valuesCheck = message.check(job_title,job_description,employee_type,job_role,location,skill_set,qualification,experience,salary_range,no_of_vacancies)
        print(valuesCheck)
        if valuesCheck:
            employee_id = post_job_insert_query.email_id(email)
            # employee_id, registered_by, email = create_account_user_query.user_check(email)  # Get employee_id using company_name
            company_id = post_job_insert_query.company_id(company_name)  # Get company_id using company_name
            if employee_id is not None and company_id is not None:
                employee_type_id = post_job_insert_query.employee_type_id(employee_type)  # Get employee_type_id here
                job_role_id = post_job_insert_query.job_role_id(job_role)  # Get job_role_id here
                # If job_role is not in the table, it will execute
                location_id = post_job_insert_query.location_id(location)  # Get location_id here
                if employee_type_id is not None and job_role_id is not None and location_id is not None:
                    # If location_id is not in the table, it will execute
                    resul_postJob = post_job_insert_query.jobPost_insertQuery(employee_id, company_id, job_title, job_description, qualification, experience, salary_range, no_of_vacancies, employee_type_id, job_role_id, location_id)
                    print(resul_postJob, 'result_postJob')
                    job_id = post_job_insert_query.get_id(job_title)  # After insert the job_post data, get that job_id
                    print(job_id)
                    for skill in skill_set:
                        print(skill)
                        skill_id = post_job_insert_query.skill_set(skill)  # Insert the skill_set in skill_sets table
                        post_job_insert_query.skill_set_insert(employee_id, skill_id, job_id)  # Map the skill_id in skill_set_mapping table
                    if resul_postJob:
                        return message.response1('Success', 'postJob', employee_id)
                    else:
                        return message.response('Error', 'postJobError')
                else:
                    return message.response('Error', 'locationError')
            else:
                return message.response('Error', 'companyError')
        else:
            return message.response('Error', 'InputError')
    except Exception as e:
        print(f"The Error is : ", str(e))
        return message.serverErrorResponse()
  

# Get all location data in locations table
@csrf_exempt
def locations(request):
   con.execute("select location from location")
   rows = con.fetchall()
   locations_list = [{'location': row[0]} for row in rows]    
   json_result = json.dumps(locations_list)
   json_data = json.loads(json_result)
   print(json_data)
   return JsonResponse(json_data,safe=False)

# Get all experience data in job_post table    
@csrf_exempt
def experience(request):
   con.execute("SELECT DISTINCT experience FROM job_post")
   rows = con.fetchall()
   print(rows)
   locations_list = [{'experience': row[0]} for row in rows]    
   json_result = json.dumps(locations_list)
   json_data = json.loads(json_result)
   print(json_data)
   return JsonResponse(json_data,safe=False) 

# Get all job_role data in job_role table
@csrf_exempt
def job_role(request):
   con.execute("select job_role from job_role ")
   rows = con.fetchall()
   locations_list = [{'role': row[0]} for row in rows]    
   json_result = json.dumps(locations_list)
   json_data = json.loads(json_result)
   print(json_data)
   return JsonResponse(json_data,safe=False)    

# Get all employee_type data in employees_types table
@csrf_exempt
def employment_type(request):
   con.execute("select employee_type from employees_types")
   rows = con.fetchall()
   locations_list = [{'employee_type': row[0]} for row in rows]    
   json_result = json.dumps(locations_list)
   json_data = json.loads(json_result)
   print(json_data)
   return JsonResponse(json_data,safe=False)  

# Get all company_name data in company_details table
@csrf_exempt
def company_name(request):
   con.execute("select DISTINCT company_name from company_details")
   rows = con.fetchall()
   locations_list = [{'company_name': row[0]} for row in rows]    
   json_result = json.dumps(locations_list)
   json_data = json.loads(json_result)
   print(json_data)
   return JsonResponse(json_data,safe=False)

# Get all skill_set and job_title data in skill_sets and job_post table
@csrf_exempt
def skill_set(request):
    # Execute the first query to get skill_set
    con.execute("SELECT skill_set FROM skill_sets")
    skill_rows = con.fetchall()
    skill_list = [{'skill_set': row[0]} for row in skill_rows]
    # Execute the second query to get job_title
    con.execute("SELECT DISTINCT job_title FROM job_post")
    job_rows = con.fetchall()
    job_title_list = [{'job_title': row[0]} for row in job_rows]
    combined_list = skill_list + job_title_list
    json_result = json.dumps(combined_list)
    json_data = json.loads(json_result)
    print(json_data)
    return JsonResponse(json_data, safe=False)

# employee_type_id = post_job_insert_query.employee_type_id(employee_type) # Get employee_type_id here
# if employee_type_id == None: 
#     post_job_insert_query.employee_type_insert(employee_type) 
#     employee_type_id = post_job_insert_query.employee_type_id(employee_type) 
# job_role_id = post_job_insert_query.job_role_id(job_role) # Get job_role_id here
# if job_role_id == None: # If job_role is not in the table , it will execute
#     post_job_insert_query.job_role_insert(job_role) # Insert job_role data in job_role table
#     job_role_id = post_job_insert_query.job_role_id(job_role) # After insert the job_role, get that job_role_id
# location_id = post_job_insert_query.location_id(location) # Get location_id here
# if location_id == None: # If location_id is not in the table , it will execute
#     post_job_insert_query.location_insert(location) # Insert location data in locations table
#     location_id = post_job_insert_query.location_id(location) # After insert the location, get that location_id
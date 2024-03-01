from django.views.decorators.csrf import csrf_exempt
import json
from django.db import OperationalError, connection
import json
from functools import wraps
from time import sleep
from data.Account_creation import message
from django.http import JsonResponse
from data.Job.Query import post_job_insert_query 
from django.core.management import call_command

con = connection.cursor()

def retry_database_operation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        max_retries = 3
        sleep_duration = 2

        for attempt in range(1, max_retries + 1):
            with connection.cursor() as cursor:
                try:
                    result = func(cursor, *args, **kwargs)
                    return result
                except OperationalError as e:
                    print(f"Attempt {attempt}: Database connection error - {e}")
                    if attempt < max_retries:
                        print(f"Retrying in {sleep_duration} seconds...")
                        sleep(sleep_duration)
                    else:
                        # Trigger a project restart on max retries
                        print("Restarting the project...")
                        call_command('runserver', '--noreload')
                        # You may need to customize this based on your project structure
                        return JsonResponse({'error': 'Database connection error. Project restarting...'}, status=500)
                finally:
                    connection.close()  # Close the connection explicitly
    return wrapper

# Insert the data into required tables
# Check the data is empty value or not
# Get employee_id using email in Signup Table
# Once account is created - Send mail to registered email as (Account Created Successfully message)
@csrf_exempt
@retry_database_operation
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
        print(f"The Error is: {str(e)}")
        return message.tryExceptError(str(e))

# Function to retrieve location data
@csrf_exempt
@retry_database_operation
def locations(cursor, request):
    try:
        cursor.execute("SELECT location FROM location")
        rows = cursor.fetchall()
        locations_list = [{'location': row[0]} for row in rows]
        json_result = json.dumps(locations_list)
        json_data = json.loads(json_result)
        print(json_data)
        return JsonResponse(json_data, safe=False)
    except Exception as e:
        # Handle the specific exception or log the error
        print(f"An error occurred: {e}")
        # Raise the exception to trigger the project restart
        raise

# Get all experience data in job_post table    
@csrf_exempt
@retry_database_operation
def experience(cursor,request):
   cursor.execute("SELECT DISTINCT experience FROM job_post")
   rows = cursor.fetchall()
   print(rows)
   locations_list = [{'experience': row[0]} for row in rows]    
   json_result = json.dumps(locations_list)
   json_data = json.loads(json_result)
   print(json_data)
   return JsonResponse(json_data,safe=False) 

# Get all job_role data in job_role table
@csrf_exempt
@retry_database_operation
def job_role(cursor,request):
   cursor.execute("select job_role from job_role ")
   rows = cursor.fetchall()
   locations_list = [{'role': row[0]} for row in rows]    
   json_result = json.dumps(locations_list)
   json_data = json.loads(json_result)
   print(json_data)
   return JsonResponse(json_data,safe=False)    

# Get all employee_type data in employees_types table
@csrf_exempt
@retry_database_operation
def employment_type(cursor,request):
   cursor.execute("select employee_type from employees_types")
   rows = cursor.fetchall()
   locations_list = [{'employee_type': row[0]} for row in rows]    
   json_result = json.dumps(locations_list)
   json_data = json.loads(json_result)
   print(json_data)
   return JsonResponse(json_data,safe=False)  

# Example usage
@csrf_exempt
@retry_database_operation
def company_name(cursor, request):
    cursor.execute("SELECT DISTINCT company_name FROM company_details")
    rows = cursor.fetchall()
    locations_list = [{'company_name': row[0]} for row in rows]
    json_result = json.dumps(locations_list)
    json_data = json.loads(json_result)
    print(json_data)
    return JsonResponse(json_data, safe=False)

# Get all skill_set and job_title data
# @csrf_exempt
# @retry_database_operation
# def skill_set(cursor, request):
#     cursor.execute("SELECT skill_set FROM skill_sets")
#     skill_rows = cursor.fetchall()
#     skill_list = [{'skill_set': row[0]} for row in skill_rows]

#     cursor.execute("SELECT DISTINCT job_title FROM job_post")
#     job_rows = cursor.fetchall()
#     job_title_list = [{'job_title': row[0]} for row in job_rows]

#     combined_list = skill_list + job_title_list
#     json_result = json.dumps(combined_list)
#     json_data = json.loads(json_result)
#     print(json_data)
#     return JsonResponse(json_data, safe=False)


@csrf_exempt
@retry_database_operation
def skill_set(cursor, request):
    try:
        cursor.execute("SELECT skill_set FROM skill_sets")
        skill_rows = cursor.fetchall()

        skill_list = []

        for row in skill_rows:
            skill_set = row[0]
            present_in_mapping = check_skill_in_mapping(cursor, skill_set)
            if present_in_mapping:
                skill_list.append({'skill_set': skill_set})

        cursor.execute("SELECT DISTINCT job_title FROM job_post")
        job_rows = cursor.fetchall()
        job_title_list = [{'job_title': row[0]} for row in job_rows]

        combined_list = skill_list + job_title_list
        json_result = json.dumps(combined_list)
        json_data = json.loads(json_result)
        print(json_data)
        return JsonResponse(json_data, safe=False)
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({"error": "Failed"}, status=500)

def check_skill_in_mapping(cursor, skill_set):
    try:
        check_sql = "SELECT COUNT(*) FROM skill_set_mapping WHERE skill_id = (SELECT id FROM skill_sets WHERE skill_set = %s)"
        cursor.execute(check_sql, [skill_set])
        count = cursor.fetchone()[0]
        return count > 0
    except Exception as e:
        print(f"Error in check_skill_in_mapping: {str(e)}")
        return False
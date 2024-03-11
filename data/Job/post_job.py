from django.views.decorators.csrf import csrf_exempt
import json
from django.db import OperationalError, connection
import json
from functools import wraps
from time import sleep
from data import message
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
                    result = func( *args, **kwargs)
                    return result
                except OperationalError as e:
                    print(f"Attempt {attempt}: Database connection error - {e}")
                    if attempt < max_retries:
                        print(f"Retrying in {sleep_duration} seconds...")
                        sleep(sleep_duration)
                    else:
                        # Trigger a project restart on max retries
                        call_command('runserver', '--noreload')
                        # You may need to customize this based on your project structure
                        return message.serverErrorResponse()
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
        additional_queries= data.get('additional_queries')
        print(data)
        valuesCheck = message.check(job_title,job_description,employee_type,job_role,location,skill_set,qualification,experience,salary_range,no_of_vacancies)
        print(valuesCheck)
        if valuesCheck:
            qualifications_list = data.get('qualification')
            employee_id = post_job_insert_query.email_id(email)
            # employee_id, registered_by, email = create_account_user_query.email_check(email)  # Get employee_id using company_name
            company_id = post_job_insert_query.company_id(company_name)  # Get company_id using company_name
            if employee_id is not None and company_id is not None:
                employee_type_id = post_job_insert_query.employee_type_id(employee_type)  # Get employee_type_id here
                job_role_id = post_job_insert_query.job_role_id(job_role)  # Get job_role_id here
                # If job_role is not in the table, it will execute
                location_id = post_job_insert_query.location_id(location)  # Get location_id here
                if employee_type_id is not None and job_role_id is not None and location_id is not None:
                    # If location_id is not in the table, it will execute
                    qualification="B.E"
                    resul_postJob = post_job_insert_query.jobPost_insertQuery(employee_id, company_id, job_title, job_description, qualification, experience, salary_range, no_of_vacancies, employee_type_id, job_role_id, location_id,additional_queries)
                    print(resul_postJob, 'result_postJob')
                    job_id = post_job_insert_query.get_id(job_title)  # After insert the job_post data, get that job_id
                    print(job_id)
                    for skill in skill_set:
                        print(skill)
                        skill_id = post_job_insert_query.skill_set(skill)  # Insert the skill_set in skill_sets table
                        post_job_insert_query.skill_set_insert(employee_id, skill_id, job_id)  # Map the skill_id in skill_set_mapping table
                    for qualification_value in qualifications_list:
                        print(qualification_value)
                        qualification_id = post_job_insert_query.qualification(qualification_value) # Insert the qualification in qualifications table
                        post_job_insert_query.qualification_insert(employee_id, qualification_id, job_id) # Map the qualification_id in qualification_mapping table
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

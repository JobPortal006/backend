from django.views.decorators.csrf import csrf_exempt
import json
from django.db import OperationalError, connection
import json
from functools import wraps
from time import sleep
from backend.data import message
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
            call_command('runserver', '--noreload')
            # You may need to customize this based on your project structure
            return message.serverErrorResponse()
        finally:
            connection.close()  # Close the connection explicitly
  return wrapper

# Function to retrieve location data
@csrf_exempt
@retry_database_operation
def locations(cursor, request):
    try:
        cursor.execute("SELECT DISTINCT l.location FROM location l JOIN job_post jp ON l.id = jp.location_id")
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
   cursor.execute("SELECT DISTINCT jp.experience JOIN job_post jp ON l.id = jp.location_id")
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
   cursor.execute("select DISTINCT jr.job_role from job_role jr JOIN job_post jp ON jr.id = jp.job_role_id")
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
   cursor.execute("select DISTINCT e.employee_type from employees_types e JOIN job_post jp ON e.id = jp.employee_type_id")
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
    cursor.execute("SELECT DISTINCT cd.id,cd.company_name FROM company_details cd JOIN job_post jp ON cd.id = jp.company_id")
    rows = cursor.fetchall()
    print(rows[0])
    locations_list = [{'company_name': row[1]} for row in rows]
    json_result = json.dumps(locations_list)
    json_data = json.loads(json_result)
    print(json_data)
    return JsonResponse(json_data, safe=False)

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
from django.db import connection
from data.Job import json_response

# Send a job details data in JSON format 
# Data is send in response as (Data/Month/Year)
def employer_post_jobs(employee_id, processed_job_ids):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('GetJobsDetailsByEmployeeId', [employee_id])
            results = cursor.fetchall()
            print(results, 'results-----------')  # Corrected from 'result' to 'results'
            if results:
                job_id = results[0][0]
                print(job_id, 'job-id-------')
                result = json_response.response(results, employee_id, job_id, cursor, processed_job_ids)
                return result
            else:
                print("No results found")
                return None
    except Exception as e:
        print(f"Error: {e}")
        return None

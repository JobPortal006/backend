from django.db import connection
from data.Job import json_response

# Send a job details data in JSON format 
# Data is send in response as (Data/Month/Year)
def employer_post_jobs(employee_id, processed_job_ids):
    try:
        result = None  # Initialize result variable
        with connection.cursor() as cursor:
            cursor.callproc('GetJobsDetailsByEmployeeId', [employee_id])
            results = cursor.fetchall()
            print(result,'result-----------')
            if results:
                # for row in results:
                #     print(row,'row-----------')
                job_id = results[0]
                print(job_id,'job-id-------')
                #     if job_id in processed_job_ids:
                #         continue
                #     processed_job_ids.add(job_id)
                result = json_response.response(results, job_id, cursor, processed_job_ids)
                return result
            else:
                print("No results found")
                return None
    except Exception as e:
        print(f"Error: {e}")
        return None

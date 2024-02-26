from django.db import connection
import json
from datetime import datetime
from humanize import naturaldelta
from data.Job.Query import job_details_query

# Send a job details data in JSON format 
# Data is send in response as (Data/Month/Year)
def employer_post_jobs(employee_id, processed_job_ids):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('GetJobsDetailsByEmployeeId', [employee_id])
            results = cursor.fetchall()
            print(results)
            if results:
                for row in results:
                    job_id = row[0]
                    if job_id in processed_job_ids:
                        continue
                    processed_job_ids.add(job_id)
                    result=job_details_query.response(results,job_id,cursor,processed_job_ids)
                return result
            else:
                print("No results found")
                return None
    except Exception as e:
        print(f"Error: {e}")
        return False

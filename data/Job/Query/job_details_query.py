from django.db import connection
from data.Job import json_response
con=connection.cursor()
# Send a job details data in JSON format 
# Data is send in response as (Data/Month/Year)
def job_result(job_id, processed_job_ids):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('GetJobsDetailsById', [job_id])
            results = cursor.fetchall()
            if results:
                for row in results:
                    job_id = row[0]
                    result = json_response.response(results, job_id, cursor, processed_job_ids)  # Corrected variable name
                return result
            else:
                print("No results found")
                return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def check_user_id(user_id):
    check_sql = "SELECT a.id FROM apply_job a JOIN job_post j ON j.id = a.job_id WHERE a.user_id= %s"
    con.execute(check_sql, [user_id])
    user = con.fetchone()
    if user is not None:
        return False
    else:
        return True
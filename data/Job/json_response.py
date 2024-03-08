from django.db import connection
from datetime import datetime
from humanize import naturaldelta
import base64

def job_response_details(results,set_data_id):
    jobs = []
    with connection.cursor() as cursor:
        for row in results:  # Corrected variable name from 'results' to 'row'
            job_id = row[0]
            # Check if job_id is already processed, skip if it is
            if job_id in set_data_id:
                continue
            set_data_id.add(job_id)
            print(f"Job ID: {job_id}")
            cursor.nextset()
            cursor.callproc('GetSkillSet', [job_id])
            skills = cursor.fetchall()
            company_logo = row[10]
            company_logo = base64.b64encode(company_logo).decode('utf-8')
            created_at = row[14]
            created_at_humanized = naturaldelta(datetime.utcnow() - created_at)
            job = {
                'id': row[0],
                'job_title': row[1],
                'job_description':row[2],
                'qualification':row[3],
                'company_name': row[4],
                'employee_type': row[5],
                'location': row[6],
                'experience': row[7],
                'salary_range': row[8],
                'no_of_vacancies': row[9],
                'company_logo': company_logo,
                'company_logo_path':row[11],
                'job_role': row[12],
                'skills': [skill[0] for skill in skills],
                'created_at': created_at_humanized
            }
            jobs.append(job)
        pass
    jobs = sorted(jobs, key=lambda x: x['created_at'])
    return jobs


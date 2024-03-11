from django.db import connection
from datetime import datetime
from humanize import naturaldelta
import base64
import json

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
            cursor.nextset()
            # Call the second stored procedure
            cursor.callproc('GetQualification', [job_id])
            qualification = cursor.fetchall()
            company_logo = row[9]
            company_logo = base64.b64encode(company_logo).decode('utf-8')
            created_at = row[13]
            created_at_humanized = naturaldelta(datetime.utcnow() - created_at)
            job = {
                'id': row[0],
                'job_title': row[1],
                'job_description':row[2],
                'qualification':[qualification[0] for qualification in qualification],
                'company_name': row[3],
                'employee_type': row[4],
                'location': row[5],  
                'experience': row[6],
                'salary_range': row[7],
                'no_of_vacancies': row[8],
                'company_logo': company_logo,
                'company_logo_path':row[10],
                'job_role': row[11],
                'skills': [skill[0] for skill in skills],
                'created_at': created_at_humanized
            }
            jobs.append(job)
        pass
    jobs = sorted(jobs, key=lambda x: x['created_at'])
    return jobs

# Send the response here
def response(results, job_id, cursor, processed_job_ids):
    data = []
    for row in results:  # Corrected variable name from 'results' to 'row'
        job_id = row[0]
        # Check if job_id is already processed, skip if it is
        # if job_id in processed_job_ids:
        #     continue
        processed_job_ids.add(job_id)
        print(f"Job ID: {job_id}")
        (job_post_id, job_title, job_description, experience, salary_range, no_of_vacancies, created_at,
            company_logo, company_name, industry_type, company_description, no_of_employees, company_website_link, company_logo_path,
            location, employee_type, job_role,street, city, state, country, pincode) = row
        created_at_humanized = naturaldelta(datetime.utcnow() - created_at)
        # Fetching skills for the current row
        cursor.nextset()
        # check_sql = """
        #     SELECT ss.skill_set
        #     FROM skill_sets ss
        #     JOIN skill_set_mapping ssm ON ss.id = ssm.skill_id
        #     WHERE ssm.job_id = %s
        # """
        cursor.callproc('GetSkillSet', [job_id])
        skills = cursor.fetchall()

        # Move to the next result set
        cursor.nextset()

        # Call the second stored procedure
        cursor.callproc('GetQualification', [job_id])
        qualification = cursor.fetchall()
        cursor.execute("SELECT company_details.id,company_details.company_logo FROM company_details join job_post on company_details.id = job_post.company_id WHERE job_post.id = %s", [job_id])
        company_id,logo_result = cursor.fetchone()
        # print(company_id,logo_result,'c----------')
        # cursor.execute("SELECT company_details.company_logo FROM company_details join job_post on company_details.id = job_post.company_id WHERE job_post.id = %s", [job_id])
        # logo_result = cursor.fetchone()
        # company_logo = logo_result[0]
        # print(company_logo,'l--------')
        company_logo = base64.b64encode(logo_result).decode('utf-8')
        job_data = {
            "job_post_id": job_post_id,
            "job_title": job_title,
            "job_description": job_description,
            "qualification": [qualification[0] for qualification in qualification],
            "experience": experience,
            "salary_range": salary_range,
            "no_of_vacancies": no_of_vacancies,
            "created_at": created_at.strftime('%d %b %Y'),
            "date": created_at_humanized,
            "company_id": company_id,
            "company_logo": company_logo,
            "company_logo_path": company_logo_path,
            "company_name": company_name,
            "industry_type": industry_type,
            "company_description": company_description,
            "no_of_employees": no_of_employees,
            "company_website_link": company_website_link,
            "skills": [skill[0] for skill in skills],
            "location": location,
            "employee_type": employee_type,
            "job_role": job_role,
            "address": {
                "street": street,
                "city": city,
                "state": state,
                "country": country,
                "pincode": pincode,
            }
        }
        data.append(job_data)
    data = sorted(data, key=lambda x: x['job_post_id'], reverse=True)
    def datetime_serializer(obj):
        try:
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S') # Convert to string representation
            else:
                # For any other types, return a string representation
                return str(obj)
        except Exception:
            # Handle exceptions if any
            return None
    result_json = json.dumps(data, default=datetime_serializer)
    return result_json
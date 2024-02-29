from django.db import connection
import json
from datetime import datetime
from humanize import naturaldelta
import base64

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
                    result = response(results, job_id, cursor, processed_job_ids)  # Corrected variable name
                return result
            else:
                print("No results found")
                return None
    except Exception as e:
        print(f"Error: {e}")
        return None

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
        (job_post_id, job_title, job_description, qualification, experience, salary_range, no_of_vacancies, created_at,
            company_logo, company_name, industry_type, company_description, no_of_employees, company_website_link,
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
        # cursor.execute(check_sql, [job_id])   
        skills = cursor.fetchall()
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
            "qualification": qualification,
            "experience": experience,
            "salary_range": salary_range,
            "no_of_vacancies": no_of_vacancies,
            "created_at": created_at.strftime('%d %b %Y'),
            "date": created_at_humanized,
            "company_id": company_id,
            "company_logo": company_logo,
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
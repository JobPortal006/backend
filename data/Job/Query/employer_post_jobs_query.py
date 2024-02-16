from django.db import connection
import json
from datetime import datetime
from humanize import naturaldelta

def employer_post_jobs(employee_id, processed_job_ids):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('GetJobsDetailsByEmployeeId', [employee_id])
            results = cursor.fetchall()
            if results:
                data = []
                for row in results:
                    job_id = row[0]
                    # Check if job_id is already processed, skip if it is
                    if job_id in processed_job_ids:
                        continue
                    processed_job_ids.add(job_id)
                    print(f"Job ID: {job_id}")
                    (job_post_id, job_title, job_description, qualification, experience, salary_range, no_of_vacancies, created_at,
                     company_logo, company_name, industry_type, company_description, no_of_employees, company_website_link,
                     location, employee_type, job_role, street, city, state, country, pincode) = row
                    created_at_humanized = naturaldelta(datetime.utcnow() - created_at)
                    # Fetching skills for the current row
                    cursor.nextset()
                    check_sql = """
                        SELECT ss.skill_set
                        FROM skill_sets ss
                        JOIN skill_set_mapping ssm ON ss.id = ssm.skill_id
                        WHERE ssm.job_id = %s
                    """
                    cursor.execute(check_sql, [job_id])   
                    skills = cursor.fetchall()
                    job_data = {
                        "job_post_id": job_post_id,
                        "job_title": job_title,
                        "job_description": job_description,
                        "qualification": qualification,
                        "experience": experience,
                        "salary_range": salary_range,
                        "no_of_vacancies": no_of_vacancies,
                        "created_at": created_at.strftime('%d %b %Y'),  # Format as "17 Jun 2018"
                        "date": created_at_humanized,  # Keep the naturaldelta format for 'date'
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

                def datetime_serializer(obj):
                    if isinstance(obj, datetime):
                        return obj.strftime('%Y-%m-%d %H:%M:%S')
                    raise TypeError("Type not serializable")

                result_json = json.dumps(data, default=datetime_serializer)
                return result_json
            else:
                print("No results found")
                return None
    except Exception as e:
        print(f"Error: {e}")
        return False

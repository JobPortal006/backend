from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connection
from data.Account_creation import message
from django.http import JsonResponse
from data.Job.Query import view_jobs_query, search_job_query

# Search the job details data in database
# Send a response as JSON format 
# Date as converted into this format(Data/Month/Year)
# Skills are sent as a response in an array
@csrf_exempt
def search_job(request):
    try:
        data = json.loads(request.body)
        location = data.get('location')
        skills = data.get('skill')
        experience = data.get('experience')
        set_data_id = set()
        jobs = []

        for skill_set in skills:
            skill_result = view_jobs_query.skill_check(skill_set)
            job_title = view_jobs_query.job_title(skill_set)

            print(set_data_id, 'id---------')

            if skill_result is not None and location is not None and experience is not None:
                f1 = "ss.skill_set = %s and l.location = %s and j.experience=%s"
                value = skill_result, location, experience
                list1 = tuple(value)
                result = search_job_query.execute_get_experience(f1, list1)
                print(result, 're----------1')

            elif job_title is not None and location is not None and experience is not None:
                f1 = "j.job_title = %s and l.location = %s and j.experience=%s"
                value = job_title, location, experience
                list1 = tuple(value)
                result = search_job_query.execute_get_experience(f1, list1)
                print(result, 're----------2')

            elif skill_result is not None and location is not None:
                f1 = "ss.skill_set = %s and l.location = %s"
                value = skill_result, location
                list1 = tuple(value)
                result = search_job_query.execute_get_experience(f1, list1)
                print(result, 're----------3')

            elif job_title is not None and location is not None:
                f1 = "j.job_title = %s and l.location = %s"
                value = job_title, location
                list1 = tuple(value)
                result = search_job_query.execute_get_experience(f1, list1)
                print(result, 're----------4')

            elif experience is not None and location is not None:
                f1 = "l.location = %s and j.experience = %s"
                value = location, experience
                list1 = tuple(value)
                result = search_job_query.execute_get_experience(f1, list1)
                print(result, 're----------5')

            else:
                f1 = 'ss.skill_set= %s or j.job_title= %s or l.location= %s or j.experience= %s'
                value = skill_result, job_title, location, experience
                list1 = tuple(value)
                result = search_job_query.execute_get_experience(f1, list1)
                print(result, 're----------6')

            with connection.cursor() as cursor:
                print(" 1 ------------------ ")
                if result:
                    for row in result:
                        job_id = row[0]
                        # Check if job_id is already processed, skip if it is
                        if job_id in set_data_id:
                            continue
                        set_data_id.add(job_id)
                        print(f"Job ID: {job_id}")
                        check_sql = """
                            SELECT ss.skill_set
                            FROM skill_sets ss
                            JOIN skill_set_mapping ssm ON ss.id = ssm.skill_id
                            WHERE ssm.job_id = %s
                        """
                        cursor.execute(check_sql, [job_id])
                        skills = cursor.fetchall()
                        job = {
                            'id': row[0],
                            'job_title': row[1],
                            'company_name': row[2],
                            'employee_type': row[3],
                            'location': row[4],
                            'experience': row[5],
                            'salary_range': row[6],
                            'no_of_vacancies': row[7],
                            'company_logo': row[8],
                            'job_role': row[9],
                            "skills": [skill[0] for skill in skills],
                            'created_at': row[10].strftime('%Y-%m-%d %H:%M:%S')
                        }
                        jobs.append(job)

        return JsonResponse(jobs, safe=False)
    except Exception as e:
        print(str(e))
        return JsonResponse("Failed", safe=False)

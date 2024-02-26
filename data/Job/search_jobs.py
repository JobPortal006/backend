from django.views.decorators.csrf import csrf_exempt
import json
import base64
from datetime import datetime
from humanize import naturaldelta
from django.db import connection
from data.Account_creation import message
from django.http import JsonResponse
from data.Job.Query import search_jobs_query
from sqlalchemy import and_, or_
from data.Account_creation.Tables.table import SkillSets,Location,JobPost
job_response = ""

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
        print(request.body)
        set_data_id = set()
        skill_results = []
        job_titles = []
        # Assuming `skill_check` expects a single string parameter, you may need to pass one skill at a time
        for skill in skills:
            skill_result = search_jobs_query.skill_check(skill)
            job_title = search_jobs_query.job_title(skill)
            if skill_result is not None:
                skill_results.append(str(skill_result))
            if job_title is not None:
                job_titles.append(str(job_title))
        skill_result = ', '.join(skill_results)
        job_title = ', '.join(job_titles)
        print("Skill Results:", skill_result)
        print("Job Titles:", job_title)
        if skill_result != '' and job_title == '' and experience == '' and location == '':
            conditions = (SkillSets.skill_set == skill_result)
            result = search_jobs_query.execute_query(conditions)
        elif skill_result == '' and job_title != '' and experience == '' and location == '':
            conditions = (JobPost.job_title == job_title)
            result = search_jobs_query.execute_query(conditions)
        elif skill_result == '' and job_title == '' and experience != '' and location == '':
            conditions = ( JobPost.experience == experience)
            result = search_jobs_query.execute_query(conditions)
        elif skill_result == '' and job_title == '' and experience == '' and location != '':
            conditions = (Location.location == location)
            result = search_jobs_query.execute_query(conditions)
        elif job_title != '' and location != '' and experience != '' and skill_result == '':
            # Combine conditions using and_
            conditions = and_(
                JobPost.job_title == job_title,
                Location.location == location,
                JobPost.experience == experience)
            result = search_jobs_query.execute_query(conditions) 
            conditions = or_(
                JobPost.job_title == job_title,
                Location.location == location,
                JobPost.experience == experience)
            result = search_jobs_query.execute_query(conditions)

        elif skill_result != '' and location != '' and experience != '' and job_title == '':
            # Combine conditions using and_
            conditions = and_(
                SkillSets.skill_set == skill_result,
                Location.location == location,
                JobPost.experience == experience)
            result = search_jobs_query.execute_query(conditions) 
            conditions = or_(
                SkillSets.skill_set == skill_result,
                Location.location == location,
                JobPost.experience == experience)
            result = search_jobs_query.execute_query(conditions)

        elif skill_result != '' and location != '' and experience == '' and job_title == '':
            conditions = and_(
                SkillSets.skill_set == skill_result,
                Location.location == location)
            result = search_jobs_query.execute_query(conditions)
            conditions = or_(
                SkillSets.skill_set == skill_result,
                Location.location == location)
            result = search_jobs_query.execute_query(conditions)

        elif job_title != '' and location != '' and skill_result == '' and experience == '':
            conditions = and_(
                JobPost.job_title == job_title,
                Location.location == location)
            result = search_jobs_query.execute_query(conditions)
            conditions = or_(
                JobPost.job_title == job_title,
                Location.location == location)
            result = search_jobs_query.execute_query(conditions)

        elif experience != '' and location != '' and skill_result == '' and job_title == '':
            conditions = and_(
                Location.location == location,
                JobPost.experience == experience)
            result = search_jobs_query.execute_query(conditions)
            conditions = or_(
                Location.location == location,
                JobPost.experience == experience)
            result = search_jobs_query.execute_query(conditions)
        else:
            conditions = and_(
                SkillSets.skill_set == skill_result,
                JobPost.job_title == job_title,
                Location.location == location,
                JobPost.experience == experience)
            result = search_jobs_query.execute_query(conditions)
            # Second query if the first one returns no results
            conditions = or_(
                SkillSets.skill_set == skill_result,
                JobPost.job_title == job_title,
                Location.location == location,
                JobPost.experience == experience)
            result = search_jobs_query.execute_query(conditions)
        jobs=job_response_details(result,set_data_id)
        global job_response
        job_response = jobs
        # return JsonResponse(jobs, safe=False)
        return message.response('Success','searchJob')
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {str(e)}")
        # return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        return message.response('Error','searchJobError')

@csrf_exempt
def get_view_jobs(request):
    try:
        url_response = job_response
        if url_response:
            return message.response1('Success', 'getJobDetails', url_response)
        else:
            return message.response1('Error', 'searchJobError', data={})
    except Exception as e:
        print(f"The Error is: {str(e)}")
        return message.serverErrorResponse()
    
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
            # print(skills,'skill-----------')
            # cursor.execute("SELECT company_details.company_logo FROM company_details join job_post on company_details.id = job_post.company_id WHERE job_post.id = %s", [job_id])
            # logo_result = cursor.fetchone()
            company_logo = row[8]
            company_logo = base64.b64encode(company_logo).decode('utf-8')
            created_at = row[10]
            created_at_humanized = naturaldelta(datetime.utcnow() - created_at)
            job = {
                'id': row[0],
                'job_title': row[1],
                'company_name': row[2],
                'employee_type': row[3],
                'location': row[4],
                'experience': row[5],
                'salary_range': row[6],
                'no_of_vacancies': row[7],
                'company_logo': company_logo,
                'job_role': row[9],
                "skills": [skill[0] for skill in skills],
                'created_at': created_at_humanized
            }
            jobs.append(job)
            # jobs = sorted(jobs, key=lambda x: x['created_at'], reverse=True)
    jobs = sorted(jobs, key=lambda x: x['created_at'])
    return jobs
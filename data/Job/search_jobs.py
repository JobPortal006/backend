from django.views.decorators.csrf import csrf_exempt
from django.db import OperationalError, DatabaseError, connection
from time import sleep
import json
from datetime import datetime
from humanize import naturaldelta
import base64
from django.http import JsonResponse
from data import message
from data.Job.Query import search_jobs_query
from sqlalchemy import and_, or_
from data.Account_creation.Tables.table import SkillSets, Location, JobPost

job_response = ""

def retry_database_operation(operation, max_retries=3, sleep_duration=2):
    for attempt in range(1, max_retries + 1):
        try:
            operation()
            break
        except (OperationalError, DatabaseError) as e:
            print(f"Database operation error: {e}")
            print(f"Retrying... (Attempt {attempt}/{max_retries})")
            sleep(sleep_duration)

# Search the job details data in database
# Send a response as JSON format 
# Date as converted into this format(Data/Month/Year)
# Skills are sent as a response in an array
@csrf_exempt
def search_job(request):
    try:
        data = json.loads(request.body)
        print(data)
        location = data.get('location')
        skills = data.get('skill')
        experience = data.get('experience')
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
        # Combine conditions using and_ and or_
        # check skill_result in Database  
        if skill_result != '' and job_title == '' and experience == '' and location == '':
            conditions = (SkillSets.skill_set == skill_result)
            result = search_jobs_query.execute_query(conditions)
        # check job_title in Database
        elif skill_result == '' and job_title != '' and experience == '' and location == '':
            conditions = (JobPost.job_title == job_title)
            result = search_jobs_query.execute_query(conditions)
        # check experience in Database
        elif skill_result == '' and job_title == '' and experience != '' and location == '':
            conditions = ( JobPost.experience == experience)
            result = search_jobs_query.execute_query(conditions)
        # check location in Database
        elif skill_result == '' and job_title == '' and experience == '' and location != '':
            conditions = (Location.location == location)
            result = search_jobs_query.execute_query(conditions)
        # check job_title, location and experience in Database
        elif job_title != '' and location != '' and experience != '' and skill_result == '':
            conditions = and_(JobPost.job_title == job_title, Location.location == location,JobPost.experience == experience)
            result = search_jobs_query.execute_query(conditions) 
            conditions = or_(JobPost.job_title == job_title,Location.location == location,JobPost.experience == experience)
            result = search_jobs_query.execute_query(conditions)
        # check skill_result, location and experience in Database
        elif skill_result != '' and location != '' and experience != '' and job_title == '':
            conditions = and_(SkillSets.skill_set == skill_result,Location.location == location,JobPost.experience == experience)
            result = search_jobs_query.execute_query(conditions) 
            conditions = or_(SkillSets.skill_set == skill_result,Location.location == location,JobPost.experience == experience)
            result = search_jobs_query.execute_query(conditions)
        # check skill_result and location in Database
        elif skill_result != '' and location != '' and experience == '' and job_title == '':
            conditions = and_(SkillSets.skill_set == skill_result,Location.location == location)
            result = search_jobs_query.execute_query(conditions)
            conditions = or_(SkillSets.skill_set == skill_result,Location.location == location)
            result = search_jobs_query.execute_query(conditions)
        # check job_title and location in Database
        elif job_title != '' and location != '' and skill_result == '' and experience == '':
            conditions = and_(JobPost.job_title == job_title,Location.location == location)
            result = search_jobs_query.execute_query(conditions)
            conditions = or_(JobPost.job_title == job_title,Location.location == location)
            result = search_jobs_query.execute_query(conditions)
        # check location and experience in Database
        elif experience != '' and location != '' and skill_result == '' and job_title == '':
            conditions = and_(Location.location == location,JobPost.experience == experience)
            result = search_jobs_query.execute_query(conditions)
            conditions = or_( Location.location == location,JobPost.experience == experience)
            result = search_jobs_query.execute_query(conditions)
        # check skill_result, job_title, location and experience in Database
        else:
            conditions = and_(SkillSets.skill_set == skill_result,JobPost.job_title == job_title,
                Location.location == location,JobPost.experience == experience)
            result = search_jobs_query.execute_query(conditions)
            conditions = or_(SkillSets.skill_set == skill_result,JobPost.job_title == job_title,
                Location.location == location,JobPost.experience == experience)
            result = search_jobs_query.execute_query(conditions)
        jobs=job_response_details(result,set_data_id)
        global job_response
        job_response = jobs
        if jobs:
           return message.response1('Success', 'getJobDetails', jobs)
        else:
            return message.response('Error', 'searchJobError')
    except (OperationalError, DatabaseError) as e:
        print(f"Database connection error: {e}")
        # Retry database operation
        retry_database_operation(connection.close)

@csrf_exempt
def get_view_jobs(request):
    try:
        url_response = job_response
        if url_response:
            return message.response1('Success', 'getJobDetails', url_response)
        else:
            return message.response1('Error', 'searchJobError', data={})
    except (OperationalError, DatabaseError) as e:
        print(f"Database connection error: {e}")
        # Retry database operation
        retry_database_operation(connection.close)
    
def job_response_details(results,set_data_id):
    print("success")
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
            created_at = row[13]
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
                'job_role': row[11],
                'skills': [skill[0] for skill in skills],
                'created_at': created_at_humanized
            }
            jobs.append(job)
        pass
    jobs = sorted(jobs, key=lambda x: x['created_at'])
    return jobs

def result():
    return job_response
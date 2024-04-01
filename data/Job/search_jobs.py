from django.views.decorators.csrf import csrf_exempt
from django.db import OperationalError, DatabaseError
import json
from data.token import decode_token
from data import message
from data.Job.Query import search_jobs_query
from data.Job import json_response
from sqlalchemy import and_, or_
from data.Job.post_job import retry_database_operation
from data.Tables.table import SkillSets, Location, JobPost
from data.Job import job_details_by_companyName
from data.Job import job_details_by_employeeType

# def retry_database_operation(operation, max_retries=3, sleep_duration=2):
#     for attempt in range(1, max_retries + 1):
#         try:
#             operation()
#             break
#         except (OperationalError, DatabaseError) as e:
#             print(f"Database operation error: {e}")
#             print(f"Retrying... (Attempt {attempt}/{max_retries})")
#             sleep(sleep_duration)

# Search the job details data in database
# Send a response as JSON format 
# Date as converted into this format(Data/Month/Year)
# Skills are sent as a response in an array
@csrf_exempt
@retry_database_operation
def search_job(request):
    global job_response,search_fun_call
    try:
        data = json.loads(request.body)
        print(data)
        location = data.get('location')
        skills = data.get('skill')
        experience = data.get('experience')
        # token = data.get('token')
        # user_id, registered_by, email = decode_token(token)
        # print(user_id, registered_by, email)
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
        search_fun_call = 'search'
        job_details_by_companyName.company_fun_call  = None
        job_details_by_employeeType.employee_call_fun = None

        # Combine conditions using and_ and or_
        # check skill_result in Database  
        if skill_result and not job_title and not experience and not location:
            conditions = (SkillSets.skill_set == skill_result)
            result = search_jobs_query.execute_query(conditions)

        # check job_title in Database
        elif not skill_result and job_title and not experience and not location:
            conditions = (JobPost.job_title == job_title)
            result = search_jobs_query.execute_query(conditions)

        # check experience in Database
        elif not skill_result and not job_title and experience and not location:
            conditions = ( JobPost.experience == experience)
            result = search_jobs_query.execute_query(conditions)

        # check location in Database
        elif not skill_result and not job_title and not experience and location:
            conditions = (Location.location == location)
            result = search_jobs_query.execute_query(conditions)

        # check job_title, location and experience in Database
        elif job_title and location and experience and not skill_result:
            conditions = and_(JobPost.job_title == job_title, Location.location == location,JobPost.experience == experience)
            result = search_jobs_query.execute_query(conditions) 
            if not result:  # Check if result is an empty list
                job_title_location_result = job_title_location(job_title,location) # Print the result after calling job_title_location
                location_experience_result = location_experience(location, experience) # Print the result after calling location_experience
                result = job_title_location_result + location_experience_result # Combine results from both functions
            # conditions = or_(JobPost.job_title == job_title,Location.location == location,JobPost.experience == experience)
            # result = search_jobs_query.execute_query(conditions)
                
        # check skill_result, location and experience in Database
        elif skill_result and location and experience and not job_title:
            conditions = and_(SkillSets.skill_set == skill_result,Location.location == location,JobPost.experience == experience)
            result = search_jobs_query.execute_query(conditions) 
            print(result,'Initial Result')  # Print the initial result
            if not result:  # Check if result is an empty list
                skill_location_result = skill_location(skill_result, location) # Print the result after calling skill_location
                location_experience_result = location_experience(location, experience) # Print the result after calling location_experience
                result = skill_location_result + location_experience_result # Combine results from both functions
            # conditions = or_(SkillSets.skill_set == skill_result,Location.location == location,JobPost.experience == experience)
            # result = search_jobs_query.execute_query(conditions)
                
        # check skill_result and location in Database
        elif skill_result and location and not experience and not job_title:
            result = skill_location(skill_result,location)
            # conditions = or_(SkillSets.skill_set == skill_result,Location.location == location)
            # result = search_jobs_query.execute_query(conditions)

        # check job_title and location in Database
        elif job_title and location and not skill_result and not experience:
            conditions = and_(JobPost.job_title == job_title,Location.location == location)
            result = search_jobs_query.execute_query(conditions)
            # conditions = or_(JobPost.job_title == job_title,Location.location == location)
            # result = search_jobs_query.execute_query(conditions)

        # check location and experience in Database
        elif location and experience and not skill_result and not job_title:
            result = location_experience(location,experience)
            # conditions = or_( Location.location == location,JobPost.experience == experience)
            # result = search_jobs_query.execute_query(conditions)
            
        # check skill_result, job_title, location and experience in Database
        else:
            conditions = and_(SkillSets.skill_set == skill_result,JobPost.job_title == job_title,
                Location.location == location,JobPost.experience == experience)
            result = search_jobs_query.execute_query(conditions)
            if not result:  # Check if result is an empty list
                skill_location_result = skill_location(skill_result, location) # Print the result after calling skill_location
                job_title_location_result = job_title_location(job_title,location) # Print the result after calling job_title_location
                location_experience_result = location_experience(location, experience) # Print the result after calling location_experience
                result = skill_location_result + job_title_location_result + location_experience_result # Combine results from both functions
            # conditions = or_(SkillSets.skill_set == skill_result,JobPost.job_title == job_title,
            #     Location.location == location,JobPost.experience == experience)
            # result = search_jobs_query.execute_query(conditions)
        # jobs=json_response.job_response_details(result,set_data_id,user_id)
        jobs=json_response.job_response_details(result,set_data_id)
        job_response = jobs
        if jobs:
           return message.response1('Success', 'getJobDetails', jobs)
        else:
            return message.response('Error', 'searchJobError')
    except Exception as e:
    # except (OperationalError, DatabaseError) as e:
        return message.tryExceptError(str(e))

# @csrf_exempt
# @retry_database_operation
# def get_view_jobs(request):
#     try:
#         url_response = job_response
#         if url_response:
#             return message.response1('Success', 'getJobDetails', url_response)
#         else:
#             return message.response1('Error', 'searchJobError', data={})
#     except (OperationalError, DatabaseError) as e:
#         print(f"Database connection error: {e}")
#         # Retry database operation
#         # retry_database_operation(connection.close)
    
def skill_location(skill_result,location):
    conditions = and_(SkillSets.skill_set == skill_result,Location.location == location)
    result = search_jobs_query.execute_query(conditions)
    return result

def job_title_location(job_title,location):
    conditions = and_(JobPost.job_title == job_title, Location.location == location)
    result = search_jobs_query.execute_query(conditions)
    return result

def location_experience(location,experience):
    conditions = and_(Location.location == location,JobPost.experience == experience)
    result = search_jobs_query.execute_query(conditions)
    return result

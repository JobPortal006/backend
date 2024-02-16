from django.views.decorators.csrf import csrf_exempt
import json
from data.Account_creation import message
from data.Job.Query import view_jobs_query

job_response = []

@csrf_exempt
def view_jobs(request):
    try:
        if request.body:
            data = json.loads(request.body)
            location = data.get('location')
            skills = data.get('skill')
            experience = data.get('experience')
            values_check = message.searchcheck(location, experience)

            if values_check:
                processed_job_ids = set()
                search_results_for_skill = []  # Initialize result list

                for skill_set in skills:
                    skill_result = view_jobs_query.skill_check(skill_set)
                    job_title = view_jobs_query.job_title(skill_set)

                    if skill_result is not None:
                        search_results_for_skill.extend(view_jobs_query.search_skill(skill_result, processed_job_ids))

                    if job_title is not None:
                        search_results_for_skill.extend(view_jobs_query.search_jobTitle(job_title, processed_job_ids))

                    if location is not None:
                        search_results_for_skill.extend(view_jobs_query.search_location(location, processed_job_ids))

                    if experience is not None:
                        search_results_for_skill.extend(view_jobs_query.search_experience(experience, processed_job_ids))

                    if skill_result is not None and location is not None:
                        search_results_for_skill.extend(view_jobs_query.search_skill_location(skill_set, location, processed_job_ids))

                    if job_title is not None and location is not None:
                        search_results_for_skill.extend(view_jobs_query.search_jobTitle_location(job_title, location, processed_job_ids))

                    if experience is not None and location is not None:
                        search_results_for_skill.extend(view_jobs_query.search_location_experience(location, experience, processed_job_ids))

                    if skill_result is not None and location is not None and experience is not None:
                        search_results_for_skill.extend(view_jobs_query.search_skill_location_and_experience(skill_set, location, experience, processed_job_ids))
                    else:
                        search_results_for_skill.extend(view_jobs_query.search_jobTitle_location_and_experience(job_title, location, experience, processed_job_ids))

                if search_results_for_skill:
                    job_response.extend(search_results_for_skill)
                    result = [json.loads(result) for result in job_response]
                    return message.response1('Success', 'searchJob', result)
                else:
                    return message.response1('Error', 'searchJobError', data={})
            else:
                return message.response1('Error', 'ValuesCheckError', data={})
        else:
            return message.response1('Error', 'EmptyRequestBody', data={})
    except Exception as e:
        print(f"The Error is: {str(e)}")
        return message.serverErrorResponse()

# @csrf_exempt
# def get_view_jobs(request):
#     try:
#         if job_response:
#             return message.response1('Success', 'getSearchJob', job_response)
#         else:
#             return message.response1('Error', 'searchJobError', data={})
#     except Exception as e:
#         print(f"The Error is: {str(e)}")
#         return message.serverErrorResponse()

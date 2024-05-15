from django.views.decorators.csrf import csrf_exempt
import json
from data import message
from data.token import decode_token
from data.Job.Query import job_notification_query,job_details_query
from data.Tables.table import JobNotification

@csrf_exempt
# def job_notification(request):
def job_notification(job_id,skills,locations):
  try:
    # data = json.loads(request.body)
    # job_id = data.get('job_id')
    # skills = data.get('skills')
    # locations = data.get('locations')
    
    table_name = 'skill_sets' 
    column_name ='skill_set'
    job_column = 'key_skills'
    skill_id = job_notification_query.query_function(skills,table_name,column_name,job_column)
    
    table_name = 'location' 
    column_name ='location'
    job_column = 'preferred_locations'
    location_id = job_notification_query.query_function(locations,table_name,column_name,job_column)
    
    S_set = set(skill_id)
    L_set = set(location_id)
    merged_set = S_set.union(L_set)
    result_list = list(merged_set)
    
    job_notification_query.notification_tab(result_list,job_id)
    
    # Mail send
    emails =  job_notification_query.get_emails(result_list)
    job_notification_query.send_email(emails)
    
    return message.response('Success', 'jobNotification')
  except Exception as e:
    return message.tryExceptError(str(e))
  
@csrf_exempt
def get_job_notifications(request):
  try:
    data = json.loads(request.body)
    token = data.get('token')
    user_id,registered_by,email = decode_token(token)
    print(user_id, registered_by,email)
    if user_id is not None:
      session = message.create_session()
      saved_job_ids = session.query(JobNotification.job_id).filter_by(user_id=user_id).all()
      # Extract job IDs from the result and convert them into a list
      job_ids_list = [job_id[0] for job_id in saved_job_ids]
      print(job_ids_list)
      response_data = []
      set_data_id = set()
      for job_id in job_ids_list:
        if job_id in set_data_id:
          continue
        # set_data_id.add(job_id)
        job_result = job_details_query.job_result(job_id,user_id, set_data_id)
        job_result_dict = json.loads(job_result)  # Convert search_result to a Python dictionary
        response_data.append(job_result_dict)  # Append the job data inside the loop
      if response_data:
        return message.response1('Success', 'searchJob', response_data)
      else:
        return message.response1('Error', 'searchJobError', data={})
    else:
      return message.response('Error', 'tokenError')
  except Exception as e:
    return message.tryExceptError(str(e))
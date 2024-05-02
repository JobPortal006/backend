from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connection
from data import message
from data.Job.post_job import retry_database_operation
from data.token import decode_token
from data.Job.Query import job_details_query
from data.Tables.table import SavedJob

con = connection.cursor()
session = message.create_session()

@csrf_exempt
@retry_database_operation
def save_job(request):
  try:
    data = json.loads(request.body)
    job_id = data.get('job_id')
    token = data.get('token')
    user_id,registered_by,email = decode_token(token)
    print(user_id, registered_by,email)
    if user_id is not None:
      # Check if the record already exists
      existing_record = session.query(SavedJob).filter_by(user_id=user_id, job_id=job_id).first()
      
      if existing_record:
        # If the record already exists, return an error
        return message.response('Error', 'alreadySavedJobError')
      else:
        save_job_instance = SavedJob(user_id=user_id, job_id=job_id)
        session.add(save_job_instance)
        session.commit()
        session.close()
      if save_job_instance:  # Checking if response_data is not empty
        return message.response('Success', 'savedJob')
      else:
        return message.response('Error', 'savedJobError')
    else:
      return message.response('Error', 'tokenError')
  except Exception as e:
    return message.tryExceptError(str(e))
  
@csrf_exempt
@retry_database_operation
def delete_save_job(request):
  try:
    data = json.loads(request.body)
    job_id = data.get('job_id')
    token = data.get('token')
    user_id,registered_by,email = decode_token(token)
    print(user_id, registered_by,email)
    if user_id is not None:
      saved_job_instance = session.query(SavedJob).filter_by(user_id=user_id, job_id=job_id).first()
      if saved_job_instance:
        session.delete(saved_job_instance)
        session.commit()
        session.close()
        return message.response('Success', 'savedUnJob',)
      else:
        session.close()
        return message.response('Error', 'savedJobError')
    else:
      return message.response('Error', 'tokenError')
  except Exception as e:
    return message.tryExceptError(str(e))
  
@csrf_exempt
@retry_database_operation
def get_all_saved_jobs(request):
  try:
    data = json.loads(request.body)
    token = data.get('token')
    user_id, registered_by, email = decode_token(token)
    print(user_id, registered_by, email)
    if user_id is not None:
      saved_job_ids = session.query(SavedJob.job_id).filter_by(user_id=user_id).all()
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
        return message.response1('Success', 'userApplyJob', response_data)
      else:
        return message.response1('Error', 'searchJobError', data={})
    else:
      return message.response('Error', 'tokenError')
  except Exception as e:
    return message.tryExceptError(str(e))

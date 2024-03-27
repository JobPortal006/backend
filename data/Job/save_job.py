from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connection
from data import message
from data.Job.post_job import retry_database_operation
from data.token import decode_token
from data.Account_creation.Tables.table import SavedJob
con = connection.cursor()

@csrf_exempt
@retry_database_operation
def save_job(request):
  try:
    data = json.loads(request.body)
    job_id = data.get('job_id')
    token = data.get('token')
    user_id,registered_by,email = decode_token(token)
    print(user_id, registered_by,email)
    session = message.create_session()
    save_job_instance = SavedJob(user_id=user_id, job_id=job_id)
    session.add(save_job_instance)
    session.commit()
    session.close()
    if save_job_instance:  # Checking if response_data is not empty
      return message.response('Success', 'savedJob',)
    else:
      return message.response('Error', 'savedJobError')
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
    saved_job_instance = SavedJob.objects.filter(user_id=user_id, job_id=job_id).first()
    if saved_job_instance:
      saved_job_instance.delete()  # Checking if response_data is not empty
      return message.response('Success', 'savedJob',)
    else:
      return message.response('Error', 'savedJobError')
  except Exception as e:
    return message.tryExceptError(str(e))
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connection
from data import message
from data.Job.Query import user_job_apply_list_query 
from data.Account_creation.User_account import get_user_account
from data.Account_creation.Query import create_account_user_query
con = connection.cursor()

@csrf_exempt
def user_job_apply_list(request):
  try:
    data = json.loads(request.body)
    job_id = data.get('job_id')
    print(job_id)
    global global_job_id
    global_job_id = job_id
    user_ids = user_job_apply_list_query.applyJob_datas(job_id)
    if not user_ids:  # If the list is empty
      return message.response1('Error', 'userJobViewError', data={})
    response_data = []
    for user_id in user_ids:
      user_details = get_user_account.user_details(user_id)
      total_experience, current_ctc, expected_ctc, notice_period = user_job_apply_list_query.additional_query(job_id, user_id)
      if total_experience is not None:
        user_details['additional_queries'] = {
          'total_experience': total_experience,
          'current_ctc': current_ctc,
          'expected_ctc': expected_ctc,
          'notice_period': notice_period
        }
      response_data.append(user_details)
    if response_data:  # Checking if response_data is not empty
      return message.response1('Success', 'getJobDetails', response_data)
    else:
      return message.response1('Error', 'searchJobError', data={})
  except Exception as e:
    return message.tryExceptError(str(e))
  
@csrf_exempt
def user_profile_list(request):
  try:
    data = json.loads(request.body)
    email = data.get('email')
    print(email)
    user_id, registered_by, email = create_account_user_query.email_check(email)
    user_details = get_user_account.user_details(user_id)
    job_id=global_job_id
    if job_id is not None:
      total_experience, current_ctc, expected_ctc, notice_period = user_job_apply_list_query.additional_query(job_id, user_id)
      if total_experience is not None:
        user_details['additional_queries'] = {
          'total_experience': total_experience,
          'current_ctc': current_ctc,
          'expected_ctc': expected_ctc,
          'notice_period': notice_period
        }
      if user_details is not None:
        return message.response1('Success', 'getJobDetails', user_details)
      else:
        return message.response1('Error', 'searchJobError', data={})
    else:
      return message.response1('Error', 'searchJobError', data={})
  except Exception as e:
    return message.tryExceptError(str(e))
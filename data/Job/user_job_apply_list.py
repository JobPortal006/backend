from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connection
from data import message
from data.Job.Query import user_job_apply_list_query 
from data.Account_creation.User_account import get_user_account
con = connection.cursor()

@csrf_exempt
def user_job_apply_list(request):
  try:
    data = json.loads(request.body)
    job_id = data.get('job_id')
    print(job_id)
    user_id = user_job_apply_list_query.applyJob_datas(job_id)
    user_details = get_user_account.user_details(user_id)
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
  except Exception as e:
    return message.tryExceptError(str(e))
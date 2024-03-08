from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connection
from django.http import JsonResponse
from data.Job.Query import search_jobs_query
from data.Job import json_response
from sqlalchemy import and_
from data.Account_creation.Tables.table import JobPost

con = connection.cursor()
@csrf_exempt
def get_job_details_by_id(request):
    try:
        data = json.loads(request.body)
        job_id = data.get('job_id')
        print(job_id)
        global select_val
        set_data_id = set()
        conditions = and_(JobPost.id == job_id)
        result = search_jobs_query.execute_query(conditions)
        json_data = json_response.job_response_details(result,set_data_id)
        select_val = json_data
        return JsonResponse(json_data, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse("Failed", safe=False)

@csrf_exempt
def select_get_job_details(request):
    if request.method == 'GET':
        try:
            json_data = json.loads(select_val.content)
            print(json_data)
            return JsonResponse(json_data, safe=False)
        except:
            return JsonResponse("Failed", safe=False)
    else:
        return JsonResponse("Incorrect Method Type - Use GET")

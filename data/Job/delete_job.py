from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connection
from backend.data import message
from django.http import JsonResponse
from data.Job.Query import delete_job_query

@csrf_exempt
def delete_jobPost(request):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            print(data)
            job_id = data.get('job_id')
            if job_id != None:
                value = delete_job_query.delete_postJob(job_id)
                if value == True:
                    return message.response("Error","deletePostJob")
                else:
                    return message.response("Error","searchJobError")
            else:
                return message.response("Error","InputError")
        except Exception as e:
            return message.tryExceptError(str(e))
    else:
        return message.response("Error","deleteJobPost_Method")
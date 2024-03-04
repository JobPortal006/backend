from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connection
from data.Account_creation import message
from django.http import JsonResponse
from data.Job.Query import delete_job_query

@csrf_exempt
def delete_jobPost(request):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            id = data.get('id')
            if id != None:
                delete_job_query.update_jobs(id)
                return message.response('Success','deletePostJob')
        except Exception as e:
            return message.tryExceptError(str(e))
    else:
        # return JsonResponse("Request miss match",safe=False)
        return message.response('Error','deleteJobPost_Method')
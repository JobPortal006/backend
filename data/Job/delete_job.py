from django.views.decorators.csrf import csrf_exempt
import json
from data import message
from data.Job.Query import delete_job_query

@csrf_exempt
def delete_jobPost(request):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            job_id = data.get('job_id')
            print(job_id)
            if job_id != None:
                value = delete_job_query.delete_postJob(job_id)
                # print(value)
                if value == 1:
                    return message.response("Success","deletePostJob")
                else:
                    return message.response("Error","searchJobError")
            else:
                return message.response("Error","InputError")
        except Exception as e:
            return message.tryExceptError(str(e))
    else:
        return message.response("Error","deleteJobPost_Method")
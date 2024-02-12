from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connection
from data.Account_creation import message
from data.Job.Query import view_jobs_query

con = connection.cursor()

@csrf_exempt
def view_jobs(request):
    try:
      data = json.loads(request.body) 
      location  = data.get('location')            
      skill = data.get('skill')
      experience    = data.get('experience')
      print(data)
      valuesCheck = message.searchcheck(location,experience)
      print(valuesCheck)
      if valuesCheck:
        # location_result =view_jobs_query.location(location)
        # print(location_result)  
        # experienct_result =view_jobs_query.experience(experience)
        # print(experienct_result)  
        print(skill)
        for s in skill:  # Change variable name to avoid conflict
          print(s)
          skill_result = view_jobs_query.skill_check(s)
          if skill_result is None:
            job_title = view_jobs_query.job_title(s) 
            s = ''
            skill_result = view_jobs_query.skill(s, job_title)
            print(skill_result)
          else:
            job_title = ''
            skill_result = view_jobs_query.skill(s, job_title)
            print(skill_result)
        
        if skill_result != '':
            return message.response('Success','postJob')
        else:
            return message.response('Error','postJobError') 
      else:
          return message.response('Error','InputError')
    except Exception as e:
        print(f"Tha Error is : ",{str(e)})
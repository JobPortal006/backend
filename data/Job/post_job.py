from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from django.db import connection
from data.Account_creation.Query import login_query
from data.Account_creation import message
from django.http import JsonResponse
from data.Job.Query import post_job_insert_query 


con = connection.cursor()

@csrf_exempt
def post_jobs(request):
    try:
        data = json.loads(request.body)
        job_title = data.get('job_title')
        job_description = data.get('job_description')
        employee_type = data.get('employee_type')  # --------
        job_category  = data.get('job_category')   # ------------
        location  = data.get('location')            # ----------- 
        skill_set = data.get('skill_set')            # --------------
        qualification = data.get('qualification')
        experience    = data.get('experience')
        salary_range  = data.get('salary_range')
        no_of_vacancies = data.get('no_of_vacancies') 
        
        print("---------------------------------")
        print(data)
        
        valuesCheck = message.check(job_title,job_description,employee_type,job_category,location,skill_set,qualification,experience,salary_range,no_of_vacancies)
        
        if valuesCheck == True:
            resul_postJob =post_job_insert_query.jobPost_insertQuery(job_title,job_description,employee_type,job_category,location,skill_set,qualification,experience,salary_range,no_of_vacancies)
            # if resul_postJob == True :
            #     val = post_job_insert_query.employetype_query(employee_type)
            #     return JsonResponse("Good",safe=False)
            if resul_postJob == True:
                return message.response('Success','postJob')
            else:
                return message.response('Error','postJobError')
                
            # else:
            #     return JsonResponse("Its Failed Insert..",safe=False)
            
        else:
            return message.response('Error','postJobInput')
        
    except Exception as e:
        print(f"Tha Error is : ",{str(e)})
    
    
    
    # return  JsonResponse("Success",safe=False)

@csrf_exempt
def locations(request):
    
   con.execute("select location from locations")
   
   rows = con.fetchall()
   locations_list = [{'location': row[0]} for row in rows]    
   json_result = json.dumps(locations_list)
   json_data = json.loads(json_result)
   print(json_data)

   print(json_data)
    
   return JsonResponse(json_data,safe=False)
    
    
@csrf_exempt
def experience(request):
    
   con.execute("select exeperience from exp_years")
   
   rows = con.fetchall()
   locations_list = [{'experience': row[0]} for row in rows]    
   json_result = json.dumps(locations_list)
   json_data = json.loads(json_result)
   print(json_data)

   print(json_data)
    
   return JsonResponse(json_data,safe=False)    


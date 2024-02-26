from django.db import connection

from django.http import JsonResponse
import base64
from datetime import datetime
from humanize import naturaldelta



def where_condition(data,experience_value,and_op,filter_valyes,where_cons):
    key_value = None
    for key, value in data.items():
        if value == experience_value:
            key_value = key
            break
    if experience_value:
            if where_cons == "":
                where_cons = f"{key_value} = %s "
                
            else:
                where_cons = where_cons + f" {and_op} {key_value} = %s"
              
            return where_cons 
        
        
   
def execute_join_jobPost(f1,list1):
    try:
        
        print(f1," ----------->>>>>>>>>>>>>>>>>>>>")
        print("^^^^^^^^",list1)
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    j.id,
                    j.job_title,
                    c.company_name,
                    et.employee_type,
                    l.location,
                    j.experience,
                    j.salary_range,
                    j.no_of_vacancies,
                    c.company_logo,
                    jr.job_role,
                    j.created_at,
                    ss.skill_set
                FROM job_post j
                JOIN location l ON j.location_id = l.id
                JOIN employees_types et ON j.employee_type_id = et.id
                JOIN job_role jr ON j.job_role_id = jr.id
                JOIN skill_set_mapping ssm ON j.id = ssm.job_id
                JOIN skill_sets ss ON ssm.skill_id = ss.id
                JOIN company_details c ON j.company_id = c.id
                WHERE  
            """+ f1, tuple(list1))
            
            print("3 ----------- 3")
            
            
            
            
            
            # Fetch the results
            rows = cursor.fetchall()
            
            # print("ROWSS : ",rows)
            print("Select ----  ",rows)
            
            # Process the results as needed
            return rows
    except Exception as e:
        return JsonResponse({'errorsssssssssss': str(e)}, status=500)
def result_fun(results):    
    with connection.cursor() as cursor:
        print("RESULTS: ",results)
        try:
            set_data_id = set()
            jobs=[]
            count = 0
            
                
            print(" 1 ------------------ ")
        
            print("2 ------------- ")
                
            if results:
                for row in results:
                    job_id = row[0]
                    # Check if job_id is already processed, skip if it is
                    if job_id in set_data_id:
                        continue
                    set_data_id.add(job_id)
                    print(f"Job ID: {job_id}")
                    
                    check_sql = """
                        SELECT ss.skill_set
                        FROM skill_sets ss
                        JOIN skill_set_mapping ssm ON ss.id = ssm.skill_id
                        WHERE ssm.job_id = %s
                    """
                    cursor.execute(check_sql, [job_id])   
                    skills = cursor.fetchall()
                    # skills = [skill[0] for skill in cursor.fetchall()]
                    
                    row = [str(item) if isinstance(item, bytes) else item for item in row]
                    skills = [str(skill) if isinstance(skill, bytes) else skill for skill in skills]
                    
                    cursor.execute("SELECT company_details.company_logo FROM company_details join job_post on company_details.id = job_post.company_id WHERE job_post.id = %s", [job_id])
                    logo_result = cursor.fetchone()
                    company_logo = logo_result[0]
                    company_logo = base64.b64encode(company_logo).decode('utf-8')
                    created_at = row[10]
                    created_at_humanized = naturaldelta(datetime.utcnow() - created_at)
                    
                    count+=1
                    
                    job = {
                        'id': row[0],
                        'job_title': row[1],
                        'company_name': row[2],
                        'employee_type': row[3],
                        'location': row[4],
                        'experience': row[5],
                        'salary_range': row[6],
                        'no_of_vacancies': row[7],
                        'company_logo': company_logo,
                        'job_role': row[9],
                        "skills": [skill[0] for skill in skills],
                        'created_at': created_at_humanized 
                    }
                    jobs.append(job) 
                    
                   
                print("COUNT :",count)
                
            
                return JsonResponse(jobs,safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

from django.db import connection

# f1 = "location = %s and experience = %s"


# list1 = ["Chennai","2-5 years"]
 
def execute_get_experience(f1,list1):
    print(f1," -----------")
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                j.id,
                j.job_title,
                c.company_name,
                et.employee_type,
                l.location,
                j.experience,
        ss.skill_set
                        j.salary_range,
                j.no_of_vacancies,
                c.company_logo,
                jr.job_role,
                j.created_at,
            FROM job_post j
            JOIN locations l ON j.location_id = l.id
            JOIN employees_types et ON j.employee_type_id = et.id
            JOIN job_role jr ON j.job_role_id = jr.id
            JOIN skill_set_mapping ssm ON j.id = ssm.job_id
            JOIN skill_sets ss ON ssm.skill_id = ss.id
            JOIN company_details c ON j.company_id = c.id  
            WHERE  
        """+ f1, list1)
          
        print("3 ----------- ")
        # """+ f1, tuple(list1))
        # Fetch the results
        rows = cursor.fetchall()
        
        # Process the results as needed
        return rows
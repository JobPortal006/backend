from django.db import connection


con = connection.cursor()
#    Post Job    -----------  Insert Query

def jobPost_insertQuery(job_title,job_description,employee_type,job_category,location,skill_set,qualification,experience,salary_range,no_of_vacancies):
    print("1 ----------------------------------")
    try: # --- insert with job_post table
        jobPost_sql = "INSERT INTO job_post(job_title,job_description,qualification,experience,salary_range,no_of_vacancies) VALUES(%s,%s,%s,%s,%s,%s)"
        jobPost_value = (job_title,job_description,qualification,experience,salary_range,no_of_vacancies)
        con.execute(jobPost_sql,jobPost_value)
        print("2 ----------------------------")
        
        
        con.execute("INSERT INTO employees_types(employee_type) VALUES(%s)",[employee_type])
        
        con.execute("INSERT INTO jobs_category(job_category) VALUES(%s)",[job_category])
        
        con.execute("INSERT INTO location(location) VALUES(%s)",[location])
        
        con.execute("INSERT INTO skill_set(skill_set) VALUES(%s)",[skill_set])
        
        # employeesType_sql = "INSERT INTO employees_types(employee_type) VALUES(%s)"
        # employeeType_values = (employee_type)
        # print(" -------------------------------------",employee_type)
        # con.execute(employeesType_sql,employeeType_values)  
        # print("3 -------------------")
        
        
        
        # jobsCategory_sql = "INSERT INTO jobs_category(job_category) values(%s)"
        # jobsCategory_values = [job_category]
        # con.execute(jobsCategory_sql,jobsCategory_values)
        
        # location_sql = "INSERT INTO location(location) values(%s)"
        # location_values = [location]
        # con.execute(location_sql,location_values)
        
        # skill_set_sql = "INSERT INTO skill_set(skill_set) values(%s)"
        # skill_set_values = [skill_set]
        # con.execute(skill_set_sql,skill_set_values)
        
        
        print("Hello ............................")
        
        return True
    except Exception as e:
        print(f"Error during Signup: {e}")
        return False
    

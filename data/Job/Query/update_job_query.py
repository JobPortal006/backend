from django.db import connection
from django.http import JsonResponse
import base64
from datetime import datetime
from humanize import naturaldelta
from data.Account_creation import message


con = connection.cursor()

def getId_companyDetails(job_id):
    try:
        con = connection.cursor()
        id_sql = "select employee_id from company_details where id =%s"
        id_value = [job_id]
        con.execute(id_sql,id_value)
        id = con.fetchone()
        
        for i in id:
            con.close()
            print("EMP: ",i)
            return i
        
    except:
        return False
    
    
    
def jobPost_updateQuery( job_title, job_description, qualification, experience, salary_range, no_of_vacancies,postJob_id):
    try:
        con = connection.cursor()
        
        update_sql = "UPDATE job_post set job_title=%s , job_description=%s, qualification=%s, experience=%s, salary_range=%s, no_of_vacancies=%s where id = %s "
        update_values = ( job_title, job_description, qualification, experience, salary_range, no_of_vacancies, postJob_id)
        con.execute(update_sql, update_values)
        con.close()
        print(" j i i  i i i")
        return True
    except Exception as e:
        con.close()
        return message.tryExceptError(str(e))  
    
def update_skillSet(skill_set,employee_id,postJob_id):
    try:
        con = connection.cursor()
        
        for i in skill_set:
            var = i
            con.execute("select id from skill_sets where skill_set = %s",[var])   
            result = con.fetchone()   
            
            if result:
                id = result[0]
                sql_2 = "select id from skill_set_mapping where job_id=%s and skill_id=%s"
                value_2 =[postJob_id,id]
                con.execute(sql_2,value_2)
                data = con.fetchone()
                if data:
                    print("Updated Mapping")
                else:
                    sql_3 = "insert into skill_set_mapping (skill_id,job_id) values(%s,%s)"
                    value_3 = (id,postJob_id)
                    con.execute(sql_3,value_3)
            else:
                con.execute("insert into skill_sets(skill_set) values(%s)",[var])
                con.execute("select id from skill_sets where skill_set = %s",[var])
                result = con.fetchone()  
                if result:
                    id = result[0]
                    
                    sql_3 = "insert into skill_set_mapping (skill_id,job_id) values(%s,%s)"
                    value_3 = (id,postJob_id)
                    con.execute(sql_3,value_3)
                    
        con.execute("select skill_id from skill_set_mapping where job_id = %s", [postJob_id])
        skill_id_mapping = con.fetchall()

        print("Loop 1")
        for row in skill_id_mapping:
            skill_id = row[0]
            b1 = False
            for deleting_id in skill_set:
                con.execute("select id from skill_sets where skill_set = %s",[deleting_id])
                deleting_id = con.fetchone()
                
                print("deleting_id:", deleting_id[0])
                if skill_id == deleting_id[0]:
                    print("count ")
                    b1 = True
                    break 
                
            if not b1:
                con.execute("DELETE FROM skill_set_mapping WHERE skill_id = %s", [skill_id])

        # Commit the changes to the d  database
        con.commit()
        con.close()
        return True    
                        
    except Exception as e:
        con.close()
        return message.tryExceptError(str(e))
    

def location_eType_jRole(location,employee_type,job_role,job_id):
    try:
        con = connection.cursor()
        #  Location ---  Table
        con.execute("select id from location where location = %s",[location])
        print("hello")
        res_id = con.fetchone()
        if res_id:
            loc_id = res_id[0]
        else:
            con.execute("insert into location(location) values(%s)",[location])
            loc_id = con.lastrowid
            
        print("employee_type :",employee_type)
        print("job_role : ",job_role)
        
        
        # Employee_Type ----->    Table
        
        con.execute("select id from employees_types where employee_type = %s",[employee_type])
        emp_id = con.fetchone()
        print("--------------> ",emp_id[0])
        print("emp_id :",emp_id[0])
        
        # Job_Role ---------->    Table
        con.execute("select id from job_role where job_role =%s",[job_role])
        value_id = con.fetchone()
        if value_id:
            jobR_id=value_id[0]
        else:
            con.execute("insert into job_role(job_role) values(%s)",[job_role])
            job_id = con.lastrowid
            
        print("job_id : ",job_id)  
        
        # Job_Post Table Updated Values   
        # sql = "update job_post set employee_type_id=%s, job_role_id=%s, location_id=%s where id=%s"
        # values = (emp_id[0],job_id,loc_id,job_id)
        # print(emp_id[0],job_id,loc_id,job_id)
        # con.execute(sql,values)
        
        con.execute("update job_post set employee_type_id=%s, job_role_id=%s, location_id=%s where id=%s",[emp_id[0],jobR_id,loc_id,job_id])
        print("Finish Upadted")
        con.close()
        return True
    except Exception as e:
        con.close()
        return message.tryExceptError(str(e))
    
def execute_join_jobPost(f1,list1): 
    try:
        print(f1," ----------->>>>>>>>>>>>>>>>>>>>")
        print("^^^^^^^^",list1)
        # f1 = "j.id = %s "
        # list1 = 1  

        with connection.cursor() as cursor:
        # Wrap list1 in a tuple when passing it as a parameter
            cursor.execute("""
                SELECT 
                    j.id,
                    j.job_title,
                    j.job_description,
                    j.qualification,
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
            """ + f1, tuple(list1))  # Note the comma after list1 to create a tuple with a single element
            print("3 ----------- 3")
            # Fetch the results
            rows = cursor.fetchone()
            
            # print("ROWSSS ---------> ",rows)
            
            if not rows:
                print("EMPTY")
            
            
            # Process the results as needed
            return rows
    except Exception as e:
       
        return message.tryExceptError(str(e))
    
def result_fun(results):    
    with connection.cursor() as cursor:
        print("RESULTS: ",results)
        try:
            jobs=[]
                
            if results:
                # for row in results:
                    print("Hii i  i")
                    job_id = results[0]
                    
                    print(f"Job ID: --------------> {job_id}")
                    
                    check_sql = """
                        SELECT ss.skill_set
                        FROM skill_sets ss 
                        JOIN skill_set_mapping ssm ON ss.id = ssm.skill_id
                        WHERE ssm.job_id = %s
                    """
                    cursor.execute(check_sql, [job_id])   
                    skills = cursor.fetchall()
                    print(" Skill ")
                    # skills = [skill[0] for skill in cursor.fetchall()]
                    
                    # row = [str(item) if isinstance(item, bytes) else item for item in row]
                    print("HII")
                    skills = [str(skill) if isinstance(skill, bytes) else skill for skill in skills]
                    print("Oiii")
                    
                    cursor.execute("SELECT company_details.company_logo FROM company_details join job_post on company_details.id = job_post.company_id WHERE job_post.id = %s", [job_id])
                    logo_result = cursor.fetchone()
                    company_logo = logo_result[0]
                    company_logo = base64.b64encode(company_logo).decode('utf-8')
                    created_at = results[12]
                    created_at_humanized = naturaldelta(datetime.utcnow() - created_at)
                    
                    job = {
                        'id': results[0],
                        'job_title': results[1],
                        'job_description':results[2],
                        'qualification':results[3],
                        'company_name': results[4],
                        'employee_type': results[5],
                        'location': results[6],
                        'experience': results[7],
                        'salary_range': results[8],
                        'no_of_vacancies': results[9],
                        # 'company_logo': company_logo,
                        'job_role': results[11],
                        "skills": [skill[0] for skill in skills],
                        'created_at': created_at_humanized  
                    }
                    jobs.append(job) 
            # print("RS:",jobs)
            return JsonResponse(jobs,safe=False)
        except Exception as e:
            con.close() 
            return JsonResponse({"error": str(e)})

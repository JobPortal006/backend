from django.db import connection

con = connection.cursor()

def jobPost_insertQuery(employee_id, company_id, job_title, job_description, qualification, experience, salary_range, no_of_vacancies, employee_type_id, job_category_id, location_id):
    try:
        # Print SQL query and parameters for debugging
        jobPost_sql = "INSERT INTO job_post (employee_id, company_id, job_title, job_description, qualification, experience, salary_range, no_of_vacancies, employee_type_id, job_category_id, location_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        jobPost_values = (employee_id, company_id, job_title, job_description, qualification, experience, salary_range, no_of_vacancies, employee_type_id, job_category_id, location_id)
        con.execute(jobPost_sql, jobPost_values)
        return True
    except Exception as e:
        print(f"Error during post a job: {e}")
        return False

    
def employee_type_insert(employee_type):
    con.execute("INSERT INTO employees_types (employee_type) VALUES (%s)", [employee_type])
    return True
    
def job_category_insert(job_category):
    con.execute("INSERT INTO job_category (job_category) VALUES (%s)", [job_category])
    return True

def location_insert(location):
    con.execute("INSERT INTO locations (location) VALUES (%s)", [location])
    return True

def job_category_id(job_category):
    check_sql = "SELECT id FROM job_category WHERE job_category = %s"
    con.execute(check_sql, [job_category])
    user = con.fetchone()
    if user:
        job_category_id = user[0]  
        print(f"job_category ID: {job_category_id}")
        return job_category_id
    
# def experience(job_id,company_id,experience):
#     try:
#         # Print SQL query and parameters for debugging
#         jobPost_sql = "INSERT INTO experience(job_id,company_id,experience) VALUES (%s, %s, %s)"
#         jobPost_values = (job_id,company_id,experience)
#         con.execute(jobPost_sql, jobPost_values)
#         return True
#     except Exception as e:
#         print(f"Error during post a job: {e}")
#         return False
    
def skill_set(skill_set):
    print(skill_set)
    check_sql = "SELECT id FROM skill_sets WHERE skill_set = %s"
    con.execute(check_sql, [skill_set])
    user = con.fetchone()
    print(user)
    if user != None:
        skill_id = user[0]  
        print(f"Skill ID: {skill_id}")
        return skill_id
    else:
        check_sql = "INSERT INTO skill_sets(skill_set) VALUES (%s)"
        con.execute(check_sql, [skill_set])
        user = con.fetchone()
        if user:
            skill_id = user[0]  
            print(f"Skill ID: {skill_id}")
            return skill_id

def skill_set_insert(employee_id,skill_id,job_id,company_id):
    jobPost_sql = "INSERT INTO skill_set_mapping(employee_id,skill_id,company_id,job_id) VALUES (%s, %s,%s, %s)"
    jobPost_values = (employee_id,skill_id,company_id,job_id)
    con.execute(jobPost_sql, jobPost_values)

def get_id(job_title):
    check_sql = "SELECT id FROM job_post WHERE job_title = %s"
    con.execute(check_sql, [job_title])
    user = con.fetchone()
    if user:
        job_id = user[0]  
        print(f"Job ID: {job_id}")
        return job_id  

def employee_id(company_name):
    check_sql = "SELECT employee_id FROM company_details WHERE company_name = %s"
    con.execute(check_sql, [company_name])
    user = con.fetchone()
    if user:
        employee_id = user[0]  
        print(f"Employee ID: {employee_id}")
        return employee_id
    
def company_id(company_name):
    check_sql = "SELECT id FROM company_details WHERE company_name = %s"
    con.execute(check_sql, [company_name])
    user = con.fetchone()
    if user:
        company_id = user[0]  
        print(f"Company ID: {company_id}")
        return company_id
    
def employee_type_id(employee_type):
    check_sql = "SELECT id FROM employees_types WHERE employee_type = %s";
    con.execute(check_sql, [employee_type])
    user = con.fetchone()
    if user:
        employee_type_id = user[0]  
        print(f"Employee Type ID: {employee_type_id}")
        return employee_type_id
    
def location_id(location):
    check_sql = "SELECT id FROM locations WHERE location = %s"
    con.execute(check_sql, [location])
    user = con.fetchone()
    if user:
        location_id = user[0]  
        print(f"Location ID: {location_id}")
        return location_id
    

# def location(job_id,company_id,location):
#     try:
#         # Print SQL query and parameters for debugging
#         jobPost_sql = "INSERT INTO locations(job_id,company_id,location) VALUES (%s, %s, %s)"
#         jobPost_values = (job_id,company_id,location)
#         con.execute(jobPost_sql, jobPost_values)
#         return True
#     except Exception as e:
#         print(f"Error during post a job: {e}")
#         return False
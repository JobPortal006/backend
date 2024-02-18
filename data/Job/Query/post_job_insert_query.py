from django.db import connection

con = connection.cursor()

# Insert the Job Post data into job_post table
def jobPost_insertQuery(employee_id, company_id, job_title, job_description, qualification, experience, salary_range, no_of_vacancies, employee_type_id, job_role_id, location_id):
    try:
        # Print SQL query and parameters for debugging
        jobPost_sql = "INSERT INTO job_post (employee_id, company_id, job_title, job_description, qualification, experience, salary_range, no_of_vacancies, employee_type_id, job_role_id, location_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        jobPost_values = (employee_id, company_id, job_title, job_description, qualification, experience, salary_range, no_of_vacancies, employee_type_id, job_role_id, location_id)
        con.execute(jobPost_sql, jobPost_values)
        return True
    except Exception as e:
        print(f"Error during post a job: {e}")
        return False

# Insert the employees_type data
# def employee_type_insert(employee_type):
#     con.execute("INSERT INTO employees_types (employee_type) VALUES (%s)", [employee_type])
#     return True

# Insert the job_role data 
# def job_role_insert(job_role):
#     con.execute("INSERT INTO job_role (job_role) VALUES (%s)", [job_role])
#     return True

# Insert the location data
# def location_insert(location):
#     con.execute("INSERT INTO locations (location) VALUES (%s)", [location])
#     return True

# Get the job_role_id using job_role value
# If job_role input is not present in the table, insert the job_role value into job_role table 
def job_role_id(job_role):
    check_sql = "SELECT id FROM job_role WHERE job_role = %s"
    con.execute(check_sql, [job_role])
    user = con.fetchone()
    if user:
        job_role_id = user[0]  
        print(f"job_role ID: {job_role_id}")
        return job_role_id
    else:
        check_sql = "INSERT INTO job_role (job_role) VALUES (%s)"
        con.execute(check_sql, [job_role])
        user = con.fetchone()
        if user:
            job_role_id = user[0]  
            print(f"job_role ID: {job_role_id}")
            return job_role_id
    
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
    
# Get the skill id using skill value
# If skill input is not present in the table, insert the skill value into skill_sets table 
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

# Insert skill_id int skill_set_mapping table
def skill_set_insert(employee_id,skill_id,job_id,company_id):
    jobPost_sql = "INSERT INTO skill_set_mapping(employee_id,skill_id,company_id,job_id) VALUES (%s, %s,%s, %s)"
    jobPost_values = (employee_id,skill_id,company_id,job_id)
    con.execute(jobPost_sql, jobPost_values)

# Get job_post id here
def get_id(job_title):
    check_sql = "SELECT id FROM job_post WHERE job_title = %s"
    con.execute(check_sql, [job_title])
    user = con.fetchone()
    if user:
        job_id = user[0]  
        print(f"Job ID: {job_id}")
        return job_id  

# Get employee_id here
def employee_id(company_name):
    check_sql = "SELECT employee_id FROM company_details WHERE company_name = %s"
    con.execute(check_sql, [company_name])
    user = con.fetchone()
    if user:
        employee_id = user[0]  
        print(f"Employee ID: {employee_id}")
        return employee_id
    
# Get company_id here
def company_id(company_name):
    check_sql = "SELECT id FROM company_details WHERE company_name = %s"
    con.execute(check_sql, [company_name])
    user = con.fetchone()
    if user:
        company_id = user[0]  
        print(f"Company ID: {company_id}")
        return company_id
    
# Get the employee_type_id using job_role value
# If employee_type input is not present in the table, insert the employee_type value into employees_types table 
def employee_type_id(employee_type):
    check_sql = "SELECT id FROM employees_types WHERE employee_type = %s";
    con.execute(check_sql, [employee_type])
    user = con.fetchone()
    if user != None:
        employee_type_id = user[0]  
        print(f"Employee Type ID: {employee_type_id}")  # Insert employee_type data in employee_types table
        return employee_type_id
    else:
        check_sql = "INSERT INTO employees_types (employee_type) VALUES (%s)" # After insert the employee_type, get that employee_type_id
        con.execute(check_sql, [employee_type])
        user = con.fetchone()
        if user:
            semployee_type_id = user[0]  
            print(f"Employee Type ID: {employee_type_id}")
            return employee_type_id
    
# Get the location_id using location value
# If location input is not present in the table, insert the location value into locations table 
def location_id(location):
    check_sql = "SELECT id FROM locations WHERE location = %s"
    con.execute(check_sql, [location])
    user = con.fetchone()
    if user:
        location_id = user[0]  
        print(f"Location ID: {location_id}")
        return location_id
    else:
        check_sql = "INSERT INTO locations (location) VALUES (%s)"
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
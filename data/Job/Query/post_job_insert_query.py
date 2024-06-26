from django.db import connection
con = connection.cursor()

# Insert the Job Post data into job_post table
def jobPost_insertQuery(employee_id, company_id, job_title, job_description, experience, salary_range, no_of_vacancies, employee_type_id, job_role_id, additional_queries):
    try:
        # Print SQL query and parameters for debugging
        jobPost_sql = "INSERT INTO job_post (employee_id, company_id, job_title, job_description, experience, salary_range, no_of_vacancies, employee_type_id, job_role_id, additional_queries) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        jobPost_values = (employee_id, company_id, job_title, job_description, experience, salary_range, no_of_vacancies, employee_type_id, job_role_id, additional_queries)
        con.execute(jobPost_sql, jobPost_values)
        # Fetch the last inserted ID
        con.execute("COMMIT")
        con.execute("SELECT LAST_INSERT_ID()")
        job_id = con.fetchone()[0]  # Fetch the first column of the first row
        print("Job ID", job_id)
        return True, job_id
    except Exception as e:
        print(f"Error during post a job: {e}")
        return False, None
    
# Get the employee_type_id using job_role value
# If employee_type input is not present in the table, insert the employee_type value into employees_types table 
def employee_type_id(employee_type):
    check_sql = "SELECT id FROM employees_types WHERE employee_type = %s"
    con.execute(check_sql, [employee_type])
    user = con.fetchone()
    if user:
        employee_type_id = user[0]  
        print(f"Employee Type ID: {employee_type_id}")  # Insert employee_type data in employee_types table
        return employee_type_id
    else:
        check_sql = "INSERT INTO employees_types (employee_type) VALUES (%s)" # After insert the employee_type, get that employee_type_id
        con.execute(check_sql, [employee_type])
        employee_type_id = con.lastrowid 
        print(f"Employee Type ID: {employee_type_id}")
        return employee_type_id
    
# Get the location_id using location value
# If location input is not present in the table, insert the location value into locations table 
def location_id(location):
    check_sql = "SELECT id FROM location WHERE location = %s"
    con.execute(check_sql, [location])
    existing_location = con.fetchone()
    if existing_location:
        location_id = existing_location[0]
        print(f"Location ID: {location_id}")
        return location_id
    else:
        insert_sql = "INSERT INTO location (location) VALUES (%s)"
        con.execute(insert_sql, [location])
        location_id = con.lastrowid
        print(f"Location ID: {location_id}")
        return location_id
    
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
        job_role_id = con.lastrowid 
        print(f"job_role ID: {job_role_id}")
        return job_role_id
    
# Get the skill id using skill value
# If skill input is not present in the table, insert the skill value into skill_sets table 
def skill_set(skill_set):
    print(skill_set)
    check_sql = "SELECT id FROM skill_sets WHERE skill_set = %s"
    con.execute(check_sql, [skill_set])
    user = con.fetchone()
    print(user)
    if user is not None:
        skill_id = user[0]  
        print(f"Skill ID: {skill_id}")
        return skill_id
    else:
        check_sql = "INSERT INTO skill_sets(skill_set) VALUES (%s)"
        con.execute(check_sql, [skill_set])
        con.execute("SELECT LAST_INSERT_ID()")
        user = con.fetchone()
        if user is not None:
            skill_id = user[0]  
            print(f"Skill ID: {skill_id}")
            return skill_id

# Insert skill_id int skill_set_mapping table
def skill_set_insert(employee_id,skill_id,job_id):
    jobPost_sql = "INSERT INTO skill_set_mapping(employee_id,skill_id,job_id) VALUES (%s, %s, %s)"
    jobPost_values = (employee_id,skill_id,job_id)
    con.execute(jobPost_sql, jobPost_values)

# Get the qualification id using qualification value
# If qualification input is not present in the table, insert the qualification value into qualification table 
def qualification(qualification):
    print(qualification)
    check_sql = "SELECT id FROM qualification WHERE qualification = %s"
    con.execute(check_sql, [qualification])
    user = con.fetchone()
    print(user)
    if user is not None:
        qualification_id = user[0]  
        print(f"qualification ID: {qualification_id}")
        return qualification_id
    else:
        check_sql = "INSERT INTO qualification(qualification) VALUES (%s)"
        con.execute(check_sql, [qualification])
        con.execute("SELECT LAST_INSERT_ID()")
        user = con.fetchone()
        if user is not None:
            qualification_id = user[0]  
            print(f"qualification ID: {qualification_id}")
            return qualification_id
        
# Insert qualification_id int qualification_mapping table
def qualification_insert(employee_id,qualification_id,job_id):
    jobPost_sql = "INSERT INTO qualification_mapping(employee_id,qualification_id,job_id) VALUES (%s, %s, %s)"
    jobPost_values = (employee_id,qualification_id,job_id)
    con.execute(jobPost_sql, jobPost_values)
        
# Get the qualification id using qualification value
# If qualification input is not present in the table, insert the qualification value into qualification table 
def location(location):
    print(location)
    check_sql = "SELECT id FROM location WHERE location = %s"
    con.execute(check_sql, [location])
    user = con.fetchone()
    print(user)
    if user is not None:
        location_id = user[0]  
        print(f"location ID: {location_id}")
        return location_id
    else:
        check_sql = "INSERT INTO location(location) VALUES (%s)"
        con.execute(check_sql, [location])
        con.execute("SELECT LAST_INSERT_ID()")
        user = con.fetchone()
        if user is not None:
            location_id = user[0]  
            print(f"location ID: {location_id}")
            return location_id
        
# Insert qualification_id int qualification_mapping table
def location_insert(employee_id,location_id,job_id):
    jobPost_sql = "INSERT INTO location_mapping(employee_id,location_id,job_id) VALUES (%s, %s, %s)"
    jobPost_values = (employee_id,location_id,job_id)
    con.execute(jobPost_sql, jobPost_values)

# Get job_post id here
def get_id(job_title):
    check_sql = "SELECT id FROM job_post WHERE job_title = %s"
    con.execute(check_sql, [job_title])
    con.execute("SELECT LAST_INSERT_ID()")
    user = con.fetchone()
    if user is not None:
        job_id = user[0]  
        print(f"Job ID: {job_id}")
        return job_id  

# Get employee_id here
def email_id(email):
    check_sql = "SELECT id FROM signup WHERE email = %s"
    val=con.execute(check_sql, [email])
    user = con.fetchone()
    if user is not None:
        employee_id = user[0]  
        print(f"Employee ID: {employee_id}")
        return employee_id
    
# Get company_id here
def company_id(employee_id):
    check_sql = "SELECT id FROM company_details WHERE employee_id = %s"
    con.execute(check_sql, [employee_id])
    user = con.fetchone()
    if user is not None:
        company_id = user[0]  
        print(f"Company ID: {company_id}")
        return company_id

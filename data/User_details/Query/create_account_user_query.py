from django.db import connection

con = connection.cursor()

#Get id in signup table using mobile number
def mobileNumber(mobile_number):
    check_sql = "SELECT id, signup_by, email FROM signup WHERE mobile_number = %s"
    con.execute(check_sql, [mobile_number])
    user = con.fetchone()
    if user:
        user_id, registered_by, email = user 
        print(f"User ID: {user_id}, Signup By: {registered_by}, Email: {email}")
        return user_id, registered_by, email
    else:
        return None, None, None

# Insert the data into personal_details table
def personal_details(user_id, registered_by, first_name, last_name, date_of_birth, gender, profile_picture):
    sql = "INSERT INTO personal_details (user_id, registered_by, first_name, last_name, date_of_birth, gender, profile_picture) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (user_id, registered_by, first_name, last_name, date_of_birth, gender, profile_picture)
    try:
        con.execute(sql, values)
        connection.commit()
        return True
    except Exception as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
        return False
    
# Insert the data into address table
def address_details(user_id,registered_by,street,city,state,country,pincode,address_type):
    sql = "INSERT INTO address (user_id,registered_by,street,city,state,country,pincode,address_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (user_id,registered_by,street,city,state,country,pincode,address_type)
    try:
        con.execute(sql, values)
        connection.commit()
        return True
    except Exception as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
        return False
    
# Insert the data into education_details table and college_details table
def education_details(user_id, sslc_school_name, sslc_start_year, sslc_end_year, sslc_percentage, hsc_school_name, 
    hsc_start_year, hsc_end_year, hsc_percentage, college_name, start_year, end_year,percentage, department, 
    degree, education_type,pg_college_name,pg_college_start_year,pg_college_end_year,pg_college_percentage,
    pg_college_department,pg_college_degree,diploma_college_name,diploma_college_start_year,
    diploma_college_end_year,diploma_college_percentage,diploma_college_department,diploma_college_degree):
    try:
        # Insert into education_details table
        education_sql = "INSERT INTO education_details (user_id, sslc_school_name, sslc_start_year, sslc_end_year, sslc_percentage, hsc_school_name, hsc_start_year, hsc_end_year, hsc_percentage) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        education_values = (user_id, sslc_school_name, sslc_start_year, sslc_end_year, sslc_percentage, hsc_school_name, hsc_start_year, hsc_end_year, hsc_percentage)
        con.execute(education_sql, education_values)
        # Insert into college_details table 
        # Check if pg_college_name or diploma_college_name are present in input,it store as education_type will change - PG or Diploma
        college_sql = "INSERT INTO college_details (user_id, college_name, start_year, end_year, percentage, department, degree, education_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        college_values = (user_id, college_name, start_year, end_year, percentage, department, degree, education_type)
        con.execute(college_sql, college_values)
        if pg_college_name != '' and pg_college_name != None:
          education_type='PG'
          college_sql = "INSERT INTO college_details (user_id, college_name, start_year, end_year, percentage, department, degree, education_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
          college_values = (user_id,pg_college_name,pg_college_start_year,pg_college_end_year,pg_college_percentage,pg_college_department,pg_college_degree,education_type)
          con.execute(college_sql, college_values)
        if diploma_college_name != '' and diploma_college_name != None:
          education_type='Diploma'
          college_sql = "INSERT INTO college_details (user_id, college_name, start_year, end_year, percentage, department, degree, education_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
          college_values = (user_id,diploma_college_name,diploma_college_start_year,diploma_college_end_year,
                diploma_college_percentage,diploma_college_department,diploma_college_degree,education_type)
          con.execute(college_sql, college_values)
        connection.commit()
        return True
    except Exception as e: 
        print(f"Error inserting data: {e}")
        connection.rollback()
        return False

# Insert the data into job_preference_details table
def job_preference_details(user_id,key_skills, department, industry, prefered_locations):
    sql = "INSERT INTO job_preferences (user_id,key_skills, department, industry, preferred_locations) VALUES (%s, %s, %s, %s, %s)"
    values = (user_id,key_skills, department, industry, prefered_locations)
    try:
        con.execute(sql, values)
        connection.commit()
        return True
    except Exception as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
        return False

# Insert the data into professional_details table
def professional_details(user_id, registered_by, company_name, years_of_experience, job_role, skills):
    sql = "INSERT INTO professional_details (user_id, registered_by, company_name, years_of_experience, job_role, skills) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (user_id, registered_by, company_name, years_of_experience, job_role, skills)
    try:
        con.execute(sql, values)
        connection.commit()
        return True
    except Exception as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
        return False
    
# Insert the data into resume_details table
def employment_status(user_id,registered_by,employment_status,resume):
    sql = "INSERT INTO resume_details (user_id,registered_by,employment_status,resume) VALUES (%s, %s, %s, %s)"
    values = (user_id,registered_by,employment_status,resume)
    try:
        con.execute(sql, values)
        connection.commit()
        return True
    except Exception as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
        return False
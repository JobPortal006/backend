from django.db import connection

con = connection.cursor()

#Get id in signup table using mobile number
def mobileNumber(mobile_number):
    check_sql = "SELECT id, signup_by FROM signup WHERE mobile_number = %s"
    con.execute(check_sql, [mobile_number])
    user = con.fetchone()
    if user:
        user_id, registered_by = user
        print(f"User ID: {user_id}, Signup By: {registered_by}")
        return user_id, registered_by
    else:
        return None, None

def personal_details(user_id, registered_by, first_name, last_name, date_of_birth, gender, profile_picture):
    sql = "INSERT INTO personal_details (user_id, registered_by, first_name, last_name, date_of_birth, gender, profile_picture) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (user_id, registered_by, first_name, last_name, date_of_birth, gender, profile_picture)

    try:
        con.execute(sql, values)
        # Commit the transaction
        connection.commit()
        return True
    except Exception as e:
        print(f"Error inserting data: {e}")
        # Rollback the transaction in case of an error
        connection.rollback()
        return False
    
def address_details(user_id,registered_by,street,city,state,country,pincode,address_type):
    sql = "INSERT INTO address (user_id,registered_by,street,city,state,country,pincode,address_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (user_id,registered_by,street,city,state,country,pincode,address_type)

    try:
        con.execute(sql, values)
        # Commit the transaction
        connection.commit()
        return True
    except Exception as e:
        print(f"Error inserting data: {e}")
        # Rollback the transaction in case of an error
        connection.rollback()
        return False
    
def education_details(user_id, sslc_school_name, sslc_start_year, sslc_end_year, sslc_percentage, hsc_school_name, 
                      hsc_start_year, hsc_end_year, hsc_percentage, college_name, start_year, end_year,
                      percentage, department, degree, education_type,pg_college_name,pg_college_start_year,pg_college_end_year,
                        pg_college_percentage,pg_college_department,pg_college_degree):
    try:
        # Insert into education_details table
        education_sql = "INSERT INTO education_details (user_id, sslc_school_name, sslc_start_year, sslc_end_year, sslc_percentage, hsc_school_name, hsc_start_year, hsc_end_year, hsc_percentage) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        education_values = (user_id, sslc_school_name, sslc_start_year, sslc_end_year, sslc_percentage, hsc_school_name, hsc_start_year, hsc_end_year, hsc_percentage)
        con.execute(education_sql, education_values)

        # Retrieve the education_id for the recently inserted record
        con.execute("SELECT LAST_INSERT_ID()")
        education_id = con.fetchone()[0]

        # Insert into college_details table with education_id as a foreign key
        college_sql = "INSERT INTO college_details (user_id, education_id, college_name, start_year, end_year, percentage, department, degree, education_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        college_values = (user_id, education_id, college_name, start_year, end_year, percentage, department, degree, education_type)
        con.execute(college_sql, college_values)
        if pg_college_name != '' and pg_college_name != None:
          education_type='PG'
          college_sql = "INSERT INTO college_details (user_id, education_id, college_name, start_year, end_year, percentage, department, degree, education_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
          college_values = (user_id,education_id,pg_college_name,pg_college_start_year,pg_college_end_year,pg_college_percentage,pg_college_department,pg_college_degree,education_type)
          con.execute(college_sql, college_values)
        # Commit the transaction
        connection.commit()
        return True
    except Exception as e: 
        print(f"Error inserting data: {e}")
        # Rollback the transaction in case of an error
        connection.rollback()
        return False

def job_preference_details(user_id,key_skills, department, industry, prefered_locations):
    sql = "INSERT INTO job_preferences (user_id,key_skills, department, industry, preferred_locations) VALUES (%s, %s, %s, %s, %s)"
    values = (user_id,key_skills, department, industry, prefered_locations)

    try:
        con.execute(sql, values)
        # Commit the transaction
        connection.commit()
        return True
    except Exception as e:
        print(f"Error inserting data: {e}")
        # Rollback the transaction in case of an error
        connection.rollback()
        return False

def professional_details(user_id, registered_by, company_name, years_of_experience, job_role, skills):
    sql = "INSERT INTO professional_details (user_id, registered_by, company_name, years_of_experience, job_role, skills) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (user_id, registered_by, company_name, years_of_experience, job_role, skills)

    try:
        con.execute(sql, values)
        # Commit the transaction
        connection.commit()
        return True
    except Exception as e:
        print(f"Error inserting data: {e}")
        # Rollback the transaction in case of an error
        connection.rollback()
        return False
    
def employment_status(user_id,registered_by,employment_status,resume):
    sql = "INSERT INTO resume_details (user_id,registered_by,employment_status,resume) VALUES (%s, %s, %s, %s)"
    values = (user_id,registered_by,employment_status,resume)
    try:
        con.execute(sql, values)
        # Commit the transaction
        connection.commit()
        return True
    except Exception as e:
        print(f"Error inserting data: {e}")
        # Rollback the transaction in case of an error
        connection.rollback()
        return False
from django.db import connection

con = connection.cursor()

# Insert the data into personal_details table
def company_details(user_id,company_logo_content,company_name,industry_type,company_description, no_of_employees,company_website_link,contact_person_name,contact_person_position,address_id,s3_key):
    sql = "INSERT INTO company_details(employee_id,company_logo,company_name,company_industry,company_description, no_of_employees,company_website_link,contact_person_name,contact_person_position,address_id,company_logo_path) VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s ,%s)"
    values = (user_id,company_logo_content,company_name,industry_type,company_description, no_of_employees,company_website_link,contact_person_name,contact_person_position,address_id,s3_key)
    try:
        con.execute(sql, values)
        connection.commit()
        return True
    except Exception as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
        return False
    
def userid_check(user_id):
    check_sql_company = "SELECT * FROM company_details WHERE employee_id = %s"
    query_company = con.execute(check_sql_company, [user_id])
    if query_company:
        return False
    else:
        return True
    
def get_id(user_id,registered_by):
    check_sql = "SELECT id FROM address WHERE user_id = %s and registered_by=%s"
    con.execute(check_sql, [user_id,registered_by])
    user = con.fetchone()
    if user:
        address_id = user[0]  
        print(f"Address ID: {address_id}")
        return address_id
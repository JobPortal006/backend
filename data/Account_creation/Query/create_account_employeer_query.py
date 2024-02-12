from django.db import connection

con = connection.cursor()

# Insert the data into personal_details table
def company_details(user_id,company_logo,company_name,industry_type,company_description, no_of_employees,company_website_link,contact_person_name,contact_person_position):
    sql = "INSERT INTO company_details(employee_id,company_logo,company_name,industry_type,company_description, no_of_employees,company_website_link,contact_person_name,contact_person_position) VALUES (%s, %s, %s, %s, %s, %s, %s, %s ,%s)"
    values = (user_id,company_logo,company_name,industry_type,company_description, no_of_employees,company_website_link,contact_person_name,contact_person_position)
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
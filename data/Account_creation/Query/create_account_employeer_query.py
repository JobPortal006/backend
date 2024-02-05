from django.db import connection

con = connection.cursor()

# Insert the data into personal_details table
def company_details(user_id,company_name, company_location, no_of_employees, industry, designation,company_logo):
    sql = "INSERT INTO company_details(employee_id,company_name, company_location, no_of_employees, industry, designation,company_logo) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (user_id,company_name, company_location, no_of_employees, industry, designation,company_logo)
    try:
        con.execute(sql, values)
        connection.commit()
        return True
    except Exception as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
        return False
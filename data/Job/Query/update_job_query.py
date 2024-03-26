from django.db import connection
from data import message

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
        return True
    except Exception as e:
        con.close()
        return message.tryExceptError(str(e))  
    
def update_maping_tables(values,postJob_id,table_name,field_name,mapping_table,mapping_id):
    try:
        con = connection.cursor()
        for var in values:
            con.execute(f"select id from {table_name} where {field_name} = %s",[var])   
            result = con.fetchone()   
            
            if result:
                id = result[0]
                sql_2 = f"select id from {mapping_table} where job_id=%s and {mapping_id}=%s"
                value_2 =[postJob_id,id]
                con.execute(sql_2,value_2)
                data = con.fetchone()
                if data:
                    print("Updated Mapping")
                else:
                    sql_3 = f"insert into {mapping_table} ({mapping_id},job_id) values(%s,%s)"
                    value_3 = (id,postJob_id)
                    con.execute(sql_3,value_3)
            else:
                con.execute(f"insert into {table_name} ({field_name}) values(%s)",[var])
                id = con.lastrowid
                sql_3 = f"insert into {mapping_table} ({mapping_id},job_id) values(%s,%s)"
                value_3 = (id,postJob_id)
                con.execute(sql_3,value_3)
        con.execute(f"select {mapping_id} from {mapping_table} where job_id = %s", [postJob_id])
        id_mapping = con.fetchall()
        for row in id_mapping:
            qualifications_id = row[0]
            b1 = False
            for deleting_id in values: # field name
                con.execute(f"select id from {table_name} where {field_name} = %s",[deleting_id])
                deleting_id = con.fetchone()
                if qualifications_id == deleting_id[0]:
                    b1 = True
                    break 
            if not b1:
                con.execute(f"DELETE FROM {mapping_table} WHERE {mapping_id} = %s", [qualifications_id])
        # Commit the changes to the d  database
        con.commit()
        con.close()
        return True            
    except Exception as e:
        con.close()
        return message.tryExceptError(str(e))
   
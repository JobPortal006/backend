from django.db import connection
from data import message

def delete_postJob(job_id):
   try:
      con = connection.cursor()
      con.execute("select id,employee_type_id,job_role_id from job_post where id = %s", [job_id])
      job_result = con.fetchone()

      job_id, employee_type_id, job_role_id = job_result
      print(job_id, employee_type_id, job_role_id)

      con.execute("select id,skill_id from skill_set_mapping where job_id=%s", [job_id])  
      final_result = con.fetchall()
      print(final_result)  

      if final_result is None or final_result == '':
         print("Id does not contain job list")
      else:
         for i, skill_id in final_result:
            con.execute("delete from skill_set_mapping where id = %s", [i])
            print("Deleting skill set", i)

            # Use skill_id here
            con.execute("SELECT COUNT(*) FROM skill_set_mapping WHERE skill_id = %s", (skill_id,))
            count = con.fetchone()[0]
            if count == 0:
               con.execute("DELETE FROM skill_sets WHERE id = %s", (skill_id,)) 
      
      con.execute("select id,qualification_id from qualification_mapping where job_id=%s", [job_id])  
      final_result = con.fetchall()
      print(final_result)
      
      if final_result is None or final_result == '':
         print("Id does not contain job list")
      else:
         for i, qualification_id in final_result:
            con.execute("delete from qualification_mapping where id = %s", [i])
            print("Deleting qualification", i)

            # Use qualification_id here
            con.execute("SELECT COUNT(*) FROM qualification_mapping WHERE qualification_id = %s", (qualification_id,))
            count = con.fetchone()[0]
            if count == 0:
               con.execute("DELETE FROM qualification WHERE id = %s", (qualification_id,))

      con.execute("select id,location_id from location_mapping where job_id=%s", [job_id])  
      final_result = con.fetchall()
      print(final_result)
      
      if final_result is None or final_result == '':
         print("Id does not contain job list")
      else:
         for i, location_id in final_result:
            con.execute("delete from location_mapping where id = %s", [i])
            print("Deleting location", i)
  
            # Use skill_id here
            con.execute("SELECT COUNT(*) FROM location_mapping WHERE location_id = %s", (location_id,))
            count = con.fetchone()[0]
            if count == 0:
               con.execute("DELETE FROM location WHERE id = %s", (location_id,))
      
      result = con.execute("DELETE FROM job_post WHERE id = %s", [job_id])

      if result == 1:
         con.execute("SELECT COUNT(*) FROM job_post WHERE employee_type_id = %s", (employee_type_id,))
         count = con.fetchone()[0]
         if count == 0:
            con.execute("DELETE FROM employees_types WHERE id = %s", (employee_type_id,))

         con.execute("SELECT COUNT(*) FROM job_post WHERE job_role_id = %s", (job_role_id,))
         count = con.fetchone()[0]
         if count == 0:
            con.execute("DELETE FROM job_role WHERE id = %s", (job_role_id,))
      con.close()
      return result
   except Exception as e:
      print(f"The Error is: {str(e)}")
      return message.tryExceptError(str(e))

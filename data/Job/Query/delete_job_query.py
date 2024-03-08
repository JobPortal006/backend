from django.db import connection
from django.http import JsonResponse
from data import message

def delete_postJob(job_id):
   try:
      con = connection.cursor()
      con.execute("select id,employee_type_id,job_role_id,location_id from job_post where id = %s", [job_id])
      job_id, employee_type_id, job_role_id, location_id = con.fetchone()
      print(job_id, employee_type_id, job_role_id, location_id)
      con.execute("select id,skill_id from skill_set_mapping where job_id=%s", [job_id])  
      final_result = con.fetchall()
      print(final_result)  
      if not final_result:
         return JsonResponse("Id does not contain job list", safe=False)
      
      for i, skill_id in final_result:
         con.execute("delete from skill_set_mapping where id = %s", [i])
         print("Deleting", i)
      
      result = con.execute("DELETE FROM job_post WHERE id = %s", [job_id])

      # Check if any rows were deleted
      if result.rowcount > 0:
         con.execute("SELECT COUNT(*) FROM job_post WHERE employee_type_id = %s", (employee_type_id,))
         count = con.fetchone()[0]
         if count == 0:
            con.execute("DELETE FROM employees_types WHERE id = %s", (employee_type_id,))

         con.execute("SELECT COUNT(*) FROM job_post WHERE job_role_id = %s", (job_role_id,))
         count = con.fetchone()[0]
         if count == 0:
            con.execute("DELETE FROM job_role WHERE id = %s", (job_role_id,))

         con.execute("SELECT COUNT(*) FROM job_post WHERE location_id = %s", (location_id,))
         count = con.fetchone()[0]
         if count == 0:
            con.execute("DELETE FROM location WHERE id = %s", (location_id,))

         con.execute("SELECT COUNT(*) FROM skill_set_mapping WHERE skill_id = %s", (skill_id,))
         count = con.fetchone()[0]
         if count == 0:
            con.execute("DELETE FROM skill_sets WHERE id = %s", (skill_id,))
         
         con.close()
         return JsonResponse("Job successfully deleted", safe=False)
         
   except Exception as e:
      print(f"The Error is: {str(e)}")
      return message.tryExceptError(str(e))

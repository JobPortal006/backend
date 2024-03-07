from django.db import connection
from django.http import JsonResponse


def delete_postJob(id):
    try:
        con = connection.cursor()
        con.execute("select id,employee_type_id,job_role_id,location_id from job_post where id = %s",[id])
        id_check,employee_type_id,job_role_id,location_id = con.fetchone()
        print(id_check,employee_type_id,job_role_id,location_id)
        
        if id_check is None:
            return False
             
        con.execute("select id from skill_set_mapping where job_id=%s",[id])    
        final_result = con.fetchall()
        
        for i in final_result:
            if not i:
                 return JsonResponse("Id is not contain job list",safe=False)
                
            # con.execute("delete from skill_set_mapping where id = %s",[i])
            print("Deleting",i)
        # result = con.execute("DELETE FROM job_post WHERE id = %s", [id])
        # if result:
        #     con.close()
        #     return True
            
    except:
        return JsonResponse("Query Problem",safe=False)
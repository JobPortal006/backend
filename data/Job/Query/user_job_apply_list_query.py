from django.db import connection
from django.http import JsonResponse
from data import message

def applyJob_datas(job_id):
    try:
        con = connection.cursor()
        id_sql = "SELECT user_id FROM apply_job WHERE job_id = %s"
        id_value = [job_id]
        con.execute(id_sql, id_value)
        id_results = con.fetchall()
        user_ids = [user_id[0] for user_id in id_results]
        return user_ids
    except Exception as e:
        return message.tryExceptError(str(e))
    
def additional_query(job_id, user_id):
    try:
        con = connection.cursor()
        query = "SELECT total_experience, current_ctc, expected_ctc, notice_period FROM additional_queries WHERE job_id = %s AND user_id = %s"
        params = (job_id, user_id)
        con.execute(query, params)
        result = con.fetchone()
        # Check if result is empty, if so return None
        if not result:
            return None,None,None,None
        # Unpack the fetched row
        total_experience, current_ctc, expected_ctc, notice_period = result
        return total_experience, current_ctc, expected_ctc, notice_period
    except Exception as e:
        return message.tryExceptError(str(e))
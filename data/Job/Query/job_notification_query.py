from django.db import connection
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.http import JsonResponse

def send_email(email):
    for i in email:    
        subject = 'Job match for your profile'
        message_html = "Check and apply for job "
        message_plain = strip_tags(message_html)
        from_email = 'brochill547@gmail.com'
        recipient_list = [i]
        send_mail(subject, message_plain, from_email, recipient_list, html_message=message_html)

def get_emails(user_id):
    con = connection.cursor()
    user_email = []
    for i in user_id:
        con.execute("select email from signup where id =%s",[i]) 
        rs = con.fetchall()
        user_email.append(list(rs))
    final_list = [item for sublist in user_email for item in sublist]
    con.close()
    email_list = [email[0] for email in final_list]
    return email_list
     
def query_function(locations,table_name,column_name,job_preferences):
    con = connection.cursor()
    skill_id = []
    loction_user = []
    for i in locations:
        con.execute(f"select id from {table_name} where {column_name} = %s",[i])
        result = con.fetchall()
        skill_id.append(list(result[0]))
    single_list = [item for sublist in skill_id for item in sublist]
    
    for i in single_list:
        con.execute(f"select user_id  from job_preferences where FIND_IN_SET(%s, {job_preferences})",[i]) 
        rs = con.fetchall()
        loction_user.append(list(rs))
    final_list = [item for sublist in loction_user for item in sublist]
    con.close()
    return final_list


def notification_tab(result_list,job_id):
    try:
        con = connection.cursor()
        print("< ------ >",result_list)
        for i in result_list:
            con.execute("SELECT COUNT(*) AS row_count FROM job_notification WHERE user_id = %s",[i])
            count = con.fetchone()
            print(i , "count" ,  count[0])
            if count[0] >= 20 :
                print("delete ", i)
                con.execute("DELETE FROM job_notification WHERE user_id = %s ORDER BY created_at ASC LIMIT 1",[i])
                print(" YES")
            query = "INSERT INTO job_notification (user_id, job_id) VALUES (%s, %s)"
            values = (i, job_id)
            con.execute(query, values)     
        con.close()    
            
    except Exception as e:
        print(f"Exception: {str(e)}")
        JsonResponse(f"Exception: {str(e)}",safe=False)
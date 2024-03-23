from django.db import connection
con = connection.cursor()

def get_ids(user_id):
  check_sql = "SELECT key_skills,proferred_locations FROM job_preferences WHERE user_id = %s"
  con.execute(check_sql, [user_id])
  user = con.fetchone()
  if user:
    key_skills = user[0]
    proferred_locations = user[1] 
    print(key_skills,proferred_locations)
    return key_skills,proferred_locations
  
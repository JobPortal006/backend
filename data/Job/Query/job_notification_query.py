from django.db import connection
from data import message
from sqlalchemy import and_, or_
from data.Job.Query import search_jobs_query
from data.Job import json_response
from data.Account_creation.Tables.table import SkillSetMapping, LocationMapping, JobPost

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
  
def get_matching_jobs(skill_ids, location_ids):
    session = message.create_session()
    try:
        # Query jobs that match any of the user's skills or preferred locations
        set_data_id = set()
        conditions = or_(
            SkillSetMapping.skill_id.in_(skill_ids),
            LocationMapping.location_id.in_(location_ids)
        )
        result = search_jobs_query.execute_query(conditions)
        jobs=json_response.job_response_details(result,set_data_id)
        return jobs
    except Exception as e:
        print(f"Error in get_matching_jobs: {e}")
        return [] 
    finally:
        session.close()
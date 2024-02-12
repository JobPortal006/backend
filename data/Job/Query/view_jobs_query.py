from django.db import connection

con = connection.cursor()

def location(location_name):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('GetJobsByLocation', [location_name])
            results = cursor.fetchall()
            return results
    except Exception as e:
        print(f"Error: {e}")
        return False
    
def experience(experience):
    try:
         with connection.cursor() as cursor:
            cursor.callproc('GetJobsByExperience', [experience])
            results = cursor.fetchall()
            return results
    except Exception as e:
        print(f"Error: {e}")
        return False

def skill(skill,job_title):
    try:
         with connection.cursor() as cursor:
            cursor.callproc('GetJobsBySkillAndTitle', [skill,job_title])
            results = cursor.fetchall()
            print(results)
            return results
    except Exception as e:
        print(f"Error: {e}")
        return False
    
def skill_check(skill):
    check_sql = "SELECT ss.skill_set FROM skill_set_mapping sm JOIN job_post j ON sm.job_id = j.id JOIN company_details c ON j.company_id = c.id JOIN skill_sets ss ON sm.skill_id = ss.id WHERE ss.skill_set = %s"
    con.execute(check_sql, [skill])
    user = con.fetchone()
    if user:
        skill = user[0]  
        print(f"Skill: {skill}")
        return skill
    
def job_title(skill):
    check_sql = "SELECT j.job_title FROM job_post j JOIN company_details c ON j.company_id = c.id WHERE j.job_title = %s"
    con.execute(check_sql, [skill])  
    user = con.fetchone()
    if user:
        job_title = user[0]  
        print(f"Job Title: {job_title}")
        return job_title
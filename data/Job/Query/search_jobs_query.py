from sqlalchemy.orm import sessionmaker
from django.db import connection
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import declarative_base
import os
from data.Account_creation.Tables.table import SkillSets, Location, JobPost, CompanyDetails, EmployeeTypes, JobRole, SkillSetMapping, LocationMapping
con = connection.cursor()
Base = declarative_base()

# Use the appropriate database connection string
# engine = create_engine('mysql://root:mysqllocal@localhost:3306/jobportal')
engine = create_engine('mysql://theuser:thepassword@13.51.66.252:3306/jobportal')

Base.metadata.create_all(engine)

def execute_query(conditions):
    try:
        print('Condition--------->',conditions)
        Session = sessionmaker(bind=engine)
        session = Session()
        # Joining tables
        query = session.query(
            JobPost.id,
            JobPost.job_title,
            JobPost.job_description,
            CompanyDetails.company_name,
            EmployeeTypes.employee_type,
            JobPost.experience,
            JobPost.salary_range,
            JobPost.no_of_vacancies,
            CompanyDetails.company_logo_path,
            JobRole.job_role,
            JobPost.created_at
        )\
        .join(LocationMapping, JobPost.id == LocationMapping.job_id)\
        .join(Location, LocationMapping.location_id == Location.id)\
        .join(EmployeeTypes, JobPost.employee_type_id == EmployeeTypes.id)\
        .join(JobRole, JobPost.job_role_id == JobRole.id)\
        .join(SkillSetMapping, JobPost.id == SkillSetMapping.job_id)\
        .join(SkillSets, SkillSetMapping.skill_id == SkillSets.id)\
        .join(CompanyDetails, JobPost.company_id == CompanyDetails.id)
        # Applying filter conditions
        if conditions is not None:
            query = query.filter(conditions)
        # Execute the query
        result = query.all()
        return result
    except Exception as e:
        # manage_py_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'manage.py')
        # os.utime(manage_py_path, None)
        print(f"Error during job search: {e}")
        return None
    
def skill_check(skill):
    check_sql = "select ss.skill_set from skill_sets ss join skill_set_mapping ssm on ssm.skill_id = ss.id where ss.skill_set = %s"
    con.execute(check_sql, [skill])
    user = con.fetchone()
    if user:
        skill = user[0]  
        print(f"Skill: {skill}")
        return skill
    else:
        return None  
    
def job_title(skill):
    check_sql = "SELECT job_title FROM job_post WHERE job_title = %s"
    con.execute(check_sql, [skill])  
    user = con.fetchone()
    if user:
        job_title = user[0]  
        print(f"Job Title: {job_title}")
        return job_title
    else:
        return None
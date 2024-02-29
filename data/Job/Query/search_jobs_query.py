from sqlalchemy.orm import sessionmaker
from django.db import connection
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import declarative_base
from data.Account_creation.Tables.table import SkillSets, Location, JobPost, CompanyDetails, EmployeeTypes, JobRole, SkillSetMapping
con = connection.cursor()
Base = declarative_base()

# Use the appropriate database connection string
# engine = create_engine('mysql://root:mysqllocal@localhost:3306/backend')
engine = create_engine('mysql://theuser:thepassword@13.51.207.189:3306/backend1')

Base.metadata.create_all(engine)

def execute_query(conditions):
    try:
        print(conditions,'condition--------->')
        Session = sessionmaker(bind=engine)
        session = Session()
        # Joining tables
        query = session.query(
            JobPost.id,
            JobPost.job_title,
            CompanyDetails.company_name,
            EmployeeTypes.employee_type,
            Location.location,
            JobPost.experience,
            JobPost.salary_range,
            JobPost.no_of_vacancies,
            CompanyDetails.company_logo,
            JobRole.job_role,
            JobPost.created_at,
            SkillSets.skill_set
        )\
            .join(Location, JobPost.location_id == Location.id)\
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
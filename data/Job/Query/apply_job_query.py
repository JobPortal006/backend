from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from django.http import JsonResponse
from data.Account_creation.Tables.table import Signup, ResumeDetails
from sqlalchemy.orm import declarative_base
from django.views.decorators.csrf import csrf_exempt
import base64
from django.db import connection

Base = declarative_base()
con = connection.cursor()
@csrf_exempt
def get_user_details(user_id):
    try:
        engine = create_engine('mysql://theuser:thepassword@16.171.137.133:3306/backend1')
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        user = session.query(Signup).filter_by(id=user_id).first()
        resume = session.query(ResumeDetails).filter_by(user_id=user_id).first()
        resume_base64 = base64.b64encode(resume.resume).decode('utf-8')
        response_data = {
                'email': user.email,
                'mobile_number': user.mobile_number,
                'resume': resume_base64 
        }
        return response_data

    except Exception as e:
        print(f"Error: {e}")
        return {'status': 'Error', 'message': str(e)}

def insert_apply_job(user_id,job_id,company_id,resume_id):
    try:
        engine = create_engine('mysql://theuser:thepassword@16.171.137.133:3306/backend1')
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()
        sql = "INSERT INTO signup(email,mobile_number,password,signup_by) VALUES(%s,%s,%s,%s)"
        value = (user_id,job_id,company_id,resume_id)
        con.execute(sql,value)
    except Exception as e:
        print(f"Error: {e}")
        return {'status': 'Error', 'message': str(e)}
    
# Get the employee_type_id using job_role value
# If employee_type input is not present in the table, insert the employee_type value into resume table 
def resume_id(resume):
    check_sql = "SELECT id FROM resume WHERE resume = %s"
    con.execute(check_sql, [resume])
    user = con.fetchone()
    if user:
        resume_id = user[0]  
        print(f"Resume ID: {resume_id}")  # Insert resume data in resumes table
        return resume_id
    else:
        check_sql = "INSERT INTO resume (resume) VALUES (%s)" # After insert the resume, get that resume_id
        con.execute(check_sql, [resume])
        resume_id = con.lastrowid 
        print(f"Resume ID: {resume_id}")
        return resume_id
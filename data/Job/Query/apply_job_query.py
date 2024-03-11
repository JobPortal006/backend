from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from django.http import JsonResponse
from data.Account_creation.Tables.table import Signup, ResumeDetails, JobPost
from sqlalchemy.orm import declarative_base
from django.views.decorators.csrf import csrf_exempt
import base64
from django.db import connection

Base = declarative_base()
con = connection.cursor()
@csrf_exempt
def get_user_details(user_id,job_id):
    try:
        engine = create_engine('mysql://theuser:thepassword@13.51.66.252:3306/backend')
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        user = session.query(Signup).filter_by(id=user_id).first()
        resume = session.query(ResumeDetails).filter_by(user_id=user_id).first()
        job_post = session.query(JobPost).filter_by(id=job_id).first()
        additional_queries = job_post.additional_queries
        response_data = {
            'user_id': user.id,
            'email': user.email,
            'mobile_number': user.mobile_number,
            'resume_path': resume.resume_path,
            'additional_queries': additional_queries
        }
        return response_data

    except Exception as e:
        print(f"Error: {e}")
        return {'status': 'Error', 'message': str(e)}

def insert_apply_job(user_id,job_id,company_id,resume_id):
    try:
        engine = create_engine('mysql://theuser:thepassword@13.51.66.252:3306/backend')
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
    
def user_expectation_table(job_id,user_id,current_ctc,expected_ctc,total_experience,notice_period):
    try:
        con = connection.cursor()    
        sql ="insert into user_expectation (job_id,user_id,total_experience,current_ctc,expected_ctc,notice_period) values(%s,%s,%s,%s,%s,%s)"
        values = (job_id,user_id,current_ctc,expected_ctc,total_experience,notice_period)
        check_val = con.execute(sql,values)
        last_id = con.lastrowid
        if check_val:
            con.execute("SELECT * FROM user_expectation WHERE id = %s", [last_id])    
            results = con.fetchone()
            user_exp = []  # Initialize user_exp as a list
            if results:
                additional_information = {
                    'id': results[0],
                    'job_id': results[1],
                    'user_id': results[2],
                    'current_ctc': results[3],
                    'expected_ctc': results[4],
                    'total_experience': results[5],
                    'notice_period': results[6],
                }
                user_exp.append(additional_information) 
            con.close()    
            return user_exp
    except Exception as e:
            return JsonResponse(str(e),safe=False)
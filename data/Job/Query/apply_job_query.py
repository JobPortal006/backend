from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from django.http import JsonResponse
from data.Account_creation.Tables.table import Signup, ResumeDetails, JobPost
from sqlalchemy.orm import declarative_base
from django.views.decorators.csrf import csrf_exempt
from data.Job import json_response
from django.db import connection
from data import message

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
def get_resume_id(resume,user_id):
    check_sql = "SELECT id FROM resume_details WHERE resume_path = %s"
    con.execute(check_sql, [resume])
    user = con.fetchone()
    if user:
        resume_id = user[0]  
        print(f"Resume ID: {resume_id}")  # Insert resume data in resumes table
        return resume_id
    else:
        check_sql = "INSERT INTO resume_details (user_id,resume_path) VALUES (%s,%s)" # After insert the resume, get that resume_id
        con.execute(check_sql, [user_id,resume])
        resume_id = con.lastrowid 
        print(f"Resume ID: {resume_id}")
        return resume_id
    
def apply_job_table(job_id, user_id, resume_id):
    try:
        con = connection.cursor()

        # Check if the entry already exists
        check_sql = "SELECT * FROM apply_job WHERE job_id = %s AND user_id = %s"
        check_values = (job_id, user_id)
        con.execute(check_sql, check_values)
        existing_entry = con.fetchone()

        if existing_entry:
            return False
        else:
            # Entry does not exist, insert the data
            insert_sql = "INSERT INTO apply_job (job_id, user_id, resume_id) VALUES (%s, %s, %s)"
            insert_values = (job_id, user_id, resume_id)
            con.execute(insert_sql, insert_values)
            return True
    except Exception as e:
        return JsonResponse(str(e), safe=False)
    finally:
        con.close()
    
def additional_queries_table(job_id,user_id,current_ctc,expected_ctc,total_experience,notice_period):
    try:
        con = connection.cursor()    
        sql ="insert into additional_queries (job_id,user_id,total_experience,current_ctc,expected_ctc,notice_period) values(%s,%s,%s,%s,%s,%s)"
        values = (job_id,user_id,current_ctc,expected_ctc,total_experience,notice_period)
        check_val = con.execute(sql,values)
        # last_id = con.lastrowid
        # if check_val:
        #     con.execute("SELECT * FROM additional_queries WHERE id = %s", [last_id])    
        #     results = con.fetchone()
        #     user_exp = []  # Initialize user_exp as a list
        #     if results:
        #         additional_information = {
        #             'id': results[0],
        #             'job_id': results[1],
        #             'user_id': results[2],
        #             'current_ctc': results[3],
        #             'expected_ctc': results[4],
        #             'total_experience': results[5],
        #             'notice_period': results[6],
        #         }
        #         user_exp.append(additional_information) 
        #     con.close()    
        #     return user_exp
        return True
    except Exception as e:
            return JsonResponse(str(e),safe=False)
    

# Send a job details data in JSON format 
# Data is send in response as (Data/Month/Year)
def view_apply_jobs(user_id, processed_job_ids):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('GetApplyJobDetails', [user_id])
            results = cursor.fetchall()
            if results is not None:
                for row in results:
                    job_id = row[0]
                    if job_id in processed_job_ids:
                        continue
                    processed_job_ids.add(job_id)
                    result=json_response.response(results,job_id,cursor,processed_job_ids)
                    # print(result)
                return result
            else:
                print("No results found")
                return None
    except Exception as e:
        print(f"Error: {e}")
        return False

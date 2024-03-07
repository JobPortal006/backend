from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from data.Account_creation.Tables.table import Signup,PersonalDetails,ProfessionalDetails,Address,CollegeDetails,EducationDetails,JobPreferences,ResumeDetails
from sqlalchemy.orm import declarative_base
import json
import base64
from backend.data import message

Base = declarative_base()
job_response = ""
@csrf_exempt
def get_user_details(request):
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        print(user_id)
        # engine = create_engine('mysql://theuser:thepassword@13.51.66.252:3306/backend1')
        # Base.metadata.create_all(engine)
        # Session = sessionmaker(bind=engine) 
        # session = Session()
        # Call create_session to get a session object
        session = message.create_session()
        user_details_data=user_details(session,user_id)
        global job_response
        job_response = user_details_data
        session.close()
        return JsonResponse(user_details_data)
    except Exception as e:
        print(str(e))
        return JsonResponse({"error": "Failed"})


@csrf_exempt
def get_user_details_view(request):
    try:
        url_response=job_response
        # print(url_response)
        if url_response is not None and url_response != '':
            # return message.response1('Success', 'getJobDetails', url_response)
            return JsonResponse(url_response)
        else:
            return message.response1('Error', 'searchJobError', data={})  
    except Exception as e:
        print(f"The Error is: {str(e)}")
        return message.serverErrorResponse()
    
def user_details(session,user_id):
    user_details = {}
    signup_details = session.query(Signup).filter_by(id=user_id).first()
    if signup_details:
        user_details['Signup'] = { 
            'email': signup_details.email,
            'mobile_number': signup_details.mobile_number
        }
    # print(user_details,'1-----------')
    personal_details = session.query(PersonalDetails).filter_by(user_id=user_id).first()
    if personal_details:
        profile_picture = personal_details.profile_picture
        profile_picture_base64 = base64.b64encode(profile_picture).decode('utf-8') if profile_picture else None
        # profile_picture_path = get_employeer_account.get_company_logo_from_s3(str(f'profile_picture/{user_id}_company_logo.jpg'))

        user_details['userDetails'] = {
            'date_of_birth': personal_details.date_of_birth.strftime('%Y-%m-%d'),
            'first_name': personal_details.first_name,
            'gender': personal_details.gender,
            'last_name': personal_details.last_name,
            'profile_picture_path': personal_details.profile_picture_path,
            'profile_picture': profile_picture_base64,
        }
    # print(user_details,'2-------------')
    address_details = session.query(Address).filter_by(user_id=user_id).all()
    user_details['address'] = {}
    for address in address_details:
        user_details['address'][address.address_type.lower()] = {
            'address_type': address.address_type,
            'city': address.city,
            'country': address.country,
            'pincode': address.pincode,
            'state': address.state,
            'street': address.street,
        }
    # print(user_details,'3-------------')

    education_details = session.query(EducationDetails).filter_by(user_id=user_id).first()
    if education_details:
        user_details['education_details'] = {
            'hsc_start_year': education_details.hsc_start_year,
            'hsc_end_year': education_details.hsc_end_year,
            'hsc_percentage': education_details.hsc_percentage,
            'hsc_school_name': education_details.hsc_school_name,
            'sslc_end_year': education_details.sslc_end_year,
            'sslc_percentage': education_details.sslc_percentage,
            'sslc_school_name': education_details.sslc_school_name,
            'sslc_start_year': education_details.sslc_start_year,
        }
    # print(user_details,'4-------------')
    college_details = session.query(CollegeDetails).filter_by(user_id=user_id, education_type='UG').first()
    if college_details:
        user_details['college_details'] = {
            'college_end_year': college_details.end_year,
            'college_name': college_details.college_name,
            'college_percentage': college_details.percentage,
            'college_start_year': college_details.start_year,
            'degree': college_details.degree,
            'department': college_details.department,
            'education_type': college_details.education_type,
        }

        # Initialize PG_college_details and Diploma_college_details as dictionaries
        user_details['PG_college_details'] = {}
        user_details['Diploma_college_details'] = {}

        # Include PG and Diploma details only for 'UG' education type
        pg_college_details = session.query(CollegeDetails).filter_by(user_id=user_id, education_type='PG').first()
        if pg_college_details:
            user_details['PG_college_details'].update({
                'pg_college_degree': pg_college_details.degree,
                'pg_college_department': pg_college_details.department,
                'pg_college_end_year': pg_college_details.end_year,
                'pg_college_name': pg_college_details.college_name,
                'pg_college_percentage': pg_college_details.percentage,
                'pg_college_start_year': pg_college_details.start_year,
                'pg_college_education_type': pg_college_details.education_type
            })

        diploma_college_details = session.query(CollegeDetails).filter_by(user_id=user_id, education_type='Diploma').first()
        if diploma_college_details:
            user_details['Diploma_college_details'].update({
                'diploma_college_degree': diploma_college_details.degree,
                'diploma_college_department': diploma_college_details.department,
                'diploma_college_end_year': diploma_college_details.end_year,
                'diploma_college_name': diploma_college_details.college_name,
                'diploma_college_percentage': diploma_college_details.percentage,
                'diploma_college_start_year': diploma_college_details.start_year,
                'diploma_college_education_type': diploma_college_details.education_type
            })

    # print(user_details, '5-------------')
    job_preferences = session.query(JobPreferences).filter_by(user_id=user_id).first()
    if job_preferences:
        user_details['jobPreference'] = {
            'department': job_preferences.department,
            'industry': job_preferences.industry,
            'key_skills': job_preferences.key_skills,
            'prefered_locations': job_preferences.preferred_locations,
        }
    # print(user_details,'6-------------')
    professional_details = session.query(ProfessionalDetails).filter_by(user_id=user_id).all()
    user_details['professionalDetails'] = {
        'companies': [],
        'numberOfCompanies': str(len(professional_details)),
    }
    # print(user_details,'7-------------')
    for prof_detail in professional_details:
        user_details['professionalDetails']['companies'].append({
            'company_name': prof_detail.company_name,
            'years_of_experience': prof_detail.years_of_experience,
            'job_role': prof_detail.job_role,
            'skills': prof_detail.skills,
        })
    # print(user_details,'8-------------')
    resume_details = session.query(ResumeDetails).filter_by(user_id=user_id).first()
    if resume_details:
        resume = personal_details.profile_picture
        resume_base64 = base64.b64encode(resume).decode('utf-8') if resume else None
        user_details['resume'] = {
            'resume':resume_base64,
            'resume_path':resume_details.resume_path
        }
    # print(user_details,'9-------------')
    return user_details
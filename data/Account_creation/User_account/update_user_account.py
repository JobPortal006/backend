# update_user_details.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from data.Account_creation.Tables.table import Signup, PersonalDetails, ProfessionalDetails, Address, CollegeDetails, EducationDetails, JobPreferences, ResumeDetails
import json
import base64
from data.Account_creation.Query import create_account_user_query
from data.Account_creation import message
from sqlalchemy.orm import declarative_base

Base = declarative_base()

@csrf_exempt
def update_user_details(request):
    try:
        data = json.loads(request.body)
        updated_data = data
        print(updated_data)
        email=updated_data['data']['Signup']['email']
        user_id, registered_by , email= create_account_user_query.user_check(email)
        print(user_id, registered_by, email)
        engine = create_engine('mysql://theuser:thepassword@51.20.54.231:3306/backend1')

        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine) 
        session = Session()
        # Update Signup table
        signup_details = session.query(Signup).filter_by(id=user_id).first()
        if signup_details:
            signup_details.email = updated_data['data']['Signup']['email']
            signup_details.mobile_number = updated_data['data']['Signup']['mobile_number']

        # Update PersonalDetails table
        personal_details = session.query(PersonalDetails).filter_by(user_id=user_id).first()
        if personal_details:
            personal_details.date_of_birth = updated_data['data']['userDetails']['date_of_birth']
            personal_details.first_name = updated_data['data']['userDetails']['first_name']
            personal_details.gender = updated_data['data']['userDetails']['gender']
            personal_details.last_name = updated_data['data']['userDetails']['last_name']

        # Update Address table
        address_details = session.query(Address).filter_by(user_id=user_id).all()
        for address in address_details:
            updated_address = updated_data['data']['address'].get(address.address_type.lower())
            if updated_address:
                address.city = updated_address['city']
                address.country = updated_address['country']
                address.pincode = updated_address['pincode']
                address.state = updated_address['state']
                address.street = updated_address['street']

        # # Update EducationDetails table
        # education_details = session.query(EducationDetails).filter_by(user_id=user_id).first()
        # if education_details:
        #     education_details.hsc_end_year = updated_data['data']['education_details']['hsc_end_year']
        #     education_details.hsc_percentage = updated_data['data']['education_details']['hsc_percentage']
        #     education_details.hsc_school_name = updated_data['data']['education_details']['hsc_school_name']
        #     education_details.sslc_end_year = updated_data['data']['education_details']['sslc_end_year']
        #     education_details.sslc_percentage = updated_data['data']['education_details']['sslc_percentage']
        #     education_details.sslc_school_name = updated_data['data']['education_details']['sslc_school_name']
        #     education_details.sslc_start_year = updated_data['data']['education_details']['sslc_start_year']

        # # Update CollegeDetails table for UG education type
        # college_details_ug = session.query(CollegeDetails).filter_by(user_id=user_id, education_type='UG').first()
        # if college_details_ug:
        #     college_details_ug.end_year = updated_data['data']['college_details']['college_end_year']
        #     college_details_ug.college_name = updated_data['data']['college_details']['college_name']
        #     college_details_ug.percentage = updated_data['data']['college_details']['college_percentage']
        #     college_details_ug.start_year = updated_data['data']['college_details']['college_start_year']
        #     college_details_ug.degree = updated_data['data']['college_details']['degree'] 
        #     college_details_ug.department = updated_data['data']['college_details']['department']

        # # Update CollegeDetails table for PG education type
        # college_details_pg = session.query(CollegeDetails).filter_by(user_id=user_id, education_type='PG').first()
        # if college_details_pg:
        #     college_details_pg.degree = updated_data['data']['PG_college_details']['pg_college_degree']
        #     college_details_pg.department = updated_data['data']['PG_college_details']['pg_college_department']
        #     college_details_pg.end_year = updated_data['data']['PG_college_details']['pg_college_end_year']
        #     college_details_pg.college_name = updated_data['data']['PG_college_details']['pg_college_name']
        #     college_details_pg.percentage = updated_data['data']['PG_college_details']['pg_college_percentage']
        #     college_details_pg.start_year = updated_data['data']['PG_college_details']['pg_college_start_year']
        #     college_details_pg.education_type = updated_data['data']['PG_college_details']['pg_college_education_type']

        # # Update CollegeDetails table for Diploma education type
        # college_details_diploma = session.query(CollegeDetails).filter_by(user_id=user_id, education_type='Diploma').first()
        # if college_details_diploma:
        #     college_details_diploma.degree = updated_data['data']['Diploma_college_details']['diploma_college_degree']
        #     college_details_diploma.department = updated_data['data']['Diploma_college_details']['diploma_college_department']
        #     college_details_diploma.end_year = updated_data['data']['Diploma_college_details']['diploma_college_end_year']
        #     college_details_diploma.college_name = updated_data['data']['Diploma_college_details']['diploma_college_name']
        #     college_details_diploma.percentage = updated_data['data']['Diploma_college_details']['diploma_college_percentage']
        #     college_details_diploma.start_year = updated_data['data']['Diploma_college_details']['diploma_college_start_year']
        #     college_details_diploma.education_type = updated_data['data']['Diploma_college_details']['diploma_college_education_type']

        # # Update JobPreferences table
        # job_preferences = session.query(JobPreferences).filter_by(user_id=user_id).first()
        # if job_preferences:
        #     job_preferences.department = updated_data['data']['jobPreference']['department']
        #     job_preferences.industry = updated_data['data']['jobPreference']['industry']
        #     job_preferences.key_skills = updated_data['data']['jobPreference']['key_skills']
        #     job_preferences.preferred_locations = updated_data['data']['jobPreference']['prefered_locations']

        # # Update ProfessionalDetails table
        # professional_details = session.query(ProfessionalDetails).filter_by(user_id=user_id).all()
        # for i, prof_detail in enumerate(professional_details):
        #     prof_detail.company_name = updated_data['data']['professionalDetails']['companies'][i]['company_name']
        #     prof_detail.years_of_experience = updated_data['data']['professionalDetails']['companies'][i]['years_of_experience']
        #     prof_detail.job_role = updated_data['data']['professionalDetails']['companies'][i]['job_role']
        #     prof_detail.skills = updated_data['data']['professionalDetails']['companies'][i]['skills']

        session.commit()
        session.close()
        
        return JsonResponse({"message": "Data updated successfully"})
    except Exception as e:
        print(str(e))
        return JsonResponse({"error": "Failed to update data"})

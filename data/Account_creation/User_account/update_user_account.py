from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from data.Account_creation.Tables.table import Signup, PersonalDetails, ProfessionalDetails, Address, CollegeDetails, EducationDetails, JobPreferences, ResumeDetails
import json
import base64
import io
import boto3
from data.Account_creation.Query import create_account_user_query
from data.Account_creation import message
from data.Account_creation.Employeer_account import get_employeer_account
from sqlalchemy.orm import declarative_base

Base = declarative_base()

@csrf_exempt
def update_user_details(request):
    try:
        # data = json.loads(request.body)
        # print(data)
        # user_details = data.get('data', {}).get('userDetails', {})
        # address_data = data.get('data', {}).get('address', {})
        # education_data = data.get('data', {}).get('education_details', {})
        # job_preference_data = data.get('data', {}).get('jobPreference', {})
        user_details = json.loads(request.POST.get('userDetails', '{}'))
        print(user_details)
        address_data = json.loads(request.POST.get('address', '{}'))
        print(address_data)
        education_data = json.loads(request.POST.get('education', '{}'))
        print(education_data)
        job_preference_data = json.loads(request.POST.get('jobPreference', '{}'))
        print(job_preference_data)
        professional_details_data = json.loads(request.POST.get('professionalDetails'))
        print(professional_details_data)

        # Extracting user details
        first_name = user_details.get('first_name')
        last_name = user_details.get('last_name')
        gender = user_details.get('gender')
        date_of_birth = user_details.get('date_of_birth')
        mobile_number = user_details.get('mobile_number')
        profile_picture = request.FILES.get('profilePicture')
        profile_picture_name=profile_picture.name
        profile_picture = profile_picture.read()
        resume = request.FILES.get("resume")
        resume_name=resume.name
        resume = resume.read()

        # Extracting current address details
        current_address = address_data.get('current', {})
        street_current = current_address.get('street')
        city_current = current_address.get('city')
        state_current = current_address.get('state')
        country_current = current_address.get('country')
        pincode_current = current_address.get('pincode')
        # address_type_current = current_address.get('address_type')

        # Extracting permanent address details
        permanent_address = address_data.get('permanent', {})
        street_permanent = permanent_address.get('street')
        city_permanent = permanent_address.get('city')
        state_permanent = permanent_address.get('state')
        country_permanent = permanent_address.get('country')
        pincode_permanent = permanent_address.get('pincode')
        # address_type_permanent = permanent_address.get('address_type')

        # Extracting education details
        sslc_school_name = education_data.get('sslc_school_name')
        sslc_start_year = education_data.get('sslc_start_year')
        sslc_end_year = education_data.get('sslc_end_year')
        sslc_percentage = education_data.get('sslc_percentage')
        hsc_school_name = education_data.get('hsc_school_name')
        hsc_start_year = education_data.get('hsc_start_year')
        hsc_end_year = education_data.get('hsc_end_year')
        hsc_percentage = education_data.get('hsc_percentage')
        college_name = education_data.get('college_name')
        college_start_year = education_data.get('college_start_year')
        college_end_year = education_data.get('college_end_year')
        college_percentage = education_data.get('college_percentage')
        department = education_data.get('department')
        degree = education_data.get('degree')
        # education_type = education_data.get('education_type')
        pg_college_degree = education_data.get("pg_college_degree")
        pg_college_department = education_data.get("pg_college_department")
        pg_college_end_year = education_data.get("pg_college_end_year")
        pg_college_name = education_data.get("pg_college_name")
        pg_college_percentage = education_data.get("pg_college_percentage")
        pg_college_start_year = education_data.get("pg_college_start_year")
        diploma_college_name = education_data.get("diploma_college_name")
        diploma_college_start_year = education_data.get("diploma_college_start_year")
        diploma_college_end_year = education_data.get("diploma_college_end_year")
        diploma_college_percentage = education_data.get("diploma_college_percentage")
        diploma_college_department = education_data.get("diploma_college_department")
        diploma_college_degree = education_data.get("diploma_college_degree")

        # Extracting job preference details
        department = job_preference_data.get('department')
        industry = job_preference_data.get('industry')
        key_skills = job_preference_data.get('key_skills')
        prefered_locations = job_preference_data.get('preferred_locations')

        # Extracting professional details
        # professional_details_list = professional_details_data.get("companies", [])
        employment_status = professional_details_data
        print(employment_status,'employment_status-------')
        if professional_details_data is None:
            professional_details_data = json.loads(request.POST.get('professionalDetails', '{}'))
            isExperienced = professional_details_data.get('isExperienced')
            print(isExperienced)
        else:
            employment_status = "Experienced"
            professional_details_data = json.loads(request.POST.get('professionalDetails', '{}'))
            companies = professional_details_data.get('companies', [])
            # number_of_companies = professional_details_data.get('numberOfCompanies', 0)


        # Fetching user ID
        user_id, registered_by, mobile_number = create_account_user_query.mobile_number(mobile_number)
        print(user_id, registered_by, mobile_number)

        # Creating SQLAlchemy engine and session
        engine = create_engine('mysql://theuser:thepassword@16.171.154.253:3306/backend1')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        s3 = boto3.client('s3', aws_access_key_id='AKIAZI2LB2XIRFQPYDJ4', aws_secret_access_key='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', region_name='eu-north-1')
        # Update PersonalDetails table
        profile_picture_key = f'profile_picture/{user_id}_{profile_picture_name}'
        s3.upload_fileobj(io.BytesIO(profile_picture), 'backendcompanylogo', profile_picture_key)
        update_personal_details(session, user_id, date_of_birth, first_name, gender, last_name,profile_picture, profile_picture_key)

        # Update Address table for current address
        update_address(session, user_id, 'Current', city_current, country_current, pincode_current, state_current,
                       street_current)

        # Update Address table for permanent address
        update_address(session, user_id, 'Permanent', city_permanent, country_permanent, pincode_permanent,
                       state_permanent, street_permanent)

        # Update EducationDetails table
        update_education_details(session, user_id, sslc_end_year, sslc_percentage, sslc_school_name, sslc_start_year,
                                 hsc_end_year, hsc_percentage, hsc_school_name, hsc_start_year)

        # Update CollegeDetails table for UG education type
        update_college_details(session, user_id, 'UG', college_end_year, college_name, college_percentage,
                               college_start_year, degree, department)

        # Update CollegeDetails table for PG education type
        update_college_details(session, user_id, 'PG', pg_college_end_year, pg_college_name, pg_college_percentage,
                               pg_college_start_year, pg_college_degree, pg_college_department)

        # Update CollegeDetails table for Diploma education type
        update_college_details(session, user_id, 'Diploma', diploma_college_end_year, diploma_college_name,
                               diploma_college_percentage, diploma_college_start_year, diploma_college_degree,
                               diploma_college_department)

        # Update JobPreferences table
        update_job_preferences(session, user_id, department, industry, key_skills, prefered_locations)
        
        # Delete existing professional details for the user
        delete_existing_professional_details(session, user_id)

        # Update ProfessionalDetails table
        update_professional_details(session, user_id, companies)


        # Update ProfessionalDetails table
        # def update_professional_details(session, user_id,company_name,years_of_experience,job_role,skills):
    #     professional_details = session.query(ProfessionalDetails).filter_by(user_id=user_id).all()
    #         for i, prof_detail in enumerate(professional_details):
    #             if i < len(professional_details_list):
    #                 company = professional_details_list[i]
    #                 prof_detail.company_name = company.get('company_name')
    #                 prof_detail.years_of_experience = company.get('years_of_experience')
    #                 prof_detail.job_role = company.get('job_role')
    #                 prof_detail.skills = company.get('skills')
        # update_professional_details(session, user_id,company_name,years_of_experience,job_role,skills)
            
        # Update resemeDetails table
        resume_key = f'resume/{user_id}_{resume_name}'
        s3.upload_fileobj(io.BytesIO(resume), 'backendcompanylogo', resume_key)
        update_resume_details(session, user_id, employment_status, resume, resume_key)

        session.commit()
        session.close()

        return JsonResponse({"message": "Data updated successfully"})
    except Exception as e:
        print(str(e))
        return JsonResponse({"error": "Failed to update data"})


def update_personal_details(session, user_id, date_of_birth, first_name, gender, last_name, profile_picture_path):
    personal_details = session.query(PersonalDetails).filter_by(user_id=user_id).first()
    if personal_details:
        personal_details.date_of_birth = date_of_birth
        personal_details.first_name = first_name
        personal_details.gender = gender
        personal_details.last_name = last_name
        personal_details.profile_picture_path = profile_picture_path


def update_address(session, user_id, address_type, city, country, pincode, state, street):
    address_obj = session.query(Address).filter_by(user_id=user_id, address_type=address_type).first()
    if address_obj:
        address_obj.city = city
        address_obj.country = country
        address_obj.pincode = pincode
        address_obj.state = state
        address_obj.street = street
    else:
        new_address = Address(user_id=user_id, address_type=address_type, city=city, country=country, pincode=pincode,
                              state=state, street=street)
        session.add(new_address)


def update_college_details(session, user_id, education_type, end_year, college_name, percentage, start_year, degree, department):
    college_details = session.query(CollegeDetails).filter_by(user_id=user_id, education_type=education_type).first()
    if college_details:
        college_details.end_year = end_year
        college_details.college_name = college_name
        college_details.percentage = percentage
        college_details.start_year = start_year
        college_details.degree = degree
        college_details.department = department


def update_education_details(session, user_id, sslc_end_year, sslc_percentage, sslc_school_name, sslc_start_year,
                             hsc_end_year, hsc_percentage, hsc_school_name, hsc_start_year):
    education_details = session.query(EducationDetails).filter_by(user_id=user_id).first()
    if education_details:
        education_details.hsc_end_year = hsc_end_year
        education_details.hsc_start_year = hsc_start_year
        education_details.hsc_percentage = hsc_percentage
        education_details.hsc_school_name = hsc_school_name
        education_details.sslc_end_year = sslc_end_year
        education_details.sslc_percentage = sslc_percentage
        education_details.sslc_school_name = sslc_school_name
        education_details.sslc_start_year = sslc_start_year


def update_job_preferences(session, user_id, department, industry, key_skills, preferred_locations):
    job_preferences = session.query(JobPreferences).filter_by(user_id=user_id).first()
    if job_preferences:
        job_preferences.department = department
        job_preferences.industry = industry
        job_preferences.key_skills = key_skills
        job_preferences.preferred_locations = preferred_locations

def delete_existing_professional_details(session, user_id):
    professional_details = session.query(ProfessionalDetails).filter_by(user_id=user_id).all()
    for prof_detail in professional_details:
        session.delete(prof_detail)

def update_professional_details(session, user_id, companies):
    for company in companies:
        prof_detail = ProfessionalDetails(
            user_id=user_id,
            company_name=company.get('company_name'),
            years_of_experience=company.get('years_of_experience'),
            job_role=company.get('job_role'),
            skills=company.get('skills')
        )
        session.add(prof_detail)

def update_resume_details(session, user_id, employment_status, resume, resume_path):
    resume_details = session.query(ResumeDetails).filter_by(user_id=user_id).first()
    if resume_details:
        resume_details.employment_status = employment_status
        resume_details.resume = resume
        resume_details.resume_path = resume_path

def upload_logo_to_s3(company_logo, company_logo_name, user_id,existing_logo_key):
    s3 = boto3.client('s3', aws_access_key_id='AKIAZI2LB2XIRFQPYDJ4', aws_secret_access_key='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', region_name='eu-north-1')
    new_logo_key = f'profile_picture/{user_id}_{company_logo_name}'

    # Check if the new logo key is different from the existing one
    if existing_logo_key != new_logo_key:
        s3.upload_fileobj(io.BytesIO(company_logo), 'backendcompanylogo', new_logo_key)
        if existing_logo_key:
            s3.delete_object(Bucket='backendcompanylogo', Key=existing_logo_key)
            print(f"Existing object with key '{existing_logo_key}' deleted from S3.")
    return new_logo_key
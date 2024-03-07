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
from data.Account_creation.User_account import get_user_account
from sqlalchemy.orm import declarative_base


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
        college_details.education_type = education_type
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

def update_resume_details(session, user_id, employment_status, resume_path):
    resume_details = session.query(ResumeDetails).filter_by(user_id=user_id).first()
    if resume_details:
        resume_details.employment_status = employment_status
        resume_details.resume_path = resume_path

def get_profile_picture_path(session,user_id):
    personal_details = session.query(PersonalDetails).filter_by(user_id=user_id).first()
    profile_picture_key=personal_details.profile_picture_path 
    if profile_picture_key:
        return profile_picture_key
    else:
        return None

def upload_profile_picture_file(profile_picture, profile_picture_name, user_id,existing_profile_picture_key):
    s3 = boto3.client('s3', aws_access_key_id='AKIAZI2LB2XIRFQPYDJ4', aws_secret_access_key='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', region_name='eu-north-1')
    new_logo_key = f'profile_picture/{user_id}_{profile_picture_name}'

    # Check if the new logo key is different from the existing one
    if existing_profile_picture_key != new_logo_key:
        s3.upload_fileobj(io.BytesIO(profile_picture), 'backendcompanylogo', new_logo_key)
        # if existing_profile_picture_key is None:
        #     s3.delete_object(Bucket='backendcompanylogo', Key=existing_profile_picture_key)
        #     print(f"Existing object with key '{existing_profile_picture_key}' deleted from S3.")
    return new_logo_key

def upload_profile_picture_path(company_logo,existing_logo_key):
    print('path-----------')
    new_logo_key = company_logo 
    return new_logo_key

def get_resume_path(session,user_id):
    resume_details = session.query(ResumeDetails).filter_by(user_id=user_id).first()
    resume_key=resume_details.resume_path 
    if resume_key:
        return resume_key
    else:
        return None

def upload_resume_file(resume, resume_name, user_id,existing_resume_key):
    s3 = boto3.client('s3', aws_access_key_id='AKIAZI2LB2XIRFQPYDJ4', aws_secret_access_key='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', region_name='eu-north-1')
    new_logo_key = f'resume/{user_id}_{resume_name}'
    print(new_logo_key,'new_logo_key-----------')
    # Check if the new logo key is different from the existing one
    if existing_resume_key != new_logo_key:
        print('1-------------')
        s3.upload_fileobj(io.BytesIO(resume), 'backendcompanylogo', new_logo_key)
        # if existing_resume_key is None:
        #     s3.delete_object(Bucket='backendcompanylogo', Key=existing_resume_key)
        #     print(f"Existing object with key '{existing_resume_key}' deleted from S3.")
    return new_logo_key

def upload_resume_path(resume_path,existing_logo_key):
    print('path-----------')
    new_logo_key = resume_path 
    return new_logo_key
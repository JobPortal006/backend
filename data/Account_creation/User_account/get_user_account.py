from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from data.Tables.table import Signup,PersonalDetails,ProfessionalDetails,Address,CollegeDetails,EducationDetails,JobPreferences,ResumeDetails,SkillSets,Location
import json
from data import message
from data.token import decode_token
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
private_key = RSA.generate(2048)
public_key = private_key.publickey()

job_response = ""

@csrf_exempt
def get_user_details(request):
    try:
        user_details_data = None
        data = json.loads(request.body)
        token = data.get('token')
        user_id, registered_by, email = decode_token(token)
        print(user_id, registered_by, email)
        
        if user_id is not None:
            session = message.create_session()
            user_details_data = user_details(user_id)
            global job_response
            job_response = user_details_data
            session.close()
            
            if user_details_data is not None:
                return message.response1('Success', 'getJobDetails', user_details_data)
                # return JsonResponse(user_details_data)
            else:
                return message.response1('Error', 'searchJobError', data={})
        else:
            return message.response('Error', 'tokenError')
    except json.JSONDecodeError:
        return message.response('Error', 'invalidJSON')
    except Exception as e:
        print(f"The Error is: {str(e)}")
        return message.tryExceptError(str(e))

@csrf_exempt
def get_user_details_view(request):
    try:
        # url_response= ""
        # if job_response is not None and job_response != '':
        url_response=job_response
        if url_response is not None and url_response != '':
            # return message.response1('Success', 'getJobDetails', url_response)
            return JsonResponse(url_response)
        else:
            return message.response1('Error', 'searchJobError', data={})  
    except Exception as e:
        print(f"The Error is: {str(e)}")
        return message.tryExceptError(str(e))
    
def user_details(user_id):  
    session = message.create_session()
    user_details = {}
    signup_details = session.query(Signup).filter_by(id=user_id).first()
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_email = base64.b64encode(cipher.encrypt(signup_details.email.encode())).decode()
    if signup_details:
        user_details['Signup'] = { 
            'email': signup_details.email,
            'mobile_number': signup_details.mobile_number,
            # 'encrypted_email': encrypted_email
        }
    personal_details = session.query(PersonalDetails).filter_by(user_id=user_id).first()
    if personal_details is not None:
        user_details['userDetails'] = {
            'date_of_birth': personal_details.date_of_birth.strftime('%Y-%m-%d'),
            'first_name': personal_details.first_name,
            'gender': personal_details.gender, 
            'last_name': personal_details.last_name,
            'profile_picture_path': personal_details.profile_picture_path
        }
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
        # Initialize PG_college_details and Diploma_college_details as dictionaries
        user_details['college_details'] = {}
        user_details['PG_college_details'] = {}
        user_details['Diploma_college_details'] = {}
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
        job_preferences = session.query(JobPreferences).filter_by(user_id=user_id).first()
        if job_preferences:
            skill_details_list = []
            key_skills = job_preferences.key_skills
            skill_ids = key_skills.split(",")
            for skill_id in skill_ids:
                skill_details = session.query(SkillSets).filter_by(id=skill_id).first()
                if skill_details:
                    skill_details_list.append(str(skill_details.skill_set))
            key_skills = ",".join(skill_details_list)
            prefered_locations_list = []
            prefered_locations = job_preferences.preferred_locations
            location_ids = prefered_locations.split(",")
            for location_id in location_ids:
                location_details = session.query(Location).filter_by(id=location_id).first()
                if location_details:
                    prefered_locations_list.append(str(location_details.location))
            prefered_locations = ",".join(prefered_locations_list)
            user_details['jobPreference'] = {
                'department': job_preferences.department,
                'industry': job_preferences.industry,
                # 'key_skills': job_preferences.key_skills,
                # 'prefered_locations': job_preferences.preferred_locations,
                'key_skills': skill_details_list,
                'prefered_locations': prefered_locations_list
            }
        professional_details = session.query(ProfessionalDetails).filter_by(user_id=user_id).all()
        user_details['professionalDetails'] = {
            'companies': [],
            'numberOfCompanies': str(len(professional_details)),
        }
        for prof_detail in professional_details:
            user_details['professionalDetails']['companies'].append({
                'company_name': prof_detail.company_name,
                'years_of_experience': prof_detail.years_of_experience,
                'job_role': prof_detail.job_role,
                'skills': prof_detail.skills,
            })
        resume_details = session.query(ResumeDetails).filter_by(user_id=user_id).first()
        if resume_details:
            user_details['resume'] = {
                'resume_path':resume_details.resume_path,
                'employment_status':resume_details.employment_status
            }
        return user_details
    else:
        return None
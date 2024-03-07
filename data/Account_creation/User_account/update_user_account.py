from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from data.Account_creation.Tables.table import Signup, PersonalDetails, ProfessionalDetails, Address, CollegeDetails, EducationDetails, JobPreferences, ResumeDetails
import json
import base64
import io
import boto3
# from data.Account_creation.User_account.Query.update_user_account_query import update_address,update_college_details,update_education_details,update_job_preferences,update_personal_details,update_professional_details,update_resume_details,upload_profile_picture,delete_existing_professional_details,get_profile_picture_path,get_resume_path,upload_resume
from data.Account_creation.User_account.Query import update_user_account_query
from data.Account_creation.Query import create_account_user_query
from data.Account_creation.message import create_session
from data.Account_creation.User_account import get_user_account
# from sqlalchemy.orm import declarative_base

# Base = declarative_base()

@csrf_exempt
def update_user_details(request):
    try:
        # data = json.loads(request.body)
        # print(data)
        # user_details = data.get('data', {}).get('userDetails', {})
        # address_data = data.get('data', {}).get('address', {})
        # education_data = data.get('data', {}).get('education_details', {})
        # job_preference_data = data.get('data', {}).get('jobPreference', {})
        # professional_details_data = data.get('data', {}).get('professionalDetails', {})
        user_details = json.loads(request.POST.get('userDetails', '{}'))
        signup_data = json.loads(request.POST.get('Signup', '{}'))
        address_data = json.loads(request.POST.get('address', '{}'))
        education_data = json.loads(request.POST.get('education_details', '{}'))
        college_data = json.loads(request.POST.get('college_details','{}'))
        pg_college__data = json.loads(request.POST.get('PG_college_details','{}'))
        diploma_college_data = json.loads(request.POST.get('Diploma_college_details','{}'))
        job_preference_data = json.loads(request.POST.get('jobPreference', '{}'))
        professional_details_data = json.loads(request.POST.get('professionalDetails'))
        resume_data = json.loads(request.POST.get('resume', '{"resume_path": null}'))
        # Extracting user details
        print(user_details)
        print(address_data)
        print(education_data)
        print(college_data)
        print(pg_college__data)
        print(diploma_college_data)
        print(job_preference_data)
        print(professional_details_data)
        print(resume_data,'r------')
        first_name = user_details.get('first_name')
        last_name = user_details.get('last_name')
        gender = user_details.get('gender')
        date_of_birth = user_details.get('date_of_birth')
        mobile_number = signup_data.get('mobile_number')
        # profile_picture_path = request.FILES.get("profile_picture_path")
        # print(profile_picture_path,'profile_picture_path')
        # if profile_picture_path is None:
        #     profile_picture_path = request.POST.get('profile_picture_path')
        # else:
        #     profile_picture_name=profile_picture_path.name
        #     profile_picture_path = profile_picture_path.read()
        #     print(profile_picture_name)
        # print(profile_picture_path,'profile_picture_path')
        profile_picture_path = request.FILES.get('profilePicture')
        if profile_picture_path is not None:
            profile_picture_name = profile_picture_path.name
            profile_picture_path = profile_picture_path.read()
            print(profile_picture_name,'n-----------')
        else:
            profile_picture_path = request.POST.get('profile_picture_path')

        print(profile_picture_path,'p===========')
        
        resume_file = resume_data.get('resume_path')
        print(resume_file,'resume_file----------')

        if resume_file is not None:
            resume_name = resume_file.name
            resume_path = resume_file.read()
            print(resume_name, 'resume_name------------')
        else:
            resume_path = request.POST.get('resume', '{"resume_path"}')
            print(resume_path, 'resume_path-------')

        print(resume_path, 'final resume_path---------')
        # resume_name=resume.name
        # print(resume_name,'resume_name')
        # resume = resume.read()
        # Extracting current address details
        current_address = address_data.get('current', {})
        street_current = current_address.get('street')
        city_current = current_address.get('city')
        state_current = current_address.get('state')
        country_current = current_address.get('country')
        pincode_current = current_address.get('pincode')
        address_type_current = current_address.get('address_type')
        # Extracting permanent address details
        permanent_address = address_data.get('permanent', {})
        street_permanent = permanent_address.get('street')
        city_permanent = permanent_address.get('city')
        state_permanent = permanent_address.get('state')
        country_permanent = permanent_address.get('country')
        pincode_permanent = permanent_address.get('pincode')
        address_type_permanent = permanent_address.get('address_type')
        # Extracting education details    
        sslc_school_name = education_data.get('sslc_school_name')
        sslc_start_year = education_data.get('sslc_start_year')
        sslc_end_year = education_data.get('sslc_end_year')
        sslc_percentage = education_data.get('sslc_percentage')
        hsc_school_name = education_data.get('hsc_school_name')
        hsc_start_year = education_data.get('hsc_start_year')
        hsc_end_year = education_data.get('hsc_end_year')
        hsc_percentage = education_data.get('hsc_percentage')

        college_name = college_data.get('college_name')
        college_start_year = college_data.get('college_start_year')
        college_end_year = college_data.get('college_end_year')
        college_percentage = college_data.get('college_percentage')
        department = college_data.get('department')
        degree = college_data.get('degree')
        education_type = college_data.get('education_type')

        pg_college_degree = pg_college__data.get("pg_college_degree")
        pg_college_department = pg_college__data.get("pg_college_department")
        pg_college_end_year = pg_college__data.get("pg_college_end_year")
        pg_college_name = pg_college__data.get("pg_college_name")
        pg_college_percentage = pg_college__data.get("pg_college_percentage")
        pg_college_start_year = pg_college__data.get("pg_college_start_year")
        pg_college_education_type = diploma_college_data.get("pg_college_education_type")

        diploma_college_name = diploma_college_data.get("diploma_college_name")
        diploma_college_start_year = diploma_college_data.get("diploma_college_start_year")
        diploma_college_end_year = diploma_college_data.get("diploma_college_end_year")
        diploma_college_percentage = diploma_college_data.get("diploma_college_percentage")
        diploma_college_department = diploma_college_data.get("diploma_college_department")
        diploma_college_degree = diploma_college_data.get("diploma_college_degree")
        diploma_college_education_type = diploma_college_data.get("diploma_college_education_type")
        # Extracting job preference details
        department = job_preference_data.get('department')
        industry = job_preference_data.get('industry')
        key_skills = job_preference_data.get('key_skills')
        prefered_locations = job_preference_data.get('preferred_locations')
        # Extracting professional details
        # professional_details_list = professional_details_data.get("companies", [])
        # employment_status = professional_details_data
        # print(employment_status,'employment_status-------')
        if professional_details_data is None:
            employment_status = "Fresher"
            # professional_details_data = json.loads(request.POST.get('professionalDetails', '{}'))
            isExperienced = professional_details_data.get('isExperienced')
            print(isExperienced)
        else:
            employment_status = "Experienced"
            # professional_details_data = json.loads(request.POST.get('professionalDetails', '{}'))
            companies = professional_details_data.get('companies', [])
            # number_of_companies = professional_details_data.get('numberOfCompanies', 0)
        # Fetching user ID
        print(mobile_number,'mobile------------')
        user_id, registered_by, mobile_number = create_account_user_query.mobile_number(mobile_number)
        print(user_id, registered_by, mobile_number)
        # Creating SQLAlchemy engine and session
        # engine = create_engine('mysql://theuser:thepassword@13.51.66.252:3306/backend1')
        # Base.metadata.create_all(engine)
        # Session = sessionmaker(bind=engine)
        # session = Session()
        session = create_session()

        # s3 = boto3.client('s3', aws_access_key_id='AKIAZI2LB2XIRFQPYDJ4', aws_secret_access_key='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', region_name='eu-north-1')
        # profile_picture_key = f'profile_picture/{user_id}_{profile_picture_name}'
        # s3.upload_fileobj(io.BytesIO(profile_picture), 'backendcompanylogo', profile_picture_key)
        existing_profile_picture_key = update_user_account_query.get_profile_picture_path(session,user_id)
        print(existing_profile_picture_key,'e------')
        if profile_picture_path is not None:
            print('if conditiong working fine------->1')
            profile_picture_key = update_user_account_query.upload_profile_picture_file(profile_picture_path, profile_picture_name, user_id, existing_profile_picture_key)
            # print(company_logo_key+" "+ "if condition ---->2")

        else:
            # profile_picture_key = update_user_account_query.upload_profile_picture_path(profile_picture_path,existing_profile_picture_key)         
            profile_picture_key = profile_picture_path
        # existing_profile_picture_key = update_user_account_query.get_profile_picture_path(session,user_id)
        # profile_picture_key = update_user_account_query.upload_profile_picture(profile_picture, profile_picture_name, user_id,existing_profile_picture_key)
        # Update PersonalDetails table
        update_user_account_query.update_personal_details(session, user_id, date_of_birth, first_name, gender, last_name, profile_picture_key)

        # Update Address table for permanent address
        update_user_account_query.update_address(session, user_id, address_type_permanent, city_permanent, country_permanent, pincode_permanent,
                    state_permanent, street_permanent)
    
        if address_type_current is not None and address_type_current != '':
            # Update Address table for current address
            update_user_account_query.update_address(session, user_id, address_type_current, city_current, country_current, pincode_current, state_current,
                        street_current)

        # Update EducationDetails table
        update_user_account_query.update_education_details(session, user_id, sslc_end_year, sslc_percentage, sslc_school_name, sslc_start_year,
                                 hsc_end_year, hsc_percentage, hsc_school_name, hsc_start_year)
        if education_type == 'UG':
            # Update CollegeDetails table for UG education type
            update_user_account_query.update_college_details(session, user_id, education_type, college_end_year, college_name, college_percentage,
                                college_start_year, degree, department)
            if pg_college_name is not None and pg_college_name != '':  
                # Update CollegeDetails table for PG education type
                education_type = pg_college_education_type
                update_user_account_query.update_college_details(session, user_id, education_type, pg_college_end_year, pg_college_name, pg_college_percentage,
                                    pg_college_start_year, pg_college_degree, pg_college_department)
            if diploma_college_name is not None and diploma_college_name != '':
                # Update CollegeDetails table for Diploma education type
                education_type = diploma_college_education_type
                update_user_account_query.update_college_details(session, user_id, education_type, diploma_college_end_year, diploma_college_name,
                                    diploma_college_percentage, diploma_college_start_year, diploma_college_degree,
                                    diploma_college_department)

        # Update JobPreferences table
        update_user_account_query.update_job_preferences(session, user_id, department, industry, key_skills, prefered_locations)
        
        # Delete existing professional details for the user
        update_user_account_query.delete_existing_professional_details(session, user_id)

        # Update ProfessionalDetails table
        update_user_account_query.update_professional_details(session, user_id, companies)
            
        # Update resemeDetails table
        # resume_key = f'resume/{user_id}_{resume_name}'
        # s3.upload_fileobj(io.BytesIO(resume), 'backendcompanylogo', resume_key)
        # existing_resume_key = update_user_account_query.get_resume_path(session,user_id)
        # resume_key = update_user_account_query.upload_resume(resume_file, resume_name, user_id,existing_resume_key)

        existing_resume_key = update_user_account_query.get_resume_path(session,user_id)
        print(existing_resume_key,'e------')
        if resume_file is not None:
            print('if conditiong working fine------->1')
            resume_key = update_user_account_query.upload_resume_file(resume_file, resume_name, user_id, existing_resume_key)
            # print(company_logo_key+" "+ "if condition ---->2")

        else:
            # resume_key = update_user_account_query.upload_resume_path(resume_path,existing_resume_key) 
            resume_key = resume_path  
 

        update_user_account_query.update_resume_details(session, user_id, employment_status, resume_key)
        
        updated_data = get_user_account.user_details(session,user_id)

        session.commit()
        session.close()

        # return JsonResponse({"message": "Data updated successfully"})
        return JsonResponse({"message": "Data updated successfully", "data": updated_data})
    except Exception as e:
        print(str(e))
        return JsonResponse({"error": "Failed to update data"})

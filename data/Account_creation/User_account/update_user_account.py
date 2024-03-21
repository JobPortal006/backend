from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from data.Account_creation.User_account.Query import update_user_account_query
from data.message import create_session
from data.Account_creation.User_account import get_user_account
from data.token import decode_token
from data import message

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
        token = request.POST.get('token')
        user_id,registered_by,email = decode_token(token)
        print(user_id, registered_by,email) 
        if user_id is not None:
            user_details = json.loads(request.POST.get('userDetails', '{}'))
            signup_data = json.loads(request.POST.get('Signup', '{}'))
            address_data = json.loads(request.POST.get('address', '{}'))
            education_data = json.loads(request.POST.get('education_details', '{}'))
            college_data = json.loads(request.POST.get('college_details','{}'))
            pg_college__data = json.loads(request.POST.get('PG_college_details','{}'))
            diploma_college_data = json.loads(request.POST.get('Diploma_college_details','{}'))
            job_preference_data = json.loads(request.POST.get('jobPreference', '{}'))
            professional_details_data = json.loads(request.POST.get('professionalDetails'))
            # Extracting user details
            print(user_details)
            print(address_data)
            print(education_data)
            print(college_data)
            print(pg_college__data)
            print(diploma_college_data)
            print(job_preference_data)
            print(professional_details_data)
            first_name = user_details.get('first_name')
            last_name = user_details.get('last_name')
            gender = user_details.get('gender')
            date_of_birth = user_details.get('date_of_birth')
            profile_picture_file = request.FILES.get('profilePicture')
            if profile_picture_file is not None:
                profile_picture_name = profile_picture_file.name
                profile_picture_file = profile_picture_file.read()  
            else:
                profile_picture_path = user_details.get('profile_picture_path')
            resume_file = request.FILES.get('resume')
            if resume_file is not None:
                resume_name = resume_file.name
                resume_file = resume_file.read()
            else:
                resume_path = request.POST.get('resume') 
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
            prefered_locations = job_preference_data.get('prefered_locations')
            session = create_session()
            existing_profile_picture_key = update_user_account_query.get_profile_picture_path(session,user_id)
            if profile_picture_file is not None:
                profile_picture_key = update_user_account_query.upload_profile_picture_file(profile_picture_file, profile_picture_name, user_id, existing_profile_picture_key)

            else:       
                profile_picture_key = profile_picture_path
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
            numberOfCompanies = professional_details_data.get('numberOfCompanies')

            if numberOfCompanies == "0":
                employment_status = "Fresher"
            else:
                employment_status = "Experienced"
                # professional_details_data = json.loads(request.POST.get('professionalDetails', '{}'))
                companies = professional_details_data.get('companies', [])
                # number_of_companies = professional_details_data.get('numberOfCompanies', 0)

                # Update ProfessionalDetails table
                update_user_account_query.update_professional_details(session, user_id, companies)

            existing_resume_key = update_user_account_query.get_resume_path(session,user_id)
            if resume_file is not None:
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
        else:
            return message.response('Error', 'tokenError')
    except Exception as e:
        print(str(e))
        return message.tryExceptError(str(e))

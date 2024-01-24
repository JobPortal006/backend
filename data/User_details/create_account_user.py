from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from data import response
from data.User_details.Query import create_account_user_query

@csrf_exempt
def user_register(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            
            user_details = data.get('userDetails', {})
            date_of_birth = user_details.get('date_of_birth')
            first_name = user_details.get('first_name')
            last_name = user_details.get('last_name')
            mobile_number = user_details.get('mobile_number')
            gender = user_details.get('gender')
            profile_picture = user_details.get('profile_picture')

            # Extract address details
            address_data = data.get('address', {})
            current_address = address_data.get('current', {})
            permanent_address = address_data.get('permanent', {})

            # Extract education details
            education_data = data.get('education', {})
            # Extract job preference details
            job_preference_data = data.get('jobPreference', {})
            # Extract professional details
            professional_details_data = data.get('professional_details', {})
            employment_status=data.get("professional_details")
            # Extract resume details
            resume = data.get("resume")

            # Extract personal details
            if mobile_number:
                user_id, registered_by = create_account_user_query.mobileNumber(mobile_number)
                print(user_id, registered_by)
                if user_id:
                    personal_details_result = create_account_user_query.personal_details(
                        user_id, registered_by, first_name, last_name, date_of_birth, gender,profile_picture
                    )
                    print('Personal_details ->',personal_details_result)

                    # Extract and insert current address
                    street_current = current_address.get('street')
                    city_current = current_address.get('city')
                    state_current = current_address.get('state')
                    country_current = current_address.get('country')
                    pincode_current = current_address.get('pincode')
                    address_type_current = current_address.get('address_type')
                    address_details_current_result = create_account_user_query.address_details(
                        user_id, registered_by, street_current, city_current, state_current, country_current, pincode_current, address_type_current
                    )
                    print('Address_details_current ->',address_details_current_result)

                    # Extract and insert permanent address
                    street_permanent = permanent_address.get('street')
                    city_permanent = permanent_address.get('city')
                    state_permanent = permanent_address.get('state')
                    country_permanent = permanent_address.get('country')
                    pincode_permanent = permanent_address.get('pincode')
                    address_type_permanent = permanent_address.get('address_type')
                    address_details_permanent_result = create_account_user_query.address_details(
                        user_id, registered_by, street_permanent, city_permanent, state_permanent, country_permanent, pincode_permanent, address_type_permanent
                    )
                    print('Address_details_permanent ->',address_details_permanent_result)

                    # Extract and insert education details
                    sslc_school_name = education_data.get('sslc_school_name')
                    sslc_start_year = education_data.get('sslc_start_year')
                    sslc_end_year = education_data.get('sslc_end_year')
                    sslc_percentage = education_data.get('sslc_percentage')
                    hsc_school_name = education_data.get('hsc_school_name')
                    hsc_start_year = education_data.get('hsc_start_year')
                    hsc_end_year = education_data.get('hsc_end_year')
                    hsc_percentage = education_data.get('hsc_percentage')
                    college_name = education_data.get('college_name')
                    start_year = education_data.get('start_year')
                    end_year = education_data.get('end_year')
                    percentage = education_data.get('college_percentage')
                    department = education_data.get('department')
                    degree = education_data.get('degree')
                    education_type = education_data.get('education_type')
                    pg_college_degree = education_data.get("pg_college_degree")
                    pg_college_department = education_data.get("pg_college_department")
                    pg_college_end_year = education_data.get("pg_college_end_year")
                    pg_college_name = education_data.get("pg_college_name")
                    pg_college_percentage = education_data.get("pg_college_percentage")
                    pg_college_start_year = education_data.get("pg_college_start_year")
                    education_details_result = create_account_user_query.education_details(
                        user_id, sslc_school_name, sslc_start_year, sslc_end_year, sslc_percentage, hsc_school_name,
                        hsc_start_year, hsc_end_year, hsc_percentage, college_name, start_year, end_year,
                        percentage, department, degree, education_type,pg_college_name,pg_college_start_year,pg_college_end_year,
                        pg_college_percentage,pg_college_department,pg_college_degree
                    )
                    print('Education_details ->',education_details_result)

                    # Extract and insert job preference details
                    department = job_preference_data.get('department')
                    industry = job_preference_data.get('industry')
                    key_skills = job_preference_data.get('key_skills')
                    prefered_locations = job_preference_data.get('prefered_locations')
                    job_preference_result = create_account_user_query.job_preference_details(
                        user_id, key_skills, department, industry, prefered_locations
                    )
                    print('Job_preference ->',job_preference_result)

                    # Extract and insert professional details
                    is_experienced = data.get("professional_details", {}).get("isExperienced")
                    print(employment_status)
                    if employment_status != 'Fresher' or is_experienced==True:
                        employment_status='Experienced'
                        create_account_user_query.employment_status(user_id,registered_by,employment_status,resume)
                        companies = professional_details_data.get('companies', [])
                        for company in companies:
                            company_name = company.get('company_name')
                            years_of_experience = company.get('years_of_experience')
                            job_role = company.get('job_role')
                            skills = company.get('skills')
                            professional_details_result = create_account_user_query.professional_details(
                                user_id, registered_by, company_name, years_of_experience, job_role, skills
                            )
                            print('Professional_details ->',professional_details_result)
                    else:
                        employment_status_result=create_account_user_query.employment_status(user_id,registered_by,employment_status,resume)
                        print('Professional_details ->',employment_status_result)

                    # Other relevant code for sending emails, handling responses, etc.

                    return response.handleSuccess("Account created Successfully")
                else:
                    return response.errorResponse("Mobile number is not registered")
            else:
                return response.errorResponse("Mobile number is required")
        else:
            return response.errorResponse("Invalid request method")
    except Exception as e:
        print(str(e))
        return response.serverErrorResponse("Server error")

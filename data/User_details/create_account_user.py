from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from data import response
from data.User_details.Query import create_account_user_query
from django.utils.decorators import method_decorator
from django.views import View
from django.core.files.storage import FileSystemStorage
import os
from data.User_details import message

# Insert the data into required tables
# Get user_id, email data by using mobile_number
# Store profile_picture and resume fils on project folders (Profile Picture and Resume)
# Once account is created - Send mail to registered email as (Account Created Successfully message)
@method_decorator(csrf_exempt, name='dispatch')
class user_register(View):
    def post(self, request, *args, **kwargs):
        try:
            if request.method == 'POST':
                # Extract user details
                user_details = json.loads(request.POST.get('userDetails', '[]'))
                # Extract address details
                address_data = json.loads(request.POST.get('address', '{}'))
                current_address = address_data.get('current', {})
                permanent_address = address_data.get('permanent', {})
                # Extract education details
                education_data = json.loads(request.POST.get('education', '{}'))
                # Extract job preference details
                job_preference_data = json.loads(request.POST.get('jobPreference', '{}'))
                # Extract professional details
                professional_details_data = json.loads(request.POST.get('professional_details', '{}'))
                employment_status = request.POST.get("professional_details")
                # Extract resume details
                resume = request.FILES.get("resume")
                
                mobile_number = user_details.get('mobile_number')
                if mobile_number:
                    user_id, registered_by , email= create_account_user_query.mobileNumber(mobile_number)
                    print(user_id, registered_by, email)
                    first_name = user_details.get('first_name')
                    last_name = user_details.get('last_name')
                    gender = user_details.get('gender')
                    date_of_birth = user_details.get('date_of_birth')
                    profile_picture = request.FILES.get('profilePicture')
                    fs = FileSystemStorage()
                    full_file_path = os.path.join(r'D:\python check\backend\Profile Pictures', profile_picture.name)
                    # Save the file
                    with open(full_file_path, 'wb') as destination:
                        for chunk in profile_picture.chunks():
                            destination.write(chunk)
                    # Update the profile_picture variable to the correct URL
                    profile_picture = profile_picture.name
                    # Extract and insert User details
                    # print('User Details Data ----->', first_name, last_name, mobile_number, gender, date_of_birth,profile_picture)
                    personal_details_result = create_account_user_query.personal_details(
                        user_id, registered_by, first_name, last_name, date_of_birth, gender, profile_picture
                    )
                    print('Personal_details ->', personal_details_result)

                    # Extract and insert current address
                    street_current = current_address.get('street')
                    city_current = current_address.get('city')
                    state_current = current_address.get('state')
                    country_current = current_address.get('country')
                    pincode_current = current_address.get('pincode')
                    address_type_current = current_address.get('address_type')
                    address_details_current_result = create_account_user_query.address_details(
                        user_id, registered_by, street_current, city_current, state_current, country_current,
                        pincode_current, address_type_current
                    )
                    print('Address_details_current ->', address_details_current_result)

                    # Extract and insert permanent address
                    street_permanent = permanent_address.get('street')
                    city_permanent = permanent_address.get('city')
                    state_permanent = permanent_address.get('state')
                    country_permanent = permanent_address.get('country')
                    pincode_permanent = permanent_address.get('pincode')
                    address_type_permanent = permanent_address.get('address_type')
                    address_details_permanent_result = create_account_user_query.address_details(
                        user_id, registered_by, street_permanent, city_permanent, state_permanent, country_permanent,
                        pincode_permanent, address_type_permanent
                    )
                    print('Address_details_permanent ->', address_details_permanent_result)

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
                    diploma_college_name = education_data.get("diploma_college_name")
                    diploma_college_start_year = education_data.get("diploma_college_start_year")
                    diploma_college_end_year = education_data.get("diploma_college_end_year")
                    diploma_college_percentage = education_data.get("diploma_college_percentage")
                    diploma_college_department = education_data.get("diploma_college_department")
                    diploma_college_degree = education_data.get("diploma_college_degree")
                    education_details_result = create_account_user_query.education_details(
                        user_id, sslc_school_name, sslc_start_year, sslc_end_year, sslc_percentage, hsc_school_name,
                        hsc_start_year, hsc_end_year, hsc_percentage, college_name, start_year, end_year,
                        percentage, department, degree, education_type, pg_college_name, pg_college_start_year,
                        pg_college_end_year, pg_college_percentage, pg_college_department, pg_college_degree,
                        diploma_college_name, diploma_college_start_year, diploma_college_end_year,
                        diploma_college_percentage, diploma_college_department, diploma_college_degree
                    )
                    print('Education_details ->', education_details_result)

                    # Extract and insert job preference details
                    department = job_preference_data.get('department')
                    industry = job_preference_data.get('industry')
                    key_skills = job_preference_data.get('key_skills')
                    prefered_locations = job_preference_data.get('prefered_locations')
                    job_preference_result = create_account_user_query.job_preference_details(
                        user_id, key_skills, department, industry, prefered_locations
                    )
                    print('Job_preference ->', job_preference_result)
                    fs = FileSystemStorage()
                    full_file_path = os.path.join(r'D:\python check\backend\Resume', resume.name)
                    # Save the file
                    with open(full_file_path, 'wb') as destination:
                        for chunk in resume.chunks():
                            destination.write(chunk)
                    # Update the profile_picture variable to the correct URL
                    resume = fs.url(full_file_path)

                    # Extract and insert professional details
                    is_experienced = professional_details_data.get('isExperienced')
                    if employment_status != 'Fresher' or is_experienced:
                        employment_status = 'Experienced'
                        create_account_user_query.employment_status(user_id, registered_by, employment_status, resume)
                        companies = professional_details_data.get('companies', [])
                        for company in companies:
                            company_name = company.get('company_name')
                            years_of_experience = company.get('years_of_experience')
                            job_role = company.get('job_role')
                            skills = company.get('skills')
                            professional_details_result = create_account_user_query.professional_details(
                                user_id, registered_by, company_name, years_of_experience, job_role, skills
                            )
                            print('Professional_details ->', professional_details_result)
                    else:
                        employment_status_result = create_account_user_query.employment_status(
                            user_id, registered_by, employment_status, resume
                        )
                        print('Professional_details ->', employment_status_result)

                    # sending email
                    subject = 'Account Creation'
                    message_html = render_to_string('account.html', {'name': first_name})
                    message_plain = strip_tags(message_html)
                    from_email = 'brochill547@gmail.com'
                    recipient_list = [email]
                    send_mail(subject, message_plain, from_email, recipient_list, html_message=message_html)
                    return message.success('accountCreation')
                else:
                    return message.error('loginWithOTPError')
            else:
                return message.error('Error')
        except Exception as e:
            print(str(e))
            return message.serverErrorResponse()

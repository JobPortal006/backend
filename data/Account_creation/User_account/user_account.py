from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from data.Account_creation.Query import create_account_user_query
from django.utils.decorators import method_decorator
from django.views import View
from data import message
import io
import boto3
from data.token import decode_token
from data.Job.Query import post_job_insert_query 

# Insert the data into required tables
# Get user_id, email data by using mobile_number
# Store profile_picture and resume fils on project folders (Profile Picture and Resume)
# Once account is created - Send mail to registered email as (Account Created Successfully message)
@method_decorator(csrf_exempt, name='dispatch') # Dispatch method is handle HTTP method (GET, POST, etc.) 
class user_register(View): # View class provides a creating views by defining methods for different HTTP methods (e.g., get, post).
    def post(self, request, *args, **kwargs):
        try:
            if request.method == 'POST':
                token = request.POST.get('token')
                user_id,registered_by,email = decode_token(token)
                print(user_id, registered_by,email) 
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
                first_name = user_details.get('first_name')
                last_name = user_details.get('last_name')
                gender = user_details.get('gender')
                date_of_birth = user_details.get('date_of_birth')
                profile_picture = request.FILES.get('profilePicture')
                profile_picture_name=profile_picture.name
                profile_picture = profile_picture.read()
                resume = request.FILES.get("resume")
                resume_name=resume.name
                resume = resume.read()
                # current_address = address_data.get('current', {})
                # street_current = current_address.get('street')
                # city_current = current_address.get('city')
                # state_current = current_address.get('state')
                # country_current = current_address.get('country')
                # pincode_current = current_address.get('pincode')
                # address_type_current = current_address.get('address_type')

                # permanent_address = address_data.get('permanent', {})
                # street_permanent = permanent_address.get('street')
                # city_permanent = permanent_address.get('city') 
                # state_permanent = permanent_address.get('state')
                # country_permanent = permanent_address.get('country')
                # pincode_permanent = permanent_address.get('pincode')
                # address_type_permanent = permanent_address.get('address_type')

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

                employment_status = request.POST.get("professional_details")
                department = job_preference_data.get('department')
                industry = job_preference_data.get('industry')
                key_skills = job_preference_data.get('key_skills')
                prefered_locations = job_preference_data.get('prefered_locations')
                # Check if either current or permanent address has non-empty street field
                if user_id is not None:
                    userid_check = create_account_user_query.userid_check(user_id)
                    print(userid_check)
                    if userid_check:
                        # Update the profile_picture variable to the correct URL 
                        # Check user details data is empty or not
                        personal_details_data = message.personal_details(first_name, last_name,date_of_birth, gender) 
                        # Check permanent address details data is empty or not
                        # address_details_permanent_data= message.address_details_permanent(
                        #         street_permanent, city_permanent, state_permanent, country_permanent,
                        #         pincode_permanent, address_type_permanent)
                        # Check educational details data is empty or not
                        educational_details_data = message.educational_details(sslc_school_name, sslc_start_year, sslc_end_year, sslc_percentage, hsc_school_name,
                            hsc_start_year, hsc_end_year, hsc_percentage, college_name, college_start_year, college_end_year,college_percentage, department, degree)
                        # Check job preference details data is empty or not
                        job_preference_data = message.job_preference_details(key_skills, department, industry, prefered_locations)
                        print(personal_details_data,educational_details_data,job_preference_data)
                        #check input value is none or not
                        # if personal_details_data and address_details_permanent_data and educational_details_data and job_preference_data:
                        s3 = boto3.client('s3', aws_access_key_id='AKIAZI2LB2XIRFQPYDJ4', aws_secret_access_key='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', region_name='eu-north-1')
                        profile_picture_key = f'profile_picture/{user_id}_{profile_picture_name}'  # Adjust the key based on your needs
                        s3.upload_fileobj(io.BytesIO(profile_picture), 'backendcompanylogo', profile_picture_key)
                        print(profile_picture_key)
                        personal_details_result = create_account_user_query.personal_details(
                            user_id, first_name, last_name, date_of_birth, gender,profile_picture_key)
                        print('Personal_details ->', personal_details_result)
                       
                        for address_type, address_details in address_data.items():
                            if address_type in ['current', 'permanent']:
                                street = address_details.get('street')
                                city = address_details.get('city')
                                state = address_details.get('state')
                                country = address_details.get('country')
                                pincode = address_details.get('pincode')
                                address_type = address_details.get('address_type')
                                if street != '':
                                    address_details_result = create_account_user_query.address_details(
                                        user_id, registered_by, street, city, state, country, pincode, address_type)
                                    print(f'{address_type} Address details:', address_details_result)

                        education_details_result = create_account_user_query.education_details(
                            user_id, sslc_school_name, sslc_start_year, sslc_end_year, sslc_percentage, hsc_school_name,
                            hsc_start_year, hsc_end_year, hsc_percentage, college_name, college_start_year, college_end_year,
                            college_percentage, department, degree, education_type, pg_college_name, pg_college_start_year,
                            pg_college_end_year, pg_college_percentage, pg_college_department, pg_college_degree,
                            diploma_college_name, diploma_college_start_year, diploma_college_end_year,
                            diploma_college_percentage, diploma_college_department, diploma_college_degree)
                        print('Education_details ->', education_details_result)
                        skill_ids = []
                        for skill in key_skills: 
                            skill_id = post_job_insert_query.skill_set(skill)  # Insert the skill_set in skill_sets table
                            skill_ids.append(str(skill_id))  # Append the skill_id to the list and convert it to a string
                        key_skills = ",".join(skill_ids)
                        location_ids = []
                        for location_name in prefered_locations:
                            location_id = post_job_insert_query.location(location_name)
                            location_ids.append(str(location_id))
                        prefered_locations = ",".join(location_ids)
                        job_preference_result = create_account_user_query.job_preference_details(
                        user_id, key_skills, department, industry, prefered_locations)
                        print('Job_preference ->', job_preference_result)
                        employment_status = professional_details_data
                        if professional_details_data is None:
                            professional_details_data = json.loads(request.POST.get('professionalDetails', '{}'))
                            isExperienced = professional_details_data.get('isExperienced')
                            print(isExperienced)
                        resume_key = f'resume/{user_id}_{resume_name}'  # Adjust the key based on your needs
                        s3.upload_fileobj(io.BytesIO(resume), 'backendcompanylogo', resume_key)
                        print(resume_key)
                        if employment_status == 'Fresher' and employment_status is not None:
                            employment_status_result = create_account_user_query.resume_details(
                                user_id, employment_status,resume_key
                            )
                            print('Professional_details ->', employment_status_result)
                            
                        else:
                            employment_status = 'Experienced'
                            employment_status_result = create_account_user_query.resume_details(
                                user_id, employment_status,resume_key
                            )
                            companies = professional_details_data.get('companies', [])
                            for company in companies: 
                                company_name = company.get('company_name')
                                years_of_experience = company.get('years_of_experience')
                                job_role = company.get('job_role')
                                skills = company.get('skills')
                                professional_details_result = create_account_user_query.professional_details(
                                    user_id, company_name, years_of_experience, job_role, skills)
                                print('Professional_details ->', professional_details_result)
                        # sending email
                        subject = 'Account Creation'
                        message_html = render_to_string('account.html', {'name': first_name})
                        message_plain = strip_tags(message_html)
                        from_email = 'brochill547@gmail.com'
                        recipient_list = [email]
                        send_mail(subject, message_plain, from_email, recipient_list, html_message=message_html)
                        if employment_status_result:
                            return message.response('Success','accountCreation')
                    else:
                        return message.response('Error','UserIdError')
                else:
                    return message.response('Error','tokenError')
            else:
                return message.response('Error','Error')
        except Exception as e:
            print(str(e))
            return message.tryExceptError(str(e))

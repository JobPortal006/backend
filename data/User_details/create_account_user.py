from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
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
                data = json.loads(request.body)
                print(data)
                user_details = data.get('userDetails', {})
                print(user_details, 'user details ---------------')
                # print(type(user_details))
                # print(request.body),'1---------------------'
                # data = json.loads(request.body)
                # print(data)
                # Extract address details
                address_data = json.loads(request.POST.get('address', '{}'))
                address_data = data.get('address', {})
                print(address_data)
                current_address = address_data.get('current', {})
                permanent_address = address_data.get('permanent', {})
                # Extract education details
                education_data = json.loads(request.POST.get('education', '{}'))
                education_data = data.get('education', {})
                print(education_data)
                # Extract job preference details
                job_preference_data = json.loads(request.POST.get('jobPreference', '{}'))
                job_preference_data = data.get('jobPreference', {})
                print(job_preference_data)
                # Extract professional details
                professional_details_data = json.loads(request.POST.get('professionalDetails', '{}'))
                professional_details_data = data.get('professionalDetails', {})
                print(professional_details_data)
                first_name = user_details.get('first_name')
                last_name = user_details.get('last_name')
                gender = user_details.get('gender')
                date_of_birth = user_details.get('date_of_birth')
                mobile_number = user_details.get('mobile_number')
                print(mobile_number)

                profile_picture = request.FILES.get('profilePicture')
                profile_picture = user_details.get('profile_picture')
                # profile_picture=request.FILES['profilePicture']
                resume = request.FILES.get("resume")
                resume = data.get('resume')
                # resume = request.FILES['resume']
                print(profile_picture,"profile_picture 1-----------")
                print(resume,'resume 2---------------')

                street_current = current_address.get('street')
                city_current = current_address.get('city')
                state_current = current_address.get('state')
                country_current = current_address.get('country')
                pincode_current = current_address.get('pincode')
                address_type_current = current_address.get('address_type')
                print(state_current)

                street_permanent = permanent_address.get('street')
                city_permanent = permanent_address.get('city') 
                state_permanent = permanent_address.get('state')
                country_permanent = permanent_address.get('country')
                pincode_permanent = permanent_address.get('pincode')
                address_type_permanent = permanent_address.get('address_type')
                print(state_permanent)

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
                print(sslc_school_name,hsc_school_name,college_name,pg_college_name,diploma_college_name)

                employment_status = request.POST.get("professional_details")
                department = job_preference_data.get('department')
                industry = job_preference_data.get('industry')
                key_skills = job_preference_data.get('key_skills')
                prefered_locations = job_preference_data.get('prefered_locations')
                print(department)
                if mobile_number:
                    user_id, registered_by , email= create_account_user_query.mobile_number(mobile_number)
                    print(user_id, registered_by, email)
                    userid_check = create_account_user_query.userid_check(user_id)
                    print(userid_check,'user id ---------------')
                    if userid_check:
                        def is_valid_file_format(file_name):
                            allowed_extensions = ['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx'] 
                            file_extension = file_name.split('.')[-1].lower()
                            return file_extension in allowed_extensions

                        if profile_picture and not is_valid_file_format(profile_picture):
                            # Handle invalid profile picture format
                            return message.error('FileError')

                        if resume and not is_valid_file_format(resume):
                            # Handle invalid resume format
                            return message.error('FileError')
                        # profile_picture = profile_picture1.name
                        # resume = resume.name
                        # fs = FileSystemStorage()
                        # full_file_path = os.path.join(r'D:\python check\backend\Profile Pictures', profile_picture.name)
                        # # Save the file
                        # with open(full_file_path, 'wb') as destination:
                        #     for chunk in profile_picture.chunks():
                        #         destination.write(chunk)
                        # Update the profile_picture variable to the correct URL 
                        # Check user details data is empty or not
                        personal_details_data = message.personal_details(first_name, last_name,date_of_birth, gender) 
                        # Check permanent address details data is empty or not
                        address_details_permanent_data= message.address_details_permanent(
                                street_permanent, city_permanent, state_permanent, country_permanent,
                                pincode_permanent, address_type_permanent)
                        # Check educational details data is empty or not
                        educational_details_data = message.educational_details(sslc_school_name, sslc_start_year, sslc_end_year, sslc_percentage, hsc_school_name,
                            hsc_start_year, hsc_end_year, hsc_percentage, college_name, college_start_year, college_end_year,college_percentage, department, degree)
                        # Check job preference details data is empty or not
                        job_preference_data = message.job_preference_details(key_skills, department, industry, prefered_locations)
                        print(personal_details_data,address_details_permanent_data,educational_details_data,job_preference_data)
                        if personal_details_data and address_details_permanent_data and educational_details_data and job_preference_data:
                            personal_details_result,data = create_account_user_query.personal_details(
                                user_id, registered_by, first_name, last_name, date_of_birth, gender, profile_picture)
                            print('Personal_details ->', personal_details_result)

                            address_details_current_result = create_account_user_query.address_details(
                            user_id, registered_by, street_current, city_current, state_current, country_current,
                            pincode_current, address_type_current)
                            print('Address_details_current ->', address_details_current_result)

                            address_details_permanent_result = create_account_user_query.address_details(
                                user_id, registered_by, street_permanent, city_permanent, state_permanent, country_permanent,
                                pincode_permanent, address_type_permanent)
                            print('Address_details_permanent ->', address_details_permanent_result)

                            education_details_result = create_account_user_query.education_details(
                            user_id, sslc_school_name, sslc_start_year, sslc_end_year, sslc_percentage, hsc_school_name,
                            hsc_start_year, hsc_end_year, hsc_percentage, college_name, college_start_year, college_end_year,
                            college_percentage, department, degree, education_type, pg_college_name, pg_college_start_year,
                            pg_college_end_year, pg_college_percentage, pg_college_department, pg_college_degree,
                            diploma_college_name, diploma_college_start_year, diploma_college_end_year,
                            diploma_college_percentage, diploma_college_department, diploma_college_degree)
                            print('Education_details ->', education_details_result)

                            job_preference_result = create_account_user_query.job_preference_details(
                            user_id, key_skills, department, industry, prefered_locations)
                            print('Job_preference ->', job_preference_result)

                            employment_status = professional_details_data
                            isExperienced = professional_details_data.get('isExperienced')
                            print(isExperienced)
                            if employment_status == 'Fresher' and employment_status != None:
                                employment_status_result = create_account_user_query.employment_status(
                                    user_id, registered_by, employment_status, resume
                                )
                                print('Professional_details ->', employment_status_result)
                                
                            else:
                                employment_status = 'Experienced'
                                companies = professional_details_data.get('companies', [])
                                for company in companies: 
                                    companyName = company.get('companyName')
                                    years_of_exprence = company.get('years_of_exprence')
                                    job_role = company.get('job_role')
                                    skills = company.get('skills')
                                    print(companyName,years_of_exprence,job_role,skills)
                                    professional_details_result = create_account_user_query.professional_details(
                                        user_id, registered_by, companyName, years_of_exprence, job_role, skills
                                    )
                                    print('Professional_details ->', professional_details_result)
                            # sending email
                            subject = 'Account Creation'
                            message_html = render_to_string('account.html', {'name': first_name})
                            message_plain = strip_tags(message_html)
                            from_email = 'brochill547@gmail.com'
                            recipient_list = [email]
                            send_mail(subject, message_plain, from_email, recipient_list, html_message=message_html)
                            return message.success('accountCreation',data)
                        else:
                            return message.error('InputError')
                    else:
                        return message.error('UserIdError')
                    # Extract and insert job preference details                   
                    
                    # fs = FileSystemStorage()
                    # full_file_path = os.path.join(r'D:\python check\backend\Resume', resume.name)
                    # # Save the file
                    # with open(full_file_path, 'wb') as destination:
                    #     for chunk in resume.chunks():
                    #         destination.write(chunk)
                    # Update the profile_picture variable to the correct URL
                    
                    # Extract resume details
                    # Extract and insert professional details
                    
                else:
                    return message.error('loginWithOTPError')
            else:
                return message.error('Error')
        except Exception as e:
            print(str(e))
            return message.serverErrorResponse()

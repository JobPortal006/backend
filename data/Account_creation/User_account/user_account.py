from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from data.Account_creation.Query import create_account_user_query
from django.utils.decorators import method_decorator
from django.views import View
from data.Account_creation import message

# Insert the data into required tables
# Get user_id, email data by using mobile_number
# Store profile_picture and resume fils on project folders (Profile Picture and Resume)
# Once account is created - Send mail to registered email as (Account Created Successfully message)
@method_decorator(csrf_exempt, name='dispatch') # Dispatch method is handle HTTP method (GET, POST, etc.) 
class user_register(View): # View class provides a creating views by defining methods for different HTTP methods (e.g., get, post).
    def post(self, request, *args, **kwargs):
        try:
            if request.method == 'POST':       
                # Extract user details
                # data = json.loads(request.body)
                # print(data)
                # if data != None:
                # user_details = data.get('userDetails', {})
                # address_data = data.get('address', {})
                # education_data = data.get('education', {})
                # job_preference_data = data.get('jobPreference', {})
                # professional_details_data = data.get('professionalDetails', {})
                # else:
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
                email = user_details.get('email')
                profile_picture = request.FILES.get('profilePicture')
                # profile_picture = profile_picture.read()
                # print(profile_picture,"profile_picture 1-----------")
                # profile_picture = user_details.get('profile_picture')
                resume = request.FILES.get("resume")
                # resume = resume.read()
                # resume = data.get('resume')
                # print(resume,'resume 2---------------')
                current_address = address_data.get('current', {})
                street_current = current_address.get('street')
                city_current = current_address.get('city')
                state_current = current_address.get('state')
                country_current = current_address.get('country')
                pincode_current = current_address.get('pincode')
                address_type_current = current_address.get('address_type')

                permanent_address = address_data.get('permanent', {})
                street_permanent = permanent_address.get('street')
                city_permanent = permanent_address.get('city') 
                state_permanent = permanent_address.get('state')
                country_permanent = permanent_address.get('country')
                pincode_permanent = permanent_address.get('pincode')
                address_type_permanent = permanent_address.get('address_type')

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
                # Get user_id using mobile number in signup table
                user_id, registered_by , email= create_account_user_query.user_check(email)
                print(user_id, registered_by, email)
                # if user_id:
                #     if email_address == email:
                #         # Check permanent address details data is empty or not
                #         userid_check = create_account_employeer_query.userid_check(user_id)
                #         print(userid_check)
                #         if userid_check:  
                if email:
                    userid_check = create_account_user_query.userid_check(user_id)
                    print(userid_check)
                    if userid_check == False:
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
                        #check input value is none or not
                        # if personal_details_data and address_details_permanent_data and educational_details_data and job_preference_data:
                        personal_details_result = create_account_user_query.personal_details(
                            user_id, first_name, last_name, date_of_birth, gender, profile_picture)
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
                        print(employment_status,'employment_status-------')
                        if professional_details_data is None:
                            professional_details_data = json.loads(request.POST.get('professionalDetails', '{}'))
                            isExperienced = professional_details_data.get('isExperienced')
                            print(isExperienced)
                        if employment_status == 'Fresher' and employment_status is not None:
                            employment_status_result = create_account_user_query.employment_status(
                                user_id, employment_status, resume
                            )
                            print('Professional_details ->', employment_status_result)
                            
                        else:
                            employment_status = 'Experienced'
                            employment_status_result = create_account_user_query.employment_status(
                                user_id, employment_status, resume
                            )
                            companies = professional_details_data.get('companies', [])
                            for company in companies: 
                                company_name = company.get('company_name')
                                years_of_experience = company.get('years_of_experience')
                                job_role = company.get('job_role')
                                skills = company.get('skills')
                                # print(company_name,years_of_experience,job_role,skills)
                                professional_details_result = create_account_user_query.professional_details(
                                    user_id, company_name, years_of_experience, job_role, skills
                                )
                                print('Professional_details ->', professional_details_result)
                        # sending email
                        subject = 'Account Creation'
                        message_html = render_to_string('account.html', {'name': first_name})
                        message_plain = strip_tags(message_html)
                        from_email = 'brochill547@gmail.com'
                        recipient_list = [email]
                        send_mail(subject, message_plain, from_email, recipient_list, html_message=message_html)
                        return message.response('Success','accountCreation')
                        # else:
                        #   return message.response('Error','UserIdError')
                    else:
                        return message.response('Error','UserIdError')
                else:
                    return message.response('Error','emailSentError')
            else:
                return message.response('Error','Error')
        except Exception as e:
            print(str(e))
            return message.serverErrorResponse()

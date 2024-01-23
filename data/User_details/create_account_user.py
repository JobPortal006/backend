from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from data import query, response
from data.User_details.Query import create_account_user_query

@csrf_exempt
def user_register(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            personal_details = data.get('personal_details', [])[0]
            first_name = personal_details.get('first_name')
            last_name = personal_details.get('last_name')
            date_of_birth = personal_details.get('date_of_birth')
            mobile_number = personal_details.get('mobile_number')
            gender = personal_details.get('gender')
            profile_picture = personal_details.get('profile_picture')

            # # Extract address details
            # address_details = data.get('address', [])[0]
            # address = address_details.get('address')
            # city = address_details.get('city')
            # state = address_details.get('state')
            # country = address_details.get('country')
            # address_type = address_details.get('address_type')

            # # Extract education details
            # education_details = data.get('education_details', [])[0]
            # sslc_school_name = education_details.get('sslc_school_name')
            # sslc_start_year = education_details.get('sslc_start_year')
            # sslc_end_year = education_details.get('sslc_end_year')
            # sslc_percentage = education_details.get('sslc_percentage')
            # hsc_school_name = education_details.get('hsc_school_name')
            # hsc_start_year = education_details.get('hsc_start_year')
            # hsc_end_year = education_details.get('hsc_end_year')
            # hsc_percentage = education_details.get('hsc_percentage')

            # # Extract college details
            # college_details = data.get('college_details', [])[0]
            # college_name = college_details.get('college_name')
            # start_year = college_details.get('start_year')
            # end_year = college_details.get('end_year')
            # percentage = college_details.get('percentage')
            # department = college_details.get('department')
            # degree = college_details.get('degree')
            # education_type = college_details.get('education_type')

            # # Extract resume details
            # resume_details = data.get('resume_details', [])[0]
            # resume = resume_details.get('resume')

            # # Extract job preferences
            # job_preferences = data.get('job_preferences', [])[0]
            # employment_status = job_preferences.get('employment_status')
            # key_skills = job_preferences.get('key_skills')
            # industry = job_preferences.get('industry')
            # department_job = job_preferences.get('department')
            # preferred_locations = job_preferences.get('preferred_locations')

            # # Extract experience details
            # experience_details = data.get('experience_details', [])[0]
            # previous_company_name = experience_details.get('previous_company_name')
            # no_of_years_experience = experience_details.get('no_of_years_experience')
            # job_role = experience_details.get('job_role')
            # skills = experience_details.get('skills')
            # registered_by_experience = experience_details.get('registered_by')
            user_id=create_account_user_query.mobileNumber(mobile_number)
            registered_by = 'User'
            print(user_id)
            if user_id != '':
              if first_name!='':
                  create_account_user_query.personal_details(user_id,registered_by,first_name,last_name,date_of_birth,mobile_number,gender,profile_picture)

                  # subject = 'Account Creation'
                  # message_html = render_to_string('account.html')
                  # message_plain = strip_tags(message_html)
                  # from_email = 'brochill547@gmail.com'
                  # recipient_list = [email]
                  # send_mail(subject, message_plain, from_email, recipient_list, html_message=message_html)

                  return response.handleSuccess("Account created Successfully")
              else:
                  return response.errorResponse("Invalid input data")
    except Exception as e:
        print(str(e))
        return response.serverErrorResponse("Server error")

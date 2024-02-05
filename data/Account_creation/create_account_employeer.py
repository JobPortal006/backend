from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.decorators import method_decorator
from django.views import View
from data.Account_creation.Query import create_account_employeer_query,create_account_user_query
from data.Account_creation import message

@method_decorator(csrf_exempt, name='dispatch') # Dispatch method is handle HTTP method (GET, POST, etc.) 
class employeerRegister(View): # View class provides a creating views by defining methods for different HTTP methods (e.g., get, post).
    def post(self, request, *args, **kwargs):
        try:
            if request.method == 'POST':
                data = json.loads(request.body)
                user_details = data.get('userDetails', {})
                first_name = user_details.get('first_name')
                last_name = user_details.get('last_name')
                gender = user_details.get('gender')
                date_of_birth = user_details.get('date_of_birth')
                mobile_number = user_details.get('mobile_number')
                profile_picture = user_details.get('profile_picture')

                address_data = data.get('address', {})
                current_address = address_data.get('current', {})
                permanent_address = address_data.get('permanent', {})
                street_current = current_address.get('street')
                city_current = current_address.get('city')
                state_current = current_address.get('state')
                country_current = current_address.get('country')
                pincode_current = current_address.get('pincode')
                address_type_current = current_address.get('address_type')

                street_permanent = permanent_address.get('street')
                city_permanent = permanent_address.get('city') 
                state_permanent = permanent_address.get('state')
                country_permanent = permanent_address.get('country')
                pincode_permanent = permanent_address.get('pincode')
                address_type_permanent = permanent_address.get('address_type')

                company_details = data.get('company_etails', {})
                company_name = company_details.get('company_name') 
                company_location = company_details.get('company_location')
                no_of_employees = company_details.get('no_of_employees')
                industry = company_details.get('industry')
                designation = company_details.get('designation')
                company_logo = company_details.get('company_logo')
                if mobile_number:
                    user_id, registered_by , email= create_account_user_query.mobile_number(mobile_number)
                    print(user_id, registered_by, email)
                    userid_check = create_account_user_query.userid_check(user_id)
                    if userid_check:
                        personal_details_data = message.personal_details(first_name, last_name,date_of_birth, gender) 
                        # Check permanent address details data is empty or not
                        address_details_permanent_data= message.address_details_permanent(
                                street_permanent, city_permanent, state_permanent, country_permanent,
                                pincode_permanent, address_type_permanent)
                        # Check company details data is empty or not
                        company_details_data = message.company_details(company_name, company_location, no_of_employees, industry, designation,company_logo)
                        
                        if personal_details_data and address_details_permanent_data and company_details_data:
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

                            company_details_result = create_account_employeer_query.company_details(user_id,
                                company_name, company_location, no_of_employees, industry, designation,company_logo)
                            print('Company_details_result ->', company_details_result)

                            # sending email
                            subject = 'Account Creation'
                            message_html = render_to_string('account.html', {'name': first_name})
                            message_plain = strip_tags(message_html)
                            from_email = 'brochill547@gmail.com'
                            recipient_list = [email]
                            send_mail(subject, message_plain, from_email, recipient_list, html_message=message_html)
                            return message.response('Success','accountCreation')
                        else:
                            return message.response('Error','InputError')
                    else:
                        return message.response('Error','loginWithOTPError')
                else:
                    return message.response('Error','Error')
        except Exception as e:
            print(str(e))
            return message.serverErrorResponse()
    